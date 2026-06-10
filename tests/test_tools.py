from test_snapshots import seed_trend


def test_expected_move(env, capsys):
    import update_data, expected_move
    con = seed_trend(env)
    update_data.cmd_snapshots(con)
    expected_move.run("TREND", 10, con)
    out = capsys.readouterr().out
    assert '"typical_rs"' in out and '"typical_pct"' in out and '"days": 10' in out


def test_technicals(env, capsys):
    import update_data, technicals
    con = seed_trend(env)
    update_data.cmd_snapshots(con)
    technicals.run("TREND", con)
    out = capsys.readouterr().out
    for key in ('"symbol"', '"rsi14"', '"trend"', '"support"', '"resistance"',
                '"as_of"', '"data_age_days"'):
        assert key in out
