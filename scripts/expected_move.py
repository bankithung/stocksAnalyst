import argparse
import common


def run(symbol, days, con):
    symbol = symbol.upper()
    r = con.execute("SELECT date, close, atr14 FROM snapshots WHERE symbol=? "
                    "ORDER BY date DESC LIMIT 1", (symbol,)).fetchone()
    if not r:
        common.fail(f"no snapshot for {symbol}")
    d, close, atr = r
    em = atr * days ** 0.5
    common.json_out({"symbol": symbol, "as_of": d, "close": close, "days": days,
                     "daily_atr_rs": round(atr, 2),
                     "conservative_rs": round(0.7 * em, 1),
                     "typical_rs": round(em, 1),
                     "optimistic_rs": round(1.3 * em, 1),
                     "typical_pct": round(em / close * 100, 2),
                     "note": "ATR*sqrt(days) range estimate, not a prediction"})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("symbol")
    p.add_argument("--days", type=int, default=10)
    a = p.parse_args()
    run(a.symbol, a.days, common.db())
