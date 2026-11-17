"""
PressurePulse — Scoring, Eligibility & Top 10 Ranking Service (L2)
Calculates composite PressureScore for Batters and Bowlers,
applies sample filters, generates Official Top 10 lists and near-miss boards.
"""

import logging
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, RANKINGS_DIR, QA_DIR

logger = logging.getLogger(__name__)

def score_batters(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates transparent composite PressureScore for eligible batters."""
    data = df.copy()

    # Eligibility filter
    eligible_mask = (
        (data["pressure_balls"] >= 50) &
        (data["baseline_balls"] >= 40) &
        (data["pressure_matches"] >= 5)
    )
    eligible = data[eligible_mask].copy()

    # 1. Quality Score (SR 110-180, Boundary% 12-28, Avg 15-45)
    sr_q = np.clip((eligible["pressure_sr"] - 110.0) / (180.0 - 110.0), 0.0, 1.0) * 100.0
    bp_q = np.clip((eligible["pressure_boundary_pct"] - 12.0) / (28.0 - 12.0), 0.0, 1.0) * 100.0
    avg_q = np.clip((eligible["pressure_avg"] - 15.0) / (45.0 - 15.0), 0.0, 1.0) * 100.0
    quality = 0.50 * sr_q + 0.30 * bp_q + 0.20 * avg_q

    # 2. Uplift Score (-10 to +40 SR uplift)
    uplift = np.clip((eligible["sr_uplift"] - (-10.0)) / (40.0 - (-10.0)), 0.0, 1.0) * 100.0

    # 3. Consistency (0-100)
    consistency = eligible["consistency_score"] * 100.0

    # 4. Volume & Sample Depth (0-250 balls)
    volume = np.clip(eligible["pressure_balls"] / 250.0, 0.0, 1.0) * 100.0

    # 5. IPL Relevance Multiplier (up to +15% boost for IPL sample)
    ipl_ratio = np.where(eligible["pressure_balls"] > 0, eligible["ipl_pressure_balls"] / eligible["pressure_balls"], 0.0)
    ipl_multiplier = 1.0 + (ipl_ratio * 0.15)

    eligible["pressure_score"] = np.round(
        (0.40 * quality + 0.25 * uplift + 0.20 * consistency + 0.15 * volume) * ipl_multiplier,
        2
    )

    eligible["rank"] = eligible["pressure_score"].rank(ascending=False, method="min").astype(int)
    return eligible.sort_values("rank").reset_index(drop=True)

def score_bowlers(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates transparent composite PressureScore for eligible bowlers."""
    data = df.copy()

    # Eligibility filter
    eligible_mask = (
        (data["pressure_balls"] >= 80) &
        (data["baseline_balls"] >= 60) &
        (data["pressure_matches"] >= 5)
    )
    eligible = data[eligible_mask].copy()

    # 1. Restrictiveness / Economy in Clutch Situations (6.0 to 11.5 economy benchmark)
    econ_overall = np.clip((11.5 - eligible["pressure_economy"]) / (11.5 - 6.0), 0.0, 1.0) * 100.0
    econ_death = np.clip((11.5 - eligible["death_pressure_economy"]) / (11.5 - 6.0), 0.0, 1.0) * 100.0
    dot_q = np.clip((eligible["pressure_dot_pct"] - 28.0) / (50.0 - 28.0), 0.0, 1.0) * 100.0
    restrict_score = 0.45 * econ_overall + 0.35 * econ_death + 0.20 * dot_q

    # 2. Wicket Threat Under Pressure (Balls per wicket 11-24, total wickets volume)
    wkt_sr = np.clip((24.0 - eligible["pressure_balls_per_wicket"]) / (24.0 - 11.0), 0.0, 1.0) * 100.0
    wkt_vol = np.clip(eligible["pressure_wickets"] / 40.0, 0.0, 1.0) * 100.0
    threat_score = 0.65 * wkt_sr + 0.35 * wkt_vol

    # 3. Uplift & Baseline Resistance (diff between pressure and baseline economy)
    econ_diff = eligible["pressure_economy"] - eligible["baseline_economy"]
    uplift_score = np.clip((2.5 - econ_diff) / (2.5 - (-1.0)), 0.0, 1.0) * 100.0

    # 4. Consistency & Volume
    consistency_score = eligible["consistency_score"] * 100.0
    vol_score = np.clip(eligible["pressure_balls"] / 400.0, 0.0, 1.0) * 100.0

    # 5. IPL Relevance Multiplier
    ipl_ratio = np.where(eligible["pressure_balls"] > 0, eligible["ipl_pressure_balls"] / eligible["pressure_balls"], 0.0)
    ipl_multiplier = 1.0 + (ipl_ratio * 0.15)

    eligible["pressure_score"] = np.round(
        (0.35 * restrict_score + 0.30 * threat_score + 0.15 * uplift_score + 0.10 * consistency_score + 0.10 * vol_score) * ipl_multiplier,
        2
    )

    eligible["rank"] = eligible["pressure_score"].rank(ascending=False, method="min").astype(int)
    return eligible.sort_values("rank").reset_index(drop=True)

def run_ranking_pipeline(
    batting_metrics_df: pd.DataFrame = None,
    bowling_metrics_df: pd.DataFrame = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Scores, ranks, cuts official Top 10 lists and exports deliverables."""
    logger.info("Executing official scoring and ranking pipeline...")

    if batting_metrics_df is None:
        batting_metrics_df = pd.read_parquet(PROCESSED_DATA_DIR / "metrics_batting.parquet")
    if bowling_metrics_df is None:
        bowling_metrics_df = pd.read_parquet(PROCESSED_DATA_DIR / "metrics_bowling.parquet")

    RANKINGS_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)

    # Score full universes
    ranked_batters = score_batters(batting_metrics_df)
    ranked_bowlers = score_bowlers(bowling_metrics_df)

    # Official Top 10s
    top10_batters = ranked_batters.head(10).copy()
    top10_bowlers = ranked_bowlers.head(10).copy()

    # Cross-list duplicate check
    bat_ids = set(top10_batters["player_id"])
    bowl_ids = set(top10_bowlers["player_id"])
    overlap = bat_ids.intersection(bowl_ids)
    if overlap:
        logger.warning(f"Cross-list overlap detected for player IDs: {overlap}. Resolving priority.")
        for pid in overlap:
            # If batter score higher than bowler score, remove from bowler and shift
            b_score = top10_batters.loc[top10_batters["player_id"] == pid, "pressure_score"].values[0]
            bw_score = top10_bowlers.loc[top10_bowlers["player_id"] == pid, "pressure_score"].values[0]
            if b_score >= bw_score:
                ranked_bowlers = ranked_bowlers[ranked_bowlers["player_id"] != pid].reset_index(drop=True)
                ranked_bowlers["rank"] = range(1, len(ranked_bowlers) + 1)
                top10_bowlers = ranked_bowlers.head(10).copy()
            else:
                ranked_batters = ranked_batters[ranked_batters["player_id"] != pid].reset_index(drop=True)
                ranked_batters["rank"] = range(1, len(ranked_batters) + 1)
                top10_batters = ranked_batters.head(10).copy()

    # Re-index ranks 1 to 10 strictly
    top10_batters["rank"] = range(1, 11)
    top10_bowlers["rank"] = range(1, 11)

    # Near miss boards (11 to 20)
    near_miss_batters = ranked_batters.iloc[10:20].copy()
    near_miss_bowlers = ranked_bowlers.iloc[10:20].copy()

    # Export CSVs
    top10_batters.to_csv(RANKINGS_DIR / "top10_batters.csv", index=False)
    top10_bowlers.to_csv(RANKINGS_DIR / "top10_bowlers.csv", index=False)
    ranked_batters.to_csv(RANKINGS_DIR / "full_batter_rankings.csv", index=False)
    ranked_bowlers.to_csv(RANKINGS_DIR / "full_bowler_rankings.csv", index=False)
    
    near_miss = pd.concat([
        near_miss_batters.assign(category="Batter"),
        near_miss_bowlers.assign(category="Bowler")
    ])
    near_miss.to_csv(RANKINGS_DIR / "near_miss_11_20.csv", index=False)

    logger.info("Official Top 10 Batters and Bowlers exported successfully.")

    # Write Ranking QA Summary
    summary_lines = [
        "# PressurePulse — Official Top 10 Rankings (Draft Freeze)",
        "",
        "## 1. Official Top 10 Batters Under Pressure",
        "| Rank | Player Name | Primary Role | Pressure Score | Pressure Balls | Pressure SR | SR Uplift | Confidence |",
        "|:---:|---|---|:---:|:---:|:---:|:---:|:---:|"
    ]
    for _, r in top10_batters.iterrows():
        summary_lines.append(
            f"| **{r['rank']}** | {r['player_name']} | {r['primary_role']} | **{r['pressure_score']}** | "
            f"{int(r['pressure_balls'])} | {r['pressure_sr']:.1f} | {r['sr_uplift']:+.1f} | {r['sample_confidence']} |"
        )

    summary_lines.extend([
        "",
        "## 2. Official Top 10 Bowlers Under Pressure",
        "| Rank | Player Name | Primary Role | Pressure Score | Pressure Balls | Pressure Econ | Death Econ | Wickets | Confidence |",
        "|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|"
    ])
    for _, r in top10_bowlers.iterrows():
        summary_lines.append(
            f"| **{r['rank']}** | {r['player_name']} | {r['primary_role']} | **{r['pressure_score']}** | "
            f"{int(r['pressure_balls'])} | {r['pressure_economy']:.2f} | {r['death_pressure_economy']:.2f} | "
            f"{int(r['pressure_wickets'])} | {r['sample_confidence']} |"
        )

    summary_lines.extend([
        "",
        "## 3. Near-Miss Board (Ranks 11–15 Highlights)",
        "- **Batters:** " + ", ".join([f"#{r['rank']} {r['player_name']} ({r['pressure_score']})" for _, r in near_miss_batters.head(5).iterrows()]),
        "- **Bowlers:** " + ", ".join([f"#{r['rank']} {r['player_name']} ({r['pressure_score']})" for _, r in near_miss_bowlers.head(5).iterrows()]),
        "",
        "## 4. Verification & Integrity",
        f"- **No Duplicates within Batters List:** {top10_batters['player_id'].nunique() == 10}",
        f"- **No Duplicates within Bowlers List:** {top10_bowlers['player_id'].nunique() == 10}",
        f"- **No Cross-List Overlap:** {len(set(top10_batters['player_id']).intersection(set(top10_bowlers['player_id']))) == 0}",
        "- **Official View:** Combined IPL + T20I with IPL Auction Weighting (1.30x)."
    ])

    (QA_DIR / "ranking_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    return top10_batters, top10_bowlers

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_ranking_pipeline()
