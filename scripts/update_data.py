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


def cmd_daily(con, days=7):
    raise NotImplementedError


def cmd_surveillance(con):
    raise NotImplementedError


def cmd_fii(con):
    raise NotImplementedError


def cmd_snapshots(con):
    raise NotImplementedError


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["universe", "backfill", "daily",
                                   "surveillance", "fii", "snapshots", "full"])
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--symbols", default=None, help="comma list (backfill subset)")
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
        elif a.cmd == "snapshots":
            common.json_out(cmd_snapshots(con))
        elif a.cmd == "full":
            out = {}
            out.update(cmd_daily(con, a.days))
            out.update(cmd_surveillance(con))
            out.update(cmd_fii(con))
            out.update(cmd_snapshots(con))
            common.json_out(out)
    except Exception as e:
        common.fail(e)


if __name__ == "__main__":
    main()
