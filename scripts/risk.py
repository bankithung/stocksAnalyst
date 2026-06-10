import argparse, math
import common


def charges_round_trip(buy_val, sell_val, ch):
    brok = (buy_val + sell_val) * ch["brokerage_pct"] / 100
    stt = (buy_val + sell_val) * ch["stt_pct"] / 100
    exch = (buy_val + sell_val) * ch["exchange_pct"] / 100
    sebi = (buy_val + sell_val) * ch["sebi_pct"] / 100
    stamp = buy_val * ch["stamp_buy_pct"] / 100
    gst = (brok + exch + sebi) * ch["gst_pct"] / 100
    return round(brok + stt + exch + sebi + stamp + gst, 2)


def run(entry, stop, target, capital, risk_pct, mode, cfg):
    if mode == "A":
        if stop is None or stop >= entry:
            common.fail("Mode A requires stop below entry (long-only v1)")
        risk_amt = capital * risk_pct / 100
        qty = math.floor(risk_amt / (entry - stop))
        if qty < 1:
            common.fail("risk budget too small for this stop distance")
    else:
        qty = math.floor(capital / cfg["mode_b_positions"] / entry)
        if qty < 1:
            common.fail("capital slot too small for this price")
    exposure = qty * entry
    out = {"mode": mode, "entry": entry, "stop": stop, "target": target,
           "qty": qty, "exposure_rs": round(exposure, 1),
           "charges_round_trip_rs": charges_round_trip(
               exposure, qty * (target or entry), cfg["charges"])}
    if mode == "A":
        out.update({
            "max_loss_rs": round(qty * (entry - stop), 1),
            "risk_pct_of_capital": round(qty * (entry - stop) / capital * 100, 2),
            "rr": round((target - entry) / (entry - stop), 2) if target else None})
    else:
        out["note"] = ("Mode B: no stop by user policy — survivability comes from "
                       "the quality gate, equal-weight sizing and diversification")
    common.json_out(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--entry", type=float, required=True)
    p.add_argument("--stop", type=float, default=None)
    p.add_argument("--target", type=float, default=None)
    p.add_argument("--capital", type=float, default=None)
    p.add_argument("--risk-pct", type=float, default=None)
    p.add_argument("--mode", choices=["A", "B"], default="A")
    a = p.parse_args()
    cfg = common.load_config()
    run(a.entry, a.stop, a.target, a.capital or cfg["capital"],
        a.risk_pct or cfg["risk_pct"], a.mode, cfg)
