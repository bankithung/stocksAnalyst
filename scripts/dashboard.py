import argparse, json
from datetime import datetime
import common
from screener import gather
from setups import SETUPS

TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><title>stock-research dashboard</title>
<style>
:root{--bg:#0f1419;--panel:#171d24;--line:#2a3441;--tx:#d6dee8;--dim:#8395a7;
--acc:#4fc3f7;--good:#66bb6a;--warn:#ffa726;--bad:#ef5350}
*{box-sizing:border-box;margin:0}body{background:var(--bg);color:var(--tx);
font:14px/1.45 system-ui,Segoe UI,sans-serif;padding:18px}
h1{font-size:18px;margin-bottom:2px}.sub{color:var(--dim);font-size:12px;margin-bottom:14px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:end;background:var(--panel);
border:1px solid var(--line);border-radius:10px;padding:12px;margin-bottom:14px}
.f{display:flex;flex-direction:column;gap:3px;font-size:11px;color:var(--dim)}
.f input,.f select{background:var(--bg);color:var(--tx);border:1px solid var(--line);
border-radius:6px;padding:5px 8px;font-size:13px;min-width:90px}
.f input[type=range]{min-width:120px;padding:0}
.modes button{background:var(--bg);color:var(--dim);border:1px solid var(--line);
padding:6px 14px;cursor:pointer;font-size:13px}
.modes button.on{color:var(--bg);background:var(--acc);border-color:var(--acc);font-weight:600}
.modes button:first-child{border-radius:6px 0 0 6px}.modes button:last-child{border-radius:0 6px 6px 0}
.count{margin-left:auto;color:var(--dim);font-size:12px}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--dim);
text-align:right;padding:9px 10px;border-bottom:1px solid var(--line);cursor:pointer;user-select:none;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
tr.row{cursor:pointer}tr.row:hover{background:#1d2630}
.sym{font-weight:700;font-size:15px;letter-spacing:.02em;color:var(--acc)}.tag{font-size:10px;border:1px solid var(--line);
border-radius:4px;padding:1px 5px;margin-left:6px;color:var(--dim)}
.s-hi{color:var(--good);font-weight:600}.s-md{color:var(--warn)}.s-lo{color:var(--dim)}
.flag{color:var(--bad);font-weight:700}
.detail td{background:#131a21;text-align:left;font-size:12.5px;color:var(--dim);padding:10px 14px}
.detail b{color:var(--tx)}.kv{display:inline-block;margin-right:18px}
.note{margin-top:12px;color:var(--dim);font-size:11.5px}
</style></head><body>
<h1>stock-research — scan dashboard</h1>
<div class="sub" id="sub"></div>
<div class="bar">
 <div class="f">Mode<span class="modes"><button id="mA" class="on">A · swing</button><button id="mB">B · quality</button></span></div>
 <div class="f">Setup<select id="setup"><option value="">all</option><option>pullback</option><option>breakout</option></select></div>
 <div class="f">Min score <span id="vScore">60</span><input id="score" type="range" min="0" max="100" value="60"></div>
 <div class="f">Max price ₹<input id="price" type="number" placeholder="any"></div>
 <div class="f">Max stop %<input id="stop" type="number" placeholder="any" step="0.5"></div>
 <div class="f">Min move ₹ (10s)<input id="em" type="number" placeholder="any"></div>
 <div class="f">Search<input id="q" type="text" placeholder="symbol"></div>
 <div class="count" id="count"></div>
</div>
<table><thead><tr id="head"></tr></thead><tbody id="body"></tbody></table>
<div class="note">Mode A = swing with stops (1% rule, R:R ≥ 2.5). Mode B = quality gate, no penny/SME/flagged names, patience exits.
Expected move = ATR×√10 range estimate, not a prediction; down is as likely as up. Analytics, not advice. Validate via backtest before live use.</div>
<script>
const P=__PAYLOAD__;
const COLS=[["symbol","Symbol"],["close","Close ₹"],["score","Score"],["sc_entry","Entry Q"],
["rr10","R:R"],["em10_rs","Move ₹"],["em10_pct","Move %"],["stop_pct","Stop %"],
["rsi14","RSI"],["ret5","5d %"],["vol_surge","Vol×"],["deliv_surge","Del×"],["adv20_cr","ADV cr"]];
let mode="A",sortK="score",sortD=-1,openSym=null;
const el=id=>document.getElementById(id);
el("sub").textContent=`data as of ${P.as_of} · generated ${P.generated} · ${P.A.length} Mode-A rows · ${P.B.length} Mode-B rows (pre-filter)`;
el("head").innerHTML=COLS.map(c=>`<th data-k="${c[0]}">${c[1]}</th>`).join("");
function fmt(k,v){if(v==null)return"";if(k==="symbol")return v;
 if(["close","em10_rs"].includes(k))return(+v).toFixed(1);
 if(["score","sc_entry","rsi14"].includes(k))return(+v).toFixed(0);
 return(+v).toFixed(2)}
function cls(k,v){if(k==="score")return v>=85?"s-hi":v>=70?"s-md":"s-lo";return""}
function rows(){let r=P[mode];const s=+el("score").value,p=+el("price").value||1e12,
 st=+el("stop").value||1e12,em=+el("em").value||0,q=el("q").value.toUpperCase(),
 su=el("setup").value;
 r=r.filter(x=>x.score>=s&&x.close<=p&&x.stop_pct<=st&&x.em10_rs>=em
   &&(!q||x.symbol.includes(q))&&(!su||x.setups.includes(su)));
 r.sort((a,b)=>(a[sortK]>b[sortK]?1:-1)*sortD);return r}
function draw(){const r=rows();el("vScore").textContent=el("score").value;
 el("count").textContent=r.length+" match"+(r.length===1?"":"es");
 el("body").innerHTML=r.map(x=>{
  const tags=x.setups.filter(t=>t!=="none").map(t=>`<span class="tag">${t}</span>`).join("")
   +(x.flagged?`<span class="tag flag">FLAG</span>`:"");
  const tr=`<tr class="row" data-s="${x.symbol}">`+COLS.map(c=>
   `<td class="${cls(c[0],x[c[0]])}">${c[0]==="symbol"?`<span class="sym">${x.symbol}</span>${tags}`:fmt(c[0],x[c[0]])}</td>`).join("")+"</tr>";
  const det=openSym===x.symbol?`<tr class="detail"><td colspan="${COLS.length}">
   <span class="kv">stop <b>₹${(+x.stop_price).toFixed(1)}</b> (−${(+x.stop_pct).toFixed(1)}%)</span>
   <span class="kv">move est <b>₹${(+x.em10_rs).toFixed(0)} / ${(+x.em10_pct).toFixed(1)}%</b> in 10 sessions</span>
   <span class="kv">52w-high dist <b>${(+x.dist_52w_high).toFixed(1)}%</b></span>
   <span class="kv">score parts — trend <b>${(+x.sc_trend).toFixed(0)}</b> · momentum <b>${(+x.sc_mom).toFixed(0)}</b> · vol/deliv <b>${(+x.sc_voldel).toFixed(0)}</b> · vol-fit <b>${(+x.sc_volfit).toFixed(0)}</b> · liquidity <b>${(+x.sc_liq).toFixed(0)}</b> · entry <b>${(+x.sc_entry).toFixed(0)}</b></span>
   </td></tr>`:"";
  return tr+det}).join("")}
document.addEventListener("input",draw);
document.addEventListener("click",e=>{
 const th=e.target.closest("th");if(th){const k=th.dataset.k;
  sortD=(sortK===k)?-sortD:(k==="symbol"?1:-1);sortK=k;draw();return}
 const tr=e.target.closest("tr.row");if(tr){openSym=openSym===tr.dataset.s?null:tr.dataset.s;draw();return}
 if(e.target.id==="mA"||e.target.id==="mB"){mode=e.target.id==="mA"?"A":"B";
  el("mA").classList.toggle("on",mode==="A");el("mB").classList.toggle("on",mode==="B");draw()}});
draw();
</script></body></html>"""


def build_payload(con, limit=300):
    a = gather(con, mode="A", setup="any", min_score=0, limit=limit,
               include_flagged=True, full=True)
    b = gather(con, mode="B", setup="any", min_score=0, limit=limit, full=True)
    for blk in (a, b):
        for r in blk["results"]:
            r["setups"] = [k for k in ("pullback", "breakout")
                           if SETUPS[k](r)] or ["none"]
    return {"as_of": a["as_of"],
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "A": a["results"], "B": b["results"]}


def build_html(payload):
    return TEMPLATE.replace("__PAYLOAD__", json.dumps(payload))


def run(con, limit=300, open_browser=True):
    payload = build_payload(con, limit)
    out = common.DATA_DIR / "dashboard.html"
    out.write_text(build_html(payload), encoding="utf-8")
    if open_browser:
        import webbrowser
        webbrowser.open(out.as_uri())
    common.json_out({"dashboard": str(out), "as_of": payload["as_of"],
                     "rows_A": len(payload["A"]), "rows_B": len(payload["B"])})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=300)
    p.add_argument("--no-open", action="store_true")
    a = p.parse_args()
    run(common.db(), a.limit, not a.no_open)
