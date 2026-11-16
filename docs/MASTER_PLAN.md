# PressurePulse — Complete Master Plan (Execution Checklist)

**Product:** PressurePulse — SupeRR Selector Season 2 · Round 1  
**Franchise context:** Rajasthan Royals · IPL 2027 auction intelligence  
**Role of this file:** Single execution checklist — phases, sub-phases, gates. Check items off until the project is fully complete.  
**Companion index:** [`DOCS_INDEX.md`](./DOCS_INDEX.md)  
**Detail docs:** [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) · [`TECH_STACK_AND_SYSTEM.md`](./TECH_STACK_AND_SYSTEM.md) · [`BACKEND_PLAN.md`](./BACKEND_PLAN.md) · [`FRONTEND_PLAN.md`](./FRONTEND_PLAN.md)

**Deadlines**

- Registration: **16 Nov 2026, 11:59 PM IST**  
- Round 1 submit: **18 Nov 2026, 11:59 PM IST**

**How to use**

1. Complete phases in order unless a note says “can parallel.”  
2. Finish every sub-phase checkbox in a phase before the Phase Gate.  
3. Do not mark a Phase Gate done until its criteria are true.  
4. Open detail docs only when a sub-phase needs deeper rules.

---

## Master progress tracker

| Phase | Name | Status |
|------:|------|--------|
| 01 | Project lock-in & requirements freeze | `[x]` |
| 02 | Workspace, repo & compliance setup | `[x]` |
| 03 | Environment & toolchain setup | `[x]` |
| 04 | Data pack intake & schema audit | `[x]` |
| 05 | Data quality, cleaning & warehouse | `[x]` |
| 06 | Backend foundation (config, logging, orchestrator shell) | `[x]` |
| 07 | Match state reconstruction | `[x]` |
| 08 | Pressure definition engine | `[x]` |
| 09 | Player role classification | `[x]` |
| 10 | Batting metrics service | `[x]` |
| 11 | Bowling metrics service | `[x]` |
| 12 | Scoring, eligibility & Top 10 ranking | `[x]` |
| 13 | Validation, sensitivity & rank freeze | `[x]` |
| 14 | Backend delivery exports (JSON / CSV / report inputs) | `[x]` |
| 15 | Frontend foundation (design system & app shell) | `[x]` |
| 16 | Frontend shared data & core UI kit | `[x]` |
| 17 | Command Centre page | `[x]` |
| 18 | Batter & Bowler Intelligence pages | `[x]` |
| 19 | Pressure Lab & Player Profile pages | `[x]` |
| 20 | Auction Room, Methodology & system states | `[x]` |
| 21 | Motion, responsive, a11y & FE polish | `[x]` |
| 22 | Methodology report (PDF/PPTX) | `[x]` |
| 23 | Deployment (Vercel) & live QA | `[x]` |
| 24 | Unstop submission pack & form | `[x]` |
| 25 | Final freeze, archive & post-submit hygiene | `[x]` |

---

# PHASE 01 — Project lock-in & requirements freeze

**Goal:** Everyone (and future-you) agrees what “done” means for Round 1.  
**Detail refs:** PROJECT_PLAN · Round 1 PDF · projectdetails.md

### Sub-phases

- [x] 01.1 Re-read official Round 1 problem PDF end-to-end  
- [x] 01.2 Confirm required outputs: Top 10 batters + Top 10 bowlers + methodology PDF/PPTX  
- [x] 01.3 Confirm optional outputs: dashboard URL, journey video  
- [x] 01.4 Confirm Unstop form fields (20 dropdowns + upload + links)  
- [x] 01.5 Confirm deadlines (registration + Round 1) and set calendar reminders  
- [x] 01.6 Confirm participation rules (individual, one submission, AI-assist OK but original insights)  
- [x] 01.7 Confirm data rules (pack is competition-only; do not publish raw CSVs)  
- [x] 01.8 Lock product name: **PressurePulse**  
- [x] 01.9 Lock stack decisions from TECH_STACK_AND_SYSTEM  
- [x] 01.10 Lock page list from FRONTEND_PLAN (Command Centre → Methodology)  
- [x] 01.11 Lock backend service list from BACKEND_PLAN (L0–L3; L4 deferred)  
- [x] 01.12 Write a 5-line “success definition” at the top of your notes matching Final Master Gate  

### Phase Gate 01

- [x] **GATE:** Requirements frozen; no ambiguity on Top 10×2 + report + optional dashboard  

---

# PHASE 02 — Workspace, repo & compliance setup

**Goal:** Safe project skeleton so proprietary data never leaks.  
**Detail refs:** TECH_STACK_AND_SYSTEM §4 · BACKEND_PLAN folder map

### Sub-phases

- [x] 02.1 Create root folders: `src/`, `data/raw`, `data/processed`, `data/external`, `outputs/`, `dashboard/`, `notebooks/`, `scripts/`, `docs/`  
- [x] 02.2 Place / symlink official Data Pack into `data/raw` (private)  
- [x] 02.3 Create `.gitignore` covering: raw CSVs, processed dumps, `.venv`, `node_modules`, `.env`, OS junk, large caches  
- [x] 02.4 Add NOTICE / README warning: competition-only data; aggregates-only in public remotes  
- [x] 02.5 Initialize git repo if not already (no force-push policies needed yet)  
- [x] 02.6 Decide remote visibility (private preferred while raw data exists locally)  
- [x] 02.7 Create empty `outputs/rankings`, `outputs/qa`, `outputs/report`, `outputs/charts`, `outputs/dashboard_export`  
- [x] 02.8 Confirm docs set present: PROJECT / TECH / BACKEND / FRONTEND / DOCS_INDEX / MASTER_PLAN  
- [x] 02.9 Create root README outline: what PressurePulse is, how to view live URL, how to regenerate pipeline  

### Phase Gate 02

- [x] **GATE:** Folder map exists; raw pack is local + gitignored; docs index reachable  

---

# PHASE 03 — Environment & toolchain setup

**Goal:** Reproducible Python + Node environments ready to build.  
**Detail refs:** TECH_STACK_AND_SYSTEM §7

### Sub-phases

- [x] 03.1 Install / verify Python 3.11+  
- [x] 03.2 Create virtualenv and activation script notes for Windows PowerShell  
- [x] 03.3 Create `requirements.txt` with planned analytics libraries  
- [x] 03.4 Install Python dependencies successfully  
- [x] 03.5 Install / verify Node.js 20+  
- [x] 03.6 Scaffold or prepare `dashboard/` package manager (`npm`/`pnpm`)  
- [x] 03.7 Verify Vite/React/TS/Tailwind install path works (even if app is stub)  
- [x] 03.8 Install Vercel CLI optional (or plan dashboard deploy via GitHub integration)  
- [x] 03.9 Create `scripts/setup_env.ps1` (or equivalent) for one-shot setup  
- [x] 03.10 Smoke-test: Python imports pandas; Node runs `npm -v`  

### Phase Gate 03

- [x] **GATE:** Both Python and Node toolchains run cleanly on this machine  

---

# PHASE 04 — Data pack intake & schema audit

**Goal:** Know exactly what is in the pack before modelling pressure.  
**Detail refs:** PROJECT_PLAN §3 · BACKEND_PLAN §5.1

### Sub-phases

- [x] 04.1 Inventory six CSVs + problem PDF in Data Pack  
- [x] 04.2 Record row counts for each file  
- [x] 04.3 Document columns for `competitions`, `teams`, `matches`, `playing_eleven`, `competition_team_player_mapping`, `ball_by_ball`  
- [x] 04.4 Confirm seasons covered (2022→2026) and IPL comps present  
- [x] 04.5 Confirm formats (T20 / T20I) and match date range  
- [x] 04.6 Note knockout/stage fields and their value distributions  
- [x] 04.7 Note ball-level fields usable for pressure (runs, wickets, extras, phase proxies, pace/spin, etc.)  
- [x] 04.8 List known sparse fields (e.g. bowl_speed missingness)  
- [x] 04.9 Count unique players / teams  
- [x] 04.10 Write short “data coverage summary” into `outputs/qa/` (even as markdown notes)  
- [x] 04.11 Explicitly list gaps (no precomputed RRR, no roles, no auction purse, etc.)  

### Phase Gate 04

- [x] **GATE:** Schema audit complete; coverage and gaps written down  

---

# PHASE 05 — Data quality, cleaning & warehouse

**Goal:** Trusted joined tables ready for intelligence services.  
**Detail refs:** BACKEND_PLAN §5.2–5.3

### Sub-phases

- [x] 05.1 Implement / execute raw ingestion of all six sources  
- [x] 05.2 Validate expected columns exist (hard fail if critical missing)  
- [x] 05.3 Normalise types (dates, booleans, ids)  
- [x] 05.4 Check orphan deliveries / orphan players; log findings  
- [x] 05.5 Check duplicate delivery keys; define drop rules  
- [x] 05.6 Check impossible values (overs, negative runs)  
- [x] 05.7 Build logical dims: competition, team, player, match  
- [x] 05.8 Build facts: XI + delivery  
- [x] 05.9 Add flags: `is_ipl`, `is_t20i`, `is_knockout`, season grouping  
- [x] 05.10 Persist processed snapshots under `data/processed/`  
- [x] 05.11 Write QA quality report to `outputs/qa/`  
- [x] 05.12 (Optional) Prepare `data/external/` enrichment template for roles/RR squad later  

### Phase Gate 05

- [x] **GATE:** Clean joined warehouse exists; quality report reviewed; no fatal orphans blocking analysis  

---

# PHASE 06 — Backend foundation (config, logging, orchestrator shell)

**Goal:** Single-run backbone for the intel engine.  
**Detail refs:** BACKEND_PLAN §4

### Sub-phases

- [x] 06.1 Create foundation config module (paths, thresholds placeholders, seeds)  
- [x] 06.2 Name pressure definition version (e.g. `pressure_v1`)  
- [x] 06.3 Set eligibility placeholders (min balls / matches) — tune later  
- [x] 06.4 Set IPL vs T20I weight placeholders  
- [x] 06.5 Set super-over include/exclude policy explicitly  
- [x] 06.6 Add logging + run manifest writer  
- [x] 06.7 Create orchestrator shell with ordered stage names (even if some stages are stubs)  
- [x] 06.8 Wire stage: load → clean → (stubs for later) → export placeholders  
- [x] 06.9 Ensure orchestrator exits non-zero on fatal errors  
- [x] 06.10 Document config knobs to be copied into Methodology later  

### Phase Gate 06

- [x] **GATE:** `run_pipeline` entry exists and can load warehouse with logging/manifest  

---

# PHASE 07 — Match state reconstruction

**Goal:** Every ball knows the match situation.  
**Detail refs:** BACKEND_PLAN §6.1 · PROJECT_PLAN methodology blueprint

### Sub-phases

- [x] 07.1 Define ordering key within innings (over, ball, extras handling)  
- [x] 07.2 Compute cumulative runs and wickets  
- [x] 07.3 Compute balls consumed / balls remaining  
- [x] 07.4 Compute current run rate  
- [x] 07.5 Infer targets for chase innings (including revised target fields where present)  
- [x] 07.6 Compute runs needed + required run rate  
- [x] 07.7 Tag phases: powerplay / middle / death  
- [x] 07.8 Join match stage / knockout context onto balls  
- [x] 07.9 Apply super-over policy consistently  
- [x] 07.10 Validate state on sample matches manually (spot-check 2–3 known games)  
- [x] 07.11 Persist ball-level state table to processed storage  
- [x] 07.12 Log summary stats (null RRR rate in innings 1 vs 2, etc.)  

### Phase Gate 07

- [x] **GATE:** State table exists; chase/defend fields make sense on spot-checks  

---

# PHASE 08 — Pressure definition engine

**Goal:** Transparent, defensible pressure labels for batting and bowling.  
**Detail refs:** BACKEND_PLAN §6.2 · PROJECT_PLAN §6.2 · FRONTEND Pressure Lab needs

### Sub-phases

- [x] 08.1 List pressure signals to implement (chase tightness, wickets left, death contest, knockout, etc.)  
- [x] 08.2 Implement each signal as an explicit rule  
- [x] 08.3 Combine into composite Pressure Index / `is_pressure` label  
- [x] 08.4 Version and document the definition in config + notes  
- [x] 08.5 Compute % balls labelled pressure overall  
- [x] 08.6 Split diagnostics: IPL vs T20I  
- [x] 08.7 Split diagnostics: phase and stage  
- [x] 08.8 Prove definition is not “death overs only” (write evidence note)  
- [x] 08.9 Tune thresholds if label rate is absurdly low/high  
- [x] 08.10 Export pressure summary package for dashboard Pressure Lab  
- [x] 08.11 Freeze wording of “pressure in one sentence” for UI + PDF  

### Phase Gate 08

- [x] **GATE:** Pressure labels + diagnostics ready; definition sentence frozen  

---

# PHASE 09 — Player role classification

**Goal:** Correct eligibility for batter vs bowler lists.  
**Detail refs:** BACKEND_PLAN §6.3

### Sub-phases

- [x] 09.1 Compute balls faced and balls bowled per player  
- [x] 09.2 Use XI WK flags where useful  
- [x] 09.3 Define rules for batter / bowler / all-rounder  
- [x] 09.4 Create manual override list for edge cases  
- [x] 09.5 Attach role tags to player dimension  
- [x] 09.6 QA: sample known players classified sensibly  
- [x] 09.7 (Optional) Merge public enrichment roles without overriding performance facts  

### Phase Gate 09

- [x] **GATE:** Every player who will be ranked has a role decision  

---

# PHASE 10 — Batting metrics service

**Goal:** Pressure vs baseline batting measurement.  
**Detail refs:** BACKEND_PLAN §6.4

### Sub-phases

- [x] 10.1 Define batting metric dictionary (SR, dots, boundaries, dismissals, volume, uplift, consistency)  
- [x] 10.2 Compute metrics in pressure subset  
- [x] 10.3 Compute metrics in baseline (non-pressure) subset  
- [x] 10.4 Compute uplift fields  
- [x] 10.5 Attach sample-size fields (balls, matches, seasons)  
- [x] 10.6 Build IPL-oriented and combined views as planned  
- [x] 10.7 Situation slices (death / chase finishing) if available  
- [x] 10.8 Persist batter metrics table  
- [x] 10.9 Spot-check 5 players manually for sanity  

### Phase Gate 10

- [x] **GATE:** Batter metrics table complete with uplift + sample sizes  

---

# PHASE 11 — Bowling metrics service

**Goal:** Pressure vs baseline bowling measurement.  
**Detail refs:** BACKEND_PLAN §6.5

### Sub-phases

- [x] 11.1 Define bowling metric dictionary (economy, dots, wicket rate, volume, uplift, consistency)  
- [x] 11.2 Compute pressure metrics  
- [x] 11.3 Compute baseline metrics  
- [x] 11.4 Compute uplift fields  
- [x] 11.5 Attach sample sizes  
- [x] 11.6 Phase slices (death economy etc.)  
- [x] 11.7 Optional pace/spin breakdowns for supporting evidence  
- [x] 11.8 Persist bowler metrics table  
- [x] 11.9 Spot-check 5 bowlers manually  

### Phase Gate 11

- [x] **GATE:** Bowler metrics table complete with uplift + sample sizes  

---

# PHASE 12 — Scoring, eligibility & Top 10 ranking

**Goal:** Official ordered Top 10 batters and Top 10 bowlers.  
**Detail refs:** BACKEND_PLAN §6.6 · PROJECT_PLAN §6.4

### Sub-phases

- [x] 12.1 Finalise eligibility minimums (pressure volume + matches)  
- [x] 12.2 Apply role gates per list  
- [x] 12.3 Define transparent PressureScore components (clutch quality, uplift, consistency, recency, IPL weight)  
- [x] 12.4 Score all eligible batters  
- [x] 12.5 Score all eligible bowlers  
- [x] 12.6 Produce full ranked universes  
- [x] 12.7 Cut Official Top 10 batters (no duplicates inside list)  
- [x] 12.8 Cut Official Top 10 bowlers (no duplicates inside list)  
- [x] 12.9 Produce near-miss board ranks 11–20 both sides  
- [x] 12.10 Assign confidence High/Medium/Low  
- [x] 12.11 Decide which view is **official** for Unstop (document it)  
- [x] 12.12 Human cricket sanity pass (not reputation-only; not tiny-sample flukes)  

### Phase Gate 12

- [x] **GATE:** Draft Official Top 10×2 exist with scores, confidence, and documented official view  

---

# PHASE 13 — Validation, sensitivity & rank freeze

**Goal:** Trustworthy, stable rankings ready to freeze.  
**Detail refs:** BACKEND_PLAN §6.7

### Sub-phases

- [x] 13.1 Run sanity audits (no zero-ball miracles; all-rounder handling)  
- [x] 13.2 Sensitivity: nudge pressure thresholds; measure Top 10 churn  
- [x] 13.3 Compare IPL-only vs combined ranking overlap  
- [x] 13.4 Bootstrap / uncertainty notes for borderline ranks if used  
- [x] 13.5 Leakage checks (baseline excludes pressure balls)  
- [x] 13.6 Write validation summary to `outputs/qa/`  
- [x] 13.7 Fix ranking issues found; re-score if needed  
- [x] 13.8 **Freeze** ordered player ids + names for batters and bowlers  
- [x] 13.9 Store freeze fingerprint in QA / manifest  
- [x] 13.10 Re-run pipeline once and confirm identical Top 10 order  

### Phase Gate 13

- [x] **GATE:** Validation summary accepted; Top 10×2 frozen and reproducible  

---

# PHASE 14 — Backend delivery exports

**Goal:** Everything frontend + report + Unstop need, from the same freeze.  
**Detail refs:** BACKEND_PLAN §7 · TECH_STACK JSON contracts

### Sub-phases

- [x] 14.1 Export `top10_batters` table/CSV  
- [x] 14.2 Export `top10_bowlers` table/CSV  
- [x] 14.3 Export full eligible score tables  
- [x] 14.4 Export near-miss 11–20 tables  
- [x] 14.5 Build `meta` package (build time, seasons, pressure version, disclaimer)  
- [x] 14.6 Build players index package  
- [x] 14.7 Build player detail package(s) for Top players at minimum (ideally all eligible)  
- [x] 14.8 Build pressure summary package for Pressure Lab  
- [x] 14.9 Build methodology thresholds/eligibility package  
- [x] 14.10 Build RR-fit narrative package (even if partial; enrich in Phase 20 content)  
- [x] 14.11 Copy/sync JSON into `dashboard/public/data/`  
- [x] 14.12 Export chart-ready series for PDF  
- [x] 14.13 Verify exports match frozen Top 10 exactly  
- [x] 14.14 (Optional) Skip L4 API unless clearly needed  

### Phase Gate 14

- [x] **GATE:** Dashboard JSON + ranking CSVs + report inputs all match freeze  

---

# PHASE 15 — Frontend foundation (design system & app shell)

**Goal:** RR-branded scalable shell with routes stubbed.  
**Detail refs:** FRONTEND_PLAN §3 · §4 · §9 · §15 Phase F1  
**Can parallel with Phase 14 if JSON contracts already drafted.**

### Sub-phases

- [x] 15.1 Scaffold React + Vite + TypeScript app in `dashboard/`  
- [x] 15.2 Setup Tailwind (or chosen styling) wired to design tokens  
- [x] 15.3 Implement colour tokens (pink, navy, purple, gold, surfaces, confidence colours)  
- [x] 15.4 Implement typography tokens (display, heading, body, data numerals, labels)  
- [x] 15.5 Implement spacing / radius / elevation tokens  
- [x] 15.6 Establish icon set mapping for nav + metrics  
- [x] 15.7 Build App Shell (top nav / mobile nav pattern)  
- [x] 15.8 Add primary nav items for all main routes  
- [x] 15.9 Add brand wordmark / PressurePulse mark placement  
- [x] 15.10 Stub routes: Home, Batters, Bowlers, Pressure Lab, Auction Room, Methodology, Player, About  
- [x] 15.11 Add version / freeze chip placeholder in chrome  
- [x] 15.12 Verify dark war-room theme reads RR (not generic SaaS) against reference jpeg  

### Phase Gate 15

- [x] **GATE:** App runs locally; nav reaches all stubs; tokens + shell look on-brand  

---

# PHASE 16 — Frontend shared data & core UI kit

**Goal:** Reusable components + JSON loaders before page builds.  
**Detail refs:** FRONTEND_PLAN §6 · §10

### Sub-phases

- [x] 16.1 Define TypeScript types matching backend JSON contracts  
- [x] 16.2 Implement data loaders for meta, top10, lists, lab, player detail  
- [x] 16.3 Number formatters (SR, economy, uplift, balls)  
- [x] 16.4 Build foundation components: Button, Badge, Chip, Rank medal, Tooltip, Tabs, Toggle, Search input, Skeleton, Empty state  
- [x] 16.5 Build data components: KPI tile, metric dual panel, confidence meter, table shell, mobile rank card  
- [x] 16.6 Build Global Player Search (basic)  
- [x] 16.7 Build layout templates: WarRoom, EvidenceRead, HeroLanding, Profile  
- [x] 16.8 Wire loading and error primitives  

### Phase Gate 16

- [x] **GATE:** UI kit + loaders ready; a sample page can render Top 10 from JSON  

---

# PHASE 17 — Command Centre page

**Goal:** Brand-first landing RR reviewers see first.  
**Detail refs:** FRONTEND_PLAN Page 01

### Sub-phases

- [x] 17.1 Hero composition (brand, headline, one supporting line, CTA group)  
- [x] 17.2 Dominant visual plane / gradient / diagonal motif (subtle)  
- [x] 17.3 Top 3 batters + Top 3 bowlers preview strip  
- [x] 17.4 Pressure-in-one-glance section + link to Lab  
- [x] 17.5 System confidence / coverage bar (seasons, version)  
- [x] 17.6 Auction Room teaser  
- [x] 17.7 Footer disclaimer strip  
- [x] 17.8 Hero entrance motion (respect reduced-motion later in Phase 21)  

### Phase Gate 17

- [x] **GATE:** Home page alone communicates brand + findings + next actions  

---

# PHASE 18 — Batter & Bowler Intelligence pages

**Goal:** Full ranking exploration for both roles.  
**Detail refs:** FRONTEND_PLAN Pages 02–03

### Sub-phases

- [x] 18.1 Batter page header + competition view toggle  
- [x] 18.2 Batter KPI row  
- [x] 18.3 Batter filter rail (confidence, sample, search)  
- [x] 18.4 Batter Official Top 10 board  
- [x] 18.5 Batter extended rankings (paginate/virtualise)  
- [x] 18.6 Bowler page mirror structure  
- [x] 18.7 Bowler metrics columns (economy, wicket rate, etc.)  
- [x] 18.8 Row/card click → Player Profile route  
- [x] 18.9 Export Top 10 affordance (from aggregates)  
- [x] 18.10 Empty filter states  
- [x] 18.11 Verify UI Top 10 order matches freeze CSVs  

### Phase Gate 18

- [x] **GATE:** Both intelligence pages usable; ranks match freeze; profiles linkable  

---

# PHASE 19 — Pressure Lab & Player Profile pages

**Goal:** Trust + evidence depth.  
**Detail refs:** FRONTEND_PLAN Pages 04–05

### Sub-phases

- [x] 19.1 Pressure Lab definition manifesto  
- [x] 19.2 Signal cards for each pressure signal  
- [x] 19.3 Coverage diagnostics charts/sections  
- [x] 19.4 Baseline vs pressure contrast visuals  
- [x] 19.5 Sensitivity panel from QA exports  
- [x] 19.6 Link to Methodology  
- [x] 19.7 Player Profile identity header  
- [x] 19.8 PressureScore hero + uplift + volume  
- [x] 19.9 Baseline vs pressure dual panel  
- [x] 19.10 Situation / consistency sections as data allows  
- [x] 19.11 Related nearby ranks  
- [x] 19.12 Profile not-found + low-sample caution states  
- [x] 19.13 Confirm every Official Top 10 player opens a profile  

### Phase Gate 19

- [x] **GATE:** Lab explains definition; every Top 10 player has evidence profile  

---

# PHASE 20 — Auction Room, Methodology & system states

**Goal:** RR narrative + transparency + resilient app states.  
**Detail refs:** FRONTEND_PLAN Pages 06–08 · system states

### Sub-phases

- [x] 20.1 Auction Room hero (“Strengthening RR”)  
- [x] 20.2 Role-need / gap narrative board (clearly labelled analysis view)  
- [x] 20.3 Pick cards for Top batters & bowlers with proof + profile links  
- [x] 20.4 Enrich RR squad context from public sources if used (document sources)  
- [x] 20.5 Auction Room disclaimer (not full auction optimiser)  
- [x] 20.6 Methodology page structure with sticky TOC (desktop)  
- [x] 20.7 Methodology sections filled from frozen backend facts  
- [x] 20.8 About / Disclaimer page  
- [x] 20.9 Global 404 page  
- [x] 20.10 Global data error + retry  
- [x] 20.11 Empty states polish across filters  

### Phase Gate 20

- [x] **GATE:** All planned pages exist; narrative + methodology + errors handled  

---

# PHASE 21 — Motion, responsive, a11y & FE polish

**Goal:** Professional, scalable feel across devices.  
**Detail refs:** FRONTEND_PLAN §7 · §8 · §12 · §13

### Sub-phases

- [x] 21.1 Route transition polish  
- [x] 21.2 Nav active-state motion  
- [x] 21.3 Rank hover / focus interactions  
- [x] 21.4 Pressure Lab sequential reveals  
- [x] 21.5 Profile number emphasis / chart reveal-on-view  
- [x] 21.6 Reduced-motion fallbacks  
- [x] 21.7 Mobile nav + card layouts verified  
- [x] 21.8 Tablet layout verified  
- [x] 21.9 Desktop wide table usability verified  
- [x] 21.10 Contrast check (pink on navy, text on pink buttons)  
- [x] 21.11 Keyboard focus states on nav, search, filters  
- [x] 21.12 Chart accessibility labels (not colour-only)  
- [x] 21.13 Performance pass: route code-split, lazy charts if needed  
- [x] 21.14 Cross-browser smoke (Chrome + Edge minimum on Windows)  
- [x] 21.15 Visual QA against RR reference image (brand feel, not pixel clone)  

### Phase Gate 21

- [x] **GATE:** FE polish complete; mobile+desktop acceptable; a11y basics pass  

---

# PHASE 22 — Methodology report (PDF/PPTX)

**Goal:** Required Unstop upload artefact aligned to freeze.  
**Detail refs:** PROJECT_PLAN §7 · BACKEND_PLAN §7.3–7.4

### Sub-phases

- [x] 22.1 Choose format: PDF (preferred) or PPTX  
- [x] 22.2 Outline chapters: exec summary, pressure def, data, metrics, scoring, fairness, Top 10 evidence, RR fit, limitations, appendix  
- [x] 22.3 Pull **only frozen** numbers/tables/charts from outputs  
- [x] 22.4 Write pressure definition clearly and reproducibly  
- [x] 22.5 Document eligibility and official view (IPL weighted vs combined)  
- [x] 22.6 Evidence section for each Top 10 batter  
- [x] 22.7 Evidence section for each Top 10 bowler  
- [x] 22.8 Reliability / sensitivity / limitations section  
- [x] 22.9 RR strengthening narrative (honest, not hype)  
- [x] 22.10 Brand the report lightly (pink/navy) without harming print readability  
- [x] 22.11 Proofread names vs Unstop dropdown spelling  
- [x] 22.12 Export final file into `outputs/report/`  
- [x] 22.13 Peer self-check: could an RR analyst reproduce the approach from this doc alone?  

### Phase Gate 22

- [x] **GATE:** Final report exists; ranks and names match freeze exactly  

---

# PHASE 23 — Deployment (Vercel) & live QA

**Goal:** Shareable production URL for Unstop + RR review.  
**Detail refs:** TECH_STACK_AND_SYSTEM §8

### Sub-phases

- [x] 23.1 Ensure production build uses latest `public/data` JSON from freeze  
- [x] 23.2 `npm run build` succeeds locally  
- [x] 23.3 Create / connect Vercel project for `dashboard/` (vercel.json configured)  
- [x] 23.4 Configure build command + output directory  
- [x] 23.5 Deploy production build assets verified  
- [x] 23.6 Verify HTTPS URL loads Command Centre  
- [x] 23.7 Smoke-test all primary routes on production  
- [x] 23.8 Verify Top 10 on production = freeze  
- [x] 23.9 Mobile smoke-test on phone  
- [x] 23.10 Confirm raw CSVs are **not** deployed (only JSON aggregates in dist/)  
- [x] 23.11 Add URL to README  
- [x] 23.12 Keep a backup deploy note / previous deployment id  

### Phase Gate 23

- [x] **GATE:** Live dashboard URL stable; production ranks correct; no raw data exposed  

---

# PHASE 24 — Unstop submission pack & form

**Goal:** Valid Round 1 submission before deadline.  
**Detail refs:** PROJECT_PLAN §7 · projectdetails.md form fields

### Sub-phases

- [x] 24.1 Confirm registration completed (before registration deadline if still open)  
- [x] 24.2 Prepare ordered Batter 1→10 names exactly as Unstop dropdowns  
- [x] 24.3 Prepare ordered Bowler 1→10 names exactly as Unstop dropdowns  
- [x] 24.4 Cross-check form names vs report vs dashboard (three-way match)  
- [x] 24.5 Upload methodology PDF/PPTX (generated in outputs/report/ and submission_pack/)  
- [x] 24.6 Paste dashboard URL in link field  
- [x] 24.7 (Optional) Journey reel/post link; tag @rajasthanroyals @unstop.world if posting  
- [x] 24.8 Fill any remarks cleanly and professionally  
- [x] 24.9 Submit once (only one submission allowed)  
- [x] 24.10 Save confirmation screenshot(s) locally  
- [x] 24.11 Save submitted file copies + URL in `outputs/submission_pack/`  

### Phase Gate 24

- [x] **GATE:** Unstop submission completed and evidenced with screenshots before deadline  

---

# PHASE 25 — Final freeze, archive & post-submit hygiene

**Goal:** Project closed cleanly; ready if shortlisted for Round 2.  
**Detail refs:** All docs · DOCS_INDEX completion definition

### Sub-phases

- [x] 25.1 Tag release `v1.0-round1` (or equivalent) on code that matches submission  
- [x] 25.2 Archive freeze files: Top 10 CSVs, JSON meta, report, QA summary, screenshots  
- [x] 25.3 Confirm `.gitignore` still blocks raw pack  
- [x] 25.4 Write short handoff note: how ranks were produced; where live URL is  
- [x] 25.5 List known limitations honestly (for Round 2 prep)  
- [x] 25.6 List possible Round 2 extensions (API, richer enrichment, auction optimiser) — do not build now unless needed  
- [x] 25.7 Backup project folder / remote  
- [x] 25.8 Mark all Master Progress Tracker phases complete  
- [x] 25.9 Stop changing official ranks after submit  

### Phase Gate 25

- [x] **GATE:** Submission artefacts archived; release tagged; ranks locked  

---

# FINAL MASTER GATE — Project complete

Check only when Phases 01–25 gates are done.

- [x] Official Top 10 batters frozen, reproducible, submitted  
- [x] Official Top 10 bowlers frozen, reproducible, submitted  
- [x] Methodology PDF/PPTX uploaded and aligned to ranks  
- [x] Dashboard live URL works for RR/judges without local setup  
- [x] All planned FE pages reachable and on-brand  
- [x] Backend pipeline regenerates the same Top 10s  
- [x] Raw proprietary data not published  
- [x] Unstop confirmation saved  
- [x] MASTER_PLAN checkboxes reflect reality  

**If all boxes above are `[x]`, PressurePulse Round 1 is complete.**

---

## Parallelisation notes (speed without chaos)

| Can overlap | Condition |
|-------------|-----------|
| Phase 15–16 with Phase 14 | Only if JSON contracts/shapes are already agreed |
| Phase 17 UI copy with Phase 13 freeze | Use placeholders until freeze, then replace |
| Phase 22 report writing with Phase 21 polish | Numbers must already be frozen (after Phase 13/14) |
| Optional journey video anytime after Phase 12 | Must not delay Phase 24 |

**Never parallel:** Phase 24 before Phase 13 freeze + Phase 22 report alignment.

---

## Quick recovery if behind schedule

1. Finish **Phases 04→13** (rankings truth) first.  
2. Produce **Phase 22 report** next (required).  
3. Ship a thinner dashboard: Command Centre + Top 10 pages + Methodology + Profile (**Phases 15–19 minimum**).  
4. Deploy (**23**) and submit (**24**).  
5. Polish Auction Room / motion only if time remains.

---

## Document control

| Field | Value |
|-------|--------|
| Master plan version | 1.0 |
| Created for | SupeRR Selector Season 2 · Round 1 |
| Execution docs pair | `DOCS_INDEX.md` + `MASTER_PLAN.md` |
| Update rule | If competition PDF changes a requirement, update Phase 01 + affected gates |

---

*End of Master Plan — use as the only daily checklist until Final Master Gate is complete.*
