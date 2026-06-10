import argparse
from datetime import date, timedelta
import numpy as np
import pandas as pd
import common
from setups import SETUPS
from update_data import compute_one


def _snapshot_series(df, cfg):
    """Walk forward; yield (i, snapshot_dict) for each day with >=210 history."""
    cols = ["close", "atr14", "atr_pct", "rsi14", "sma20", "sma50", "sma200",
            "ret5", "ret20", "vol_surge", "deliv_surge", "adv20_cr",
            "dist_52w_high", "swing_low_10", "stop_price", "stop_pct", "em10_rs",
            "em10_pct", "rr10", "score", "sc_trend", "sc_mom", "sc_voldel",
            "sc_volfit", "sc_liq", "sc_entry", "mode_b_ok", "gap_p90", "deliv_avg"]
    for i in range(210, len(df) - 1):
        vals = compute_one(df.iloc[: i + 1], cfg, 0, False)
        yield i, dict(zip(cols, vals))


def run(con, setup="pullback", mode="A", years=5, horizon=None):
    cfg = common.load_config()
    horizon = horizon or cfg["target_days"]
    since = (date.today() - timedelta(days=365 * years)).strftime("%Y-%m-%d")
    syms = [r[0] for r in con.execute(
        "SELECT DISTINCT symbol FROM eod_prices WHERE date>=?", (since,))]
    wins = losses = timeouts = signals = 0
    rets, maes, recovery = [], [], []
    for sym in syms:
        df = pd.read_sql_query(
            "SELECT date,open,high,low,close,volume,deliv_pct FROM eod_prices "
            "WHERE symbol=? AND date>=? ORDER BY date", con, params=(sym, since),
            index_col="date", parse_dates=["date"])
        if len(df) < 230:
            continue
        cooldown = -1
        for i, s in _snapshot_series(df, cfg):
            if i <= cooldown or not SETUPS[setup](s):
                continue
            if mode == "B" and s["adv20_cr"] < cfg["liquidity_floor_cr_b"]:
                continue
            signals += 1
            cooldown = i + horizon
            entry = float(df["close"].iloc[i])
            target = entry * (1 + s["em10_pct"] / 100)
            stop = s["stop_price"]
            fwd = df.iloc[i + 1: i + 1 + horizon]
            lows, highs = fwd["low"].values, fwd["high"].values
            mae = (entry - min(lows.min(), entry)) / entry * 100 if len(lows) else 0
            maes.append(mae)
            if mode == "A":
                hit_t = int(np.argmax(highs >= target)) if (highs >= target).any() else -1
                hit_s = int(np.argmax(lows <= stop)) if (lows <= stop).any() else -1
                if hit_t >= 0 and (hit_s < 0 or hit_t <= hit_s):
                    wins += 1
                    rets.append((target - entry) / (entry - stop))
                elif hit_s >= 0:
                    losses += 1
                    rets.append(-1.0)
                else:
                    timeouts += 1
                    rets.append((float(fwd["close"].iloc[-1]) - entry) / (entry - stop))
            else:
                fut = df["close"].iloc[i + 1: i + 251].values
                above = int(np.argmax(fut > entry)) if (fut > entry).any() else -1
                recovery.append(above if above >= 0 else 999)
                wins += 1 if 0 <= above < horizon else 0
    out = {"setup": setup, "mode": mode, "years": years, "horizon": horizon,
           "symbols_scanned": len(syms), "signals": signals,
           "mae_p50_pct": round(float(np.percentile(maes, 50)), 2) if maes else None,
           "mae_p90_pct": round(float(np.percentile(maes, 90)), 2) if maes else None}
    if mode == "A":
        out.update({"wins": wins, "losses": losses, "timeouts": timeouts,
                    "win_rate_pct": round(100 * wins / signals, 1) if signals else None,
                    "expectancy_R": round(float(np.mean(rets)), 3) if rets else None})
    else:
        b = lambda lo, hi: sum(1 for r in recovery if lo <= r < hi)
        out.update({"wins": wins, "losses": 0, "timeouts": signals - wins,
                    "recovery_buckets": {"<=21d": b(0, 22), "22-63d": b(22, 64),
                                         "64-126d": b(64, 127),
                                         "127-250d": b(127, 251),
                                         "never_in_1y": b(251, 10_000)}})
    out["caveats"] = ("entry at signal close (optimistic ~0.5-1%); no slippage; "
                      "survivorship bias (current universe only); "
                      "validate before live use")
    common.json_out(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--setup", choices=list(SETUPS), default="pullback")
    p.add_argument("--mode", choices=["A", "B"], default="A")
    p.add_argument("--years", type=int, default=5)
    p.add_argument("--horizon", type=int, default=None)
    a = p.parse_args()
    run(common.db(), a.setup, a.mode, a.years, a.horizon)
