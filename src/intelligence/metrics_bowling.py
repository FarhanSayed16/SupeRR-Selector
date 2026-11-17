"""
PressurePulse — Bowling Metrics Service (L2)
Computes pressure vs baseline bowling metrics, economy, dot-ball %,
wicket rates, death over performance, and match consistency.
"""

import logging
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR

logger = logging.getLogger(__name__)

# Valid wicket types credited to bowler
BOWLER_WICKET_TYPES = ["Caught", "Bowled", "LBW", "Stump", "Hit Wicket"]

def compute_bowling_metrics(
    delivery_df: pd.DataFrame = None,
    roles_df: pd.DataFrame = None,
    save_parquet: bool = True
) -> pd.DataFrame:
    """
    Computes comprehensive bowling metrics comparing pressure to baseline.
    Returns metrics table for all eligible bowlers.
    """
    logger.info("Computing bowling metrics for eligible players...")

    if delivery_df is None:
        delivery_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet")
    if roles_df is None:
        roles_df = pd.read_parquet(PROCESSED_DATA_DIR / "dim_player_roles.parquet")

    # Filter to eligible bowlers
    eligible_pids = set(roles_df[roles_df["eligible_as_bowler"]]["player_id"])
    df = delivery_df[delivery_df["bowler_id"].isin(eligible_pids)].copy()

    # Credit wickets to bowler (excluding run outs and retirements)
    df["is_bowler_wkt"] = df["is_wicket"] & df["dismissal_type"].isin(BOWLER_WICKET_TYPES)

    # Bowler conceded runs: runs + extras EXCEPT byes and legbyes
    bowler_extras_mask = ~df["extras_type"].isin(["byes", "legbyes"])
    df["bowler_runs"] = df["runs"] + (df["extras1_runs"] + df["extras_2_runs"]).where(bowler_extras_mask, 0)
    df["is_dot_ball"] = (df["bowler_runs"] == 0) & df["is_legal_ball"]

    # Helper to aggregate bowling stats
    def aggregate_bowling(data: pd.DataFrame, prefix: str) -> pd.DataFrame:
        agg = data.groupby("bowler_id").agg(
            total_deliveries=("runs", "count"),
            legal_balls=("is_legal_ball", "sum"),
            runs_conceded=("bowler_runs", "sum"),
            wickets=("is_bowler_wkt", "sum"),
            dot_balls=("is_dot_ball", "sum"),
            matches=("match_id", "nunique")
        ).reset_index().rename(columns={"bowler_id": "player_id"})

        # Metrics
        agg[f"{prefix}_balls"] = agg["legal_balls"]
        agg[f"{prefix}_overs"] = agg["legal_balls"] / 6.0
        agg[f"{prefix}_runs"] = agg["runs_conceded"]
        agg[f"{prefix}_wickets"] = agg["wickets"]
        agg[f"{prefix}_matches"] = agg["matches"]
        agg[f"{prefix}_dots"] = agg["dot_balls"]

        # Rates
        agg[f"{prefix}_economy"] = np.where(agg["legal_balls"] > 0, (agg["runs_conceded"] / agg["legal_balls"]) * 6.0, 12.0)
        agg[f"{prefix}_dot_pct"] = np.where(agg["legal_balls"] > 0, (agg["dot_balls"] / agg["legal_balls"]) * 100.0, 0.0)
        agg[f"{prefix}_bowling_avg"] = np.where(agg["wickets"] > 0, agg["runs_conceded"] / agg["wickets"], agg["runs_conceded"].astype(float))
        agg[f"{prefix}_balls_per_wicket"] = np.where(agg["wickets"] > 0, agg["legal_balls"] / agg["wickets"], agg["legal_balls"].astype(float))

        keep_cols = [
            "player_id", f"{prefix}_balls", f"{prefix}_overs", f"{prefix}_runs",
            f"{prefix}_wickets", f"{prefix}_matches", f"{prefix}_dots",
            f"{prefix}_economy", f"{prefix}_dot_pct", f"{prefix}_bowling_avg",
            f"{prefix}_balls_per_wicket"
        ]
        return agg[keep_cols]

    # 1. Pressure vs Baseline Aggregates
    df_pressure = df[df["is_pressure"]]
    df_baseline = df[~df["is_pressure"]]

    bowl_pressure = aggregate_bowling(df_pressure, "pressure")
    bowl_baseline = aggregate_bowling(df_baseline, "baseline")

    # 2. IPL-specific and T20I-specific Pressure Aggregates
    df_ipl_pressure = df[df["is_pressure"] & df["is_ipl"]]
    df_t20i_pressure = df[df["is_pressure"] & df["is_t20i"]]

    bowl_ipl = aggregate_bowling(df_ipl_pressure, "ipl_pressure")[["player_id", "ipl_pressure_balls", "ipl_pressure_economy", "ipl_pressure_wickets"]]
    bowl_t20i = aggregate_bowling(df_t20i_pressure, "t20i_pressure")[["player_id", "t20i_pressure_balls", "t20i_pressure_economy", "t20i_pressure_wickets"]]

    # 3. Situational Slices in Pressure: Death & Defending (Chase)
    df_death = df[df["is_pressure"] & (df["match_phase"] == "death")]
    df_chase = df[df["is_pressure"] & (df["innings"] == 2)]

    bowl_death = aggregate_bowling(df_death, "death_pressure")[["player_id", "death_pressure_balls", "death_pressure_economy", "death_pressure_wickets"]]
    bowl_chase = aggregate_bowling(df_chase, "chase_pressure")[["player_id", "chase_pressure_balls", "chase_pressure_economy", "chase_pressure_wickets"]]

    # 4. Consistency Across Matches under Pressure
    match_pressure = df_pressure.groupby(["bowler_id", "match_id"]).agg(
        m_legal_balls=("is_legal_ball", "sum"),
        m_runs=("bowler_runs", "sum")
    ).reset_index()
    match_pressure = match_pressure[match_pressure["m_legal_balls"] >= 6] # Min 1 over in pressure
    match_pressure["m_econ"] = (match_pressure["m_runs"] / match_pressure["m_legal_balls"]) * 6.0

    consistency = match_pressure.groupby("bowler_id").agg(
        econ_std=("m_econ", "std"),
        econ_mean=("m_econ", "mean"),
        matches_bowled=("m_runs", "count")
    ).reset_index().rename(columns={"bowler_id": "player_id"})

    # Coefficient of variation for economy; lower is more consistent
    consistency["econ_cv"] = np.where(
        (consistency["econ_mean"] > 0) & (consistency["econ_std"].notnull()),
        consistency["econ_std"] / consistency["econ_mean"],
        0.50
    )
    consistency["consistency_score"] = np.clip(1.0 - (consistency["econ_cv"] / 1.5), 0.1, 1.0)
    consistency_cols = consistency[["player_id", "consistency_score", "econ_cv"]]

    # 5. Master Merge onto Roles Dimension
    m = roles_df[roles_df["eligible_as_bowler"]].copy()
    m = m.merge(bowl_pressure, on="player_id", how="left")
    m = m.merge(bowl_baseline, on="player_id", how="left")
    m = m.merge(bowl_ipl, on="player_id", how="left")
    m = m.merge(bowl_t20i, on="player_id", how="left")
    m = m.merge(bowl_death, on="player_id", how="left")
    m = m.merge(bowl_chase, on="player_id", how="left")
    m = m.merge(consistency_cols, on="player_id", how="left")

    # Fill nulls
    fill_zeros = [
        "ipl_pressure_balls", "ipl_pressure_economy", "ipl_pressure_wickets",
        "t20i_pressure_balls", "t20i_pressure_economy", "t20i_pressure_wickets",
        "death_pressure_balls", "death_pressure_economy", "death_pressure_wickets",
        "chase_pressure_balls", "chase_pressure_economy", "chase_pressure_wickets",
        "baseline_balls", "baseline_overs", "baseline_runs", "baseline_wickets",
        "baseline_dots", "baseline_economy", "baseline_dot_pct", "baseline_bowling_avg", "baseline_balls_per_wicket"
    ]
    for col in fill_zeros:
        m[col] = m[col].fillna(0.0)

    m["consistency_score"] = m["consistency_score"].fillna(0.50)

    # 6. Uplift Metrics
    # Economy uplift: baseline economy minus pressure economy
    # Note: Pressure economy is naturally higher in death overs; positive uplift is exceptional
    m["economy_uplift"] = m["baseline_economy"] - m["pressure_economy"]
    m["dot_uplift"] = m["pressure_dot_pct"] - m["baseline_dot_pct"]
    m["wicket_rate_uplift"] = m["baseline_balls_per_wicket"] - m["pressure_balls_per_wicket"]

    # 7. Confidence Banding
    conditions = [
        m["pressure_balls"] >= CONFIG.CONFIDENCE_HIGH_BALLS,
        m["pressure_balls"] >= CONFIG.CONFIDENCE_MED_BALLS
    ]
    choices = ["High", "Medium"]
    m["sample_confidence"] = np.select(conditions, choices, default="Low")

    logger.info(f"Bowling metrics computed for {len(m)} eligible bowlers.")

    # 8. Persist Parquet & QA Summary
    if save_parquet:
        out_parquet = PROCESSED_DATA_DIR / "metrics_bowling.parquet"
        m.to_parquet(out_parquet, index=False)
        logger.info(f"Persisted bowling metrics to {out_parquet}")

        # QA Summary
        qa_lines = [
            "# PressurePulse — Bowling Metrics & Reliability Summary",
            "",
            "## 1. Top 10 Bowlers by Lowest Pressure Economy (Min 120 Pressure Balls)",
            "| Player | Role | Pressure Balls | Pressure Econ | Baseline Econ | Dot % | Wickets | Confidence |",
            "|---|---|---|---|---|---|---|---|"
        ]
        top_econ = m[m["pressure_balls"] >= 120].sort_values("pressure_economy", ascending=True).head(10)
        for _, r in top_econ.iterrows():
            qa_lines.append(
                f"| {r['player_name']} | {r['primary_role']} | {int(r['pressure_balls'])} | "
                f"{r['pressure_economy']:.2f} | {r['baseline_economy']:.2f} | {r['pressure_dot_pct']:.1f}% | "
                f"{int(r['pressure_wickets'])} | {r['sample_confidence']} |"
            )

        qa_lines.extend([
            "",
            "## 2. Top 10 Bowlers by Pressure Wickets Taken (Min 100 Pressure Balls)",
            "| Player | Role | Pressure Balls | Wickets | Balls/Wkt | Death Econ | Chase Econ | Confidence |",
            "|---|---|---|---|---|---|---|---|"
        ])
        top_wkts = m[m["pressure_balls"] >= 100].sort_values("pressure_wickets", ascending=False).head(10)
        for _, r in top_wkts.iterrows():
            qa_lines.append(
                f"| {r['player_name']} | {r['primary_role']} | {int(r['pressure_balls'])} | "
                f"{int(r['pressure_wickets'])} | {r['pressure_balls_per_wicket']:.1f} | "
                f"{r['death_pressure_economy']:.2f} | {r['chase_pressure_economy']:.2f} | {r['sample_confidence']} |"
            )

        (QA_DIR / "bowling_metrics_summary.md").write_text("\n".join(qa_lines), encoding="utf-8")

    return m

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    compute_bowling_metrics()
