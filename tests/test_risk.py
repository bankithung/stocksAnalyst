import json

import pytest


def test_mode_a_sizing(env, capsys):
    import risk
    risk.run(entry=100.0, stop=97.0, target=110.0, capital=100000,
             risk_pct=1.0, mode="A", cfg=env.load_config())
    r = json.loads(capsys.readouterr().out)
    assert r["qty"] == 333                      # floor(1000 / 3)
    assert r["max_loss_rs"] == 999.0            # 333 * 3
    assert r["exposure_rs"] == 33300.0
    assert r["rr"] == 3.33                      # 10 / 3
    assert 0 < r["charges_round_trip_rs"] < 200
    assert r["risk_pct_of_capital"] == 1.0


def test_stop_must_be_below_entry(env, capsys):
    import risk
    with pytest.raises(SystemExit):
        risk.run(entry=100.0, stop=101.0, target=None, capital=100000,
                 risk_pct=1.0, mode="A", cfg=env.load_config())


def test_concentration_warning(env, capsys):
    import risk
    risk.run(entry=100.0, stop=99.0, target=110.0, capital=100000,
             risk_pct=1.0, mode="A", cfg=env.load_config())
    r = json.loads(capsys.readouterr().out)
    assert r["exposure_rs"] == 100000.0          # 1000 shares, 100% of capital
    assert "concentration_warning" in r


def test_mode_b_equal_weight(env, capsys):
    import risk
    risk.run(entry=200.0, stop=None, target=None, capital=80000,
             risk_pct=1.0, mode="B", cfg=env.load_config())
    r = json.loads(capsys.readouterr().out)
    assert r["qty"] == 50                       # floor(80000/8/200)
    assert r["mode"] == "B" and "no stop" in r["note"].lower()
