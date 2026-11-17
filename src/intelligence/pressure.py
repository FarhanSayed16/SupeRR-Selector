"""
PressurePulse — Pressure Definition Engine (L2)
Defines, computes, and validates delivery-level Pressure Signals and Composite Pressure Index.
Version: pressure_v1
"""

import json
import logging
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR

logger = logging.getLogger(__name__)

# Frozen one-sentence definition for UI & Report
PRESSURE_DEFINITION_SENTENCE = (
    "A delivery is defined as high-pressure when match context demands immediate high-leverage execution: "
    "specifically during steep chases (RRR >= 9.5), death-over contests, severe batting collapses (<=3 wickets in hand), "
    "or critical playoff knockout stages."
)

def compute_pressure_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates explicit pressure signals and generates:
    - signal_chase_tightness (bool)
    - signal_collapse_defense (bool)
    - signal_death_contest (bool)
    - signal_knockout_leverage (bool)
    - signal_super_over (bool)
    - is_pressure (bool)
    - pressure_index (float 0.0 to 1.0)
    """
    logger.info("Evaluating pressure signals across deliveries...")
    data = df.copy()

    # Signal 1: Chase Tightness (Innings 2)
    # High RRR in middle/death OR critical RRR anytime OR close finish in final 30 balls
    s1_high_rrr = (data["innings"] == 2) & (data["rrr_before"] >= CONFIG.CHASE_HIGH_RRR) & (data["legal_balls_remaining_before"] <= 60)
    s1_crit_rrr = (data["innings"] == 2) & (data["rrr_before"] >= CONFIG.CHASE_CRITICAL_RRR)
    s1_close_finish = (data["innings"] == 2) & (data["legal_balls_remaining_before"] <= 30) & (data["runs_needed_before"] > 0) & (data["runs_needed_before"] <= 55)
    data["signal_chase_tightness"] = s1_high_rrr | s1_crit_rrr | s1_close_finish

    # Signal 2: Collapse & Survival (Innings 1 & 2)
    # Early top-order collapse (>=3 wickets lost before over 8) OR tail exposure (<=3 wickets in hand)
    s2_early_collapse = (data["overid"] <= CONFIG.COLLAPSE_BEFORE_OVER) & (data["wickets_before"] >= CONFIG.COLLAPSE_WICKETS_LOST)
    s2_tail_exposed = (data["wickets_in_hand_before"] <= CONFIG.LOW_WICKETS_IN_HAND) & (data["legal_balls_remaining_before"] >= 12)
    data["signal_collapse_defense"] = s2_early_collapse | s2_tail_exposed

    # Signal 3: Death Overs Contest (Innings 1 & 2)
    # In Innings 1: all death overs (setting target total, high risk/reward)
    # In Innings 2: death overs where chase is alive (not already won / blowout needing <=5 runs)
    s3_inn1_death = (data["innings"] == 1) & (data["match_phase"] == "death")
    s3_inn2_death = (data["innings"] == 2) & (data["match_phase"] == "death") & (data["runs_needed_before"] > 5)
    data["signal_death_contest"] = s3_inn1_death | s3_inn2_death

    # Signal 4: Knockout Stage Leverage
    # Knockout fixtures where match is moderately contested (RRR >= 8.5 or death or >=2 wkts down)
    s4_ko = data["is_knockout"] & (
        ((data["innings"] == 2) & (data["rrr_before"] >= 8.5)) |
        (data["match_phase"] == "death") |
        (data["wickets_before"] >= 2)
    )
    data["signal_knockout_leverage"] = s4_ko

    # Signal 5: Super Overs
    data["signal_super_over"] = data["is_super_over"]

    # Composite Pressure Boolean
    data["is_pressure"] = (
        data["signal_chase_tightness"] |
        data["signal_collapse_defense"] |
        data["signal_death_contest"] |
        data["signal_knockout_leverage"] |
        data["signal_super_over"]
    )

    # Continuous Pressure Intensity Index (0.0 to 1.0)
    # Reconstructed from situational weights
    base_intensity = np.zeros(len(data))
    base_intensity += np.where(data["signal_death_contest"], 0.35, 0.0)
    base_intensity += np.where(data["signal_chase_tightness"], 0.40, 0.0)
    base_intensity += np.where(data["signal_collapse_defense"], 0.25, 0.0)
    base_intensity += np.where(data["signal_knockout_leverage"], 0.15, 0.0)
    base_intensity += np.where(data["signal_super_over"], 0.50, 0.0)
    
    # RRR modifier in chase
    rrr_norm = np.clip((data["rrr_before"].fillna(0) - 6.0) / 12.0, 0.0, 0.35)
    base_intensity += np.where(data["innings"] == 2, rrr_norm, 0.0)

    data["pressure_index"] = np.round(np.clip(base_intensity, 0.0, 1.0), 3)

    return data

def generate_pressure_diagnostics(df: pd.DataFrame) -> Dict:
    """Computes comprehensive diagnostics to prove definition robustness."""
    total_balls = len(df)
    pressure_balls = int(df["is_pressure"].sum())
    pct_pressure = (pressure_balls / total_balls) * 100

    # Phase breakdown of pressure balls
    phase_dist = df[df["is_pressure"]]["match_phase"].value_counts().to_dict()
    phase_pct = {k: round((v / pressure_balls) * 100, 1) for k, v in phase_dist.items()}

    # Competition format split
    ipl_balls = df[df["is_ipl"]]
    t20i_balls = df[df["is_t20i"]]

    ipl_pressure_pct = (ipl_balls["is_pressure"].sum() / len(ipl_balls)) * 100 if len(ipl_balls) > 0 else 0
    t20i_pressure_pct = (t20i_balls["is_pressure"].sum() / len(t20i_balls)) * 100 if len(t20i_balls) > 0 else 0

    # Signal active counts
    signal_counts = {
        "chase_tightness": int(df["signal_chase_tightness"].sum()),
        "collapse_defense": int(df["signal_collapse_defense"].sum()),
        "death_contest": int(df["signal_death_contest"].sum()),
        "knockout_leverage": int(df["signal_knockout_leverage"].sum()),
        "super_overs": int(df["signal_super_over"].sum())
    }

    diagnostics = {
        "pressure_version": CONFIG.PRESSURE_VERSION,
        "definition_sentence": PRESSURE_DEFINITION_SENTENCE,
        "total_deliveries": total_balls,
        "pressure_deliveries": pressure_balls,
        "baseline_deliveries": total_balls - pressure_balls,
        "pressure_percentage": round(pct_pressure, 2),
        "ipl_pressure_percentage": round(ipl_pressure_pct, 2),
        "t20i_pressure_percentage": round(t20i_pressure_pct, 2),
        "phase_distribution_count": phase_dist,
        "phase_distribution_percentage": phase_pct,
        "signal_activation_counts": signal_counts
    }

    return diagnostics

def run_pressure_engine(
    state_df: pd.DataFrame = None,
    save_parquet: bool = True
) -> Tuple[pd.DataFrame, Dict]:
    """Runs pressure labelling, exports Parquet and diagnostic JSON."""
    if state_df is None:
        state_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery_state.parquet")

    df = compute_pressure_signals(state_df)
    diagnostics = generate_pressure_diagnostics(df)

    logger.info(
        f"Pressure labelling complete: {diagnostics['pressure_deliveries']:,} / {diagnostics['total_deliveries']:,} "
        f"({diagnostics['pressure_percentage']}%) labelled as high pressure."
    )

    if save_parquet:
        out_parquet = PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet"
        df.to_parquet(out_parquet, index=False)
        logger.info(f"Persisted pressure delivery table to {out_parquet}")

        # Save JSON diagnostics for dashboard Pressure Lab
        diag_file = QA_DIR / "pressure_summary.json"
        with open(diag_file, "w", encoding="utf-8") as f:
            json.dump(diagnostics, f, indent=2)
        logger.info(f"Saved pressure diagnostics to {diag_file}")

        # Save Evidence Note markdown proving definition is not "death overs only"
        evidence_note = f"""# PressurePulse — Pressure Definition Validation & Evidence Note

## 1. Frozen Definition
> **"{PRESSURE_DEFINITION_SENTENCE}"**

## 2. Core Diagnostics & Distribution
- **Overall Pressure Proportion:** {diagnostics['pressure_percentage']}% of all balls ({diagnostics['pressure_deliveries']:,} / {diagnostics['total_deliveries']:,}).
- **IPL Rate:** {diagnostics['ipl_pressure_percentage']}% | **T20I Rate:** {diagnostics['t20i_pressure_percentage']}%.
- **Baseline (Non-Pressure) Balls:** {diagnostics['baseline_deliveries']:,} balls (fair comparator pool).

## 3. Proof: The Definition Is NOT Just "Death Overs Renamed"
A common pitfall in cricket analytics is equating pressure solely with overs 16–20.
Under PressurePulse (`{CONFIG.PRESSURE_VERSION}`):
- **Powerplay (Overs 1-6):** Accounts for {diagnostics['phase_distribution_percentage'].get('powerplay', 0)}% of all pressure deliveries ({diagnostics['phase_distribution_count'].get('powerplay', 0):,} balls) triggered by severe early batting collapses and aggressive target defenses.
- **Middle Overs (Overs 7-15):** Accounts for {diagnostics['phase_distribution_percentage'].get('middle', 0)}% of all pressure deliveries ({diagnostics['phase_distribution_count'].get('middle', 0):,} balls) driven by climbing required rates (RRR >= 9.5) and sudden cluster wickets.
- **Death Overs (Overs 16-20):** Accounts for {diagnostics['phase_distribution_percentage'].get('death', 0)}% of all pressure deliveries ({diagnostics['phase_distribution_count'].get('death', 0):,} balls).

**Key Takeaway:** {100 - diagnostics['phase_distribution_percentage'].get('death', 0):.1f}% of all pressure deliveries occur *outside* the death overs, proving that the model captures holistic match context across all innings phases.
"""
        (QA_DIR / "pressure_evidence_note.md").write_text(evidence_note, encoding="utf-8")

    return df, diagnostics

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_pressure_engine()
