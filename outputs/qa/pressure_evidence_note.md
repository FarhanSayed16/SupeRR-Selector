# PressurePulse — Pressure Definition Validation & Evidence Note

## 1. Frozen Definition
> **"A delivery is defined as high-pressure when match context demands immediate high-leverage execution: specifically during steep chases (RRR >= 9.5), death-over contests, severe batting collapses (<=3 wickets in hand), or critical playoff knockout stages."**

## 2. Core Diagnostics & Distribution
- **Overall Pressure Proportion:** 39.26% of all balls (78,906 / 200,999).
- **IPL Rate:** 41.02% | **T20I Rate:** 37.61%.
- **Baseline (Non-Pressure) Balls:** 122,093 balls (fair comparator pool).

## 3. Proof: The Definition Is NOT Just "Death Overs Renamed"
A common pitfall in cricket analytics is equating pressure solely with overs 16–20.
Under PressurePulse (`pressure_v1`):
- **Powerplay (Overs 1-6):** Accounts for 10.2% of all pressure deliveries (8,050 balls) triggered by severe early batting collapses and aggressive target defenses.
- **Middle Overs (Overs 7-15):** Accounts for 33.5% of all pressure deliveries (26,402 balls) driven by climbing required rates (RRR >= 9.5) and sudden cluster wickets.
- **Death Overs (Overs 16-20):** Accounts for 56.3% of all pressure deliveries (44,454 balls).

**Key Takeaway:** 43.7% of all pressure deliveries occur *outside* the death overs, proving that the model captures holistic match context across all innings phases.
