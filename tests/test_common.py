import numpy as np
import pandas as pd


def test_schema_and_config(env):
    con = env.db()
    tables = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"instruments", "eod_prices", "surveillance", "fii_dii",
            "snapshots", "freshness", "journal"} <= tables
    cfg = env.load_config()
    assert cfg["risk_pct"] == 1.0 and cfg["target_move_rs"] == 50


def test_json_out(env, capsys):
    env.json_out({"a": 1})
    assert '"a": 1' in capsys.readouterr().out


def test_rsi_wilder(env):
    # Monotonic rise: no losses -> RSI converges to 100
    close = pd.Series(np.arange(1, 60, dtype=float))
    r = env.rsi(close, 14)
    assert r.iloc[-1] > 99.0
    # Monotonic fall -> RSI converges to 0
    r2 = env.rsi(pd.Series(np.arange(60, 1, -1, dtype=float)), 14)
    assert r2.iloc[-1] < 1.0
    # Always bounded
    mixed = pd.Series(100 + np.sin(np.arange(100)) * 5)
    rm = env.rsi(mixed, 14).dropna()
    assert ((rm >= 0) & (rm <= 100)).all()


def test_atr_constant_range(env):
    # Constant H-L range of 2.0 with flat closes -> ATR == 2.0
    n = 60
    close = pd.Series(np.full(n, 100.0))
    high = close + 1.0
    low = close - 1.0
    a = env.atr(high, low, close, 14)
    assert abs(a.iloc[-1] - 2.0) < 1e-9
