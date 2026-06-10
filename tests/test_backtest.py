import json

import numpy as np
import pandas as pd


def seed_engineered(env, symbol="ENG"):
    """Uptrend, one clean pullback signal, then rally -> known Mode A win."""
    con = env.db()
    con.execute("INSERT OR REPLACE INTO instruments(symbol,name,series,isin,is_sme)"
                " VALUES(?,?,?,?,0)", (symbol, symbol, "EQ", "X"))
    n = 300
    close = 100 + 0.5 * np.arange(n, dtype=float)
    close[260:265] = close[259] * np.array([0.99, 0.975, 0.96, 0.965, 0.97])  # dip
    close[265:] = close[264] + 2.0 * np.arange(1, n - 264)                    # rally
    dates = pd.bdate_range("2025-01-01", periods=n)
    rows = [(symbol, d.strftime("%Y-%m-%d"), c, c * 1.005, c * 0.995, c,
             2_000_000, 50.0, "yf") for d, c in zip(dates, close)]
    con.executemany("INSERT OR REPLACE INTO eod_prices VALUES(?,?,?,?,?,?,?,?,?)",
                    rows)
    con.commit()
    return con


def test_backtest_runs_and_wins(env, capsys):
    import backtest
    con = seed_engineered(env)
    backtest.run(con, setup="pullback", mode="A", years=2)
    r = json.loads(capsys.readouterr().out)
    assert r["signals"] >= 1
    assert r["wins"] + r["losses"] + r["timeouts"] == r["signals"]
    assert "mae_p50_pct" in r and "expectancy_R" in r


def test_backtest_mode_b_recovery(env, capsys):
    import backtest
    con = seed_engineered(env)
    backtest.run(con, setup="pullback", mode="B", years=2)
    r = json.loads(capsys.readouterr().out)
    assert "recovery_buckets" in r and r["signals"] >= 1
