# SupeRR Selector Season 2 — Complete Project Plan

**Competition:** SupeRR Selector Season 2 — Help Shape Rajasthan Royals' IPL 2027 Auction Strategy  
**Round:** Round 1 — Identify the Most Reliable Players Under Pressure  
**Organisers:** Rajasthan Royals × Unstop  
**Deadline (Round 1):** 18 Nov 2026, 11:59 PM IST  
**Registration deadline:** 16 Nov 2026, 11:59 PM IST  
**Participation:** Individual only  

**Execution:** Use [`MASTER_PLAN.md`](./MASTER_PLAN.md) as the daily checklist · [`DOCS_INDEX.md`](./DOCS_INDEX.md) for doc map.

---

## 1. One-line verdict

Build a transparent, data-driven **Pressure Performance System** on the official RR data pack (IPL + T20I, 2022→2026), produce **Top 10 batters** and **Top 10 bowlers** who outperform their baseline when the match is tight, wrap it in an RR-branded methodology report (and optional dashboard), and submit both rankings + report on Unstop.

---

## 2. What RR is actually asking for

### Official problem (from Round 1 PDF — this is the source of truth)

> Build a data-driven system that measures how **batters** and **bowlers** perform in **high-pressure** match situations compared with their **usual** performance levels. Use it to identify and rank the players who deliver most consistently when it matters.

**Pressure is not pre-defined.** You must:

1. Define what “pressure” means (required rate, wickets left, balls left, stage of innings, closeness of contest, knockout stage, etc.).
2. Justify why that definition is meaningful.
3. Show how pressure situations differ from ordinary ones.
4. Make the method work for **both batting and bowling**.

### Required deliverables

| # | Deliverable | Where | Notes |
|---|-------------|-------|-------|
| 1 | **Top 10 batters under pressure** (ranked 1→10) | Unstop dropdowns | No repeats within the list |
| 2 | **Top 10 bowlers under pressure** (ranked 1→10) | Unstop dropdowns | No repeats within the list |
| 3 | **Methodology report** (PDF / PPTX) | Unstop upload | Must explain definition, metrics, fairness, evidence, limitations |
| 4 | Dashboard link (optional but strong) | Text field (500 chars) | Live URL preferred |
| 5 | Journey reel / post (optional) | Link field | Tag @rajasthanroyals @unstop.world — does **not** affect scoring |

### Marketing page nuance (do not get confused)

The Unstop page talks broadly about “top 10 reliable players” and “domestic leagues.” The **PDF + submission form** are stricter and clearer:

- Two separate lists: **10 batters + 10 bowlers**
- Dataset is **IPL + men’s T20I from 2022 onwards** (not Ranji / SMAT-only domestic pack)

**Follow the PDF + Unstop form.** Treat marketing copy as context only.

### Bigger competition arc (for awareness, not Round 1 scope)

| Round | What happens |
|-------|----------------|
| Round 1 | Pressure rankings + methodology (this project) |
| Round 2 | Top 16 flown to Mumbai — deeper challenge with RR Analytics |
| Round 3 | Winner joins IPL 2027 auction in Goa; present to Kumar Sangakkara & Giles Lindsay |

Round 1 success = clear method + defensible Top 10s + professional presentation. Auction purse / squad building is **not** the Round 1 ask (that was Season 1 style). Still, lightly tying picks to “how they strengthen RR” helps the story.

---

## 3. What we already have (inventory)

### 3.1 Documents & brand assets

| Asset | Path | Status |
|-------|------|--------|
| Round 1 problem statement PDF | `docs/dataset/.../Data Pack/Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf` | ✅ Available |
| Competition page scrape | `docs/projectdetails.md` | ✅ Available |
| RR website structure / nav reference | `docs/RRSitedata.md` | ✅ Available |
| RR UI / colour reference mockup | `docs/1794678506882-9180.jpeg` | ✅ Available |

### 3.2 Official data pack (6 CSVs)

Location: `docs/dataset/6af458274c1e8_data_pack/Data Pack/`

| File | Rows (approx.) | Purpose |
|------|----------------|---------|
| `competitions.csv` | 141 | Competition id, name, format (T20/T20I), season |
| `teams.csv` | 353 | Competition ↔ team mapping |
| `matches.csv` | 883 | Match meta: date, stage, venue, toss, result, knockout flag |
| `playing_eleven.csv` | 28,381 | Match XI, batting order, captain, WK, impact |
| `competition_team_player_mapping.csv` | 6,413 | Player id ↔ name ↔ team ↔ competition |
| `ball_by_ball.csv` | ~201,000 | Delivery-level events (core analysis table) |

**Coverage snapshot**

- **Seasons:** 2022 → 2026  
- **Formats:** T20I (~134 comps) + T20 (~7 comps, including **IPL 2022–2026**)  
- **IPL matches:** ~371  
- **Unique players:** ~1,217  
- **Unique teams:** ~38  
- **Date range:** 2022-01-22 → 2026-11-01  
- **Knockouts marked:** 31 matches (`knock_out = 1`)  
- **Stages:** League, Qualifier, Eliminator, Semi Final, Final, Super 4, Others  

### 3.3 Ball-by-ball fields we can use for pressure

Available and useful:

- Match / innings / over / ball sequencing  
- Striker, non-striker, bowler (ids + names)  
- Runs, fours, sixes, wickets, dismissal type  
- Extras  
- Batting type (RHB/LHB), bowling type, pace vs spin  
- Bowl speed (≈61% non-zero — usable but incomplete)  
- Stroke, delivery style, over/around, on/off side  

**Critical implication:** Required run rate, wickets in hand, balls remaining, chase closeness are **not precomputed**. They must be **engineered** by reconstructing innings state from ball-by-ball + match metadata.

### 3.4 Brand / UI reference (from mockup + site)

Use these as the visual system for dashboard / report slides:

| Token | Direction |
|-------|-----------|
| Primary | Hot pink / magenta (RR signature) |
| Secondary | Deep navy / purple |
| Accent | Royal gold (sparingly) |
| Surfaces | White cards + dark navy “premium” stat panels |
| Mood | Energetic sports branding, diagonal stripe energy, bold sans headers |
| Avoid | Generic purple-SaaS look, cream/terracotta editorial look, cluttered dashboards |

Useful live RR references (for tone, not for scraping proprietary data):

- [rajasthanroyals.com](https://www.rajasthanroyals.com/)  
- Squad / stats / auction pages linked in `RRSitedata.md`  
- Fan tools (Predictor, QuizzeRR, PoweRR Potential) show RR likes interactive product thinking  

---

## 4. What we do **not** have (gaps to close)

### 4.1 Missing from the data pack (must engineer or fetch publicly)

| Gap | Why it matters | How to handle |
|-----|----------------|---------------|
| **Precomputed pressure labels** | Core of the challenge | Define & compute ourselves |
| **Innings state features** (score, wickets, RRR, balls left, target) | Needed for chase/defend pressure | Reconstruct from ball-by-ball + match result fields |
| **Player role taxonomy** (pure batter / bowler / all-rounder) | Eligibility for batter vs bowler lists | Infer from balls faced vs balls bowled + public role if needed |
| **Player age, nationality, uncapped status** | Auction narrative / eligibility story | Public sources (ESPNcricinfo, Cricbuzz) — optional enrichment |
| **Current RR squad & retained list** | “How this player strengthens RR” | Public RR squad page + auction news |
| **Auction purse / base prices** | Not required for Round 1 rankings | Optional appendix only |
| **Domestic-only leagues** (SMAT, Vijay Hazare, etc.) | Marketing mentions “domestic”; PDF specifies IPL+T20I | **Do not invent**; stick to supplied pack. Public domestic data only as optional support, clearly labelled |
| **Player photos / official headshots** | Dashboard polish | Use placeholders or public-domain/official assets carefully |
| **Explicit evaluation rubric weights** | Unknown scoring formula | Optimise for: clarity of method, fairness, evidence, reproducibility |

### 4.2 Data quality caveats already visible

- `bowl_speed` missing on ~39% of balls  
- Some captain / MoM fields empty  
- Super overs exist (innings 3/4) — decide include/exclude rule  
- Stage value `Others` is large (226) — treat carefully vs true knockouts  
- Same player can appear across IPL franchises and national sides — aggregate by `player_id`  
- All-rounders can appear in both lists **across** categories, but **not twice inside the same Top 10**

### 4.3 Rules constraints (non-technical)

- Insights must be **your own** (AI allowed for research/build help; wholly AI-generated submission risks disqualification)  
- Data pack is **competition-only** — do not publish raw proprietary CSVs  
- One submission only  
- Individual participation  

---

## 5. What the product / project is

### Recommended project name

**PressurePulse — Rajasthan Royals Auction Intelligence (Round 1)**

### Product definition

A reproducible analytics system + presentation layer that:

1. Reconstructs match state ball-by-ball  
2. Labels each delivery (or phase) as **Pressure** vs **Baseline**  
3. Scores every batter and bowler on **pressure uplift / reliability**  
4. Outputs ranked Top 10 lists with confidence / sample-size guards  
5. Explains how each pick could help RR in IPL 2027  

### Suggested stack (full system — see detailed doc)

We are building a **complete deployable system** (pipeline + RR-branded React dashboard + PDF + Vercel), not a notebook-only submission.

| Layer | Choice | Why |
|-------|--------|-----|
| Data wrangling / models | Python 3.11 + pandas/numpy/scipy (+ optional sklearn) | Fast, reproducible war-room engine |
| Pipeline | `src/` modules + `run_pipeline.py` | Auditable, regenerates Top 10s |
| Dashboard | **React + Vite + TypeScript + Tailwind + Recharts** | Franchise-grade UI for RR review |
| Data to UI | Precomputed JSON aggregates only | Safe, fast; raw CSVs never public |
| Report | PDF/PPTX from same pipeline outputs | Required Unstop upload |
| Deploy | **Vercel** (dashboard URL) | Judges/RR open without installing anything |
| Branding | RR pink / navy / gold CSS variables | Match attached UI reference |

**Full technical architecture, repo layout, dashboard pages, env setup, and deployment checklist:** [`TECH_STACK_AND_SYSTEM.md`](./TECH_STACK_AND_SYSTEM.md)

> Ship rankings + PDF on time first; dashboard can thin-scope if the deadline is tight — but the target architecture is the full system above.

---

## 6. Core methodology blueprint (what to build analytically)

### 6.1 Phase A — Data foundation

1. Load all 6 CSVs; validate keys (`match_id`, `player_id`, `comp_id`, `team_id`)  
2. Join competitions → matches → ball-by-ball → player mapping  
3. Tag each match: `is_ipl`, `is_t20i`, `is_knockout`, season, stage  
4. Reconstruct cumulative innings state after every ball:
   - `runs_so_far`, `wickets_so_far`, `balls_bowled`, `balls_remaining`
   - For innings 2+: `target`, `runs_needed`, `required_run_rate`, `current_run_rate`, `par_diff`
5. Exclude garbage / incomplete rows with documented rules  

### 6.2 Phase B — Define Pressure (pick a clear, defensible definition)

Propose a **composite Pressure Index** (example — refine with evidence):

| Signal | Example rule | Applies to |
|--------|--------------|------------|
| Chase tightness | High RRR **and** limited balls left | 2nd innings batting & bowling |
| Collapse / survival | ≤3 wickets left early/mid | Batting & bowling |
| Death overs | Overs 16–20 with contest alive | Both |
| Powerplay choke | Overs 1–6 when chasing big / defending low | Both |
| Match leverage | Win probability swing or scoreboard closeness | Both |
| Stage pressure | Qualifier / Eliminator / Final / knock_out=1 | Both |

**Deliverable requirement:** Show distribution of pressure vs non-pressure balls; prove the definition is not just “death overs renamed.”

### 6.3 Phase C — Performance metrics

**Batters (pressure vs baseline)**

- Runs per ball / strike rate  
- Boundary % and dot %  
- Dismissal rate  
- Conversion in chase vs set totals  
- Clutch finishing (e.g., balls remaining ≤24, RRR ≥9)

**Bowlers (pressure vs baseline)**

- Economy / runs conceded per ball  
- Dot-ball %  
- Wicket rate / bowling average in pressure  
- Death-over economy  
- Ability to defend low totals / attack in high RRR chases  

**Baseline**

- Same player’s non-pressure performance (within competition type if sample allows)  
- Optionally league-adjusted baselines (IPL vs T20I skill environments)

### 6.4 Phase D — Rating & ranking logic

Suggested rating shape (transparent > black-box):

```
PressureScore = f(
  volume_in_pressure,          # enough sample?
  performance_in_pressure,     # absolute clutch quality
  uplift_vs_own_baseline,      # rises to occasion
  consistency_across_matches,  # not one-off heroics
  recency_weight               # 2024–26 > 2022 optional
)
```

**Eligibility filters (mandatory for fairness)**

- Minimum balls faced (batters) / balls bowled (bowlers) in pressure  
- Minimum matches / seasons  
- Separate IPL-weighted and combined IPL+T20I views; state which ranking is official  
- Handle all-rounders without double-counting inside one list  

**Reliability / uncertainty**

- Bootstrap CIs or simple “low / medium / high confidence” based on sample size  
- Sensitivity check: change pressure threshold ±X and show Top 10 stability  

### 6.5 Phase E — RR squad narrative (short, evidence-led)

For each Top 10 pick, 3–5 lines:

- Role (opener / finisher / death bowler / spinner etc.)  
- Pressure evidence (1 chart or 2 numbers)  
- Why RR specifically (gap in current squad / role fit) — using **public** squad info  

Do **not** invent auction budgets unless you clearly mark them as optional scenario analysis.

---

## 7. Submission package — exact checklist

### Must submit

- [ ] Unstop: Batter ranks 1–10 filled  
- [ ] Unstop: Bowler ranks 1–10 filled  
- [ ] PDF or PPTX methodology report uploaded  
- [ ] Rankings in form **exactly match** rankings in report  

### Strongly recommended

- [ ] Hosted dashboard URL  
- [ ] Methodology section reproducible enough for RR analysts to follow  
- [ ] Charts: pressure definition, Top 10 with scores, sample sizes, sensitivity  
- [ ] Limitations section (honest)  

### Optional

- [ ] 30–60s process video / LinkedIn-Instagram post  
- [ ] Public-data enrichment appendix (age, nationality, recent form)  

### Report structure (suggested)

1. Executive summary (Top 10s + 1-paragraph method)  
2. Pressure definition & validation  
3. Data & feature engineering  
4. Metrics & rating model  
5. Fairness / eligibility / IPL vs T20I handling  
6. Results — Top 10 batters with evidence  
7. Results — Top 10 bowlers with evidence  
8. How these players strengthen RR  
9. Reliability tests & limitations  
10. Appendix (formulas, thresholds, full tables)  

---

## 8. Build plan (execution order)

### Milestone 1 — Audit & state reconstruction (Day 1)

- Schema checks, nulls, join integrity  
- Innings state engine  
- Pressure label v1  

### Milestone 2 — Metrics & scores (Day 1–2)

- Player baselines  
- Pressure performance tables  
- Eligibility filters  
- Draft Top 15 → cut to Top 10  

### Milestone 3 — Validation (Day 2)

- Sensitivity / bootstrap  
- Sanity check vs known clutch performers (should not be reputation-only)  
- Red-team: “Are we just ranking death-over specialists?”  

### Milestone 4 — Story & RR fit (Day 2–3)

- Public RR squad gap notes  
- Player cards for Top 10  

### Milestone 5 — Dashboard + Report (Day 3)

- RR-branded visuals  
- PDF export  
- Dashboard deploy (Streamlit Cloud / Vercel / etc.)  

### Milestone 6 — Submit (before 18 Nov 2026 11:59 PM IST)

- Fill Unstop form carefully  
- Re-check name spelling vs dropdowns  
- Keep local copy of everything  

---

## 9. Suggested repo / folder layout

```text
SupeRR Selector/
├── docs/
│   ├── PROJECT_PLAN.md          ← this file
│   ├── projectdetails.md
│   ├── RRSitedata.md
│   ├── 1794678506882-9180.jpeg
│   └── dataset/.../Data Pack/   ← raw CSVs + PDF (do not publish)
├── data/
│   ├── processed/               ← engineered features (local only)
│   └── external/                ← optional public enrichment
├── notebooks/                   ← exploration
├── src/
│   ├── load.py
│   ├── state_reconstruction.py
│   ├── pressure.py
│   ├── metrics_batting.py
│   ├── metrics_bowling.py
│   ├── ranking.py
│   └── export.py
├── outputs/
│   ├── top10_batters.csv
│   ├── top10_bowlers.csv
│   ├── charts/
│   └── report/
├── dashboard/                   ← optional app
└── README.md
```

**Important:** Do not push proprietary raw data pack to a public GitHub repo.

---

## 10. Success criteria (how to know we’re ready)

| Criterion | Pass condition |
|-----------|----------------|
| Definition clarity | A cricket analyst can restate your pressure rule in 30 seconds |
| Dual coverage | Same framework scores batters **and** bowlers |
| Fairness | Min-sample rules documented; no tiny-sample flukes in Top 10 |
| Evidence | Every ranked player has supporting table/chart in report |
| Reproducibility | Running the pipeline regenerates the same Top 10s |
| Brand polish | Report/dashboard looks RR-native (pink/navy), not generic BI |
| Form accuracy | Unstop dropdowns == report ranks |
| Integrity | Method uses supplied data; public data only as labelled support |

---

## 11. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Pressure definition too vague or too narrow | Validate with distributions + sensitivity |
| Ranking dominated by famous names | Emphasize uplift vs baseline + sample filters |
| IPL vs T20I skill mix bias | Separate views; weight IPL higher for auction relevance |
| All-rounder / role ambiguity | Explicit classification rules |
| Deadline crunch | Ship solid PDF first; dashboard second |
| Accidental data leak | Keep raw pack private; publish only aggregates |
| Overfitting fancy ML | Prefer interpretable scores; ML only if it clearly helps |

---

## 12. Out of scope for Round 1 (do not waste time)

- Full auction purse optimiser / 25-player squad builder  
- Live ball-tracking / Hawk-Eye style models without data  
- Scraping entire ESPNcricinfo as primary rankings  
- Building a full fan website clone of rajasthanroyals.com  
- Team participation / multi-submit strategies  

---

## 13. Final “what exactly is to be done” summary

1. **Treat the Round 1 PDF as law:** measure pressure performance vs baseline for batters and bowlers.  
2. **Use the 6 CSVs** (especially ball-by-ball + matches) to reconstruct match state and invent a clear Pressure Index.  
3. **Rank Top 10 batters and Top 10 bowlers** with transparent eligibility and reliability checks.  
4. **Write a methodology report** that RR analysts can reproduce and trust.  
5. **Optionally ship an RR-branded dashboard** using the attached pink/navy UI language.  
6. **Submit on Unstop** (dropdowns + PDF/PPTX + optional links) before the deadline.  
7. **Close gaps** (roles, RR squad fit, ages) with public data only where it improves the auction narrative — never as a substitute for the pack analysis.

If this plan is followed end-to-end, Round 1 is complete and competitive: not just a list of names, but a war-room-grade pressure intelligence system ready for Royals evaluation.
