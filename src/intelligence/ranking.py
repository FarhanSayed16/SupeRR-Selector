"""
PressurePulse — Scoring, Eligibility & Top 10 Ranking Service (L2)
Auction Official (IPL floors + weighted rates) and Global Combined boards.
"""

import logging
from typing import Tuple
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, RANKINGS_DIR, QA_DIR

logger = logging.getLogger(__name__)


def score_batters(df: pd.DataFrame, board: str = "auction") -> pd.DataFrame:
    data = df.copy()
    eligible_mask = (
        (data["pressure_balls"] >= CONFIG.MIN_PRESSURE_BALLS_FACED) &
        (data["baseline_balls"] >= CONFIG.MIN_BASELINE_BALLS_FACED) &
        (data["pressure_matches"] >= CONFIG.MIN_BATTER_MATCHES)
    )
    if board == "auction":
        eligible_mask = eligible_mask & (
            data["ipl_pressure_balls"] >= CONFIG.MIN_IPL_PRESSURE_BALLS_BATTER
        )
    eligible = data[eligible_mask].copy()
    if eligible.empty:
        return eligible

    sr_col = "weighted_pressure_sr" if "weighted_pressure_sr" in eligible.columns else "pressure_sr"
    uplift_src = eligible[sr_col] - eligible["baseline_sr"]

    sr_q = np.clip((eligible[sr_col] - 110.0) / (180.0 - 110.0), 0.0, 1.0) * 100.0
    bp_q = np.clip((eligible["pressure_boundary_pct"] - 12.0) / (28.0 - 12.0), 0.0, 1.0) * 100.0
    avg_q = np.clip((eligible["pressure_avg"] - 15.0) / (45.0 - 15.0), 0.0, 1.0) * 100.0
    quality = 0.50 * sr_q + 0.30 * bp_q + 0.20 * avg_q

    uplift = np.clip((uplift_src - (-10.0)) / (40.0 - (-10.0)), 0.0, 1.0) * 100.0
    consistency = eligible["consistency_score"] * 100.0
    volume = np.clip(eligible["pressure_balls"] / 250.0, 0.0, 1.0) * 100.0

    # Weights already baked into rates — no separate IPL multiplier
    eligible["pressure_score"] = np.round(
        0.40 * quality + 0.25 * uplift + 0.20 * consistency + 0.15 * volume, 2
    )
    # Display-only shrinkage toward eligible mean (does not replace pressure_score / freeze)
    if "reliability" not in eligible.columns:
        eligible["reliability"] = eligible["pressure_balls"] / (
            eligible["pressure_balls"] + float(CONFIG.RELIABILITY_K_BATTER)
        )
    league_mean = float(eligible["pressure_score"].mean())
    eligible["adjusted_display_score"] = np.round(
        league_mean + eligible["reliability"] * (eligible["pressure_score"] - league_mean), 2
    )
    eligible["board"] = board
    eligible["sr_uplift"] = uplift_src
    eligible["rank"] = eligible["pressure_score"].rank(ascending=False, method="min").astype(int)
    return eligible.sort_values(["rank", "pressure_balls"], ascending=[True, False]).reset_index(drop=True)


def score_bowlers(df: pd.DataFrame, board: str = "auction") -> pd.DataFrame:
    data = df.copy()
    eligible_mask = (
        (data["pressure_balls"] >= CONFIG.MIN_PRESSURE_BALLS_BOWLED) &
        (data["baseline_balls"] >= CONFIG.MIN_BASELINE_BALLS_BOWLED) &
        (data["pressure_matches"] >= CONFIG.MIN_BOWLER_MATCHES)
    )
    if board == "auction":
        eligible_mask = eligible_mask & (
            data["ipl_pressure_balls"] >= CONFIG.MIN_IPL_PRESSURE_BALLS_BOWLER
        )
    eligible = data[eligible_mask].copy()
    if eligible.empty:
        return eligible

    econ_col = "weighted_pressure_economy" if "weighted_pressure_economy" in eligible.columns else "pressure_economy"
    death_col = (
        "death_pressure_economy_capped"
        if "death_pressure_economy_capped" in eligible.columns
        else "death_pressure_economy"
    )

    econ_overall = np.clip((11.5 - eligible[econ_col]) / (11.5 - 6.0), 0.0, 1.0) * 100.0
    econ_death = np.clip((11.5 - eligible[death_col]) / (11.5 - 6.0), 0.0, 1.0) * 100.0
    dot_q = np.clip((eligible["pressure_dot_pct"] - 28.0) / (50.0 - 28.0), 0.0, 1.0) * 100.0
    restrict_score = 0.45 * econ_overall + 0.35 * econ_death + 0.20 * dot_q

    wkt_sr = np.clip((24.0 - eligible["pressure_balls_per_wicket"]) / (24.0 - 11.0), 0.0, 1.0) * 100.0
    wkt_vol = np.clip(eligible["pressure_wickets"] / 40.0, 0.0, 1.0) * 100.0
    threat_score = 0.65 * wkt_sr + 0.35 * wkt_vol

    econ_diff = eligible[econ_col] - eligible["baseline_economy"]
    uplift_score = np.clip((2.5 - econ_diff) / (2.5 - (-1.0)), 0.0, 1.0) * 100.0

    consistency_score = eligible["consistency_score"] * 100.0
    vol_score = np.clip(eligible["pressure_balls"] / 400.0, 0.0, 1.0) * 100.0

    eligible["pressure_score"] = np.round(
        0.35 * restrict_score + 0.30 * threat_score + 0.15 * uplift_score
        + 0.10 * consistency_score + 0.10 * vol_score,
        2
    )
    if "reliability" not in eligible.columns:
        eligible["reliability"] = eligible["pressure_balls"] / (
            eligible["pressure_balls"] + float(CONFIG.RELIABILITY_K_BOWLER)
        )
    league_mean = float(eligible["pressure_score"].mean())
    eligible["adjusted_display_score"] = np.round(
        league_mean + eligible["reliability"] * (eligible["pressure_score"] - league_mean), 2
    )
    eligible["board"] = board
    eligible["rank"] = eligible["pressure_score"].rank(ascending=False, method="min").astype(int)
    return eligible.sort_values(["rank", "pressure_balls"], ascending=[True, False]).reset_index(drop=True)


def _resolve_overlap(ranked_batters: pd.DataFrame, ranked_bowlers: pd.DataFrame):
    top10_batters = ranked_batters.head(10).copy()
    top10_bowlers = ranked_bowlers.head(10).copy()
    bat_ids = set(top10_batters["player_id"])
    bowl_ids = set(top10_bowlers["player_id"])
    overlap = bat_ids.intersection(bowl_ids)
    if not overlap:
        top10_batters["rank"] = range(1, len(top10_batters) + 1)
        top10_bowlers["rank"] = range(1, len(top10_bowlers) + 1)
        return ranked_batters, ranked_bowlers, top10_batters, top10_bowlers

    logger.warning(f"Cross-list overlap detected for player IDs: {overlap}. Resolving priority.")
    rb, rbw = ranked_batters.copy(), ranked_bowlers.copy()
    for pid in overlap:
        b_score = top10_batters.loc[top10_batters["player_id"] == pid, "pressure_score"].values[0]
        bw_score = top10_bowlers.loc[top10_bowlers["player_id"] == pid, "pressure_score"].values[0]
        if b_score >= bw_score:
            rbw = rbw[rbw["player_id"] != pid].reset_index(drop=True)
            rbw["rank"] = range(1, len(rbw) + 1)
            top10_bowlers = rbw.head(10).copy()
        else:
            rb = rb[rb["player_id"] != pid].reset_index(drop=True)
            rb["rank"] = range(1, len(rb) + 1)
            top10_batters = rb.head(10).copy()

    top10_batters = rb.head(10).copy()
    top10_bowlers = rbw.head(10).copy()
    top10_batters["rank"] = range(1, 11)
    top10_bowlers["rank"] = range(1, 11)
    return rb, rbw, top10_batters, top10_bowlers


def run_ranking_pipeline(
    batting_metrics_df: pd.DataFrame = None,
    bowling_metrics_df: pd.DataFrame = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Scores Auction Official + Global boards; exports Official as primary Top 10."""
    logger.info("Executing official scoring and ranking pipeline...")

    if batting_metrics_df is None:
        batting_metrics_df = pd.read_parquet(PROCESSED_DATA_DIR / "metrics_batting.parquet")
    if bowling_metrics_df is None:
        bowling_metrics_df = pd.read_parquet(PROCESSED_DATA_DIR / "metrics_bowling.parquet")

    RANKINGS_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)

    # Auction Official (primary)
    auction_bat = score_batters(batting_metrics_df, board="auction")
    auction_bowl = score_bowlers(bowling_metrics_df, board="auction")
    auction_bat, auction_bowl, top10_batters, top10_bowlers = _resolve_overlap(auction_bat, auction_bowl)

    # Global Combined (secondary)
    global_bat = score_batters(batting_metrics_df, board="global")
    global_bowl = score_bowlers(bowling_metrics_df, board="global")
    global_bat, global_bowl, global_top10_bat, global_top10_bowl = _resolve_overlap(global_bat, global_bowl)

    near_miss_batters = auction_bat.iloc[10:20].copy()
    near_miss_bowlers = auction_bowl.iloc[10:20].copy()

    # Exclusions: global top players missing from auction due to IPL floor
    auction_bat_ids = set(top10_batters["player_id"])
    auction_bowl_ids = set(top10_bowlers["player_id"])
    excluded_bat = global_top10_bat[~global_top10_bat["player_id"].isin(auction_bat_ids)].copy()
    excluded_bowl = global_top10_bowl[~global_top10_bowl["player_id"].isin(auction_bowl_ids)].copy()
    excluded_bat["exclusion_reason"] = "Below Auction Official IPL sample floor"
    excluded_bowl["exclusion_reason"] = "Below Auction Official IPL sample floor"

    top10_batters.to_csv(RANKINGS_DIR / "top10_batters.csv", index=False)
    top10_bowlers.to_csv(RANKINGS_DIR / "top10_bowlers.csv", index=False)
    global_top10_bat.to_csv(RANKINGS_DIR / "top10_batters_global.csv", index=False)
    global_top10_bowl.to_csv(RANKINGS_DIR / "top10_bowlers_global.csv", index=False)
    auction_bat.to_csv(RANKINGS_DIR / "full_batter_rankings.csv", index=False)
    auction_bowl.to_csv(RANKINGS_DIR / "full_bowler_rankings.csv", index=False)
    global_bat.to_csv(RANKINGS_DIR / "full_batter_rankings_global.csv", index=False)
    global_bowl.to_csv(RANKINGS_DIR / "full_bowler_rankings_global.csv", index=False)

    near_miss = pd.concat([
        near_miss_batters.assign(category="Batter"),
        near_miss_bowlers.assign(category="Bowler")
    ])
    near_miss.to_csv(RANKINGS_DIR / "near_miss_11_20.csv", index=False)

    excluded = pd.concat([
        excluded_bat.assign(category="Batter"),
        excluded_bowl.assign(category="Bowler")
    ], ignore_index=True)
    excluded.to_csv(RANKINGS_DIR / "excluded_low_ipl_sample.csv", index=False)

    logger.info("Official Top 10 Batters and Bowlers exported successfully.")

    summary_lines = [
        "# PressurePulse — Official Top 10 Rankings (Auction Official)",
        "",
        f"**Pressure version:** `{CONFIG.PRESSURE_VERSION}`",
        f"**IPL/T20I weights baked into rates:** {CONFIG.IPL_WEIGHT}x / {CONFIG.T20I_WEIGHT}x",
        f"**IPL floors:** bat ≥{CONFIG.MIN_IPL_PRESSURE_BALLS_BATTER}, bowl ≥{CONFIG.MIN_IPL_PRESSURE_BALLS_BOWLER}",
        "",
        "## 1. Auction Official Top 10 Batters",
        "| Rank | Player Name | Primary Role | Pressure Score | Pressure Balls | Weighted SR | SR Uplift | IPL% | Confidence |",
        "|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|"
    ]
    for _, r in top10_batters.iterrows():
        ipl_pct = 100 * float(r.get("ipl_pressure_share", 0) or 0)
        wsr = float(r.get("weighted_pressure_sr", r["pressure_sr"]))
        summary_lines.append(
            f"| **{r['rank']}** | {r['player_name']} | {r['primary_role']} | **{r['pressure_score']}** | "
            f"{int(r['pressure_balls'])} | {wsr:.1f} | {r['sr_uplift']:+.1f} | {ipl_pct:.0f}% | {r['sample_confidence']} |"
        )

    summary_lines.extend([
        "",
        "## 2. Auction Official Top 10 Bowlers",
        "| Rank | Player Name | Primary Role | Pressure Score | Pressure Balls | Weighted Econ | Death Econ* | Wickets | IPL% | Confidence |",
        "|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
    ])
    for _, r in top10_bowlers.iterrows():
        ipl_pct = 100 * float(r.get("ipl_pressure_share", 0) or 0)
        we = float(r.get("weighted_pressure_economy", r["pressure_economy"]))
        de = float(r.get("death_pressure_economy_capped", r["death_pressure_economy"]))
        summary_lines.append(
            f"| **{r['rank']}** | {r['player_name']} | {r['primary_role']} | **{r['pressure_score']}** | "
            f"{int(r['pressure_balls'])} | {we:.2f} | {de:.2f} | "
            f"{int(r['pressure_wickets'])} | {ipl_pct:.0f}% | {r['sample_confidence']} |"
        )

    summary_lines.extend([
        "",
        "## 3. Global Combined Top 10 (secondary)",
        "- **Batters:** " + ", ".join([f"#{r['rank']} {r['player_name']}" for _, r in global_top10_bat.iterrows()]),
        "- **Bowlers:** " + ", ".join([f"#{r['rank']} {r['player_name']}" for _, r in global_top10_bowl.iterrows()]),
        "",
        "## 4. Excluded from Auction Official (in Global Top 10, low IPL sample)",
        "- **Batters:** " + (", ".join(excluded_bat["player_name"].tolist()) if len(excluded_bat) else "None"),
        "- **Bowlers:** " + (", ".join(excluded_bowl["player_name"].tolist()) if len(excluded_bowl) else "None"),
        "",
        "## 5. Verification",
        f"- **No Duplicates within Batters:** {top10_batters['player_id'].nunique() == 10}",
        f"- **No Duplicates within Bowlers:** {top10_bowlers['player_id'].nunique() == 10}",
        f"- **No Cross-List Overlap:** {len(set(top10_batters['player_id']).intersection(set(top10_bowlers['player_id']))) == 0}",
        f"- **Official view:** Auction Official with IPL-weighted rates ({CONFIG.IPL_WEIGHT}x / {CONFIG.T20I_WEIGHT}x).",
    ])

    (QA_DIR / "ranking_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    return top10_batters, top10_bowlers


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_ranking_pipeline()
