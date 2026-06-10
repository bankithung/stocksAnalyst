import argparse
from datetime import date, datetime
import common


def run(symbol, con):
    symbol = symbol.upper()
    row = con.execute("SELECT * FROM snapshots WHERE symbol=? ORDER BY date DESC "
                      "LIMIT 1", (symbol,)).fetchone()
    if not row:
        like = [r[0] for r in con.execute(
            "SELECT symbol FROM instruments WHERE symbol LIKE ? LIMIT 5",
            (f"%{symbol}%",))]
        common.fail(f"no snapshot for {symbol}; similar: {like}")
    cols = [c[1] for c in con.execute("PRAGMA table_info(snapshots)")]
    s = dict(zip(cols, row))
    hi20, lo20 = con.execute(
        "SELECT MAX(high), MIN(low) FROM (SELECT high, low FROM eod_prices "
        "WHERE symbol=? ORDER BY date DESC LIMIT 20)", (symbol,)).fetchone()
    flags = [dict(zip(("list_type", "stage"), r)) for r in con.execute(
        "SELECT list_type, stage FROM surveillance WHERE symbol=? AND date="
        "(SELECT MAX(date) FROM surveillance)", (symbol,))]
    events = [dict(zip(("date", "purpose"), r)) for r in con.execute(
        "SELECT date, purpose FROM events WHERE symbol=? AND date>=date('now') "
        "AND date<=date('now','+10 day') ORDER BY date", (symbol,))]
    trend = ("strong-up" if s["close"] > s["sma20"] > s["sma50"] > s["sma200"] else
             "up" if s["close"] > s["sma200"] else
             "down" if s["close"] < s["sma200"] else "sideways")
    age = (date.today() - datetime.strptime(s["date"], "%Y-%m-%d").date()).days
    common.json_out({**s, "symbol": symbol, "as_of": s["date"],
                     "data_age_days": age, "trend": trend,
                     "support": lo20, "resistance": hi20,
                     "surveillance_flags": flags,
                     "upcoming_events_10d": events})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("symbol")
    run(p.parse_args().symbol, common.db())
