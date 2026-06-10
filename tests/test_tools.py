from test_snapshots import seed_trend


def test_technicals(env, capsys):
    import update_data, technicals
    con = seed_trend(env)
    update_data.cmd_snapshots(con)
    technicals.run("TREND", con)
    out = capsys.readouterr().out
    for key in ('"symbol"', '"rsi14"', '"trend"', '"support"', '"resistance"',
                '"as_of"', '"data_age_days"'):
        assert key in out
