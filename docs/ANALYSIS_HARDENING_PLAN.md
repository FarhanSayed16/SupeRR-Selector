# PressurePulse — Analysis Hardening & Enhancement Plan

**Status:** Audit complete · Plan locked for execution  
**Audit date:** 18 Nov 2026  
**Freeze under review:** `5cdd7b7451b5a667…` (`pressure_v1`)  
**E2E suite:** `scripts/test_system_end_to_end.py` → **ALL 8 TESTS PASSED**

This plan replaces the interrupted analysis agent turn. It separates **what is already correct**, **what is wrong or soft**, and **exactly what to harden** so rankings, methodology, UI copy, and submission artefacts stay consistent.

---

## 0. Executive verdict

| Layer | Verdict |
|-------|---------|
| Warehouse / row counts | **Correct** — 200,999 balls, 883 matches, 1,217 players |
| Pressure labelling | **Correct enough** — 39.26% pressure; 43.7% outside death |
| Freeze integrity | **Correct** — CSV ↔ JSON ↔ SHA match |
| Composite PressureScore | **Transparent but imperfect** — works; not auction-optimal |
| Methodology claims vs code | **Broken in places** — docs/UI say things code does not do |
| Sensitivity / stability claims | **Not real** — hardcoded 90% / 80% numbers |

**Bottom line:** The system is competition-ready as a deterministic, auditable v1. It is **not** yet the “best model.” Do not re-freeze casually; harden in phases below, then re-run pipeline + re-freeze + re-export.

---

## 1. Re-audit evidence (fresh run)

### 1.1 Integrity that PASSED
1. Parquet warehouse schema & counts  
2. Pressure distribution band (38–41%) and outside-death (>40%)  
3. Top 10 batters/bowlers unique + zero cross-list overlap  
4. Cryptographic freeze fingerprint matches recomputed SHA  
5. Dashboard `public/data` JSON packages present & non-empty  
6. Methodology + dossier PDFs valid  
7. Submission pack staged  
8. Frontend production build present  

### 1.2 CSV ↔ UI lock
Official Top 10 batters and bowlers in `outputs/rankings/*.csv` **exactly match** `dashboard/public/data/top10_*.json`.

### 1.3 Auction-domain reality check (IPL share of pressure balls)

**Batters — mostly IPL-healthy**

| Rank | Player | IPL share |
|:---:|--------|:---------:|
| 1 | Rohit Sharma | 67% |
| 2 | Shashank Singh | 100% |
| 3 | Naman Dhir | 73% |
| 4 | Ashutosh Sharma | 98% |
| … | … | mostly ≥64% |

**Bowlers — three pure-T20I names in Top 4**

| Rank | Player | IPL share | Risk |
|:---:|--------|:---------:|------|
| 1 | Sunil Narine | 100% | OK |
| 2 | **Mohammad Nawaz** | **0%** | Auction-weak |
| 3 | **Sufiyan Muqeem** | **0%** | Auction-weak |
| 4 | **Abrar Ahmed** | **0%** | Auction-weak |
| 5+ | Kuldeep / Bumrah / Rasikh / … | 59–83% | OK / mixed |

This is the strongest product/analytic mismatch: UI sells “IPL 2027 Auction War Room” while ranks 2–4 bowling are **0% IPL sample**.

---

## 2. Confirmed defects (root causes)

### P0 — Must fix before claiming “best analysis”
| ID | Defect | Where | Why it matters |
|----|--------|-------|----------------|
| P0.1 | `CONFIG.IPL_WEIGHT = 1.30` **never applied** in scoring | `config.py` vs `ranking.py` | UI KPI + Methodology page claim **1.30x**; real boost is max **+15%** via `1 + ipl_ratio×0.15` |
| P0.2 | Sensitivity / IPL-overlap stats are **hardcoded** | `validation.py` lines ~57–63, report text | False scientific confidence in freeze report |
| P0.3 | Pure-T20I bowlers can outrank IPL death specialists | ranking formula + no IPL floor | Auction war-room narrative fails scrutiny |
| P0.4 | Batting “balls” count **wides / Overstep** as balls faced | `metrics_batting.py` `count` on all rows | ~5% of pressure rows; softens SR / inflates volume |

### P1 — Correctness / consistency
| ID | Defect | Where | Why it matters |
|----|--------|-------|----------------|
| P1.1 | Eligibility thresholds diverge | `CONFIG` min 30 vs `ranking.py` bat 50 / bowl 80 | Methodology JSON exports 30; ranking uses stricter gates |
| P1.2 | `KNOCKOUT_MULTIPLIER` unused | `config.py` / `manifest.py` | Dead config; pretend weight |
| P1.3 | `INCLUDE_SUPER_OVERS=False` but super-over signal still labels pressure | `pressure.py` + config comment | Policy unclear |
| P1.4 | Ranking QA text still says “1.30x” | `ranking.py` summary writer | Lies in QA artefact |
| P1.5 | UI “Auction Domain Weight 1.30x” | `CommandCentre.tsx` | Mirrors false claim |

### P2 — Model quality (enhancement, not crash bugs)
| ID | Soft spot | Upgrade |
|----|-----------|---------|
| P2.1 | No recency decay | Weight last 1–2 seasons higher for auction form |
| P2.2 | No opponent / venue adjustment | Optional SMS Jaipur / right-arm pace slice later |
| P2.3 | Consistency via SR CV is crude | Winsorize; require min matches before CV |
| P2.4 | Death economy imputed / thin samples | Cap death weight when `death_pressure_balls` low |
| P2.5 | No official **IPL-only** board | Add parallel freeze view for auction |

---

## 3. Target architecture after hardening

```text
fact_delivery
    → state (RRR, wickets, phase, legal ball)
    → pressure_v2 signals (same family, cleaned policy)
    → metrics (LEGAL balls for bat; weighted IPL/T20I samples)
    → score (single CONFIG-driven weights + IPL floor)
    → validate (REAL sensitivity loops)
    → freeze_v2 SHA
    → export JSON + PDF + UI
```

**Official ranking policy (proposed lock):**
1. **Primary board (Auction Official):** IPL-weighted combined sample with **minimum IPL pressure balls** (bat ≥ 40, bowl ≥ 60) OR pure-IPL board as official.  
2. **Secondary board (Global Context):** Combined IPL+T20I without IPL floor (current-style) for methodology appendix.  
3. UI default = **Auction Official**. Global board behind toggle.

---

## 4. Implementation phases (do in order)

### Phase A — Truth alignment (no rank philosophy change yet)
**Goal:** Code, CONFIG, methodology JSON, UI, QA text say the same thing.

- [ ] A1. Decide: either **implement real 1.30/1.00 sample weighting** OR **downgrade all claims to “up to +15% IPL exposure boost”**  
- [ ] A2. Prefer A1 option **implement real weights** (see Phase B)  
- [ ] A3. Until B ships: patch UI KPI + Methodology page + `ranking.py` QA string so nothing claims unused `1.30x`  
- [ ] A4. Export `methodology.json` eligibility mins from the **same constants** `ranking.py` uses  
- [ ] A5. Document unused flags or delete them (`KNOCKOUT_MULTIPLIER`)

**Gate A:** Grep for `1.30` / `1.15` / eligibility numbers returns only consistent values.

### Phase B — Metric & score correctness (`pressure_v1.1` or `v2`)
**Goal:** Fix measurement bugs that change scores for the right reasons.

- [ ] B1. Batting aggregates: count **legal balls only** (`is_legal_ball`) for balls / SR / dot% / boundary%  
- [ ] B2. Drive eligibility **only** from `CONFIG` (pick one set: recommend bat pressure ≥50, bowl ≥80, matches ≥5; update CONFIG)  
- [ ] B3. Replace `ipl_multiplier = 1 + ratio×0.15` with **delivery-level or player-level weighted rates**:  
  - Weighted pressure SR / economy using `IPL_WEIGHT=1.30`, `T20I_WEIGHT=1.00`  
  - Or: score on IPL metrics × 1.0 + T20I metrics × (1/1.3) blend — pick one formula and freeze it in CONFIG  
- [ ] B4. Add **IPL sample floor** for Auction Official board (exclude 0% IPL bowlers from official Top 10)  
- [ ] B5. Soft-cap death-economy component when death balls < N (e.g. 30)  
- [ ] B6. Clarify super-over policy: include in clutch subset flag only, or in main `is_pressure` — match `INCLUDE_SUPER_OVERS`

**Gate B:** Unit asserts on 2–3 known players (legal-ball SR changes; Nawaz cannot be Auction Official #2 with 0 IPL balls).

### Phase C — Real validation (replace fake sensitivity)
**Goal:** Freeze report becomes scientific.

- [ ] C1. Implement sensitivity runner: re-label pressure at RRR ∈ {9.0, 9.5, 10.0} and death start ∈ {15,16,17}  
- [ ] C2. Re-score Top 10; compute **actual** retention %  
- [ ] C3. Build IPL-only Top 12; compute real overlap with official Top 10  
- [ ] C4. Write results into `validation_summary.md` / fingerprint JSON (no hardcoded 90/80)  
- [ ] C5. Extend `test_system_end_to_end.py` to assert sensitivity block is computed (key present, not equal to placeholder constants unless computed equal)

**Gate C:** Re-running validation twice yields identical retention numbers (deterministic).

### Phase D — Re-freeze & re-export
**Goal:** One coherent artefact set.

- [ ] D1. `python -m src.run_pipeline` (full)  
- [ ] D2. New freeze SHA → `frozen_top10_fingerprint.json` + `meta.json`  
- [ ] D3. Regenerate methodology PDF + scouting dossier  
- [ ] D4. Sync `dashboard/public/data/*`  
- [ ] D5. Update CommandCentre / Methodology / Audit copy for new policy + SHA  
- [ ] D6. Run e2e + manual Top 10 eyeball for auction narrative  
- [ ] D7. Tag release `pressure_v1.1` (or `v2`) in CONFIG + docs

**Gate D:** E2E green; UI Top 10 = CSV = PDF; methodology claims match CONFIG.

### Phase E — Product enhancements (after analytic truth)
**Goal:** Better war-room UX on top of corrected ranks.

- [ ] E1. Toggle: **Auction Official** vs **Global Combined** boards  
- [ ] E2. Show IPL% chip on every player row / dossier  
- [ ] E3. Near-miss board with “excluded: 0% IPL” explanations  
- [ ] E4. Pressure Lab: signal contribution chart from real diagnostics  
- [ ] E5. Recency-weighted “Form under pressure (last 2 seasons)” strip  
- [ ] E6. Continue UI polish already in flight (avatars, field map, logo) — separate from rank science

---

## 5. Recommended scoring lock (concrete proposal)

### 5.1 Auction Official — Batters
Eligibility: `pressure_legal_balls ≥ 50`, `baseline_legal_balls ≥ 40`, `pressure_matches ≥ 5`, **`ipl_pressure_legal_balls ≥ 40`**

Score (0–100 then scale):
```
quality   = 0.50*SR_q + 0.30*boundary_q + 0.20*avg_q     # from IPL-weighted pressure rates
uplift    = clip(weighted_SR - weighted_baseline_SR)
consistency = existing CV score (min 5 pressure matches)
volume    = clip(pressure_legal_balls / 250)
score     = 0.40*quality + 0.25*uplift + 0.20*consistency + 0.15*volume
```
No separate mysterious multiplier if weights already baked into rates.

### 5.2 Auction Official — Bowlers
Eligibility: `pressure_legal_balls ≥ 80`, `baseline ≥ 60`, `matches ≥ 5`, **`ipl_pressure_legal_balls ≥ 60`**

Score:
```
restrict = 0.45*econ_q + 0.35*death_econ_q(+cap) + 0.20*dot_q
threat   = 0.65*bpw_q + 0.35*wkt_vol_q
uplift   = baseline resistance on weighted economies
score    = 0.35*restrict + 0.30*threat + 0.15*uplift + 0.10*consistency + 0.10*volume
```

### 5.3 What happens to Nawaz / Muqeem / Abrar?
They move to **Global Combined** board / near-miss appendix — still visible, not Auction Official Top 10 unless they clear IPL floor.

---

## 6. File touch list (when executing)

| Area | Files |
|------|-------|
| Config | `src/foundation/config.py` |
| Pressure | `src/intelligence/pressure.py` |
| Metrics | `src/intelligence/metrics_batting.py`, `metrics_bowling.py` |
| Ranking | `src/intelligence/ranking.py` |
| Validation | `src/intelligence/validation.py` |
| Export | `src/delivery/export.py` |
| Tests | `scripts/test_system_end_to_end.py` (+ new `scripts/test_ranking_sensitivity.py`) |
| UI copy | `CommandCentre.tsx`, `Methodology.tsx`, `About.tsx` |
| Docs | this file, `MASTER_PLAN.md` addendum, `methodology` PDF regen |
| Data out | `outputs/**`, `dashboard/public/data/**` |

---

## 7. Out of scope (do not sneak in)

- ML black-box rankers without explainability  
- Scraping live odds / auction prices as features  
- Changing Unstop required deliverable shape (still Top 10 + methodology)  
- Pixel redesign unrelated to analytic truth (track under UI plan)

---

## 8. Execution priority for next coding session

1. **Phase A3** quick honesty patch (same day, low risk) **or** jump straight to **B3+B4** if ranks may change before submit  
2. **Phase B** full metric/score fix  
3. **Phase C** real sensitivity  
4. **Phase D** re-freeze + regenerate artefacts  
5. **Phase E** UI toggles / IPL% chips  

**Decision needed from you before coding B/D:**  
Should **Auction Official** exclude 0% IPL players (recommended), or keep current combined Top 10 and only fix labelling/weight math?

---

## 9. Success criteria

- [ ] No document/UI string claims a weight the code does not apply  
- [ ] Batting SR uses legal balls only  
- [ ] Auction Official Top 10 has zero 0%-IPL players  
- [ ] Sensitivity % computed, not hardcoded  
- [ ] New freeze SHA; e2e green; PDF + JSON + UI identical  
- [ ] Methodology page explains Official vs Global boards in one paragraph

---

## 10. Audit log

| When | What | Result |
|------|------|--------|
| 18 Nov 2026 | Re-ran `scripts/test_system_end_to_end.py` | 8/8 PASS |
| 18 Nov 2026 | CSV↔JSON name lock | PASS |
| 18 Nov 2026 | IPL share scan on frozen Top 10 | 3 bowlers at 0% IPL |
| 18 Nov 2026 | Code review: ranking/validation/config/metrics | P0–P2 defects listed above |
