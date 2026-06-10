import json, os, sqlite3, sys
from pathlib import Path
import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("STOCK_RESEARCH_DATA", SKILL_DIR / "data"))
DB_PATH = Path(os.environ.get("STOCK_RESEARCH_DB", DATA_DIR / "market.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS instruments(
  symbol TEXT PRIMARY KEY, name TEXT, series TEXT, isin TEXT,
  is_sme INTEGER DEFAULT 0, status TEXT DEFAULT 'active');
CREATE TABLE IF NOT EXISTS eod_prices(
  symbol TEXT, date TEXT, open REAL, high REAL, low REAL, close REAL,
  volume REAL, deliv_pct REAL, source TEXT,
  PRIMARY KEY(symbol, date));
CREATE TABLE IF NOT EXISTS surveillance(
  symbol TEXT, date TEXT, list_type TEXT, stage TEXT,
  PRIMARY KEY(symbol, date, list_type));
CREATE TABLE IF NOT EXISTS fii_dii(
  date TEXT, category TEXT, buy_cr REAL, sell_cr REAL, net_cr REAL,
  PRIMARY KEY(date, category));
CREATE TABLE IF NOT EXISTS snapshots(
  symbol TEXT, date TEXT, close REAL, atr14 REAL, atr_pct REAL, rsi14 REAL,
  sma20 REAL, sma50 REAL, sma200 REAL, ret5 REAL, ret20 REAL,
  vol_surge REAL, deliv_surge REAL, adv20_cr REAL, dist_52w_high REAL,
  swing_low_10 REAL, stop_price REAL, stop_pct REAL,
  em10_rs REAL, em10_pct REAL, rr10 REAL,
  score REAL, sc_trend REAL, sc_mom REAL, sc_voldel REAL, sc_volfit REAL,
  sc_liq REAL, sc_entry REAL, mode_b_ok INTEGER,
  PRIMARY KEY(symbol, date));
CREATE INDEX IF NOT EXISTS idx_snap_date ON snapshots(date);
CREATE TABLE IF NOT EXISTS freshness(
  source TEXT PRIMARY KEY, last_date TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS journal(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, symbol TEXT, mode TEXT,
  action TEXT, price REAL, qty INTEGER, stop REAL, target REAL,
  thesis TEXT, status TEXT DEFAULT 'idea', outcome_pct REAL, closed_ts TEXT);
"""

DEFAULTS = {
    "capital": 100000, "risk_pct": 1.0, "mode_b_positions": 8, "tax_slab": 20,
    "target_move_rs": 50, "target_days": 10,
    "liquidity_floor_cr_a": 2.0, "liquidity_floor_cr_b": 5.0, "min_price_b": 50,
    "charges": {"brokerage_pct": 0.0, "stt_pct": 0.1, "exchange_pct": 0.00297,
                "sebi_pct": 0.0001, "stamp_buy_pct": 0.015, "gst_pct": 18.0},
}


def db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(SCHEMA)
    return con


def load_config():
    cfg = dict(DEFAULTS)
    p = Path(os.environ.get("STOCK_RESEARCH_CONFIG", DATA_DIR / "config.yaml"))
    if p.exists():
        user = yaml.safe_load(p.read_text()) or {}
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg


def json_out(obj):
    print(json.dumps(obj, indent=1, default=str))


def fail(msg):
    print(json.dumps({"error": str(msg)}))
    sys.exit(1)


def set_fresh(con, source, last_date):
    from datetime import datetime
    con.execute("INSERT OR REPLACE INTO freshness VALUES(?,?,?)",
                (source, str(last_date), datetime.now().isoformat(timespec="seconds")))
    con.commit()


def nse_session():
    import requests
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                      "Accept-Language": "en-US,en;q=0.9"})
    try:
        s.get("https://www.nseindia.com", timeout=10)
    except Exception:
        pass
    return s


# --- Indicators (Wilder) — replaces pandas-ta (0.3.14b0 delisted from PyPI) ---

def rsi(close, length=14):
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1.0 / length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / length, min_periods=length, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0.0, 1e-12)
    return 100.0 - 100.0 / (1.0 + rs)


def atr(high, low, close, length=14):
    import pandas as pd
    prev_close = close.shift(1)
    tr = pd.concat([(high - low).abs(),
                    (high - prev_close).abs(),
                    (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / length, min_periods=length, adjust=False).mean()
