import argparse
from datetime import datetime
import common


def _now():
    return datetime.now().isoformat(timespec="seconds")


def add(con, symbol, mode, price, stop, target, thesis):
    con.execute("INSERT INTO journal(ts,symbol,mode,action,price,stop,target,"
                "thesis,status) VALUES(?,?,?,?,?,?,?,?,'idea')",
                (_now(), symbol.upper(), mode, "suggested", price, stop, target,
                 thesis))
    con.commit()
    common.json_out({"id": con.execute("SELECT MAX(id) FROM journal").fetchone()[0],
                     "status": "idea"})


def entry(con, id_, price, qty):
    con.execute("UPDATE journal SET action='entered', price=?, qty=?, "
                "status='open', ts=? WHERE id=?", (price, qty, _now(), id_))
    con.commit()
    common.json_out({"id": id_, "status": "open"})


def exit_(con, id_, price):
    row = con.execute("SELECT price FROM journal WHERE id=?", (id_,)).fetchone()
    if not row:
        common.fail(f"no journal id {id_}")
    pct = round((price / row[0] - 1) * 100, 2)
    con.execute("UPDATE journal SET status='closed', outcome_pct=?, closed_ts=? "
                "WHERE id=?", (pct, _now(), id_))
    con.commit()
    common.json_out({"id": id_, "status": "closed", "outcome_pct": pct})


def review(con):
    rows = con.execute("SELECT symbol,mode,status,outcome_pct,thesis FROM journal"
                       ).fetchall()
    closed = [r for r in rows if r[2] == "closed"]
    wins = [r for r in closed if (r[3] or 0) > 0]
    common.json_out({
        "total": len(rows), "open": sum(1 for r in rows if r[2] == "open"),
        "closed": len(closed),
        "win_rate_pct": round(100 * len(wins) / len(closed), 1) if closed else None,
        "avg_outcome_pct": round(sum(r[3] for r in closed) / len(closed), 2)
        if closed else None,
        "by_mode": {m: sum(1 for r in closed if r[1] == m) for m in ("A", "B")},
        "rows": [dict(zip(("symbol", "mode", "status", "outcome_pct", "thesis"), r))
                 for r in rows[-30:]]})


def list_(con):
    rows = con.execute("SELECT id,ts,symbol,mode,action,price,qty,stop,target,"
                       "status,outcome_pct FROM journal ORDER BY id DESC LIMIT 50")
    cols = ("id", "ts", "symbol", "mode", "action", "price", "qty", "stop",
            "target", "status", "outcome_pct")
    common.json_out([dict(zip(cols, r)) for r in rows])


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add")
    for f in ("--symbol", "--mode", "--thesis"):
        pa.add_argument(f, required=True)
    for f in ("--price", "--stop", "--target"):
        pa.add_argument(f, type=float)
    pe = sub.add_parser("entry")
    pe.add_argument("--id", type=int, required=True)
    pe.add_argument("--price", type=float, required=True)
    pe.add_argument("--qty", type=int, required=True)
    px = sub.add_parser("exit")
    px.add_argument("--id", type=int, required=True)
    px.add_argument("--price", type=float, required=True)
    sub.add_parser("review")
    sub.add_parser("list")
    a = p.parse_args()
    con = common.db()
    {"add": lambda: add(con, a.symbol, a.mode, a.price, a.stop, a.target, a.thesis),
     "entry": lambda: entry(con, a.id, a.price, a.qty),
     "exit": lambda: exit_(con, a.id, a.price),
     "review": lambda: review(con), "list": lambda: list_(con)}[a.cmd]()
