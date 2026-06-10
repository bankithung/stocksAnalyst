import json


def test_journal_cycle(env, capsys):
    import journal
    con = env.db()
    journal.add(con, "TREND", "A", 100.0, 97.0, 110.0, "pullback test")
    capsys.readouterr()
    journal.entry(con, 1, 100.0, 333)
    capsys.readouterr()
    journal.exit_(con, 1, 110.0)
    out = json.loads(capsys.readouterr().out)
    assert out["outcome_pct"] == 10.0 and out["status"] == "closed"
    journal.review(con)
    rev = json.loads(capsys.readouterr().out)
    assert rev["closed"] == 1 and rev["win_rate_pct"] == 100.0
