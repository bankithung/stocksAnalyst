import argparse
import common
from setups import SETUPS


def run(con, mode="A", setup="any", min_em_rs=None, max_price=None,
        min_score=60, max_stop_pct=None, limit=15, include_flagged=False):
    cfg = common.load_config()
    last = con.execute("SELECT MAX(date) FROM snapshots").fetchone()[0]
    if not last:
        common.fail("no snapshots — run update_data.py full first")
    cols = [c[1] for c in con.execute("PRAGMA table_info(snapshots)")]
    flagged = {r[0] for r in con.execute(
        "SELECT DISTINCT symbol FROM surveillance WHERE date="
        "(SELECT MAX(date) FROM surveillance)")}
    out = []
    for row in con.execute("SELECT * FROM snapshots WHERE date=?", (last,)):
        s = dict(zip(cols, row))
        s["flagged"] = s["symbol"] in flagged
        if mode == "B" and not s["mode_b_ok"]:
            continue
        if mode == "A":
            if s["adv20_cr"] < cfg["liquidity_floor_cr_a"]:
                continue
            if s["flagged"] and not include_flagged:
                continue
        if not SETUPS[setup](s):
            continue
        if min_em_rs and s["em10_rs"] < min_em_rs:
            continue
        if max_price and s["close"] > max_price:
            continue
        if max_stop_pct and s["stop_pct"] > max_stop_pct:
            continue
        if s["score"] < min_score:
            continue
        out.append(s)
    out.sort(key=lambda x: -x["score"])
    keep = ["symbol", "close", "score", "sc_entry", "rr10", "em10_rs", "em10_pct",
            "stop_pct", "stop_price", "rsi14", "ret5", "vol_surge", "deliv_surge",
            "adv20_cr", "dist_52w_high", "flagged", "mode_b_ok"]
    common.json_out({"as_of": last, "mode": mode, "setup": setup,
                     "matches": len(out),
                     "results": [{k: r[k] for k in keep} for r in out[:limit]]})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["A", "B"], default="A")
    p.add_argument("--setup", choices=list(SETUPS), default="any")
    p.add_argument("--min-em-rs", type=float, default=None)
    p.add_argument("--max-price", type=float, default=None)
    p.add_argument("--min-score", type=float, default=60)
    p.add_argument("--max-stop-pct", type=float, default=None)
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--include-flagged", action="store_true")
    a = p.parse_args()
    run(common.db(), a.mode, a.setup, a.min_em_rs, a.max_price, a.min_score,
        a.max_stop_pct, a.limit, a.include_flagged)
