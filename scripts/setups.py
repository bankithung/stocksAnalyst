# Setup conditions over snapshot rows (dict s -> bool). Evidence-informed v1;
# calibration pending backtest.py (references/methodology.md).
SETUPS = {
    "pullback": lambda s: (s["close"] > s["sma200"] and s["sma50"] > s["sma200"]
                           and -7.0 <= s["ret5"] <= -1.0 and 35 <= s["rsi14"] <= 55
                           and s["stop_pct"] <= 5.0),
    "breakout": lambda s: (s["dist_52w_high"] >= -3.0 and s["vol_surge"] >= 1.8
                           and s["deliv_surge"] >= 1.2
                           and s["close"] > s["sma50"] > s["sma200"]),
    "any": lambda s: True,
}
