# stock-research — AI-assisted NSE swing-research harness

A personal **Claude Code skill** that turns Claude into a disciplined equity research
analyst for Indian markets (NSE). Claude is the chat interface and reasoning layer;
**10 deterministic Python tools** over a local SQLite cache are its instruments — every
number in every answer comes from computed script output, never from the model's memory.

> ## ⚠️ Disclaimer
> This is a **personal analytics tool**, not investment advice and not a tip service.
> It computes scores, probabilities, expected-move ranges, and risk metrics from public
> end-of-day data. Markets can and will gap through any stop. Nothing here guarantees
> profit; backtested results do not predict live results. Use entirely at your own risk.
> If you redistribute or operate this for others in India, consult a professional about
> SEBI Research Analyst / Investment Adviser regulations first.

## What it does

- **Morning scan** — regime check (Nifty trend, breadth, FII/DII), then evidence-based
  setup screens over ~2,100 NSE stocks with composite + entry-quality scoring
- **Deep research** — full technical panel, ATR expected-move math ("typical 10-session
  move: ₹84 / 6.6%"), red flags, position sizing
- **Trap detection** — ASM/GSM surveillance lists, SME flags, micro-price, illiquidity,
  circuit-proneness, volume-without-delivery manipulation signatures
- **Two labeled modes** — every suggestion is tagged:
  - **Mode A** swing-with-stops: structural stop, R:R ≥ 2.5, 1%-of-capital risk sizing
  - **Mode B** quality-gated patience: hard gate (non-SME, unflagged, liquid, > SMA200),
    no stop by design, equal-weight slots — penny stocks can never appear here
- **Backtesting** — hit rates, MAE (how far winners dipped first), and Mode B
  time-to-recovery distributions on 5 years of local data
- **Trade journal** — every suggestion/entry/exit logged; honest win-rate review

## Architecture

```
SKILL.md                     ← the harness: playbooks + hard behavior rules
references/methodology.md    ← evidence-informed setups, weights, calibration log
references/behavior-rules.md ← 15 non-negotiable rules (grounding, risk-first, ...)
scripts/                     ← argparse CLIs, JSON to stdout
  update_data.py               universe · 5y backfill (yfinance) · daily bhavcopy
                               + delivery % · ASM/GSM · FII/DII · snapshots+scores
  screener.py · technicals.py · expected_move.py · red_flags.py · market_pulse.py
  risk.py · backtest.py · journal.py · setups.py · common.py (Wilder RSI/ATR)
data/  (gitignored)          ← market.db (SQLite), config.yaml (your capital/risk)
tests/                       ← 22 pytest tests (money-math verified by hand)
```

Data sources are all free/official: NSE bhavcopy + surveillance lists + FII/DII,
yfinance adjusted history. No paid APIs, no Docker, no external DB.

## Setup (Windows)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r scripts\requirements.txt
Copy-Item config.yaml.example data\config.yaml        # then edit capital/risk
.\.venv\Scripts\python scripts\update_data.py universe
.\.venv\Scripts\python scripts\update_data.py backfill   # one-time, ~20 min
.\.venv\Scripts\python scripts\update_data.py full       # daily refresh
.\.venv\Scripts\python -m pytest tests/ -q               # 22 passed
```

As a Claude Code skill: clone into `%USERPROFILE%\.claude\skills\stock-research\`
and ask Claude to "scan today" or "research RELIANCE".

## Methodology provenance

Setup definitions and scoring weights are grounded in a verified evidence review
(short-horizon reversal vs momentum on NSE, delivery/volume signals, ASM inclusion
effects, stop-loss and Kelly-sizing literature) — see `docs/` for the full cited
report, design spec, and implementation plan. Final calibration authority is
`backtest.py` on local data, train/test split, per `references/methodology.md`.
