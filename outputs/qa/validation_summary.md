# PressurePulse — Official Ranking Validation & Freeze Report

## 1. Cryptographic Freeze Fingerprint
- **Status:** `FROZEN_OFFICIAL`
- **SHA256 Fingerprint:** `5cdd7b7451b5a6672dbfadccc3c36a9777ec5bafaec589339e22ba307202d272`
- **Pressure Specification Version:** `pressure_v1`

## 2. Integrity & Orthogonality Audits
| Audit Check | Condition Tested | Result | Status |
|---|---|:---:|:---:|
| Zero Leakage | Pressure & Baseline balls mutually exclusive | 0 leaks | **PASS** |
| Universal Delivery Coverage | Pressure + Baseline == Total | 200,999 == 200,999 | **PASS** |
| Batters Uniqueness | Top 10 Batters unique IDs | 10 / 10 | **PASS** |
| Bowlers Uniqueness | Top 10 Bowlers unique IDs | 10 / 10 | **PASS** |
| Disjoint Lists | Zero cross-category player duplication | 0 overlaps | **PASS** |
| Sample Sufficiency (Batters) | Min pressure balls faced in Top 10 | 208 >= 30 | **PASS** |
| Sample Sufficiency (Bowlers) | Min pressure balls bowled in Top 10 | 281 >= 30 | **PASS** |

## 3. Sensitivity & Domain Stability
- **Threshold Perturbation Stability:** 90% list retention under ±0.5 RRR and ±1 death over shift.
- **IPL Domain Overlap:** 80% of top performers rank in the elite tier of pure IPL-only match slices.

## 4. Official Frozen Top 10 Roster
### Batters
1. Rohit Sharma
2. Shashank Singh
3. Naman Dhir
4. Ashutosh Sharma
5. Dinesh Karthik
6. Rishabh Pant
7. Sai Sudharsan
8. Vijay Shankar
9. Suryakumar Yadav
10. Rinku Singh

### Bowlers
1. Sunil Narine
2. Mohammad Nawaz
3. Sufiyan Muqeem
4. Abrar Ahmed
5. Kuldeep Yadav
6. Jasprit Bumrah
7. Rasikh Salam
8. Rashid Khan
9. Mitchell Santner
10. Varun Chakravarthy