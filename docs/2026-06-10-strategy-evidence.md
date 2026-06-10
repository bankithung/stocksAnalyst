# Strategy Evidence Report — NSE 5-15 Session Swing Engine

**Date:** 2026-06-10
**Status:** Salvaged synthesis (v1) **+ single-analyst verification completion (v2, 2026-06-10)** —
all 13 previously-[UNVERIFIED] clusters are now resolved by direct web verification (not the swarm);
see **§8** at the end of this file. Headline: every resolution **confirms** the engine's existing
direction; **no weight or rule changes**; one finding (Kaminski & Lo) refines how we *describe* the
Mode A stop.
**Input:** 111 agent outputs (`salvage-final-outputs.json`) from a stopped deep-research workflow
(scope → 5 search agents → ~15 source-fetch/claim-extraction agents → 3-vote adversarial
verification per claim, stopped mid-phase → synthesis, which never ran and is replaced here).

> **How to read the tags.** Each claim is tagged from the salvaged votes:
> **[SUPPORTED]** = survived adversarial verification (refuted=false) in the outputs;
> **[CONTESTED]** = mixed votes, or upheld only at medium confidence with material qualifications;
> **[REFUTED]** = a verifier voted refuted=true (listed for the record, **excluded from all
> recommendations**); **[UNVERIFIED]** = the source was fetched and claims were extracted, but the
> matching verification votes are not present in the salvaged set (the workflow stopped) — treat as
> provisional. Only material **present in the input file** is used. Where the outputs carry no
> effect size, that is stated as "no effect size reported in sources."

---

## 2. Executive summary

For a 1–2 week (5–15 trading session) NSE swing screen built on end-of-day data, the salvaged,
verified evidence supports a small set of conclusions:

1. **At sub-week horizons NSE shows short-term *reversal*, not continuation.** A peer-reviewed
   Indian study (Chui et al., *Pacific-Basin Finance Journal*, 2023, 3,956 BSE stocks, 2000–2021)
   and a separate NSE-500 preprint both find contrarian/reversal dominance at the daily-to-sub-week
   scale, strongest in **illiquid** stocks. This is the single most consistently verified directional
   finding and argues for **liquidity-gating** and against naive 5-day momentum chasing.
2. **Classic technical signals used alone do not beat the unconditional return on Indian indices.**
   Standalone 14-day RSI (30/70) and MACD signals on the Sensex/large-cap indices show no
   risk-adjusted edge (Sharpe < 1), even *before* transaction costs (Muruganandan 2020).
3. **India "event" signals carry real, sized edges but mostly *pre-disclosure*.** NSE bulk/block
   deals produce ~5–7% abnormal weekly returns, with most of it accruing via front-running
   *before* public disclosure — limiting what an EOD screener can capture after the fact.
4. **Promoter share-pledging predicts crash risk** (positive, significant) in Indian large/mid caps —
   useful as a **negative filter**, at an annual (not 5–15 day) horizon.
5. **SEBI ASM inclusion kills momentum**: pre-inclusion run-ups reverse to roughly zero/negative,
   liquidity and volume collapse, and ASM exit is *not* a bullish catalyst. Low delivery % on a
   price spike flags speculative/manipulated moves.
6. **Penny/microcap manipulation has a measurable EOD signature** (pre-event illiquidity + turnover
   surge; rise-then-fall return pattern) — supporting a manipulation/red-flag screen.
7. **ML/LLM short-term edges are real pre-cost but mostly vanish after costs and in microcaps.**
   ML long-short alpha attenuates heavily once microcaps/distressed names are excluded; LLM-news
   signals drift only ~1–2 days and die at realistic round-trip costs.
8. **Risk management has the most transferable evidence:** a 10% stop on momentum cut the worst
   monthly loss dramatically and roughly doubled the Sharpe; fractional-Kelly sizing is favored
   over full Kelly because mean-return estimation error dominates.

The 52-week-high effect, F-score, and the named swing systems (CANSLIM, Weinstein, Minervini) are
**long-horizon or contested** at this 5–15 day window — usable as quality/context inputs, not as
short-horizon entry triggers. Everything below must be re-validated on the project's own data via
`backtest.py` before live use.

---

## 3. Findings by pillar

### Pillar 1 — Short-horizon momentum, reversal, technical indicators (5–15 day, India-prioritized)

**Short-term reversal at sub-week horizons (NSE 500 preprint, arXiv:2302.13245v1, submitted
2023-02-26).** Reversal/contrarian portfolios dominate at sub-week horizons; continuation appears
at 1–8 week horizons; best-of-237 (also reported as best-of-1177) configuration; **gross of
transaction costs**, sub-1 Sharpe ratios, paper's own conclusion is the portfolios are "not
suitable for investment."
- Specific result **[SUPPORTED]** (verifiers a1cb81cc, a2c1840e, a4804cf3, a7fe3c2e, a5002a81,
  ab7ed7c3, aedac0ef; high confidence): NSE 500, 2014–2021, contrarian dominance at 1–7 day
  horizons; the 3-1 (J-K) inverse-turnover portfolio shows **6.04% mean monthly return**
  (6.041535% L-W mean), **17.08× final wealth vs Nifty 50** ("16-fold" contrarian result); 4 of the
  5 best daily portfolios are contrarian; **no cost/slippage/impact modeling**. Caveats logged by
  verifiers: gross returns, both legs of the long-short spread negative, best-of-237 selection,
  unreviewed preprint.
- Boundary inference "continuation at ≥1 week, reversal at <1 week" **[REFUTED]** (verifiers
  a0f19da4, ac80f2b4; high confidence): the actionable boundary is an interpolation the paper never
  tests; no significance tests; peer-reviewed Indian evidence (Chui et al. 2023) shows reversal —
  not continuation — in the illiquid small-cap segment the engine targets. *Excluded from
  recommendations.*

**Reversal/liquidity link (Chui et al. / "Momentum, reversals and liquidity: Indian evidence,"
*Pacific-Basin Finance Journal*, Dec 2023; 3,956 BSE stocks, 2000–2021; turnover-ratio liquidity
conditioning).** **[SUPPORTED]** (verifiers a4f85077, ac607c58, ad8657249; high confidence):
short-term reversal is concentrated in **illiquid** portfolios; the liquidity-gating implication
follows directly. No effect size beyond the portfolio construction reported in sources.

**Standalone RSI on Indian large-cap indices (peer-reviewed, Colombo Business Journal; 4,545
observations, 14-day RSI, 30/70 bands, 500-rep bootstrap).** **[SUPPORTED]** (verifiers a18215bf,
ae8fb303, aecf172e; high confidence): only **43.97% of buy trades profitable**; pre-cost returns
negative; classic 30/70 RSI used standalone shows no edge on Indian large-cap indices. Verbatim in
the paper's conclusion.

**RSI + MACD non-profitability (Muruganandan 2020, Colombo Business Journal, published 2020-06-30;
Sensex).** **[SUPPORTED]** (verifiers a632e6ec, adf96421; high confidence): headline conclusion that
RSI fails to beat unconditional Sensex returns and MACD signals deliver poor risk-adjusted
performance; **MACD sell-signal statistically significant (Table 6: t=4.43, bootstrap p=0.002) but
all sell-signal Sharpe ratios < 1 (Table 7)**; result is **gross of transaction costs**; index-only
scope; unusually harsh daily-Sharpe threshold noted.
- Separately-worded claim that "MACD *bullish crossovers* carried no positive edge" **[REFUTED]**
  (verifiers a49354aa, ac5d3caa, afc20158; high confidence): the paper's "buy" is a contrarian
  *state* rule (MACD below its signal line, both negative — a Rosillo-style oversold state firing on
  ~19–52% of trading days, figure differs across votes), **not** a bullish crossover; returns are
  next-day open-to-close intraday against a negative intraday benchmark. The crossover wording
  mischaracterizes what was tested. *Excluded from recommendations.*

**Indian short-term momentum at *monthly* horizons (Dhankar & Maheshwari, SSRN 2785541, Apr 2014,
NSE 1997–2013; and an NSE working paper, Dec 2009; and a CMIE-Prowess study Jan 1995–Dec 2008).**
**[SUPPORTED] as stated, but out-of-horizon** (verifiers a6aa7d66, ad907cb6, aee422cc; high/medium
confidence): statistically significant short-term momentum and long-term reversal on the NSE — but
the **shortest tested horizon is monthly / 6 months**, not 5–15 days. Verifiers explicitly flag the
horizon mismatch and survivorship bias.
- The stronger reading that this "small-term momentum" supports **5–15 day momentum ranking**
  **[REFUTED]** (verifiers a37af8f7, a635704c; high confidence): the paper's "small term" = 3–12
  month formation/holding (shortest 3 months on monthly data); cannot support 5–15 session momentum
  signals, where the literature documents reversal; low-tier venue, sample ends 2013, newer
  India-specific work explains momentum via risk models. *Excluded from recommendations.*

**52-week-high proximity (Raju 2023, "The 52-Week High Effect and Momentum Investing: Evidence from
India," SSRN 4587697, written 2023-09-29; NSE, Oct 2004–Aug 2023).** Core finding: stocks near
their 52-week high earn higher returns and Sharpe ratios even after size controls; effect is distinct
from and more stable than academic momentum; weaker long-term reversals; robust across weighting
schemes.
- **[CONTESTED]** — upheld repeatedly only at **medium** confidence (verifiers a1605c46, a7feb512,
  a9298e6e, aa787685, af590f2a, ad1e0a92): corroborated by George & Hwang (2004, *Journal of
  Finance*) and a second India study; **but** the source is a non-peer-reviewed working paper, the
  full-text effect-size tables were not retrievable ("no effect size reported in sources"),
  HXZ (*RFS* 2020) US replication reverses the stability ordering (52w-high t=0.43, insignificant,
  vs. plain momentum surviving), and **no 5–15 day horizon evidence exists** — tests are
  monthly-horizon.
- The extrapolation to "a screening signal **across market caps** including penny/SME" **[REFUTED]**
  (verifier a97d004a; medium confidence): universe could not be confirmed beyond liquid top-N NSE
  stocks; an Indian study found the standalone 52-week-high premium statistically insignificant; an
  out-of-sample India backtest was weak (Sharpe ~0.4); international evidence shows the effect mostly
  disappears after costs. *The across-caps extrapolation is excluded from recommendations; treat
  52WH proximity as a modest-weight, large-cap-only context input.*

### Pillar 2 — India-specific signals (delivery %, bulk/block deals, promoter pledge, FII/DII)

**Bulk/block deals — abnormal returns and asymmetry.** Multiple primary sources converge:
- Rajvanshi & Paul (peer-reviewed *Managerial Finance*, Emerald, IIM Calcutta, published 2022-03-09
  / 2022-01-25; NSE bulk deals 2010–2019). **[SUPPORTED]** (verifiers a190610c, a4190bd8, a77ff28b,
  aa604425, a481293d; high confidence): **~5–7% abnormal returns within a week** around NSE bulk
  deals; **delivery-change and volume-change statistically explain** those abnormal returns; **buy
  deals signal more strongly than sell deals**. Key caveat carried in the claims and verdicts: much
  of the return accrues **pre-disclosure via front-running**, limiting post-disclosure
  exploitability for an EOD screener.
- Chaturvedula et al. (peer-reviewed *Emerging Markets Review*, 2015; BSE/NSE). **[UNVERIFIED]**
  (extraction agent a83cf341; matching verification votes not in salvaged set): significant
  bulk-trade price impact; **pre-disclosure front-running run-ups of 9.58% (small-cap) / 4.79%
  (large-cap)**; positive buy-side CARs **~4.2% over 21 days**; asymmetric weak sell-side signal;
  stronger leakage/manipulation risk in small caps. Provisional.

**Delivery percentage.** Flagged across the search outputs (agents a514d71, a5238505… search tier):
**delivery percentage has no indexed academic event-study literature — only practitioner content.**
Where it does appear with evidence it is as an *explanatory variable* for bulk-deal abnormal returns
(Rajvanshi & Paul, [SUPPORTED] above) and as a **manipulation flag** — *low delivery % on a price
spike flags speculative/manipulated moves* (ASM working paper, [SUPPORTED] in Pillar 6). No
standalone delivery-% effect size at 5–15 days reported in sources.

**Promoter pledge — crash risk (Chauhan, Mishra & Spahr, peer-reviewed; and an Emerald article,
published 2024-02-20, BSE 500, 2011–2020, 257 firms).** **[SUPPORTED]** (extraction a30abff7;
verifier ade4891c high confidence): promoter share-pledging **significantly and positively predicts
future stock price crash risk**, with a significantly negative association with future financial
performance, robust to alternative proxies and IV-2SLS. Caveats: **annual horizon, large/mid-cap
universe** (not 5–15 day or small-cap/SME); **no effect size available due to paywall** ("no effect
size reported in sources"). Useful as a negative/quality filter, not a short-horizon trigger.

**FII/DII flows.** Two primary sources, both **monthly** frequency:
- Mukherjee & Tiwari (*Asia-Pacific Financial Markets*, May 2022, PMC). **[UNVERIFIED]** (extraction
  a5362db5; votes not in salvaged set). Provisional.
- AJRBEM (Jan 2014, monthly 2007–2013). **[UNVERIFIED]** (extraction aa4b0d8c): **bi-directional
  Granger causality** between FII flows and Sensex/Nifty returns — FII flows have *some* predictive
  content but also chase returns; **monthly frequency means no direct evidence at the 5–15 day
  horizon.** Search tier (a514d71) rates FII/DII causality "medium relevance, market-level with
  unstable causality." Provisional and out-of-horizon.

### Pillar 3 — Fundamental quality filters (Piotroski F-score, debt, promoter holding)

**Piotroski F-score (practitioner blog QuantifiedStrategies, Wayback snapshot 2026-01-25, compiling
Alpha Architect / ValueSignals / Eriksen thesis).** **[UNVERIFIED]** (extraction a57a7698; votes not
in salvaged set): the F-score is a **long-horizon filter, not a 5–15 day signal**; its high-vs-low
discrimination is **strongest in small caps**. Secondary/practitioner source. No clean 5–15 day
effect size reported in sources. Provisional — consistent with using F-score (or a debt/quality
proxy) as a **trade-survival filter**, not a short-horizon entry signal.

No primary peer-reviewed effect size for debt/D-E or promoter-holding *as a 5–15 day filter* appears
in the salvaged outputs; promoter pledge (Pillar 2) is the closest quality-filter evidence.

### Pillar 4 — ML/AI and LLM/news-sentiment for short-term prediction (after costs)

**ML cross-sectional alpha after realistic frictions (Avramov, Cheng & Metzker, *Management Science*
2023; peer-reviewed).** **[UNVERIFIED]** (extraction a332feaa, ac67f2ae; explicit verification votes
not in salvaged set, though it is cited inside the ML-skeptical search angle): ML long-short alpha
**attenuates 48–94% after excluding microcaps/distressed stocks**; **87–163% monthly turnover** makes
strategies unviable after costs; headline pre-restriction returns **0.95–2.18%/month**; profits
concentrate in **high-VIX states (0.22% vs 1.66%)**; post-2001 long-leg viability concentrated in
small/illiquid stocks. Provisional but directionally central: **after-cost ML edge is fragile and
microcap-dependent.**

**LLM news-sentiment (Lopez-Lira & Tang, University of Florida, arXiv 2304.07619 v6, through journal
review).** **[UNVERIFIED]** (extraction a13cbe86, a1fe4237; explicit per-claim votes not in salvaged
set): LLM news signal drift is **1–2 days, not 5–15 days**, at **34 bps/day pre-cost**;
**unprofitable at 20 bps round-trip cost**; concentrated in **small caps and negative news**; a
**model-capability threshold** exists (GPT-4 Sharpe 2.97 vs. no predictability for basic models);
**sharp alpha decay from 2021Q4 to 2024**. Provisional. Implication: news/LLM sentiment is a
short-lived (1–2 day), cost-sensitive, small-cap-tilted edge — at best a confirmation input, not a
5–15 day driver.

**Backtest overfitting / look-ahead (Bailey et al.; the "GPT look-ahead-bias" audit; Glasserman &
Lin, Columbia, arXiv 2309.17322, 2023-09-29).** **[UNVERIFIED]** (extractions a8932d32, a9c098e8,
a903abcb; votes not in salvaged set): the methodological-hazard sources (backtest overfitting,
look-ahead bias in LLM/GPT studies) were fetched but not verified in the salvaged window. Provisional;
they reinforce the cost/overfit caution rather than supply a tradable signal.

### Pillar 5 — Risk management (sizing, stops, R:R)

**Stop-loss on momentum (Han, Zhou & Zhu working paper, Oct 2014; CICF mirror).** **[SUPPORTED]**
(extraction a1731a8b, ab78ce54; high confidence — verbatim against PDF): a **10% stop-loss cuts
momentum's worst monthly loss from −49.79% to −11.36%**, **doubles the Sharpe (0.165 → 0.369)**, and
**raises mean return 0.99% → 1.69%/month**; the stop operates intramonth on daily prices (so it
transfers to an EOD exit rule); **overnight gaps cause slippage beyond the nominal stop**; crash-month
neutralization (e.g., +9.89% during the 1932 crash). Caveat: **US monthly momentum data, not Indian
5–15 day** — transferable as exit-rule design, not as a return estimate.

**Stop-loss theory (Kaminski & Lo, *Journal of Financial Markets* 2014; MIT Sloan).** **[UNVERIFIED]**
(extraction a1542fe3, aaaed6c5; the matching per-claim verdict is not isolated in the salvaged set):
conditions under which a stop-loss policy improves expected return ("stopping premium"). Provisional;
consistent with the Han/Zhou/Zhu empirics above.

**Kelly vs fractional / fixed-fractional sizing (MacLean, Thorp & Ziemba 2010; and MacLean, Thorp,
Zhao & Ziemba 2010 simulations).** **[UNVERIFIED]** (extractions a2a3d6fd→a2c7… correction: a2a7595e,
aa4459de, ac03b337, ae4b19c6; per-claim verdicts not in salvaged set): Kelly is growth-optimal but
short-horizon-risky; **betting above full Kelly is dominated (2× Kelly ≈ risk-free growth / zero
excess)**; **mean-return estimation errors dominate variance errors ~20:2:1**, which is the rationale
for **fractional Kelly**; fixed-fraction volatility drag; 700-wager dispersion example. Provisional
but internally consistent and standard; supports **fractional-Kelly / fixed-fractional (the skill's
1% rule) over full Kelly.**

> Note: the skill already fixes **Mode A sizing at the 1% capital-risk-per-trade rule** (fixed-
> fractional), which is consistent with the fractional-Kelly evidence above. No salvaged source
> contradicts the 1% rule; none calibrates the exact fraction for NSE 5–15 day trades — so the 1%
> default **stays provisional pending `backtest.py`.**

### Pillar 6 — Small-cap/penny dangers (pump-and-dump, manipulation, ASM/GSM)

**Manipulation signature (Aggarwal & Wu working paper 2002-12-13, published *Journal of Business*
2006).** **[UNVERIFIED]** (extractions adbd0aab, adcb075e; explicit per-claim verdicts not isolated in
the salvaged set): manipulation concentrates in **penny/OTC/illiquid stocks**; pump-and-dump return
signature **+2.56%/day during, −0.13%/day after**; **pre-manipulation illiquidity + turnover/volume
surge is the detectable red flag**; manipulator-identity and episode-duration statistics. Provisional;
the rise-then-fall + turnover-surge pattern is directly usable in `red_flags.py`.

**SEBI ASM inclusion effects (Chari & Inamdar, NSE–NYU Stern Initiative working paper; NISM authors;
NSE surveillance data, 218 events).** **[SUPPORTED]** (extraction ade6afca, aed98519; consistent
across both extraction passes; the central effects are reported as significant): **ASM inclusion kills
momentum** — pre-inclusion run-up **+10.51% (pre-5d CAAR) reverses to −0.92% post-inclusion,
significant at 1%**; post-inclusion outcomes are **near-zero expectancy with 61% reversals**;
**liquidity and volume drop significantly**; **ASM exit is not a bullish catalyst**; and **low
delivery percentage on a price spike flags speculative/manipulated moves**. Directly actionable: ASM
membership is a hard exclusion / caution trigger, and an ASM-exit "bounce" must not be traded as a
catalyst.

### Pillar 7 — Documented swing strategies (CANSLIM, Weinstein, Minervini SEPA, ORB, Bollinger)

**CANSLIM.** Multiple sources, all pointing **away** from a 5–15 day fit:
- QuantifiedStrategies blog (Oddmund Groette, 2024-06-04; Wayback snapshot). **[UNVERIFIED]**
  (extractions a0e66c6c, a7ac6b96; matching verdicts not in salvaged set): claimed **18% vs 9% CAGR**
  outperformance since 2003, but **secondhand from an IBD promotional report**, ETF rules paywalled;
  **heavy recent underperformance in the live FFTY ETF era**; the outperformance **may be small-cap
  beta, not the CANSLIM criteria**; **targets long-term holds, not 1–2 week swings.**
- Lutey, Crum & Rayome (2014), OPBM II / CAN SLIM, *Journal of Accounting and Finance* 14(5).
  **[UNVERIFIED]** (extraction a2709ff7): 2010–2013 and 1999–2013 backtest effect sizes (figures not
  quoted in the salvaged summary — "no effect size reported in sources"); **7–8% stop / 20–25%
  profit-take, 3:1 rule**; corroborating prior studies (Olson et al. 1998; Schadler & Cotton 2008);
  **negative finding: German-market failure when dropping N/L/I criteria; long holding periods, not
  5–15 day swings**; lower-tier journal, no significance testing.
- AAII Journal (John Bajkowski, ~April 2003). **[UNVERIFIED]** (extractions a791bc41, af01ed7d):
  concrete CAN SLIM **setup thresholds — RS rank ≥ 80, within 10% of 52-week high, quarterly EPS
  growth ≥ 18–20%, 3-year annual EPS growth ≥ 25%** — but **only qualitative backtest evidence**
  (revised screen more volatile and regime-dependent; **no annual returns, win rates, or drawdowns
  reported**). Secondary source.

**Weinstein stage analysis.** Search tier (a8c9801c) explicitly flags: **no credible quantified
backtest exists for Weinstein stage analysis specifically; its evidence base is indirect via the
52-week-high and trend-template studies.** No claim to tag.

**Minervini SEPA / ORB / Bollinger mean reversion.** No dedicated source-fetch or verdict for these
appears in the salvaged outputs. **Evidence not present** — no tag, no recommendation derived.

**Columbia DSI / Fidelity capstone deck (Dec 2020).** **[UNVERIFIED]** (extraction a2c7d8fa): rated
primary institutional research with a small-sample caveat. Provisional; no effect size carried into
the salvaged summary.

---

## 4. Signals table

| Signal | Horizon evidence | Strength | Verdict | Source(s) |
|---|---|---|---|---|
| Short-term reversal (sub-week, illiquid) | Daily–sub-week; concentrated in illiquid | Strong | [SUPPORTED] | Chui et al., *Pacific-Basin Finance J.* 2023; NSE-500 preprint arXiv:2302.13245 |
| NSE-500 contrarian result (6.04% mo., 17.08× wealth) | 1–7 day, 2014–2021, gross of costs | Moderate (preprint, best-of-237, no costs) | [SUPPORTED] | arXiv:2302.13245v1 |
| "Continuation ≥1wk / reversal <1wk" boundary | Inferred, untested | — | [REFUTED] | arXiv:2302.13245 |
| Standalone 14-day RSI (30/70) | Indian large-cap indices; 43.97% buy-win, neg. pre-cost | Strong (negative result) | [SUPPORTED] | Colombo Business J. (4,545 obs) |
| RSI/MACD signals beating unconditional return | Sensex; Sharpe < 1 gross of costs | Strong (negative result) | [SUPPORTED] | Muruganandan 2020 |
| "MACD bullish crossover has no edge" (as worded) | Mischaracterizes a contrarian-state test | — | [REFUTED] | Muruganandan 2020 |
| Indian momentum at monthly/6-mo horizon | Monthly; significant | Moderate (out-of-horizon) | [SUPPORTED] | Dhankar & Maheshwari 2014; NSE WP 2009 |
| Indian "small-term momentum" → 5–15 day ranking | 3–12 mo formation, not 5–15 days | — | [REFUTED] | low-tier momentum paper(s) |
| 52-week-high proximity (large-cap, monthly) | Monthly; higher Sharpe, size-robust | Moderate (medium-confidence, working paper) | [CONTESTED] | Raju 2023 SSRN 4587697 |
| 52WH as screen "across market caps" incl. penny/SME | Unconfirmed in small/SME; weak OOS | — | [REFUTED] | a97d004a vote vs Raju 2023 |
| Bulk/block-deal abnormal returns (~5–7%/wk) | Within a week; mostly pre-disclosure | Strong (but front-run) | [SUPPORTED] | Rajvanshi & Paul, *Managerial Finance* 2022 |
| Bulk-deal CARs (~4.2%/21d; run-ups 9.58%/4.79%) | ~21 day; pre-disclosure | Moderate | [UNVERIFIED] | Chaturvedula et al., *Emerging Markets Review* 2015 |
| Delivery % change (explains bulk-deal returns) | Weekly, as explanatory variable | Moderate | [SUPPORTED] | Rajvanshi & Paul 2022 |
| Delivery % standalone short-horizon signal | No indexed academic event study | Weak | [UNVERIFIED] (practitioner only) | search tier a514d71 |
| Low delivery % on price spike = manipulation flag | 5–15 day event window | Moderate | [SUPPORTED] | ASM WP (Chari & Inamdar) |
| Promoter pledge → crash risk (negative filter) | Annual; large/mid cap | Moderate (annual horizon) | [SUPPORTED] | Chauhan/Mishra/Spahr; Emerald 2024 |
| FII/DII flows (Granger-causal, market-level) | Monthly; unstable causality | Weak (out-of-horizon) | [UNVERIFIED] | Mukherjee & Tiwari 2022; AJRBEM 2014 |
| Piotroski F-score (quality survival filter) | Long-horizon; strongest in small caps | Weak at 5–15 days | [UNVERIFIED] | QuantifiedStrategies (compilation) |
| ML cross-sectional alpha after costs | Attenuates 48–94% ex-microcaps; turnover kills it | Moderate (negative-after-cost) | [UNVERIFIED] | Avramov/Cheng/Metzker, *Mgmt Sci* 2023 |
| LLM news sentiment | 1–2 day drift; dies at 20 bps round-trip | Moderate (negative-after-cost) | [UNVERIFIED] | Lopez-Lira & Tang, arXiv 2304.07619 |
| 10% stop-loss on momentum | Cuts worst loss −49.79%→−11.36%; Sharpe 0.165→0.369 | Strong (US monthly) | [SUPPORTED] | Han, Zhou & Zhu 2014 |
| Fractional vs full Kelly sizing | Above-Kelly dominated; est. error 20:2:1 | Moderate (theory/sim) | [UNVERIFIED] | MacLean/Thorp/Ziemba 2010 |
| Pump-and-dump EOD signature (penny) | +2.56%/day during, −0.13%/day after; turnover surge | Moderate | [UNVERIFIED] | Aggarwal & Wu 2002/2006 |
| ASM inclusion kills momentum | +10.51%→−0.92% CAAR; 61% reversals; exit not bullish | Strong | [SUPPORTED] | Chari & Inamdar (NSE–NYU Stern) |
| CANSLIM as a 5–15 day system | Long-horizon; small-cap-beta confound; FFTY underperf. | Weak at this horizon | [UNVERIFIED] | QuantifiedStrategies; Lutey 2014; AAII 2003 |
| Weinstein / Minervini / ORB / Bollinger | No credible short-horizon backtest in set | — | Evidence not present | — |

---

## 5. What to avoid

- **Do not chase 5-day momentum on illiquid/small-cap NSE names.** Sub-week behavior is **reversal**,
  strongest exactly where the engine is tempted to fish (illiquid stocks). [SUPPORTED reversal
  evidence; REFUTED short-horizon-momentum extrapolation.]
- **Do not use standalone RSI(14) 30/70 or MACD signals as entry triggers on Indian indices** — no
  risk-adjusted edge, Sharpe < 1, negative even before costs. [SUPPORTED.]
- **Do not treat the 52-week-high effect as a cross-cap (penny/SME) screen** or as a 5–15 day signal;
  the across-caps extrapolation is refuted and all evidence is monthly-horizon, large-cap, working-
  paper. [REFUTED extrapolation.]
- **Do not infer a tradable "continuation above 1 week" rule** from the NSE-500 preprint — that
  boundary was never tested. [REFUTED.]
- **Do not assume bulk/block-deal abnormal returns are capturable after disclosure** — most of the
  ~5–7% accrues pre-disclosure via front-running; an EOD screener sees it late.
- **Do not lean on ML or LLM-news edges at 5–15 days after costs** — ML alpha attenuates 48–94%
  ex-microcaps with 87–163% turnover; LLM drift is 1–2 days and dies at 20 bps round-trip. Treat as
  fragile/confirmation-only.
- **Do not trade an ASM-exit "bounce" as a bullish catalyst** — it isn't one; post-inclusion
  expectancy is near zero with 61% reversals. ASM/GSM names are caution/exclusion, never Mode B.
- **Do not bet at or above full Kelly** — above-Kelly sizing is dominated; estimation error in mean
  returns is the dominant risk. Keep fractional/fixed-fractional sizing.
- **Do not trust backtested win rates or CAGRs from promotional/practitioner sources** (e.g., the
  18%-vs-9% CANSLIM figure is secondhand from an IBD promo report; FFTY live era underperformed).

---

## 6. Recommended engine settings

All numbers below are **derived only from the salvaged evidence**; where evidence is thin, the
skill's existing **v1-provisional** default (from `methodology.md` / decision log #12) is **kept and
explicitly re-marked provisional**. Nothing here is calibrated for NSE 5–15 day trades until
`backtest.py` runs.

### 6a. Setup definitions (evidence-aligned)

- **Reversal-aware, liquidity-gated screening (new, evidence-backed).** Because sub-week behavior is
  reversal and is concentrated in illiquid names, **gate the universe by liquidity** (keep the
  skill's ₹2 cr / ₹5 cr avg-traded-value floors) and **do not run a raw 5-day momentum rank as an
  entry trigger**. Mean-reversion-to-support setups are better aligned with the evidence at this
  horizon than breakout-momentum chasing on thin stocks. [SUPPORTED: Chui 2023; arXiv:2302.13245.]
- **Trend-pullback-to-support / breakout-with-volume / VCP-lite** (skill's existing setups) are
  retained; the evidence neither confirms nor refutes them at 5–15 days — keep them **provisional**
  and validate via `backtest.py`. Confirmation-on-volume is consistent with the broader signal
  literature but unquantified here.
- **Hard red-flag / manipulation gate (strengthen).** Exclude or hard-caution: **ASM/GSM membership**
  (momentum dies, reversals dominate — [SUPPORTED]); **low delivery % on a price spike**
  ([SUPPORTED]); **penny/microcap + pre-event illiquidity + turnover/volume surge** (pump-and-dump
  signature — [UNVERIFIED, provisional]). This maps onto `red_flags.py`.
- **Quality-survival filter (Mode B).** Keep **promoter-pledge ≈ 0** as a hard gate — pledging
  predicts crash risk ([SUPPORTED], annual horizon). F-score / debt act as long-horizon survival
  filters, **not** short-horizon triggers ([UNVERIFIED, provisional]).
- **Event-risk window.** Keep the skill's "no entry within ~5 sessions of scheduled results."
  Evidence here is indirect (LLM-news and event studies show event-driven moves) — **provisional**.

### 6b. Composite scoring weight ranges

The skill's current provisional split is **trend 25 · momentum 20 · volume/delivery 15 ·
volatility-fit 15 · fundamental 15 · liquidity 10** (decision log #12). The salvaged evidence
motivates **modest, directional** adjustments (not a recalibration — that needs the backtest):

| Component | Provisional default | Evidence-informed range | Rationale from salvaged evidence |
|---|---|---|---|
| **Trend** | 25 | **20–25** | No 5–15 day trend effect size in set; keep high but cap — sub-week edge is reversal, not trend. Provisional. |
| **Momentum** | 20 | **5–15** (lower) | Sub-week NSE behavior is **reversal**; monthly momentum doesn't transfer; short-horizon-momentum extrapolation **[REFUTED]**. Reduce weight (or re-sign toward short-term reversal). |
| **Volume / delivery** | 15 | **15–20** (higher) | Delivery-change + volume-change **statistically explain** bulk-deal abnormal returns **[SUPPORTED]**; low delivery % is a manipulation flag. Best-evidenced India EOD inputs. |
| **Volatility-fit-to-target** | 15 | **15** (keep) | No direct effect size in set; ATR expected-move math is the skill's own design. Provisional. |
| **Fundamental health** | 15 | **10–15** | Quality (pledge/F-score) is a **survival filter at annual horizon**, weak at 5–15 days; keep moderate, not a primary short-horizon driver. Provisional. |
| **Liquidity** | 10 | **10–15** (higher) | Reversal/manipulation risk is concentrated in **illiquid** names **[SUPPORTED]**; liquidity is a first-class gate, so weight it up (or enforce as a hard pre-filter). |

> Weights should sum to 100; the ranges above are intended to be tuned **down-momentum /
> up-volume-delivery / up-liquidity** relative to the v1 defaults, then **finalized only after
> `backtest.py`**. Until then they remain provisional.

### 6c. Entry-quality component guidance

| Entry-quality component | Evidence-derived setting | Status |
|---|---|---|
| **Stop distance** | Keep Mode A's ≤ ~3% to validated support **and** model an explicit **overnight-gap buffer** — Han/Zhou/Zhu show stops slip beyond the nominal level on gaps. A protective stop materially improves outcomes (−49.79%→−11.36% worst loss; Sharpe ~doubled). | [SUPPORTED] for "use a stop + gap buffer"; exact % **provisional** for NSE 5–15 day. |
| **R:R threshold** | Keep **≥ 2.5** for Mode A. No salvaged source sets an NSE-specific R:R threshold. | Provisional (kept). |
| **Trend alignment** | Keep "pullback/breakout within uptrend; no falling knives." | Provisional (kept); not contradicted. |
| **Volatility contraction (VCP-lite)** | Keep as a component. | Provisional (kept); no salvaged effect size. |
| **Confirmation (volume on reclaim)** | Keep; volume/delivery is the best-evidenced India input, so weight confirmation toward **delivery-backed** volume rather than raw volume. | [SUPPORTED] direction (delivery/volume explanatory); threshold provisional. |
| **Event risk** | Keep "no entry within ~5 sessions of results." | Provisional (kept). |
| **Gap behavior** | **Raise its weight** in stop reliability — overnight gaps are an explicit, evidenced failure mode for stops (Han/Zhou/Zhu) and pump-and-dump/ASM names gap violently. | [SUPPORTED] direction; magnitude provisional. |

---

## 7. Methodology caveats

- **Salvage limitation.** The synthesis stage never ran; this report reconstructs it from 111
  pre-synthesis agent outputs. Agent IDs are random and were classified by content into search
  results, claim extractions, and verification verdicts. Where a claim's three verification votes
  were not all present in the salvaged set, the claim is tagged **[UNVERIFIED]** and treated as
  provisional, not as established.
- **Verification was stopped mid-phase (134/~150 agents).** Several high-value extractions —
  notably the ML-after-costs (Avramov et al.), LLM-sentiment (Lopez-Lira & Tang), Kelly-sizing
  (MacLean/Thorp/Ziemba), Kaminski & Lo stop-loss theory, Chaturvedula bulk-deal CARs, FII/DII
  flows, F-score, pump-and-dump (Aggarwal & Wu), and the CANSLIM/AAII/Lutey set — are **[UNVERIFIED]**
  here. They are reported because they were extracted from named primary/secondary sources, but they
  did not receive (or did not retain) adversarial votes in the salvaged file.
- **Effect sizes are reported only where present.** Paywalled sources (e.g., the promoter-pledge
  Emerald article, some bulk-deal full texts, CANSLIM backtest tables) yielded conclusions without
  retrievable effect sizes; those are flagged "no effect size reported in sources."
- **Horizon mismatch is pervasive.** Much of the strongest evidence (momentum, 52WH, pledge, FII/DII,
  F-score, the Han/Zhou/Zhu stop) is **monthly or annual**, or **US**, not Indian 5–15 day. Direction
  often transfers; magnitudes do not. The genuinely 5–15-day-aligned, India-specific, SUPPORTED items
  are: short-term reversal/liquidity (Chui 2023; NSE-500 preprint), standalone RSI/MACD
  non-profitability, bulk-deal weekly abnormal returns (with the front-running caveat), and ASM
  inclusion effects.
- **Refuted claims are excluded from §6.** The continuation-boundary rule, the MACD-crossover
  wording, the short-horizon-momentum extrapolation, and the 52WH-across-caps extrapolation are
  recorded in §3/§4 only and contribute nothing to the recommended settings.
- **Validate everything on our own data before live use.** Every weight, threshold, stop %, and R:R
  in §6 is either evidence-*directional* or a kept v1-provisional default. Per the skill design
  (decision log #9 and §11 phase 3), these must be finalized from **`backtest.py`** runs
  (hit rate to target within N sessions, MAE distribution, time-to-recovery, by market-cap band)
  with an out-of-sample split, **before** any of it informs live suggestions.

### Claim counts (v2 — after verification completion)

- **[SUPPORTED]:** 18 distinct claims — the original 11 (short-term reversal sub-week;
  reversal–liquidity link; NSE-500 contrarian result; standalone RSI non-profitability; RSI/MACD
  non-profitability; Indian monthly momentum *as stated*; bulk-deal ~5–7% weekly abnormal returns;
  delivery/volume explain bulk-deal returns; promoter-pledge → crash risk; 10% stop-loss on momentum;
  ASM inclusion kills momentum / low-delivery flag) **+ 7 newly verified in v2** (Chaturvedula
  bulk-deal CARs; Piotroski F-score as long-horizon/small-cap filter; ML-after-costs Avramov et al.;
  LLM news-sentiment direction; Glasserman & Lin look-ahead/distraction methodological finding;
  Kelly/fractional sizing; pump-and-dump EOD signature).
- **[CONTESTED]:** 4 claims — 52-week-high proximity (v1) + **3 resolved in v2**: Kaminski & Lo stop
  theory (horizon-dependent — weak at short frequencies); FII/DII flows (bidirectional/unstable,
  out-of-horizon, context-only); CANSLIM as a system (real long-horizon outperformance, ~30% win,
  large drawdowns — not a 5–15 day swing model).
- **[REFUTED]:** 4 claims (unchanged: continuation-vs-reversal boundary rule; "MACD bullish crossover
  has no edge" as worded; "small-term momentum" → 5–15 day ranking; 52WH as a cross-cap/penny screen).
- **[UNVERIFIED]:** **0** — all 13 v1 clusters resolved in §8. (One item, the Columbia/Fidelity
  capstone deck, is tagged **[NOTED — not independently verifiable]**: a student/industry deck with
  no public primary source; carries no weight in recommendations.)

---

## 8. Verification completion (v2 — 2026-06-10, single-analyst web verification)

After the deep-research workflow was stopped for cost, the 13 [UNVERIFIED] clusters were closed by
**direct web verification against primary/authoritative sources** (main analyst, Opus 4.8 — no
multi-agent swarm). Each now carries a real verdict. **Headline: every resolution confirms the
engine's existing direction; none changes a scoring weight or a rule. One finding (Kaminski & Lo)
refines how we describe what the Mode A stop buys at this horizon.**

### Resolved verdicts

1. **ML after costs — Avramov, Cheng & Metzker, *Management Science* 69(5):2587–2619, 2023 →
   [SUPPORTED] (direction).** Published abstract confirms: excluding microcaps/distressed stocks or
   high-volatility episodes "considerably attenuates profitability," and performance "further
   deteriorates in the presence of reasonable trading costs because of high turnover and extreme
   positions." The specific 48–94% attenuation figure is consistent with the published direction
   (exact value not re-quoted in the abstract). **Build impact: ML stays out of v1 as a driver —
   correct, and it saves build effort.** Source: pubsonline.informs.org/doi/abs/10.1287/mnsc.2022.4449.

2. **LLM news sentiment — Lopez-Lira & Tang, arXiv 2304.07619 v6 → [SUPPORTED] (direction).** Abstract
   confirms: ~90% portfolio-day hit rate on the *non-tradable* initial reaction; GPT-4 scores predict
   "subsequent drift, especially for small stocks and negative news"; forecasting ability "increases
   with model size" (capability threshold); "strategy returns decline as LLM adoption rises" (the
   decay). **Build impact: sentiment is confirmation-only, never a v1 signal driver.** Source:
   arxiv.org/abs/2304.07619.

3. **Backtest look-ahead / overfit — Glasserman & Lin, arXiv 2309.17322, 2023 → [SUPPORTED]
   (methodological).** Finding: out-of-sample, look-ahead bias is *not* the main hazard; a
   "distraction effect" (the model knowing the named company) is, especially for large firms; an
   anonymization procedure de-biases backtests. **Build impact: reinforces (a) no LLM-sentiment
   signals in v1, (b) if ever added, anonymize/de-bias the backtest, (c) `backtest.py` must avoid
   look-ahead generally.** Source: arxiv.org/abs/2309.17322.

4. **Kelly / fractional sizing — MacLean, Thorp & Ziemba → [SUPPORTED].** Confirmed: above-Kelly
   betting is "growth-security dominated"; a ~10% error in the mean-return estimate can cause ~50%
   overbetting under full Kelly; fractional Kelly is the recommended fix. **Build impact: validates
   the 1% fixed-fractional rule (`risk.py`); never size at or above full Kelly.** Source:
   stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf.

5. **Stop-loss theory — Kaminski & Lo, *Journal of Financial Markets* 18:234–254, 2014 → [CONTESTED]
   (horizon-dependent).** Important nuance that *refines our framing*: stop-losses added **no value at
   short sampling frequencies**; the positive "stopping premium" (higher Sharpe, lower vol) appears at
   **longer intervals / positive-autocorrelation (momentum) regimes**, shown on a buy-and-hold
   index-futures strategy. **Build impact: at the 5–15 day horizon, describe Mode A's stop honestly as
   a risk-control / tail-cutting device (caps the bad outcome), not a Sharpe booster.** The empirical
   tail-cutting case rests on Han/Zhou/Zhu [SUPPORTED, §3 Pillar 5]; the expected-return *enhancement*
   does not clearly transfer to short horizons. Source: dspace.mit.edu/handle/1721.1/114876.

6. **Pump-and-dump signature — Aggarwal & Wu, *Journal of Business* 79(4):1915–1953, 2006 →
   [SUPPORTED] (direction).** Confirmed: manipulators are typically informed parties; "manipulated
   stocks exhibit identifiable price, volume, and volatility signatures"; manipulation raises
   volatility, (temporary) liquidity, and returns during the pump. **Build impact: validates
   `red_flags.py`** — a turnover/volume surge on a normally-illiquid, low-delivery name fits the
   documented signature. The exact +2.56%/day-during figure remains as-extracted (not separately
   reconfirmed). Source: jstor.org/stable/10.1086/503652.

7. **Bulk-deal CARs — Chaturvedula, Bang, Rastogi & Kumar, "Price manipulation, front running and
   bulk trades: Evidence from India," *Emerging Markets Review* 23:26–45, 2015 → [SUPPORTED].**
   Confirmed near-verbatim: buying a small-cap 10 days before a bulk deal and selling the day after
   earns **+9.58% over that 12-day window**; large-cap **+4.79% over 11 days**; institutional
   front-running significantly moves pre-day-0 returns; buy-side signals stronger than sell-side.
   **Build impact: confirms bulk-deal alpha is largely pre-disclosure — do NOT build a "chase bulk
   deals" signal; an EOD screener sees it too late.** Source: sciencedirect.com/science/article/abs/pii/S1566014115000138.

8. **Piotroski F-score — "FSCORE: international evidence," *Journal of Asset Management* 2020; and
   Pacific-Basin evidence → [SUPPORTED] (long-horizon, small-cap-tilted).** Confirmed: high−low
   F-score ≈ **10%/year**; ≈ **1.4%/month on smaller stocks**; **insignificant in large-cap**
   (Piotroski 2000); returns accrue because "fundamental information is only gradually incorporated"
   = **annual horizon, not 5–15 days**. **Build impact: F-score / quality belongs in the Mode B
   survival gate, not the Mode A swing trigger — exactly as designed.** Source:
   link.springer.com/article/10.1057/s41260-020-00157-2.

9. **FII/DII flows → [CONTESTED] (real but bidirectional/unstable, out-of-horizon).** Granger
   causality is bidirectional (FII→Sensex F=3.53, p=0.033; DII→Sensex F=5.52, p=0.005), but at
   **daily** frequency Nifty returns *cause* FII flows (FIIs chase returns), and recent work labels
   domestic institutions "market-responsive rather than market-driving." **Build impact: keep FII/DII
   as `market_pulse.py` regime context, never a per-stock entry signal — as designed.**

10–12. **CANSLIM (QuantifiedStrategies backtest; Lutey 2014, *J. Accounting & Finance*; AAII
   thresholds) → [CONTESTED] system, long-horizon.** Real outperformance exists (≈**0.94%/month over
   the NASDAQ-100, 1999–2013**) but with **~30% win rate**, **44–72% max drawdowns**, and **long
   holding periods** — not a 5–15 day swing model. **Build impact: not our swing system.** Useful
   corroboration, though: CANSLIM's ~30%-win-rate-with-3:1-reward structure independently **validates
   our R:R ≥ 2.5 entry-quality rule** (low win rate + high reward:risk = positive expectancy).

13. **Columbia/Fidelity capstone deck → [NOTED — not independently verifiable].** Student/industry
   deck; no public primary source; carries no weight in recommendations.

### Net effect on the engine

**Zero scoring-weight changes; zero rule changes.** v2 verification *confirms* the §6b weight ranges
and the §6a/§6c setup and entry-quality rules. The one substantive refinement is descriptive:

- **`methodology.md` / skill spec should frame the Mode A stop as primarily risk-control (tail-cutting)
  at the 5–15 day horizon** — Han/Zhou/Zhu is the empirical tail-cutting evidence; Kaminski & Lo shows
  the expected-return *boost* is a longer-horizon phenomenon, so we should not claim it for short swings.
- CANSLIM corroborates **R:R ≥ 2.5**; F-score confirmed as a **Mode B survival filter only**; ML/LLM
  confirmed **out of v1 as drivers** (and de-biased backtests required if ever added).

Everything else still routes through **`backtest.py`** as the final referee on our own NSE data with an
out-of-sample split. Verification raises confidence in the *design*; it does not substitute for
empirical calibration of magnitudes.
