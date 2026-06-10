import numpy as np
import pandas as pd


def seed_trend(env, symbol="TREND", n=300, start=100.0, drift=0.4, sme=0):
    con = env.db()
    con.execute("INSERT OR REPLACE INTO instruments(symbol,name,series,isin,is_sme)"
                " VALUES(?,?,?,?,?)", (symbol, symbol, "EQ", "X", sme))
    dates = pd.bdate_range("2025-01-01", periods=n)
    close = start + drift * np.arange(n) + np.sin(np.arange(n) / 5)
    rows = [(symbol, d.strftime("%Y-%m-%d"), c - 0.5, c + 1.0, c - 1.0, c,
             1_000_000 + (50_000 if i % 7 == 0 else 0), 45.0, "yf")
            for i, (d, c) in enumerate(zip(dates, close))]
    con.executemany("INSERT OR REPLACE INTO eod_prices VALUES(?,?,?,?,?,?,?,?,?)", rows)
    con.commit()
    return con


def test_snapshot_computed(env):
    import update_data
    con = seed_trend(env)
    out = update_data.cmd_snapshots(con)
    assert out["snapshot_rows"] == 1
    s = dict(zip([c[1] for c in con.execute("PRAGMA table_info(snapshots)")],
                 con.execute("SELECT * FROM snapshots").fetchone()))
    assert 0 <= s["rsi14"] <= 100 and s["atr14"] > 0
    assert s["rsi14"] > 55                # rising series
    assert s["stop_price"] < s["close"]
    assert 0 <= s["score"] <= 100
    assert s["em10_rs"] > 0 and s["rr10"] > 0
    assert s["mode_b_ok"] == 1            # liquid, uptrend, non-SME, price>50


def test_mode_b_excludes_sme(env):
    import update_data
    con = seed_trend(env, symbol="SMESTK", sme=1)
    update_data.cmd_snapshots(con)
    v = con.execute("SELECT mode_b_ok FROM snapshots WHERE symbol='SMESTK'").fetchone()[0]
    assert v == 0
