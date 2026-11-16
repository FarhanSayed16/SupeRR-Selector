# PressurePulse — Complete Backend Implementation Plan

**Scope:** Backend only — structure, modules, services, features, responsibilities, data handoffs.  
**No code in this document** — implementation headings and what must exist in each place.  
**Related docs:** [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) · [`TECH_STACK_AND_SYSTEM.md`](./TECH_STACK_AND_SYSTEM.md)

---

## 1. Backend mission

The backend is the **Pressure Intelligence Engine**. It must:

1. Ingest the official Rajasthan Royals data pack safely (private, local).
2. Reconstruct every ball’s match situation.
3. Label **pressure** vs **baseline** with a documented definition.
4. Score batters and bowlers for performance under pressure.
5. Produce official **Top 10 batters** and **Top 10 bowlers**.
6. Validate fairness, sample size, and ranking stability.
7. Export aggregates for the dashboard, methodology report, and Unstop submission.
8. Remain fully reproducible — same inputs + same config → same rankings.

The backend does **not** render UI. It prepares everything the frontend and PDF need.

---

## 2. Backend shape (how we think about it)

Treat the backend as **four layers**:

| Layer | Name | Job |
|-------|------|-----|
| L0 | **Foundation** | Config, paths, logging, run orchestration |
| L1 | **Data platform** | Load, clean, join, store intermediate tables |
| L2 | **Intelligence services** | State, pressure, metrics, ranking, validation |
| L3 | **Delivery services** | Dashboard JSON, report assets, ranking files, optional API |

Plus one optional layer:

| Layer | Name | Job |
|-------|------|-----|
| L4 | **Serving API** | Only if live search/filter beyond static files is required |

**Default Round 1 mode:** L0–L3 as a batch pipeline. L4 optional and deferred.

---

## 3. Top-level backend folder map

```text
src/                          ← all backend logic lives here
├── foundation/               ← L0
├── data_platform/            ← L1
├── intelligence/             ← L2
├── delivery/                 ← L3
├── api/                      ← L4 (optional)
└── run_pipeline.py           ← single orchestrator entry

data/
├── raw/                      ← official pack (private)
├── processed/                ← intermediate analytical tables
└── external/                 ← optional public enrichment

outputs/
├── rankings/                 ← Top 10 + full score tables
├── charts/                   ← report chart assets
├── report/                   ← methodology build inputs / PDF
├── dashboard_export/         ← staging copy of JSON before FE copy
└── qa/                       ← validation / audit artefacts

api/                          ← optional FastAPI app root (if separated)
notebooks/                    ← exploration only — never source of truth
scripts/                      ← run helpers (setup, full run, freeze)
```

Every folder below is described by **purpose**, **contains**, and **features** — not code.

---

## 4. Layer L0 — Foundation

### 4.1 Module: Configuration Service

**Folder:** `src/foundation/`  
**Primary file concept:** Configuration module  

**Must define / hold**

- Paths to raw CSVs, processed storage, outputs, dashboard data folder
- Pressure definition version name (e.g. `pressure_v1`)
- All thresholds (RRR cutoffs, overs bands, wicket bands, knockout weights)
- Eligibility minimums (balls, matches, seasons)
- Competition weights (IPL vs T20I)
- Recency weights by season
- Include/exclude rules (super overs, abandoned matches, null-heavy rows)
- Random seed for any bootstrap / sampling
- Export toggles (what artefacts to write this run)

**Features**

- Single source of truth for methodology knobs
- Human-readable defaults that match the report
- Ability to run alternate “sensitivity configs” without rewriting logic

---

### 4.2 Module: Logging & Run Metadata

**Primary file concepts:** Logger setup · Run context  

**Must capture**

- Run start/end time
- Config version / pressure definition version
- Row counts at each major stage
- Warnings (missing joins, dropped rows, low sample)
- Final Top 10 fingerprint (hash or ordered id list) for freeze checks

**Features**

- Console + file log for each pipeline run
- `qa/run_manifest` artefact listing what was produced

---

### 4.3 Module: Pipeline Orchestrator

**Primary file concept:** `run_pipeline` entry  

**Must sequence**

1. Validate environment & paths  
2. Load & clean  
3. Build match/ball state  
4. Apply pressure labels  
5. Compute batting metrics  
6. Compute bowling metrics  
7. Rank & cut Top 10s  
8. Run validation gates  
9. Export rankings / dashboard / report inputs  
10. Fail the run if critical QA gates fail  

**Features**

- One command regenerates the entire backend output set
- Clear stage names for debugging
- Non-zero exit when rankings would be unsafe to submit

---

## 5. Layer L1 — Data Platform

### 5.1 Module: Raw Ingestion Service

**Folder:** `src/data_platform/`  
**Primary file concept:** Loader  

**Inputs (official pack)**

| Source file | Backend entity |
|-------------|----------------|
| competitions | Competition catalogue |
| teams | Team-in-competition map |
| matches | Match header / context |
| playing_eleven | XI, roles flags, batting order |
| competition_team_player_mapping | Player identity directory |
| ball_by_ball | Delivery fact table |

**Features**

- Read all six sources
- Enforce expected columns exist
- Normalise basic types (dates, booleans, ids)
- Refuse to proceed if a critical file is missing

---

### 5.2 Module: Data Quality & Cleaning Service

**Primary file concept:** Cleaner / validator  

**Must check**

- Primary key uniqueness where expected (`match_id`, player mapping rows, etc.)
- Orphan balls (match ids not in matches)
- Orphan players (ids without names in mapping — flag, don’t silently invent)
- Null rates on critical fields (striker, bowler, runs, over)
- Duplicate delivery keys (match + innings + ball sequence)
- Impossible values (over outside 1–20 for standard T20, negative runs)

**Features**

- Quality report written to `outputs/qa/`
- Explicit drop rules documented (what was removed and why)
- Soft warnings vs hard failures separated

---

### 5.3 Module: Entity Join / Warehouse Builder

**Primary file concept:** Joiner / dim-fact builder  

**Must produce logical tables**

| Logical table | Purpose |
|---------------|---------|
| dim_competition | Season, format, IPL flag |
| dim_team | Team identity per competition |
| dim_player | Stable player_id ↔ name (and optional enrichment later) |
| dim_match | Stage, knockout, venue country, result, toss |
| fact_xi | Who played, WK, captain, batting order |
| fact_delivery | Every ball with player and match foreign keys |

**Features**

- Consistent id usage across all later services
- Flags: `is_ipl`, `is_t20i`, `is_knockout`, `season_group`
- Persist processed snapshots under `data/processed/` for reuse

---

### 5.4 Module: External Enrichment Service (optional)

**Folder tie-in:** `data/external/`  

**May add (public only, clearly labelled)**

- Player role tags (batter / bowler / all-rounder / WK)
- Nationality / overseas flag
- Approximate age band
- Current RR squad membership / retention status
- Recent public form notes (manual curated, not scraped dumps)

**Features**

- Join enrichment on `player_id` or cleaned player name with match confidence
- Never override official pack performance numbers
- Enrichment used for narrative / Auction Room, not for inventing pressure scores

---

## 6. Layer L2 — Intelligence Services (core product)

### 6.1 Service: Match State Reconstruction

**Folder:** `src/intelligence/`  
**Primary file concept:** State engine  

**Responsibility**  
Turn unordered “ball rows” into a time-aware match situation after every delivery.

**Features / fields to materialise per ball**

- Cumulative runs and wickets in the innings
- Legal balls consumed and balls remaining
- Current run rate
- Innings number handling (1, 2, and super-over policy)
- Target / runs needed / required run rate (chase innings)
- Scoreboard delta vs par / closeness proxy
- Phase tag: powerplay / middle / death
- Partnership or batting-order context where useful
- Match stage context joined from dim_match

**Depends on:** Data platform fact_delivery + dim_match  
**Feeds:** Pressure service, metrics services  

**Must document**

- How targets are inferred when revised overs / targets exist
- What happens on extras
- Super-over include/exclude decision

---

### 6.2 Service: Pressure Definition Engine

**Primary file concept:** Pressure service  

**Responsibility**  
Decide which situations count as high pressure — the heart of Round 1.

**Feature blocks inside this service**

1. **Signal library** (individual pressure signals)
   - Chase tightness (high RRR + limited balls)
   - Survival pressure (few wickets left)
   - Death-over contest still alive
   - Powerplay choke / early collapse pressure
   - Knockout / final / qualifier stage pressure
   - Close contest / small margin pressure (where definable)

2. **Composite Pressure Index**
   - Combine signals into one score or rule set
   - Produce `is_pressure` label used everywhere downstream
   - Versioned definition name for the report

3. **Definition diagnostics**
   - % of balls labelled pressure overall
   - Split by IPL vs T20I
   - Split by phase and stage
   - Proof that pressure ≠ “only death overs”

**Depends on:** State engine  
**Feeds:** All metrics + Pressure Lab exports  

---

### 6.3 Service: Player Role Classification

**Primary file concept:** Role classifier  

**Responsibility**  
Decide who is eligible as batter, bowler, or both (all-rounder).

**Features**

- Volume-based rules (balls faced vs balls bowled)
- Optional WK flag from playing XI
- Manual override list for known edge cases
- Prevents empty or wrong-category Top 10 contamination

**Depends on:** fact_delivery + fact_xi (+ optional enrichment)  
**Feeds:** Ranking eligibility  

---

### 6.4 Service: Batting Performance Metrics

**Primary file concept:** Batting metrics  

**Responsibility**  
Measure how each batter performs in pressure vs baseline.

**Metric families**

| Family | Examples of what to compute |
|--------|-----------------------------|
| Volume | Balls, inns, matches in pressure / baseline |
| Scoring | Runs, strike rate, runs per ball |
| Aggression | Boundary %, six %, dot % |
| Durability | Dismissal rate, average under pressure |
| Situation | Chase finishing slices, death batting slices |
| Uplift | Pressure performance minus own baseline |
| Consistency | Spread across matches / seasons (not one hero innings) |

**Features**

- Separate IPL-only and combined IPL+T20I metric sets
- Per-player baseline using non-pressure balls (same competition weight policy)
- Sample-size fields attached to every metric row

**Depends on:** Pressure labels + role classification  
**Feeds:** Ranking service + player detail exports  

---

### 6.5 Service: Bowling Performance Metrics

**Primary file concept:** Bowling metrics  

**Responsibility**  
Same structure as batting, for bowlers.

**Metric families**

| Family | Examples of what to compute |
|--------|-----------------------------|
| Volume | Balls bowled, spells/matches in pressure |
| Control | Economy, runs per ball, dot % |
| Wicket threat | Wicket rate, bowling average, strike rate (balls/wkt) |
| Phase | Death economy, powerplay under pressure |
| Match leverage | Defending low totals / bowling to high RRR chases |
| Uplift | Pressure vs own baseline |
| Consistency | Multi-match reliability |

**Features**

- Pace vs spin breakdowns (supporting evidence, not necessarily ranking split)
- Same eligibility and weighting philosophy as batting

**Depends on:** Pressure labels + role classification  
**Feeds:** Ranking service + player detail exports  

---

### 6.6 Service: Scoring & Ranking Engine

**Primary file concept:** Ranking service  

**Responsibility**  
Convert metrics into a transparent **PressureScore** and ordered Top 10 lists.

**Feature blocks**

1. **Eligibility gate**
   - Minimum pressure volume
   - Minimum matches / seasons
   - Role gate (batter list vs bowler list)
   - No duplicate player inside the same Top 10

2. **Score composition**
   - Absolute clutch quality under pressure
   - Uplift vs own baseline
   - Consistency / reliability term
   - Optional recency weighting
   - Optional IPL emphasis for auction relevance

3. **Ranking outputs**
   - Full ranked universe (all eligible players)
   - Official Top 10 batters
   - Official Top 10 bowlers
   - Near-miss board (ranks 11–20) for sensitivity discussion

4. **Confidence tagging**
   - High / Medium / Low based on sample size rules
   - Exposed on dashboard and in report

**Depends on:** Batting metrics + bowling metrics + config  
**Feeds:** Delivery layer + validation  

---

### 6.7 Service: Validation, Sensitivity & Audit

**Primary file concept:** Validation / QA service  

**Responsibility**  
Prove the rankings are not fragile, biased, or reputation-driven.

**Feature blocks**

1. **Sanity audits**
   - Known volume players appear with plausible samples
   - No zero-ball miracle ranks
   - All-rounder handling correct across lists

2. **Sensitivity tests**
   - Nudge pressure thresholds up/down
   - Measure Top 10 overlap / churn
   - Alternate IPL-only vs combined ranking comparison

3. **Uncertainty**
   - Bootstrap or resampling intervals where useful
   - Flag borderline ranks (e.g. 9–12 cluster)

4. **Leakage / logic checks**
   - Baseline does not accidentally include pressure balls
   - Knockout signal not double-counted incorrectly
   - Super-over policy applied consistently

5. **Submission freeze check**
   - Store final ordered player ids
   - Compare against previous freeze file if re-run

**Outputs:** `outputs/qa/` summaries that Methodology can cite  
**Gate:** Orchestrator may block exports if hard failures occur  

---

## 7. Layer L3 — Delivery Services

### 7.1 Service: Rankings Exporter

**Folder:** `src/delivery/`  
**Primary file concept:** Rankings export  

**Must produce**

- Official Top 10 batters table (rank, id, name, scores, confidence)
- Official Top 10 bowlers table
- Full eligible score table (for appendix / dashboard filters)
- Near-miss tables (11–20)

**Consumers**

- Unstop form (human copies ranks)
- Methodology report tables
- Dashboard Top 10 widgets

---

### 7.2 Service: Dashboard Data Exporter

**Primary file concept:** Dashboard export  

**Responsibility**  
Create **safe aggregates only** for the React app.

**Logical export packages**

| Package | Contents (conceptual) |
|---------|------------------------|
| Meta package | Build time, seasons covered, pressure version, disclaimer |
| Top 10 packages | Batters and bowlers with headline metrics |
| Players index | Search list: id, name, role, headline scores |
| Player detail package | Baseline vs pressure cards, small evidence series |
| Pressure Lab package | Distributions, phase mixes, definition summary stats |
| RR fit package | Narrative bullets for Auction Room (from enrichment + ranks) |
| Methodology package | Thresholds, eligibility text keys, limitation flags |

**Features**

- No raw ball-by-ball dump to frontend
- File size budgets respected
- Schema stable enough for frontend types
- Copy/sync into dashboard public data location as final step

---

### 7.3 Service: Report Asset Exporter

**Primary file concept:** Report export  

**Must prepare**

- Summary tables for PDF chapters
- Chart-ready series (pressure share, Top 10 bars, uplift plots)
- Limitations and QA highlights
- Exact Top 10 blocks matching Unstop order

**Features**

- One “numbers freeze” shared with dashboard exporter
- Report cannot drift from dashboard ranks

---

### 7.4 Service: Methodology Narrative Binder (backend-assisted)

**Primary file concept:** Report binder / content assembler  

**Responsibility**  
Assemble structured content sections the PDF/PPT builder consumes.

**Sections to bind from backend facts**

- Pressure definition statement
- Metric dictionary
- Eligibility rules
- IPL vs T20I handling
- Top 10 evidence packs
- Reliability & limitations
- RR strengthening notes

*(Writing polish can be manual; numbers must be backend-sourced.)*

---

## 8. Layer L4 — Optional Serving API

**Only if** static JSON is not enough for RR live demos.

### 8.1 API module map

| Endpoint group | Purpose |
|----------------|---------|
| Health | Service up check |
| Meta | Pressure version, data coverage |
| Rankings | Top 10 + full list with filters |
| Players | Search, detail by id |
| Pressure lab | Summary stats for definition charts |
| Export | Download CSV of current ranking view |

### 8.2 API rules

- Read from processed/exported artefacts — do **not** recompute heavy pipeline per request in Round 1
- No raw CSV exposure
- CORS limited to dashboard domain
- Same ranking freeze as batch exports

**Recommendation:** skip L4 for first submission unless needed.

---

## 9. Cross-cutting concerns (must exist across modules)

### 9.1 Identity & naming

- `player_id` is the only join key for performance
- Display names come from mapping table
- Unstop dropdown spelling reconciliation checklist (manual QA artefact)

### 9.2 Competition fairness

- Always be able to produce IPL-weighted and combined views
- Document which view is **official** for submission

### 9.3 Reproducibility

- Fixed config + seed
- Manifest of input file fingerprints (size/hash) in QA
- Version tag on pressure definition

### 9.4 Privacy & compliance

- Raw pack never leaves private storage
- Public artefacts are aggregates only
- README / NOTICE states competition-only data use

### 9.5 Error policy

| Severity | Examples | Behaviour |
|----------|----------|-----------|
| Fatal | Missing ball_by_ball, broken keys | Stop pipeline |
| Major | Eligibility yields &lt; 10 players | Stop or force config revise |
| Minor | Sparse bowl_speed | Warn; continue without depending on it |
| Info | Enrichment miss for a player | Continue; narrative gap only |

---

## 10. Feature catalogue by domain (checklist view)

### Data features

- [ ] Multi-file ingest of official pack  
- [ ] Schema validation  
- [ ] Cleaning & drop logging  
- [ ] Dimensional model build  
- [ ] Processed table persistence  
- [ ] Optional public enrichment join  

### Cricket intelligence features

- [ ] Innings state reconstruction  
- [ ] Chase/defend context  
- [ ] Phase tagging  
- [ ] Pressure signal library  
- [ ] Composite pressure label + diagnostics  
- [ ] Role classification  
- [ ] Batter pressure metrics + uplift  
- [ ] Bowler pressure metrics + uplift  
- [ ] Transparent PressureScore  
- [ ] Top 10 cut with confidence  

### Trust features

- [ ] Sensitivity analysis  
- [ ] Sample-size gates  
- [ ] Freeze / fingerprint of final ranks  
- [ ] QA manifest  

### Delivery features

- [ ] Ranking CSV/table export  
- [ ] Dashboard JSON packages  
- [ ] Report tables/charts package  
- [ ] Optional read-only API  

---

## 11. Backend data handoff contracts (what each consumer receives)

| Consumer | Receives from backend | Must not receive |
|----------|------------------------|------------------|
| React dashboard | Aggregated JSON packages | Raw deliveries CSV |
| Methodology PDF | Frozen tables + chart series + definition text keys | Ad-hoc notebook numbers |
| Unstop form | Ordered Top 10 names (via rankings export) | Internal ids only without names |
| RR reviewers | Same dashboard + PDF evidence | Local raw pack requirement |
| Optional API | Read models of the above | Direct filesystem raw pack |

---

## 12. Implementation order (backend-only build sequence)

### Stage A — Foundation & data platform

1. Foundation config + logging  
2. Ingestion of six files  
3. Quality report  
4. Dim/fact joins into processed storage  

### Stage B — State & pressure

5. Match state reconstruction  
6. Pressure signal library  
7. Composite label + diagnostics export  

### Stage C — Performance & ranks

8. Role classification  
9. Batting metrics service  
10. Bowling metrics service  
11. Scoring & ranking engine (draft Top 15 → Top 10)  

### Stage D — Trust

12. Validation & sensitivity  
13. Hard QA gates wired into orchestrator  

### Stage E — Delivery

14. Rankings exporter  
15. Dashboard exporter  
16. Report asset exporter  
17. Full orchestrated run + freeze  

### Stage F — Optional

18. Serving API on top of frozen exports  

---

## 13. Definition of done (backend)

Backend is complete when:

1. One orchestrated run produces official Top 10 batters and bowlers.  
2. Pressure definition diagnostics prove the label is meaningful.  
3. Every ranked player has metric evidence and confidence.  
4. QA gates pass (or failures are explicitly waived in writing — avoid).  
5. Dashboard JSON and report tables are generated from the **same freeze**.  
6. Re-running with the same config reproduces the same Top 10 order.  
7. Raw proprietary files remain private.  

---

## 14. How this maps to the rest of the project

| Doc | Role |
|-----|------|
| `PROJECT_PLAN.md` | Problem, data inventory, methodology intent, submission |
| `TECH_STACK_AND_SYSTEM.md` | Stack, repo, dashboard pages, deploy |
| **`BACKEND_PLAN.md`** | Backend modules, services, features, build order (this file) |

Frontend plan can be a separate doc later; it only **consumes** Layer L3 outputs.

---

## 15. One-page backend summary

**Foundation** configures and runs the system.  
**Data platform** loads and warehouses the RR pack.  
**State service** rebuilds match situations.  
**Pressure service** labels clutch moments.  
**Metrics services** score batters and bowlers vs baseline.  
**Ranking service** produces Top 10s with eligibility and confidence.  
**Validation service** proves reliability.  
**Delivery services** publish safe artefacts for dashboard, PDF, and Unstop.  
**Optional API** serves those artefacts live if needed.

That is the full backend implementation plan — structure, modules, services, and features — ready to build against without ambiguity.
