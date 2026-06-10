# Methodology v1 (evidence-informed; FINAL CALIBRATION PENDING backtest.py runs)

Evidence source: techsubmit repo, `docs/superpowers/specs/2026-06-10-strategy-evidence.md`
(v2 — all claims verified; zero unresolved). Every number below is a starting default.
After Phase-3 backtests, update this file and record the run results beside each change.

## Modes (every suggestion MUST carry its mode tag)
- **Mode A — swing with stops:** full universe (flags shown), stop ≤ ~3-5% at validated
  support − 0.5×ATR buffer, R:R ≥ 2.5 required, 1% capital risk per trade, horizon 10
  sessions, exit at stop/target/timeout. The stop is a **risk-control / tail-cutting
  device** at this horizon (Kaminski & Lo 2014: the expected-return "stopping premium"
  is a longer-horizon effect — do not present the stop as a Sharpe booster).
- **Mode B — no-loss patience (user's style):** quality gate is HARD — non-SME, no
  ASM/GSM, ADV20 ≥ ₹5 cr, price ≥ ₹50, close > SMA200. No stop; sell only in profit;
  holding may extend months. Equal-weight slots (capital / 8). Penny stocks NEVER.

## Setups (definitions live in scripts/setups.py — keep in sync)
- **pullback** (evidence: short-term reversal edge at 5-15d): uptrend (close>SMA200,
  SMA50>SMA200), dip ret5 in [-7%, -1%], RSI14 35-55, stop_pct ≤ 5.
- **breakout** (weaker evidence at this horizon — trade selectively): within 3% of 52w
  high, vol_surge ≥ 1.8, deliv_surge ≥ 1.2, close>SMA50>SMA200.

## Composite score weights (v1; fundamental weight redistributed — bulk fundamentals
## not ingested; Mode B quality confirmed at deep-dive time)
trend 22 · momentum 10 (lowered: sub-week edge is reversal, not continuation) ·
volume/delivery 20 (raised: best-evidenced India EOD signal) · volatility-fit 16 ·
liquidity 14 · entry-quality 18.

## Entry Quality
stop distance ≤3% → full marks (3-6% degrades, >6% floor); R:R < 2.5 caps the component
at 60; volatility-fit targets max(₹50, 6%) expected 10-session move; avoid entries within
~5 sessions of scheduled results (Claude checks the calendar via web at deep-dive).
R:R ≥ 2.5 is independently corroborated by CANSLIM's ~30%-win/3:1-reward structure.

## Evidence notes binding behavior
- RSI/MACD are CONTEXT ONLY, never standalone triggers (no edge vs unconditional
  returns on Indian indices — supported, peer-reviewed).
- ASM/GSM = hard red flag (run-ups historically reverse: +10.5% → −0.9% CAAR; exit from
  ASM is NOT a bullish catalyst).
- Low delivery % on a volume spike = manipulation signature (supported).
- Bulk-deal returns accrue pre-disclosure (front-running) — never chase bulk deals EOD.
- Sizing: fixed-fractional 1% rule; above-Kelly sizing is growth-security dominated.
- ML/LLM-sentiment signals: confirmed out of v1 as drivers (fragile after costs;
  1-2 day drift only).
- F-score/quality: long-horizon survival filter (Mode B gate), not a swing trigger.

## Backtest discipline (before trusting ANY change)
Run A: signals ≥ 100, win_rate, expectancy_R > 0, MAE p90 — train period pre-2024-06,
then ONE confirmation on post-2024-06 data. Reject parameter changes that only help in
one period or where ±10% parameter wiggle kills the result.

## Calibration log
- (pending first full-universe backtest runs)
