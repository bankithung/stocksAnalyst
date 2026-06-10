import argparse
import common


def run(con, nifty_df=None):
    if nifty_df is None:
        import yfinance as yf
        nifty_df = yf.download("^NSEI", period="2y", auto_adjust=True,
                               progress=False)
        if nifty_df is None or nifty_df.empty:
            common.fail("could not fetch ^NSEI")
        if hasattr(nifty_df.columns, "levels"):       # flatten MultiIndex
            nifty_df.columns = nifty_df.columns.get_level_values(0)
    c = nifty_df["Close"]
    n = float(c.iloc[-1])
    s50 = float(c.rolling(50).mean().iloc[-1])
    s200 = float(c.rolling(200).mean().iloc[-1])
    trend = "up" if n > s50 > s200 else ("down" if n < s50 else "sideways")
    last = con.execute("SELECT MAX(date) FROM snapshots").fetchone()[0]
    tot, above = con.execute(
        "SELECT COUNT(*), SUM(CASE WHEN close>sma50 THEN 1 ELSE 0 END) "
        "FROM snapshots WHERE date=?", (last,)).fetchone()
    breadth = round(100.0 * (above or 0) / tot, 1) if tot else None
    fii = [dict(zip(("date", "category", "net_cr"), r)) for r in con.execute(
        "SELECT date, category, net_cr FROM fii_dii ORDER BY date DESC LIMIT 10")]
    regime = ("supportive" if trend == "up" and (breadth or 0) >= 55 else
              "hostile" if trend == "down" or (breadth or 100) < 35 else "neutral")
    common.json_out({"as_of": last, "nifty_close": round(n, 1),
                     "nifty_trend": trend, "breadth_pct_above_sma50": breadth,
                     "fii_dii_recent": fii, "regime": regime,
                     "guidance": {"supportive": "normal sizing",
                                  "neutral": "half size / strict setups only",
                                  "hostile": "sit out or minimal size"}[regime]})


if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    run(common.db())
