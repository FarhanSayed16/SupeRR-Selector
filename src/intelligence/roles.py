"""
PressurePulse — Player Role Classification Service (L2)
Classifies players into distinct cricketing roles (Batter, Bowler, All-Rounder, WK)
and establishes eligibility gates for the Top 10 Batters and Top 10 Bowlers rankings.
"""

import logging
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR, EXTERNAL_DATA_DIR

logger = logging.getLogger(__name__)

def classify_player_roles(
    delivery_df: pd.DataFrame = None,
    xi_df: pd.DataFrame = None,
    player_df: pd.DataFrame = None,
    save_parquet: bool = True
) -> pd.DataFrame:
    """
    Computes career ball volume and role indicators for all players.
    Applies role taxonomy and outputs dim_player_roles.
    """
    logger.info("Starting player role classification...")

    if delivery_df is None:
        delivery_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet")
    if xi_df is None:
        xi_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_playing_eleven.parquet")
    if player_df is None:
        player_df = pd.read_parquet(PROCESSED_DATA_DIR / "dim_player.parquet")

    # 1. Batting career stats
    bat = delivery_df.groupby("striker_id").agg(
        career_balls_faced=("runs", "count"),
        career_runs_scored=("runs", "sum"),
        career_matches_batted=("match_id", "nunique"),
        pressure_balls_faced=("is_pressure", lambda x: int(x.sum())),
        baseline_balls_faced=("is_pressure", lambda x: int((~x).sum()))
    ).reset_index().rename(columns={"striker_id": "player_id"})

    # 2. Bowling career stats (legal balls for bowling)
    # Bowler conceded runs = runs + extras except byes/legbyes
    bowler_extras_mask = ~delivery_df["extras_type"].isin(["byes", "legbyes"])
    bowler_runs_series = delivery_df["runs"] + np.where(bowler_extras_mask, delivery_df["extras1_runs"] + delivery_df["extras_2_runs"], 0)
    delivery_df["bowler_runs_conceded"] = bowler_runs_series

    bowl = delivery_df.groupby("bowler_id").agg(
        career_balls_bowled=("runs", "count"),
        career_legal_balls_bowled=("is_legal_ball", "sum"),
        career_runs_conceded=("bowler_runs_conceded", "sum"),
        career_wickets=("is_wicket", "sum"),
        career_matches_bowled=("match_id", "nunique"),
        pressure_balls_bowled=("is_pressure", lambda x: int(x.sum())),
        baseline_balls_bowled=("is_pressure", lambda x: int((~x).sum()))
    ).reset_index().rename(columns={"bowler_id": "player_id"})

    # 3. Wicketkeeping & Fielding attributes from playing XI
    wk_players = set(xi_df[xi_df["is_wk"] == True]["player_id"])
    captain_players = set(xi_df[xi_df["is_captain"] == True]["player_id"])

    # 4. Merge onto master player dimension
    m = player_df.merge(bat, on="player_id", how="left").merge(bowl, on="player_id", how="left")
    
    # Fill nulls for non-batters or non-bowlers
    count_cols = [
        "career_balls_faced", "career_runs_scored", "career_matches_batted",
        "pressure_balls_faced", "baseline_balls_faced",
        "career_balls_bowled", "career_legal_balls_bowled", "career_runs_conceded",
        "career_wickets", "career_matches_bowled",
        "pressure_balls_bowled", "baseline_balls_bowled"
    ]
    for col in count_cols:
        m[col] = m[col].fillna(0).astype(int)

    m["is_wicketkeeper"] = m["player_id"].isin(wk_players)
    m["has_captained"] = m["player_id"].isin(captain_players)

    # 5. Role Classification Algorithm
    # Ratios and thresholds
    bf = m["career_balls_faced"]
    bb = m["career_balls_bowled"]

    def determine_role(row):
        f = row["career_balls_faced"]
        b = row["career_balls_bowled"]
        is_wk = row["is_wicketkeeper"]

        # Wicketkeepers are batters
        if is_wk and b < 30:
            return "Wicketkeeper-Batter"
        
        # Pure Batter: high balls faced, minimal balls bowled
        if f >= 40 and b < 30:
            return "Batter"
        
        # Pure Bowler: high balls bowled, minimal balls faced
        if b >= 40 and f < 40:
            return "Bowler"
        
        # Both high volume: All-Rounder
        if f >= 60 and b >= 60:
            if f >= b * 1.5:
                return "Batting All-Rounder"
            elif b >= f * 1.5:
                return "Bowling All-Rounder"
            else:
                return "All-Rounder"
        
        # Intermediate cases
        if f >= 30 and b < 30:
            return "Batter"
        if b >= 30 and f < 30:
            return "Bowler"
        if f >= b:
            return "Batter" if b == 0 else "Batting All-Rounder"
        else:
            return "Bowler" if f == 0 else "Bowling All-Rounder"

    m["primary_role"] = m.apply(determine_role, axis=1)

    # 6. Apply Manual Overrides if present in external template
    override_file = EXTERNAL_DATA_DIR / "player_roles_override_template.csv"
    if override_file.exists():
        try:
            overrides = pd.read_csv(override_file)
            if not overrides.empty and "player_id" in overrides.columns and "role_override" in overrides.columns:
                override_dict = overrides.set_index("player_id")["role_override"].dropna().to_dict()
                for pid, o_role in override_dict.items():
                    mask = m["player_id"] == pid
                    if mask.any():
                        logger.info(f"Applying manual role override for player {pid} -> {o_role}")
                        m.loc[mask, "primary_role"] = o_role
        except Exception as e:
            logger.warning(f"Could not load role overrides: {e}")

    # 7. Category Eligibility Flags
    # Batters list eligibility: Batters, WKs, and all All-Rounders with sufficient pressure batting sample
    all_rounder_roles = ["Batter", "Wicketkeeper-Batter", "Batting All-Rounder", "All-Rounder", "Bowling All-Rounder"]
    m["eligible_as_batter"] = (
        m["primary_role"].isin(all_rounder_roles) &
        (m["primary_role"] != "Bowler") &
        (m["pressure_balls_faced"] >= CONFIG.MIN_PRESSURE_BALLS_FACED) &
        (m["career_matches_batted"] >= CONFIG.MIN_BATTER_MATCHES)
    )

    # Bowlers list eligibility: Bowlers and all All-Rounders with sufficient pressure bowling sample
    bowler_roles = ["Bowler", "Bowling All-Rounder", "All-Rounder", "Batting All-Rounder"]
    m["eligible_as_bowler"] = (
        m["primary_role"].isin(bowler_roles) &
        (~m["primary_role"].isin(["Batter", "Wicketkeeper-Batter"])) &
        (m["pressure_balls_bowled"] >= CONFIG.MIN_PRESSURE_BALLS_BOWLED) &
        (m["career_matches_bowled"] >= CONFIG.MIN_BOWLER_MATCHES)
    )

    logger.info(
        f"Player role classification complete: {len(m)} players processed. "
        f"Eligible Batters: {m['eligible_as_batter'].sum()}, "
        f"Eligible Bowlers: {m['eligible_as_bowler'].sum()}"
    )

    # 8. Persist Parquet & QA Summary
    if save_parquet:
        out_parquet = PROCESSED_DATA_DIR / "dim_player_roles.parquet"
        m.to_parquet(out_parquet, index=False)
        logger.info(f"Persisted player roles dimension to {out_parquet}")

        # QA summary
        role_counts = m["primary_role"].value_counts().to_dict()
        qa_lines = [
            "# PressurePulse — Player Role Classification Summary",
            "",
            "## 1. Role Distribution Across All 1,217 Players",
            "| Primary Role | Count | % of Universe |",
            "|---|---|---|",
        ]
        for role, count in role_counts.items():
            qa_lines.append(f"| {role} | {count:,} | {count/len(m)*100:.1f}% |")

        qa_lines.extend([
            "",
            "## 2. Eligibility Gating (Pressure Volume >= 30 balls, Matches >= 5)",
            f"- **Eligible Batters Pool:** {m['eligible_as_batter'].sum():,} players",
            f"- **Eligible Bowlers Pool:** {m['eligible_as_bowler'].sum():,} players",
            f"- **Dual-Eligible All-Rounders:** {(m['eligible_as_batter'] & m['eligible_as_bowler']).sum():,} players",
            "",
            "## 3. Spot-Check Validation of Prominent Players",
            "| Player | Role | Pressure BF | Pressure BB | Eligible Batter | Eligible Bowler |",
            "|---|---|---|---|---|---|"
        ])

        sample_pids = [8, 47, 813, 2933, 3330, 1318, 2876, 4722]
        samples = m[m["player_id"].isin(sample_pids)].sort_values("career_balls_faced", ascending=False)
        for _, r in samples.iterrows():
            qa_lines.append(
                f"| {r['player_name']} | {r['primary_role']} | {r['pressure_balls_faced']} | "
                f"{r['pressure_balls_bowled']} | {r['eligible_as_batter']} | {r['eligible_as_bowler']} |"
            )

        (QA_DIR / "player_roles_summary.md").write_text("\n".join(qa_lines), encoding="utf-8")

    return m

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    classify_player_roles()
