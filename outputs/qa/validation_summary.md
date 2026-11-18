# PressurePulse — Official Ranking Validation & Freeze Report

## 1. Cryptographic Freeze Fingerprint
- **Status:** `FROZEN_OFFICIAL`
- **Board:** Auction Official
- **SHA256 Fingerprint:** `a819c0e65bf4ee045ef17c7b19824ccbec549c4b002402e9fbf47f477a04810c`
- **Pressure Specification Version:** `pressure_v1.1`

## 2. Integrity & Orthogonality Audits
| Audit Check | Condition Tested | Result | Status |
|---|---|:---:|:---:|
| Zero Leakage | Pressure & Baseline balls mutually exclusive | 0 leaks | **PASS** |
| Universal Delivery Coverage | Pressure + Baseline == Total | 200,999 == 200,999 | **PASS** |
| Batters Uniqueness | Top 10 Batters unique IDs | 10 / 10 | **PASS** |
| Bowlers Uniqueness | Top 10 Bowlers unique IDs | 10 / 10 | **PASS** |
| Disjoint Lists | Zero cross-category player duplication | 0 overlaps | **PASS** |
| Sample Sufficiency (Batters) | Min pressure balls | 208 >= 50 | **PASS** |
| Sample Sufficiency (Bowlers) | Min pressure balls | 319 >= 80 | **PASS** |
| IPL Floor (Batters) | Min IPL pressure balls | 142 >= 40 | **PASS** |
| IPL Floor (Bowlers) | Min IPL pressure balls | 81 >= 60 | **PASS** |

## 3. Sensitivity & Domain Stability (computed)
- **Batter Top 10 mean retention:** 92.5% across RRR/death perturbations.
- **Bowler Top 10 mean retention:** 95.0% across RRR/death perturbations.
- **Per-variant batter retention %:** [90.0, 100.0, 90.0, 90.0]
- **Per-variant bowler retention %:** [100.0, 100.0, 90.0, 90.0]
- **IPL-only Top 12 overlap:** batters 9/10, bowlers 9/10.

## 4. Official Frozen Top 10 Roster (Auction Official)
### Batters
1. Rohit Sharma
2. Shashank Singh
3. Naman Dhir
4. Dinesh Karthik
5. Rishabh Pant
6. Ashutosh Sharma
7. Shreyas Iyer
8. Rinku Singh
9. Marcus Stoinis
10. Suryakumar Yadav

### Bowlers
1. Sunil Narine
2. Mitchell Santner
3. Kuldeep Yadav
4. Jasprit Bumrah
5. Adam Zampa
6. Rashid Khan
7. Wanindu Hasaranga
8. Rasikh Salam
9. Varun Chakravarthy
10. Matheesha Pathirana