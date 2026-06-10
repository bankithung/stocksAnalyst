EQUITY_L_SAMPLE = """SYMBOL,NAME OF COMPANY, SERIES, DATE OF LISTING, PAID UP VALUE, MARKET LOT, ISIN NUMBER, FACE VALUE
RELIANCE,Reliance Industries Limited, EQ, 29-NOV-1995, 10, 1, INE002A01018, 10
TINYSME,Tiny SME Ltd, SM, 01-JAN-2024, 10, 1600, INE000TEST01, 10
"""


def test_parse_equity_list(env):
    import update_data
    rows = update_data.parse_equity_list(EQUITY_L_SAMPLE)
    assert ("RELIANCE", "Reliance Industries Limited", "EQ", "INE002A01018", 0) in rows
    assert ("TINYSME", "Tiny SME Ltd", "SM", "INE000TEST01", 1) in rows


def test_universe_upsert(env):
    import update_data
    con = env.db()
    update_data.upsert_universe(con, update_data.parse_equity_list(EQUITY_L_SAMPLE))
    n = con.execute("SELECT COUNT(*) FROM instruments").fetchone()[0]
    assert n == 2


BHAV_SAMPLE = """SYMBOL, SERIES, DATE1, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, LAST_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES, DELIV_QTY, DELIV_PER
RELIANCE, EQ, 09-Jun-2026, 2900, 2910, 2950, 2905, 2940, 2945.5, 2930, 5000000, 146500, 250000, 2500000, 50.00
JUNK, BE, 09-Jun-2026, 10, 10, 11, 9, 10, 10.5, 10, 100, 1, 10, 50, 50.00
"""


def test_parse_bhav(env):
    import update_data
    rows = update_data.parse_bhav(BHAV_SAMPLE)
    assert rows[0][:2] == ("RELIANCE", "2026-06-09")
    assert rows[0][7] == 50.0          # deliv_pct
    assert len(rows) == 2              # BE series kept too


def test_upsert_prices_idempotent(env):
    import pandas as pd
    import update_data
    con = env.db()
    df = pd.DataFrame({"Open": [10.0], "High": [11.0], "Low": [9.5],
                       "Close": [10.5], "Volume": [1000.0]},
                      index=pd.to_datetime(["2026-06-01"]))
    n1 = update_data.upsert_prices(con, "TEST", df, "yf")
    n2 = update_data.upsert_prices(con, "TEST", df, "yf")
    assert n1 == n2 == 1
    assert con.execute("SELECT COUNT(*) FROM eod_prices").fetchone()[0] == 1
