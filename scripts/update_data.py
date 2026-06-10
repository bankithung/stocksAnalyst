import argparse, csv, io, math, sys
from datetime import date, datetime, timedelta
import common

EQUITY_L_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
BHAV_URL = "https://archives.nseindia.com/products/content/sec_bhavdata_full_{d}.csv"
SME_SERIES = {"SM", "ST", "SZ"}


def parse_equity_list(text):
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        sym, series = r.get("SYMBOL"), r.get("SERIES", "EQ")
        if not sym:
            continue
        rows.append((sym, r.get("NAME OF COMPANY", ""), series,
                     r.get("ISIN NUMBER", ""), 1 if series in SME_SERIES else 0))
    return rows


def upsert_universe(con, rows):
    con.executemany(
        "INSERT OR REPLACE INTO instruments(symbol,name,series,isin,is_sme) "
        "VALUES(?,?,?,?,?)", rows)
    con.commit()


def cmd_universe(con):
    s = common.nse_session()
    r = s.get(EQUITY_L_URL, timeout=30)
    r.raise_for_status()
    rows = parse_equity_list(r.text)
    upsert_universe(con, rows)
    common.set_fresh(con, "universe", date.today())
    return {"universe_rows": len(rows)}


def upsert_prices(con, symbol, df, source):
    rows = [(symbol, d.strftime("%Y-%m-%d"), float(r["Open"]), float(r["High"]),
             float(r["Low"]), float(r["Close"]), float(r["Volume"]), None, source)
            for d, r in df.iterrows()
            if not math.isnan(r["Close"])]
    con.executemany(
        "INSERT OR REPLACE INTO eod_prices VALUES(?,?,?,?,?,?,?,"
        "COALESCE((SELECT deliv_pct FROM eod_prices WHERE symbol=? AND date=?),NULL),?)",
        [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[0], r[1], r[8]) for r in rows])
    con.commit()
    return len(rows)


def cmd_backfill(con, symbols=None):
    import yfinance as yf
    if symbols:
        syms = [s.strip().upper() for s in symbols.split(",")]
    else:
        syms = [r[0] for r in con.execute(
            "SELECT symbol FROM instruments WHERE status='active'")]
    total, failed = 0, []
    for i in range(0, len(syms), 50):
        chunk = syms[i:i + 50]
        try:
            data = yf.download([s + ".NS" for s in chunk], period="5y",
                               auto_adjust=True, group_by="ticker",
                               progress=False, threads=True)
        except Exception:
            failed.extend(chunk)
            continue
        for s in chunk:
            try:
                df = data[s + ".NS"].dropna(how="all")
                if len(df):
                    total += upsert_prices(con, s, df, "yf")
                else:
                    failed.append(s)
            except Exception:
                failed.append(s)
        print(f"progress {i + len(chunk)}/{len(syms)}", file=sys.stderr)
    common.set_fresh(con, "prices_backfill", date.today())
    return {"price_rows": total, "symbols": len(syms), "failed": len(failed)}


def parse_bhav(text):
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        try:
            d = datetime.strptime(r["DATE1"], "%d-%b-%Y").strftime("%Y-%m-%d")
            dp = r.get("DELIV_PER", "-")
            out.append((r["SYMBOL"], d, float(r["OPEN_PRICE"]), float(r["HIGH_PRICE"]),
                        float(r["LOW_PRICE"]), float(r["CLOSE_PRICE"]),
                        float(r["TTL_TRD_QNTY"]),
                        float(dp) if dp not in ("-", "") else None))
        except (KeyError, ValueError):
            continue
    return out


def cmd_daily(con, days=7):
    s = common.nse_session()
    got = 0
    for back in range(days):
        d = date.today() - timedelta(days=back)
        if d.weekday() >= 5:
            continue
        url = BHAV_URL.format(d=d.strftime("%d%m%Y"))
        try:
            r = s.get(url, timeout=30)
            if r.status_code != 200 or "SYMBOL" not in r.text[:200]:
                continue
        except Exception:
            continue
        rows = parse_bhav(r.text)
        con.executemany(
            "INSERT OR REPLACE INTO eod_prices VALUES(?,?,?,?,?,?,?,?,?)",
            [(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], "bhav") for x in rows])
        con.commit()
        got += len(rows)
        common.set_fresh(con, "prices_daily", d)
    return {"bhav_rows": got}


def cmd_surveillance(con):
    s = common.nse_session()
    n = 0
    for list_type, url in [("ASM", "https://www.nseindia.com/api/reportASM"),
                           ("GSM", "https://www.nseindia.com/api/reportGSM")]:
        try:
            j = s.get(url, timeout=15).json()
        except Exception:
            continue
        items = j.get("longterm", {}).get("data", []) if isinstance(j, dict) else []
        items += j.get("shortterm", {}).get("data", []) if isinstance(j, dict) else []
        if not items and isinstance(j, dict) and "data" in j:
            items = j["data"]
        today = date.today().strftime("%Y-%m-%d")
        for it in items:
            if not isinstance(it, dict):
                continue
            sym = (it.get("symbol") or "").strip()
            if sym:
                con.execute("INSERT OR REPLACE INTO surveillance VALUES(?,?,?,?)",
                            (sym, today, list_type, str(it.get("asmSurvIndicator")
                             or it.get("gsmSurvIndicator") or it.get("stage") or "1")))
                n += 1
        con.commit()
        if n:
            common.set_fresh(con, "surveillance", today)
    return {"surveillance_rows": n}


def cmd_fii(con):
    s = common.nse_session()
    try:
        j = s.get("https://www.nseindia.com/api/fiidiiTradeReact", timeout=15).json()
    except Exception:
        return {"fii_dii_rows": 0}
    n = 0
    for it in j if isinstance(j, list) else []:
        try:
            d = datetime.strptime(it["date"], "%d-%b-%Y").strftime("%Y-%m-%d")
            con.execute("INSERT OR REPLACE INTO fii_dii VALUES(?,?,?,?,?)",
                        (d, it["category"], float(it["buyValue"]),
                         float(it["sellValue"]), float(it["netValue"])))
            n += 1
        except (KeyError, ValueError):
            continue
    con.commit()
    if n:
        common.set_fresh(con, "fii_dii", date.today())
    return {"fii_dii_rows": n}


def _clip(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


def compute_one(df, cfg, is_sme, flagged):
    df = df.sort_index()
    close, high, low, vol = df["close"], df["high"], df["low"], df["volume"]
    rsi = common.rsi(close, 14).iloc[-1]
    atr = common.atr(high, low, close, 14).iloc[-1]
    sma20, sma50, sma200 = [close.rolling(w).mean().iloc[-1] for w in (20, 50, 200)]
    c = close.iloc[-1]
    ret5 = (c / close.iloc[-6] - 1) * 100 if len(close) > 6 else 0.0
    ret20 = (c / close.iloc[-21] - 1) * 100 if len(close) > 21 else 0.0
    vol_surge = vol.iloc[-1] / max(vol.rolling(20).mean().iloc[-1], 1)
    dl = df["deliv_pct"].dropna()
    deliv_surge = (dl.iloc[-1] / max(dl.rolling(20).mean().iloc[-1], 1)
                   if len(dl) >= 21 else 1.0)
    adv20_cr = (close * vol).rolling(20).mean().iloc[-1] / 1e7
    dist52 = (c / close.rolling(min(252, len(close))).max().iloc[-1] - 1) * 100
    swing = low.rolling(10).min().iloc[-1]
    stop = swing - 0.5 * atr
    stop_pct = (c - stop) / c * 100
    em10 = atr * (cfg["target_days"] ** 0.5)
    em10_pct = em10 / c * 100
    rr10 = em10 / max(c - stop, 0.01)
    atr_pct = atr / c * 100

    sc_trend = (40 if c > sma200 else 0) + (30 if c > sma50 else 0) + \
               (30 if sma50 > sma200 else 0)
    sc_mom = 100 if 45 <= rsi <= 65 else (40 if rsi < 35 else
             (60 if rsi < 45 else (50 if rsi <= 75 else 20)))
    sc_voldel = _clip(50 * vol_surge) * 0.5 + _clip(50 * deliv_surge) * 0.5
    tgt_pct = max(cfg["target_move_rs"] / c * 100, 6.0)
    sc_volfit = _clip(100 * em10_pct / tgt_pct)
    sc_liq = _clip(adv20_cr / 10 * 100)
    prev_c = close.shift(1)
    gaps = ((df["open"] - prev_c).abs() / prev_c * 100).dropna().tail(120)
    gap_p90 = float(gaps.quantile(0.9)) if len(gaps) >= 20 else 0.0
    deliv_avg = float(dl.tail(60).mean()) if len(dl) >= 10 else None

    sc_entry = (100 if stop_pct <= 3 else
                (100 - (stop_pct - 3) * 20 if stop_pct <= 6 else 20))
    if rr10 < 2.5:
        sc_entry = min(sc_entry, 60)
    if gap_p90 > 3.0:
        sc_entry = min(sc_entry, 60)   # wild gappers: stops unreliable
    score = (0.22 * sc_trend + 0.10 * sc_mom + 0.20 * sc_voldel +
             0.16 * sc_volfit + 0.14 * sc_liq + 0.18 * sc_entry)
    mode_b_ok = int((not is_sme) and (not flagged)
                    and adv20_cr >= cfg["liquidity_floor_cr_b"]
                    and c >= cfg["min_price_b"] and c > sma200
                    and (deliv_avg is None or deliv_avg >= 25.0))
    return (float(c), float(atr), float(atr_pct), float(rsi), float(sma20),
            float(sma50), float(sma200), float(ret5), float(ret20),
            float(vol_surge), float(deliv_surge), float(adv20_cr), float(dist52),
            float(swing), float(stop), float(stop_pct), float(em10),
            float(em10_pct), float(rr10), float(score), float(sc_trend),
            float(sc_mom), float(sc_voldel), float(sc_volfit), float(sc_liq),
            float(sc_entry), mode_b_ok, gap_p90,
            deliv_avg if deliv_avg is None else float(deliv_avg))


def cmd_snapshots(con):
    import pandas as pd
    cfg = common.load_config()
    flagged = {r[0] for r in con.execute(
        "SELECT DISTINCT symbol FROM surveillance WHERE date="
        "(SELECT MAX(date) FROM surveillance)")}
    sme = {r[0]: r[1] for r in con.execute("SELECT symbol,is_sme FROM instruments")}
    n = 0
    for (sym,) in con.execute("SELECT DISTINCT symbol FROM eod_prices"):
        df = pd.read_sql_query(
            "SELECT date,open,high,low,close,volume,deliv_pct FROM eod_prices "
            "WHERE symbol=? ORDER BY date", con, params=(sym,),
            index_col="date", parse_dates=["date"])
        if len(df) < 210:
            continue
        try:
            vals = compute_one(df, cfg, sme.get(sym, 0), sym in flagged)
        except Exception:
            continue
        con.execute("INSERT OR REPLACE INTO snapshots VALUES(?,?" + ",?" * 29 + ")",
                    (sym, df.index[-1].strftime("%Y-%m-%d")) + vals)
        n += 1
    con.commit()
    common.set_fresh(con, "snapshots", date.today())
    return {"snapshot_rows": n}


def cmd_events(con):
    s = common.nse_session()
    try:
        j = s.get("https://www.nseindia.com/api/event-calendar", timeout=15).json()
    except Exception:
        return {"event_rows": 0}
    n = 0
    for it in j if isinstance(j, list) else []:
        if not isinstance(it, dict):
            continue
        sym = (it.get("symbol") or "").strip()
        raw = (it.get("date") or "").strip()
        dd = None
        for fmt in ("%d-%b-%Y", "%d %b %Y", "%Y-%m-%d"):
            try:
                dd = datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue
        if sym and dd:
            con.execute("INSERT OR REPLACE INTO events VALUES(?,?,?)",
                        (sym, dd, (it.get("purpose") or "")[:120]))
            n += 1
    con.commit()
    if n:
        common.set_fresh(con, "events", date.today())
    return {"event_rows": n}


def cmd_sectors(con, limit=200):
    import yfinance as yf
    syms = [r[0] for r in con.execute(
        "SELECT symbol FROM instruments WHERE sector IS NULL AND status='active' "
        "ORDER BY symbol LIMIT ?", (limit,))]
    n = 0
    for s_ in syms:
        try:
            sec = (yf.Ticker(s_ + ".NS").info or {}).get("sector")
        except Exception:
            continue
        if sec:
            con.execute("UPDATE instruments SET sector=? WHERE symbol=?", (sec, s_))
            n += 1
    con.commit()
    remaining = con.execute("SELECT COUNT(*) FROM instruments WHERE sector IS NULL "
                            "AND status='active'").fetchone()[0]
    return {"sectors_filled": n, "sectors_remaining": remaining}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["universe", "backfill", "daily", "surveillance",
                                   "fii", "events", "sectors", "snapshots", "full"])
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--symbols", default=None, help="comma list (backfill subset)")
    p.add_argument("--limit", type=int, default=200, help="sectors batch size")
    a = p.parse_args()
    con = common.db()
    try:
        if a.cmd == "universe":
            common.json_out(cmd_universe(con))
        elif a.cmd == "backfill":
            common.json_out(cmd_backfill(con, a.symbols))
        elif a.cmd == "daily":
            common.json_out(cmd_daily(con, a.days))
        elif a.cmd == "surveillance":
            common.json_out(cmd_surveillance(con))
        elif a.cmd == "fii":
            common.json_out(cmd_fii(con))
        elif a.cmd == "events":
            common.json_out(cmd_events(con))
        elif a.cmd == "sectors":
            common.json_out(cmd_sectors(con, a.limit))
        elif a.cmd == "snapshots":
            common.json_out(cmd_snapshots(con))
        elif a.cmd == "full":
            out = {}
            out.update(cmd_daily(con, a.days))
            out.update(cmd_surveillance(con))
            out.update(cmd_fii(con))
            out.update(cmd_events(con))
            out.update(cmd_snapshots(con))
            common.json_out(out)
    except Exception as e:
        common.fail(e)


if __name__ == "__main__":
    main()
