import json

from test_snapshots import seed_trend


def seed_three(env):
    import update_data
    con = seed_trend(env, "CLEAN")
    seed_trend(env, "SMESTK", sme=1)
    seed_trend(env, "FLAGGED")
    con.execute("INSERT OR REPLACE INTO surveillance VALUES('FLAGGED',"
                "(SELECT MAX(date) FROM eod_prices),'ASM','1')")
    con.commit()
    update_data.cmd_snapshots(con)
    return con


def test_mode_b_gates(env, capsys):
    import screener
    con = seed_three(env)
    screener.run(con, mode="B", setup="any", min_score=0, limit=10)
    res = json.loads(capsys.readouterr().out)
    syms = [r["symbol"] for r in res["results"]]
    assert "CLEAN" in syms and "SMESTK" not in syms and "FLAGGED" not in syms


def test_mode_a_shows_flag(env, capsys):
    import screener
    con = seed_three(env)
    screener.run(con, mode="A", setup="any", min_score=0, limit=10,
                 include_flagged=True)
    res = json.loads(capsys.readouterr().out)
    f = [r for r in res["results"] if r["symbol"] == "FLAGGED"]
    assert f and f[0]["flagged"] is True
