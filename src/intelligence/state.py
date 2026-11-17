"""
PressurePulse — Match State Reconstruction Service (L2)
Reconstructs cumulative match situation ball-by-ball:
runs, wickets, balls remaining, current run rate, targets, and required run rate (RRR).
"""

import logging
from pathlib import Path
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR

logger = logging.getLogger(__name__)

def reconstruct_match_states(
    delivery_df: pd.DataFrame = None,
    match_df: pd.DataFrame = None,
    save_parquet: bool = True
) -> pd.DataFrame:
    """
    Computes cumulative ball-by-ball match states.
    Returns enriched DataFrame with situations, targets, and rates.
    """
    logger.info("Starting match state reconstruction...")

    if delivery_df is None:
        delivery_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery.parquet")
    if match_df is None:
        match_df = pd.read_parquet(PROCESSED_DATA_DIR / "dim_match.parquet")

    # 1. Clean sorting order: match_id -> innings -> overid -> over_ball_num
    df = delivery_df.sort_values(["match_id", "innings", "overid", "over_ball_num"]).copy()

    # 2. Determine legal delivery (wides and no-balls / Overstep do not consume scheduled balls)
    df["is_legal_ball"] = ~df["extras_type"].isin(["wide", "Overstep"])

    # 3. Innings 1 totals & target lookup
    inn1_totals = (
        df[df["innings"] == 1]
        .groupby("match_id")["total_delivery_runs"]
        .sum()
        .rename("inn1_total_runs")
    )

    # Merge match metadata (revised targets, revised overs)
    match_cols = [
        "match_id", "first_inn_revised_overs", "second_inn_revised_overs",
        "revised_target", "win_team_id", "result"
    ]
    df = df.merge(match_df[match_cols], on="match_id", how="left")
    df = df.merge(inn1_totals, on="match_id", how="left")

    # Determine target for innings 2
    df["target"] = np.nan
    inn2_mask = df["innings"] == 2
    # If revised target exists (rain affected), use it; otherwise inn1 total + 1
    df.loc[inn2_mask, "target"] = np.where(
        df.loc[inn2_mask, "revised_target"].notnull(),
        df.loc[inn2_mask, "revised_target"],
        df.loc[inn2_mask, "inn1_total_runs"] + 1
    )

    # Determine scheduled balls per innings
    df["scheduled_legal_balls"] = 120.0
    # Apply revised overs if present
    df.loc[(df["innings"] == 1) & (df["first_inn_revised_overs"].notnull()), "scheduled_legal_balls"] = df["first_inn_revised_overs"]
    df.loc[(df["innings"] == 2) & (df["second_inn_revised_overs"].notnull()), "scheduled_legal_balls"] = df["second_inn_revised_overs"]

    # 4. Cumulative computations per (match_id, innings)
    grp = df.groupby(["match_id", "innings"], sort=False)

    # Prior state before this delivery
    df["runs_before"] = grp["total_delivery_runs"].cumsum() - df["total_delivery_runs"]
    df["wickets_before"] = grp["is_wicket"].cumsum() - df["is_wicket"].astype(int)
    df["legal_balls_bowled_before"] = grp["is_legal_ball"].cumsum() - df["is_legal_ball"].astype(int)

    # State after this delivery
    df["runs_after"] = grp["total_delivery_runs"].cumsum()
    df["wickets_after"] = grp["is_wicket"].cumsum()
    df["legal_balls_bowled_after"] = grp["is_legal_ball"].cumsum()

    # Remaining context
    df["wickets_in_hand_before"] = 10 - df["wickets_before"]
    df["legal_balls_remaining_before"] = np.maximum(0, df["scheduled_legal_balls"] - df["legal_balls_bowled_before"])
    df["legal_balls_remaining_after"] = np.maximum(0, df["scheduled_legal_balls"] - df["legal_balls_bowled_after"])

    # 5. Rates and chase variables
    # Current Run Rate (CRR) before ball
    df["crr_before"] = np.where(
        df["legal_balls_bowled_before"] > 0,
        (df["runs_before"] / df["legal_balls_bowled_before"]) * 6.0,
        0.0
    )

    # Required Run Rate (RRR) before ball (Innings 2 only)
    df["runs_needed_before"] = np.nan
    df["rrr_before"] = np.nan
    
    inn2_runs_needed = np.maximum(0, df.loc[inn2_mask, "target"] - df.loc[inn2_mask, "runs_before"])
    df.loc[inn2_mask, "runs_needed_before"] = inn2_runs_needed

    balls_rem_inn2 = df.loc[inn2_mask, "legal_balls_remaining_before"]
    # Calculate RRR, cap at 36.0 when balls are very low to avoid inf
    calc_rrr = np.where(
        balls_rem_inn2 > 0,
        (inn2_runs_needed / balls_rem_inn2) * 6.0,
        np.where(inn2_runs_needed > 0, 36.0, 0.0)
    )
    df.loc[inn2_mask, "rrr_before"] = np.clip(calc_rrr, 0.0, 36.0)

    # 6. Phase Classification
    conditions = [
        df["overid"] <= 6,
        (df["overid"] >= 7) & (df["overid"] <= 15),
        df["overid"] >= 16
    ]
    choices = ["powerplay", "middle", "death"]
    df["match_phase"] = np.select(conditions, choices, default="middle")

    # Super over flag
    df["is_super_over"] = df["innings"] >= 3

    logger.info(f"Reconstructed match states for {len(df):,} deliveries across {df['match_id'].nunique()} matches.")

    # 7. Persist to data/processed/
    if save_parquet:
        out_file = PROCESSED_DATA_DIR / "fact_delivery_state.parquet"
        df.to_parquet(out_file, index=False)
        logger.info(f"Persisted enriched delivery states to {out_file}")

        # Summary logging
        log_lines = [
            "# PressurePulse — Match State Reconstruction Summary",
            "",
            f"- **Total Deliveries Analyzed:** {len(df):,}",
            f"- **Innings 1 Deliveries:** {(df['innings'] == 1).sum():,}",
            f"- **Innings 2 (Chase) Deliveries:** {(df['innings'] == 2).sum():,}",
            f"- **Super Over Deliveries:** {(df['innings'] >= 3).sum():,}",
            f"- **Phase Breakdown:**",
            f"  - Powerplay (Overs 1-6): {(df['match_phase'] == 'powerplay').sum():,}",
            f"  - Middle (Overs 7-15): {(df['match_phase'] == 'middle').sum():,}",
            f"  - Death (Overs 16-20): {(df['match_phase'] == 'death').sum():,}",
            f"- **Average Target in Innings 2:** {df.loc[inn2_mask, 'target'].mean():.1f} runs",
            f"- **Average RRR in Innings 2:** {df.loc[inn2_mask, 'rrr_before'].mean():.2f} runs/over"
        ]
        (QA_DIR / "match_state_summary.md").write_text("\n".join(log_lines), encoding="utf-8")

    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    reconstruct_match_states()
