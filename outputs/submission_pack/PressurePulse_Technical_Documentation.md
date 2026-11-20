# PressurePulse — Technical Documentation

**Product:** PressurePulse (SupeRR Selector Season 2 · Round 1)  
**Prepared by:** Farhan Sayed · [farhanbuilds.in](https://farhanbuilds.in) · 9867868597 · farhansayed54@gmail.com  
**Board:** Auction Official (`pressure_v1.1`)  
**Freeze SHA256:** `a819c0e65bf4ee045ef17c7b19824ccbec549c4b002402e9fbf47f477a04810c`

This document explains the **data model**, **technical approach**, **parameters / metrics**, and **how outcomes were produced**.

---

## 1. System overview

PressurePulse is an end-to-end cricket analytics system for Rajasthan Royals’ IPL 2027 auction strategy. It answers:

> Who are the most reliable batters and bowlers **under match pressure**, not just by career averages?

| Layer | What it does |
|---|---|
| Data engine | Ingest RR ball-by-ball pack → validated warehouse |
| Match intelligence | Reconstruct pre-delivery state (RRR, wickets, phase) |
| Pressure engine | Tag high-leverage deliveries (`pressure_v1.1`) |
| Metrics | Player-level pressure vs baseline rates |
| Ranking | Composite PressureScore → Top 10 batters + Top 10 bowlers |
| Delivery | Dashboard JSON + methodology report from the **same freeze** |

**Entry point:** `python -m src.run_pipeline`

**Scale (frozen run):** 200,999 deliveries · 78,868 pressure (39.24%) · 883 matches · ~1,217 players

---

## 2. Tech stack

| Concern | Choice |
|---|---|
| Language | Python 3.11+ |
| Data | pandas, numpy, pyarrow (Parquet) |
| Pipeline config | `src/foundation/config.py` |
| Frontend | React 19 + Vite + TypeScript + Tailwind 4 |
| Charts | Recharts |
| Report | ReportLab PDF / Markdown |
| Hosting | Vercel (static dashboard from precomputed JSON) |

**Design rule:** Browser never receives raw proprietary CSVs — only aggregates / rankings JSON.

---

## 3. Data model

### 3.1 Raw inputs (`data/raw/`)

| File | Entity | Purpose |
|---|---|---|
| `competitions.csv` | Competition | Season, IPL / T20I flags |
| `teams.csv` | Team | Franchise / national sides |
| `matches.csv` | Match | Knockout stage, revised overs/target, result |
| `playing_eleven.csv` | XI | WK / captain / impact flags |
| `competition_team_player_mapping.csv` | Player mapping | Stable player IDs + names |
| `ball_by_ball.csv` | Delivery | Ball grain — striker, bowler, runs, extras, wickets |

### 3.2 Processed warehouse (`data/processed/`)

| Artifact | Grain | Producer |
|---|---|---|
| `fact_delivery.parquet` | Delivery | `src/data_platform/warehouse.py` → `build_warehouse` |
| `fact_delivery_state.parquet` | Delivery + state | `src/intelligence/state.py` → `reconstruct_match_states` |
| `fact_delivery_pressure.parquet` | Delivery + pressure | `src/intelligence/pressure.py` → `run_pressure_engine` |
| `dim_player_roles.parquet` | Player | `src/intelligence/roles.py` → `classify_player_roles` |
| `metrics_batting.parquet` | Player | `src/intelligence/metrics_batting.py` |
| `metrics_bowling.parquet` | Player | `src/intelligence/metrics_bowling.py` |

### 3.3 Core delivery-level fields

**Match state (before the ball):**

- `runs_before`, `wickets_before`, `wickets_in_hand_before`
- `crr_before`, `rrr_before` (2nd innings; clipped)
- `target`, `runs_needed_before`
- `match_phase`: powerplay (≤6) · middle (7–15) · death (≥16)
- `is_legal_ball` (excludes wides / overstep as legal-ball rate base)
- `is_knockout`, `is_ipl`, `is_t20i`, `is_super_over`

**Pressure labels:**

- `signal_chase_tightness`
- `signal_collapse_defense`
- `signal_death_contest`
- `signal_knockout_leverage`
- `is_pressure` (OR of active signals)
- `pressure_index` (0–1 continuous score for diagnostics / bands — **not** used as Top 10 rank input)

### 3.4 Player-level grain

Metrics aggregate deliveries by `striker_id` / `bowler_id`, split into:

- **Pressure** (`is_pressure == True`)
- **Baseline** (`is_pressure == False`)
- IPL vs T20I slices for weighted rates

---

## 4. Pipeline (technical approach)

```text
Raw CSVs
  → Warehouse (schema validate + joins)
  → Match-state reconstruction (pre-ball context)
  → Pressure tagging (pressure_v1.1)
  → Role classification
  → Batting / bowling metrics
  → Ranking + overlap resolve
  → Validation + freeze SHA
  → Export dashboard JSON + report inputs
```

| Stage | Module | Key functions | Outputs |
|---|---|---|---|
| 1. Ingest | `src/data_platform/warehouse.py` | `build_warehouse` | dims + `fact_delivery` |
| 2. State | `src/intelligence/state.py` | `reconstruct_match_states` | `fact_delivery_state` |
| 3. Pressure | `src/intelligence/pressure.py` | `compute_pressure_signals`, `run_pressure_engine` | `fact_delivery_pressure` |
| 4. Roles | `src/intelligence/roles.py` | `classify_player_roles` | `dim_player_roles` |
| 5. Bat metrics | `src/intelligence/metrics_batting.py` | `compute_batting_metrics` | `metrics_batting` |
| 6. Bowl metrics | `src/intelligence/metrics_bowling.py` | `compute_bowling_metrics` | `metrics_bowling` |
| 7. Rank | `src/intelligence/ranking.py` | `score_batters`, `score_bowlers`, `run_ranking_pipeline` | Top 10 / full boards |
| 8. Freeze | `src/intelligence/validation.py` | `run_validation_and_freeze` | `frozen_top10_fingerprint.json` |
| 9. Export | `src/delivery/export.py` | `export_delivery_packages` | `dashboard/public/data/*.json` |

---

## 5. Pressure definition (`pressure_v1.1`)

A delivery is **high-pressure** when **any** of these signals fire (super overs currently **excluded**):

| Signal | Rules |
|---|---|
| **Chase tightness** (2nd innings) | RRR ≥ **9.5** with ≤60 balls left; **or** RRR ≥ **11.5** anytime; **or** ≤30 balls left needing 1–55 runs |
| **Collapse / survival** | ≥3 wickets already down by over ≤8; **or** ≤3 wickets in hand with ≥12 balls left |
| **Death contest** | Overs **16–20**; in chase, also requires runs still needed (>5) |
| **Knockout leverage** | Knockout match **and** (RRR ≥ 8.5 **or** death phase **or** ≥2 wickets down) |

**Empirical mix (frozen):** ~10% powerplay · ~34% middle · ~56% death of pressure balls — so pressure is **not** “death overs only.”

---

## 6. Metrics & parameters

### 6.1 Shared rate rules

| Parameter | Value | Meaning |
|---|---|---|
| Legal balls only | Yes | SR / economy / dots / boundaries on legal balls |
| IPL rate weight | **1.30×** | IPL deliveries count more inside blended rates |
| T20I rate weight | **1.00×** | Baseline competition weight |
| Baseline | Non-pressure balls | Same player, non-pressure context |
| Confidence High | ≥90 pressure balls | UI / dossier confidence band |
| Confidence Medium | ≥45 pressure balls | UI / dossier confidence band |

### 6.2 Batting metrics

| Metric | What it captures |
|---|---|
| Pressure SR | Scoring rate under pressure (weighted) |
| Baseline SR | Scoring rate outside pressure |
| SR uplift | Pressure SR − Baseline SR |
| Boundary % | Boundary conversion under pressure |
| Dot % | Scoring interruption |
| Pressure average | Runs per dismissal under pressure |
| Consistency | Match-level SR stability under pressure (lower CV → higher score) |
| Volume | Pressure ball count |

### 6.3 Bowling metrics

| Metric | What it captures |
|---|---|
| Pressure economy | Runs per over under pressure (weighted) |
| Death economy | Economy in overs 16–20 under pressure (soft-capped if thin sample) |
| Baseline economy | Economy outside pressure |
| Economy uplift | Baseline econ − Pressure econ (positive = tighter under pressure) |
| Balls per wicket | Strike rate under pressure |
| Wicket volume | Pressure wickets |
| Dot % | Dot-ball pressure |
| Consistency | Match-level economy stability |

**Wicket credit types:** Caught, Bowled, LBW, Stumped, Hit Wicket (run-outs excluded).

**Death soft-cap:** if death sample &lt; **30** balls, death economy blends toward overall weighted pressure economy.

---

## 7. Scoring model (PressureScore)

### 7.1 Batters (0–100)

| Component | Weight | Construction |
|---|---:|---|
| Clutch quality | **40%** | 50% SR quality + 30% boundary% quality + 20% average quality |
| SR uplift | **25%** | Map uplift from about −10 → +40 into 0–100 |
| Consistency | **20%** | From match SR coefficient of variation |
| Volume | **15%** | `pressure_balls / 250` (capped) |

**SR quality map:** weighted SR ~110 → 180  
**Boundary% map:** ~12% → 28%  
**Average map:** ~15 → 45  

### 7.2 Bowlers (0–100)

| Component | Weight | Construction |
|---|---:|---|
| Restrictiveness | **35%** | 45% overall econ + 35% death econ + 20% dot% |
| Wicket threat | **30%** | 65% balls/wkt quality + 35% wicket volume |
| Economy uplift | **15%** | Improvement vs own baseline |
| Consistency | **10%** | Match economy stability |
| Volume | **10%** | `pressure_balls / 400` (capped) |

**Economy quality map:** ~11.5 → 6.0 (lower econ = higher quality)  
**Balls/wkt map:** ~24 → 11  

### 7.3 Eligibility floors

| Gate | Batters | Bowlers |
|---|---|---|
| Pressure balls | ≥ **50** | ≥ **80** |
| Baseline balls | ≥ **40** | ≥ **60** |
| Pressure matches | ≥ **5** | ≥ **5** |
| **Auction Official IPL floor** | ≥ **40** IPL pressure balls | ≥ **60** IPL pressure balls |
| Global Combined | Shared floors only | No extra IPL floor |

### 7.4 Boards

| Board | Role |
|---|---|
| **Auction Official** (primary freeze) | IPL sample floors enforced — official Unstop Top 10 |
| **Global Combined** | Same formula without IPL floor — secondary scouting view |

**Overlap rule:** if a player appears in both Top 10 lists, keep them on the list where `pressure_score` is higher.

---

## 8. Validation & freeze

| Check | Result (frozen) |
|---|---|
| Pressure ↔ baseline leakage | **0** |
| Top 10 uniqueness / cross-list overlap | Pass |
| Batter Top 10 sensitivity retention | **92.5%** |
| Bowler Top 10 sensitivity retention | **95.0%** |
| IPL-only Top 12 overlap | bat **9/10**, bowl **9/10** |

**Sensitivity variants tested:** RRR ∈ {9.0, 10.0}; death start ∈ {15, 17}.

**Freeze:** SHA256 over ordered Top 10 identities + scores →  
`a819c0e65bf4ee045ef17c7b19824ccbec549c4b002402e9fbf47f477a04810c`  
stored in `outputs/rankings/frozen_top10_fingerprint.json` and mirrored in dashboard `meta.json`.

---

## 9. How outcomes were produced (end-to-end)

1. **Ingest** the official RR data pack and validate schemas.  
2. **Rebuild** every delivery’s pre-ball context (so labels cannot leak future information).  
3. **Tag** pressure with `pressure_v1.1` multi-signal rules.  
4. **Compute** each player’s pressure vs baseline metrics with IPL/T20I rate weights.  
5. **Score** eligible players with the published weightings.  
6. **Apply** Auction Official IPL floors and resolve dual-list overlap.  
7. **Validate** leakage, uniqueness, sample floors, sensitivity.  
8. **Freeze** Top 10 batters + bowlers under the SHA above.  
9. **Export** dashboard JSON and methodology report from that freeze.

### Frozen Top 10 Batters

1. Rohit Sharma · 2. Shashank Singh · 3. Naman Dhir · 4. Dinesh Karthik · 5. Rishabh Pant  
6. Ashutosh Sharma · 7. Shreyas Iyer · 8. Rinku Singh · 9. Marcus Stoinis · 10. Suryakumar Yadav  

### Frozen Top 10 Bowlers

1. Sunil Narine · 2. Mitchell Santner · 3. Kuldeep Yadav · 4. Jasprit Bumrah · 5. Adam Zampa  
6. Rashid Khan · 7. Wanindu Hasaranga · 8. Rasikh Salam · 9. Varun Chakravarthy · 10. Matheesha Pathirana  

---

## 10. Outputs & artifacts

| Artifact | Location |
|---|---|
| Frozen fingerprint | `outputs/rankings/frozen_top10_fingerprint.json` |
| Top 10 / full rankings | `outputs/rankings/*.csv` |
| QA summaries | `outputs/qa/` |
| Dashboard data | `dashboard/public/data/*.json` |
| Submission report (MD) | `PressurePulse_Round1_Submission.md` |
| Methodology PDF | `PressurePulse_Round1_Submission.pdf` / `outputs/submission_pack/` |

**Dashboard pages:** Command Centre · Batter / Bowler Intelligence · Pressure Lab · Player dossiers · Auction Room · Methodology · Audit.

---

## 11. Architecture diagram

```text
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ RR Data Pack │ →  │  Warehouse +    │ →  │ Pressure Engine  │
│ (6 CSVs)     │    │  Match State    │    │  pressure_v1.1   │
└──────────────┘    └─────────────────┘    └────────┬─────────┘
                                                    ↓
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ Dashboard /  │ ←  │ Freeze + Export │ ←  │ Metrics + Score  │
│ Report / MD  │    │ SHA fingerprint │    │ Auction Official │
└──────────────┘    └─────────────────┘    └──────────────────┘
```

---

## 12. Limits (stated)

- Auction Official prioritises IPL sample — some T20I-only standouts appear only on Global Combined.  
- Continuous `pressure_index` is diagnostic; ranking uses binary pressure membership + rate models.  
- Scores measure **pressure reliability**, not retention status, auction price, or franchise fitness alone.  
- No black-box ML in the official freeze — interpretable weighted formulas only.

---

## 13. Key source files

| Area | Path |
|---|---|
| Config / thresholds | `src/foundation/config.py` |
| Warehouse | `src/data_platform/warehouse.py` |
| Match state | `src/intelligence/state.py` |
| Pressure | `src/intelligence/pressure.py` |
| Bat / bowl metrics | `src/intelligence/metrics_batting.py`, `metrics_bowling.py` |
| Ranking | `src/intelligence/ranking.py` |
| Validation / freeze | `src/intelligence/validation.py` |
| Export | `src/delivery/export.py` |
| Orchestrator | `src/run_pipeline.py` |
| Stack plan | `docs/TECH_STACK_AND_SYSTEM.md` |

---

*PressurePulse · Technical documentation · Auction Official freeze · SupeRR Selector Season 2*
