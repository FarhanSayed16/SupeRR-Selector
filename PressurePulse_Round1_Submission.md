# PRESSUREPULSE
## Rajasthan Royals Auction Intelligence — IPL 2027

**Prepared by:** Farhan Sayed  
**Portfolio:** [farhanbuilds.in](https://farhanbuilds.in)  
**Phone:** 9867868597  
**Email:** farhansayed54@gmail.com

**SupeRR Selector Season 2 · Round 1** — Most reliable players under pressure

| Field | Value |
|---|---|
| Dataset | IPL & T20I, 2022–2026 |
| Deliveries | 200,999 (pressure: 78,868 · 39.24%) |
| Board | **Auction Official** (`pressure_v1.1`) |
| Freeze SHA256 | `a819c0e65bf4ee045ef17c7b19824ccbec549c4b002402e9fbf47f477a04810c` |
| Status | FROZEN_OFFICIAL |

---

## 1. What we solved

Rajasthan Royals needs auction targets who **raise their game when the match is on the line** — not career averages alone. PressurePulse rebuilds pre-delivery match state, tags high-leverage balls, scores each player against their own non-pressure baseline, and freezes a reproducible **Top 10 batters + Top 10 bowlers** list for IPL 2027.

---

## 2. Official Top 10 Batters

| Rank | Player | Role | Pressure balls | Pressure SR | Baseline SR | SR uplift | Score |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | Rohit Sharma | Batter | 208 | 193.8 | 136.3 | +56.8 | 91.9 |
| 2 | Shashank Singh | Batting All-Rounder | 415 | 180.5 | 107.6 | +72.9 | 91.1 |
| 3 | Naman Dhir | Batting All-Rounder | 285 | 189.8 | 148.8 | +44.8 | 90.3 |
| 4 | Dinesh Karthik | Wicketkeeper-Batter | 538 | 182.2 | 81.8 | +100.9 | 90.0 |
| 5 | Rishabh Pant | Wicketkeeper-Batter | 472 | 175.8 | 123.0 | +53.2 | 89.6 |
| 6 | Ashutosh Sharma | Batter | 293 | 179.9 | 86.0 | +93.1 | 89.5 |
| 7 | Shreyas Iyer | Batter | 649 | 179.5 | 139.4 | +41.9 | 87.9 |
| 8 | Rinku Singh | Batter | 845 | 171.2 | 116.9 | +54.0 | 87.5 |
| 9 | Marcus Stoinis | Batting All-Rounder | 713 | 170.3 | 131.3 | +40.8 | 86.3 |
| 10 | Suryakumar Yadav | Batter | 992 | 183.9 | 156.9 | +26.1 | 86.0 |

---

## 3. Official Top 10 Bowlers

| Rank | Player | Role | Pressure balls | Pressure econ | Death econ | Wickets | Score |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | Sunil Narine | Bowling All-Rounder | 551 | 6.49 | 6.06 | 33 | 79.6 |
| 2 | Mitchell Santner | Bowling All-Rounder | 563 | 6.91 | 9.51 | 40 | 76.8 |
| 3 | Kuldeep Yadav | Bowling All-Rounder | 714 | 7.67 | 8.45 | 51 | 74.9 |
| 4 | Jasprit Bumrah | Bowler | 780 | 7.49 | 7.41 | 53 | 74.2 |
| 5 | Adam Zampa | Bowling All-Rounder | 496 | 8.42 | 8.79 | 45 | 73.6 |
| 6 | Rashid Khan | Bowling All-Rounder | 1165 | 7.71 | 8.36 | 96 | 72.6 |
| 7 | Wanindu Hasaranga | Bowling All-Rounder | 734 | 8.31 | 8.31 | 59 | 72.0 |
| 8 | Rasikh Salam | Bowling All-Rounder | 319 | 9.10 | 9.65 | 30 | 70.1 |
| 9 | Varun Chakravarthy | Bowling All-Rounder | 877 | 8.37 | 8.56 | 66 | 69.9 |
| 10 | Matheesha Pathirana | Bowler | 726 | 9.14 | 9.29 | 61 | 68.3 |

---

## 4. Pressure definition

A delivery is **high-pressure** when pre-ball context demands high-leverage execution:

- steep chase (**RRR ≥ 9.5**)
- death overs (**16–20**)
- collapse (**≤ 3 wickets in hand**)
- knockout / playoff stages

Of **200,999** deliveries, **78,868 (39.24%)** are pressure. A material share sits **outside death** (powerplay ~10%, middle ~34%) — collapse defence and rising RRR, not slog overs alone.

---

## 5. Scoring & fairness

**Batters (0–100):** 40% clutch quality + 25% SR uplift vs own baseline + 20% consistency + 15% volume

**Bowlers (0–100):** 35% restrictiveness (economy + death soft-cap) + 30% wicket threat + 15% economy uplift + 10% consistency + 10% volume

**Rates:** legal balls only; IPL **1.30×**, T20I **1.00×**

**Eligibility:** batters ≥50 / ≥40 / ≥5 matches / ≥40 IPL pressure balls; bowlers ≥80 / ≥60 / ≥5 / ≥60 IPL. Zero batter–bowler cross-list overlap.

---

## 6. Validation & reproducibility

| Check | Result |
|---|---|
| Pressure ↔ baseline leakage | **0** |
| Batter Top 10 sensitivity retention | **92.5%** |
| Bowler Top 10 sensitivity retention | **95.0%** |
| IPL-only Top 12 overlap | bat **9/10**, bowl **9/10** |

Regen: `python -m src.run_pipeline` → SHA `a819c0e65bf4ee045ef17c7b19824ccbec549c4b002402e9fbf47f477a04810c`

---

## 7. How these picks strengthen RR

Retained core (Jaiswal, Samson, Parag, Jurel, Hetmyer, Sandeep) covers top order and death seam. Gaps: lower-order finishing, death/middle restrict at SMS, and impact cover. Season 1 pattern (Vignesh Puthur): prefer high-leverage value over brand inflation.

- **Shashank / Ashutosh / Rinku / DK / Pant** — finishers & keepers who lift SR under pressure (Shashank +73; Ashutosh +93); solve chase volatility after top-order fails.
- **Rohit / Iyer / SKY / Stoinis / Naman** — high-floor middle, experience, and float roles for Jaipur chases.
- **Narine / Santner / Kuldeep / Rashid / Hasaranga / Varun** — spin choke for SMS square boundaries (Narine death econ **6.06**).
- **Bumrah / Pathirana / Rasikh / Zampa** — death seam and wrist-spin strike; Rasikh is the domestic death-seam value pick.

**Projected XI:** Jaiswal, Rohit*, Samson (C/WK), Parag, Hetmyer, Shashank*, Jurel, Narine*, Sandeep, Rasikh*, Kuldeep* · **Impact:** Ashutosh* · (* scouted from this board)

---

## 8. Limits

Auction Official privileges IPL sample floors — some T20I-only standouts remain on Global Combined only. These rankings measure **pressure reliability**, not retention status or purse maths.

---

*PressurePulse · SupeRR Selector Season 2 · Round 1 · Auction Official freeze*
