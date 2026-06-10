import argparse
import common


def run(symbol, con):
    symbol = symbol.upper()
    s = con.execute("SELECT date, close, adv20_cr, deliv_surge FROM snapshots "
                    "WHERE symbol=? ORDER BY date DESC LIMIT 1", (symbol,)).fetchone()
    if not s:
        common.fail(f"no data for {symbol}")
    d, close, adv20, dsurge = s
    flags = []
    for lt, st in con.execute("SELECT list_type, stage FROM surveillance WHERE "
                              "symbol=? AND date=(SELECT MAX(date) FROM surveillance)",
                              (symbol,)):
        flags.append({"flag": "surveillance", "detail": f"{lt} stage {st}",
                      "sev": 3, "why": "ASM/GSM names historically reverse run-ups"})
    is_sme = con.execute("SELECT is_sme FROM instruments WHERE symbol=?",
                         (symbol,)).fetchone()
    if is_sme and is_sme[0]:
        flags.append({"flag": "sme_board", "detail": "SME series", "sev": 3,
                      "why": "thin float, manipulation-prone, Mode B never allows"})
    if close < 20:
        flags.append({"flag": "micro_price", "detail": f"price Rs {close:.2f}",
                      "sev": 3, "why": "classic operator territory"})
    if adv20 < 1.0:
        flags.append({"flag": "illiquid", "detail": f"Rs {adv20:.2f} cr/day avg",
                      "sev": 3, "why": "exit slippage; stops unreliable"})
    rets = [r[0] for r in con.execute(
        "SELECT close FROM eod_prices WHERE symbol=? ORDER BY date DESC LIMIT 61",
        (symbol,))]
    big = sum(1 for a, b in zip(rets, rets[1:]) if b and abs(a / b - 1) >= 0.095)
    if big >= 5:
        flags.append({"flag": "circuit_prone", "detail": f"{big} moves >=9.5% in 60d",
                      "sev": 2, "why": "gap/lock risk — stops jump"})
    if dsurge and dsurge < 0.6:
        flags.append({"flag": "low_delivery_spike",
                      "detail": f"delivery surge {dsurge:.2f}x", "sev": 2,
                      "why": "volume without delivery = churn/manipulation signature"})
    sev = ("high" if any(f["sev"] >= 3 for f in flags) else
           "medium" if flags else "clean")
    common.json_out({"symbol": symbol, "as_of": d, "severity": sev, "flags": flags,
                     "note": "pledge %/promoter checks: do via web at deep-dive"})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("symbol")
    run(p.parse_args().symbol, common.db())
