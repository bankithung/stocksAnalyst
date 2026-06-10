from test_snapshots import seed_trend


def test_expected_move(env, capsys):
    import update_data, expected_move
    con = seed_trend(env)
    update_data.cmd_snapshots(con)
    expected_move.run("TREND", 10, con)
    out = capsys.readouterr().out
    assert '"typical_rs"' in out and '"typical_pct"' in out and '"days": 10' in out


def test_red_flags(env, capsys):
    import json
    import update_data, red_flags
    con = seed_trend(env, "RISKY", start=8.0, drift=0.01)   # ~Rs 8 micro-price
    con.execute("INSERT OR REPLACE INTO surveillance VALUES('RISKY',"
                "(SELECT MAX(date) FROM eod_prices),'GSM','2')")
    con.commit()
    update_data.cmd_snapshots(con)
    red_flags.run("RISKY", con)
    res = json.loads(capsys.readouterr().out)
    kinds = {f["flag"] for f in res["flags"]}
    assert "surveillance" in kinds and "micro_price" in kinds
    assert res["severity"] == "high"


def test_technicals(env, capsys):
    import update_data, technicals
    con = seed_trend(env)
    update_data.cmd_snapshots(con)
    technicals.run("TREND", con)
    out = capsys.readouterr().out
    for key in ('"symbol"', '"rsi14"', '"trend"', '"support"', '"resistance"',
                '"as_of"', '"data_age_days"'):
        assert key in out
