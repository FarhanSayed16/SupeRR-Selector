"""
PressurePulse — Batting Metrics Service (L2)
Computes pressure vs baseline batting metrics, uplift indicators,
IPL/T20I splits, situation slices, and match consistency.
"""

import logging
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR

logger = logging.getLogger(__name__)

def compute_batting_metrics(
    delivery_df: pd.DataFrame = None,
    roles_df: pd.DataFrame = None,
    save_parquet: bool = True
) -> pd.DataFrame:
    """
    Computes comprehensive batting metrics comparing pressure to baseline.
    Returns metrics table for all eligible batters.
    """
    logger.info("Computing batting metrics for eligible players...")

    if delivery_df is None:
        delivery_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet")
    if roles_df is None:
        roles_df = pd.read_parquet(PROCESSED_DATA_DIR / "dim_player_roles.parquet")

    # Filter to eligible batters
    eligible_pids = set(roles_df[roles_df["eligible_as_batter"]]["player_id"])
    df = delivery_df[delivery_df["striker_id"].isin(eligible_pids)].copy()

    # Identify when striker is dismissed
    df["is_striker_out"] = df["is_wicket"] & (df["dismissed_player_id"] == df["striker_id"])

    # Helper to aggregate batting stats
    def aggregate_batting(data: pd.DataFrame, prefix: str) -> pd.DataFrame:
        agg = data.groupby("striker_id").agg(
            runs=("runs", "sum"),
            balls=("runs", "count"),
            dots=("runs", lambda x: int((x == 0).sum())),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            dismissals=("is_striker_out", "sum"),
            matches=("match_id", "nunique")
        ).reset_index().rename(columns={"striker_id": "player_id"})

        # Metrics
        agg[f"{prefix}_runs"] = agg["runs"]
        agg[f"{prefix}_balls"] = agg["balls"]
        agg[f"{prefix}_matches"] = agg["matches"]
        agg[f"{prefix}_sr"] = np.where(agg["balls"] > 0, (agg["runs"] / agg["balls"]) * 100.0, 0.0)
        agg[f"{prefix}_dot_pct"] = np.where(agg["balls"] > 0, (agg["dots"] / agg["balls"]) * 100.0, 0.0)
        agg[f"{prefix}_boundary_pct"] = np.where(agg["balls"] > 0, ((agg["fours"] + agg["sixes"]) / agg["balls"]) * 100.0, 0.0)
        agg[f"{prefix}_dismissals"] = agg["dismissals"]
        agg[f"{prefix}_avg"] = np.where(agg["dismissals"] > 0, agg["runs"] / agg["dismissals"], agg["runs"].astype(float))
        
        keep_cols = ["player_id", f"{prefix}_runs", f"{prefix}_balls", f"{prefix}_matches",
                     f"{prefix}_sr", f"{prefix}_dot_pct", f"{prefix}_boundary_pct",
                     f"{prefix}_dismissals", f"{prefix}_avg"]
        return agg[keep_cols]

    # 1. Pressure vs Baseline Aggregates
    df_pressure = df[df["is_pressure"]]
    df_baseline = df[~df["is_pressure"]]

    bat_pressure = aggregate_batting(df_pressure, "pressure")
    bat_baseline = aggregate_batting(df_baseline, "baseline")

    # 2. IPL-specific and T20I-specific Pressure Aggregates
    df_ipl_pressure = df[df["is_pressure"] & df["is_ipl"]]
    df_t20i_pressure = df[df["is_pressure"] & df["is_t20i"]]

    bat_ipl = aggregate_batting(df_ipl_pressure, "ipl_pressure")[["player_id", "ipl_pressure_balls", "ipl_pressure_sr", "ipl_pressure_runs"]]
    bat_t20i = aggregate_batting(df_t20i_pressure, "t20i_pressure")[["player_id", "t20i_pressure_balls", "t20i_pressure_sr", "t20i_pressure_runs"]]

    # 3. Situational Slices in Pressure: Death & Chase
    df_death = df[df["is_pressure"] & (df["match_phase"] == "death")]
    df_chase = df[df["is_pressure"] & (df["innings"] == 2)]

    bat_death = aggregate_batting(df_death, "death_pressure")[["player_id", "death_pressure_balls", "death_pressure_sr"]]
    bat_chase = aggregate_batting(df_chase, "chase_pressure")[["player_id", "chase_pressure_balls", "chase_pressure_sr"]]

    # 4. Consistency Across Matches under Pressure
    # Compute per-match runs and balls in pressure to measure volatility
    match_pressure = df_pressure.groupby(["striker_id", "match_id"]).agg(
        m_runs=("runs", "sum"),
        m_balls=("runs", "count")
    ).reset_index()
    match_pressure["m_sr"] = (match_pressure["m_runs"] / match_pressure["m_balls"]) * 100.0

    consistency = match_pressure.groupby("striker_id").agg(
        sr_std=("m_sr", "std"),
        sr_mean=("m_sr", "mean"),
        matches_scored=("m_runs", "count")
    ).reset_index().rename(columns={"striker_id": "player_id"})

    # Coefficient of variation (CV) for strike rate; lower is more consistent
    consistency["sr_cv"] = np.where(
        (consistency["sr_mean"] > 0) & (consistency["sr_std"].notnull()),
        consistency["sr_std"] / consistency["sr_mean"],
        1.0
    )
    # Scaled consistency score 0.0 to 1.0 (higher = more reliable match-to-match)
    consistency["consistency_score"] = np.clip(1.0 - (consistency["sr_cv"] / 2.0), 0.1, 1.0)
    consistency_cols = consistency[["player_id", "consistency_score", "sr_cv"]]

    # 5. Master Merge onto Roles Dimension
    m = roles_df[roles_df["eligible_as_batter"]].copy()
    m = m.merge(bat_pressure, on="player_id", how="left")
    m = m.merge(bat_baseline, on="player_id", how="left")
    m = m.merge(bat_ipl, on="player_id", how="left")
    m = m.merge(bat_t20i, on="player_id", how="left")
    m = m.merge(bat_death, on="player_id", how="left")
    m = m.merge(bat_chase, on="player_id", how="left")
    m = m.merge(consistency_cols, on="player_id", how="left")

    # Fill nulls for splits
    fill_zeros = [
        "ipl_pressure_balls", "ipl_pressure_sr", "ipl_pressure_runs",
        "t20i_pressure_balls", "t20i_pressure_sr", "t20i_pressure_runs",
        "death_pressure_balls", "death_pressure_sr",
        "chase_pressure_balls", "chase_pressure_sr",
        "baseline_runs", "baseline_balls", "baseline_sr", "baseline_dot_pct", "baseline_boundary_pct", "baseline_avg"
    ]
    for col in fill_zeros:
        m[col] = m[col].fillna(0.0)

    m["consistency_score"] = m["consistency_score"].fillna(0.50)

    # 6. Uplift Metrics (Pressure vs Baseline)
    m["sr_uplift"] = m["pressure_sr"] - m["baseline_sr"]
    m["dot_reduction"] = m["baseline_dot_pct"] - m["pressure_dot_pct"] # Positive means dots reduced under pressure
    m["boundary_uplift"] = m["pressure_boundary_pct"] - m["baseline_boundary_pct"]
    m["avg_uplift"] = m["pressure_avg"] - m["baseline_avg"]

    # 7. Confidence Banding (High / Med / Low sample)
    conditions = [
        m["pressure_balls"] >= CONFIG.CONFIDENCE_HIGH_BALLS,
        m["pressure_balls"] >= CONFIG.CONFIDENCE_MED_BALLS
    ]
    choices = ["High", "Medium"]
    m["sample_confidence"] = np.select(conditions, choices, default="Low")

    logger.info(f"Batting metrics computed for {len(m)} eligible batters.")

    # 8. Persist Parquet & QA Summary
    if save_parquet:
        out_parquet = PROCESSED_DATA_DIR / "metrics_batting.parquet"
        m.to_parquet(out_parquet, index=False)
        logger.info(f"Persisted batting metrics to {out_parquet}")

        # Spot-check summary
        qa_lines = [
            "# PressurePulse — Batting Metrics & Uplift Summary",
            "",
            "## 1. Top 10 Batters by Strike Rate Uplift (Min 100 Pressure Balls)",
            "| Player | Role | Pressure Balls | Pressure SR | Baseline SR | SR Uplift | Dot Reduction | Confidence |",
            "|---|---|---|---|---|---|---|---|"
        ]
        top_uplift = m[m["pressure_balls"] >= 100].sort_values("sr_uplift", ascending=False).head(10)
        for _, r in top_uplift.iterrows():
            qa_lines.append(
                f"| {r['player_name']} | {r['primary_role']} | {int(r['pressure_balls'])} | "
                f"{r['pressure_sr']:.1f} | {r['baseline_sr']:.1f} | {r['sr_uplift']:+.1f} | "
                f"{r['dot_reduction']:+.1f}% | {r['sample_confidence']} |"
            )

        qa_lines.extend([
            "",
            "## 2. Top 10 Batters by Absolute Pressure Strike Rate (Min 100 Pressure Balls)",
            "| Player | Role | Pressure Balls | Pressure SR | Boundary % | Death SR | Chase SR | Confidence |",
            "|---|---|---|---|---|---|---|---|"
        ])
        top_sr = m[m["pressure_balls"] >= 100].sort_values("pressure_sr", ascending=False).head(10)
        for _, r in top_sr.iterrows():
            qa_lines.append(
                f"| {r['player_name']} | {r['primary_role']} | {int(r['pressure_balls'])} | "
                f"{r['pressure_sr']:.1f} | {r['pressure_boundary_pct']:.1f}% | {r['death_pressure_sr']:.1f} | "
                f"{r['chase_pressure_sr']:.1f} | {r['sample_confidence']} |"
            )

        (QA_DIR / "batting_metrics_summary.md").write_text("\n".join(qa_lines), encoding="utf-8")

    return m

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    compute_batting_metrics()
