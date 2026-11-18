"""
PressurePulse — Batting Metrics Service (L2)
Legal-ball pressure vs baseline metrics, IPL/T20I weighted rates, uplift, consistency.
"""

import logging
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR

logger = logging.getLogger(__name__)


def _weighted_rate(runs_a, balls_a, runs_b, balls_b, w_a, w_b):
    """Blend two domain samples into a single rate (runs per 100 balls)."""
    num = runs_a * w_a + runs_b * w_b
    den = balls_a * w_a + balls_b * w_b
    return np.where(den > 0, (num / den) * 100.0, 0.0)


def compute_batting_metrics(
    delivery_df: pd.DataFrame = None,
    roles_df: pd.DataFrame = None,
    save_parquet: bool = True
) -> pd.DataFrame:
    logger.info("Computing batting metrics for eligible players...")

    if delivery_df is None:
        delivery_df = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet")
    if roles_df is None:
        roles_df = pd.read_parquet(PROCESSED_DATA_DIR / "dim_player_roles.parquet")

    eligible_pids = set(roles_df[roles_df["eligible_as_batter"]]["player_id"])
    df = delivery_df[delivery_df["striker_id"].isin(eligible_pids)].copy()
    df["is_striker_out"] = df["is_wicket"] & (df["dismissed_player_id"] == df["striker_id"])

    def aggregate_batting(data: pd.DataFrame, prefix: str) -> pd.DataFrame:
        # Legal balls only for SR / balls / dots / boundaries
        legal = data[data["is_legal_ball"]].copy() if len(data) else data
        if len(legal) == 0:
            return pd.DataFrame(columns=[
                "player_id", f"{prefix}_runs", f"{prefix}_balls", f"{prefix}_matches",
                f"{prefix}_sr", f"{prefix}_dot_pct", f"{prefix}_boundary_pct",
                f"{prefix}_dismissals", f"{prefix}_avg"
            ])

        agg = legal.groupby("striker_id").agg(
            runs=("runs", "sum"),
            balls=("is_legal_ball", "sum"),
            dots=("runs", lambda x: int((x == 0).sum())),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            dismissals=("is_striker_out", "sum"),
            matches=("match_id", "nunique")
        ).reset_index().rename(columns={"striker_id": "player_id"})

        agg[f"{prefix}_runs"] = agg["runs"]
        agg[f"{prefix}_balls"] = agg["balls"]
        agg[f"{prefix}_matches"] = agg["matches"]
        agg[f"{prefix}_sr"] = np.where(agg["balls"] > 0, (agg["runs"] / agg["balls"]) * 100.0, 0.0)
        agg[f"{prefix}_dot_pct"] = np.where(agg["balls"] > 0, (agg["dots"] / agg["balls"]) * 100.0, 0.0)
        agg[f"{prefix}_boundary_pct"] = np.where(
            agg["balls"] > 0, ((agg["fours"] + agg["sixes"]) / agg["balls"]) * 100.0, 0.0
        )
        agg[f"{prefix}_dismissals"] = agg["dismissals"]
        agg[f"{prefix}_avg"] = np.where(
            agg["dismissals"] > 0, agg["runs"] / agg["dismissals"], agg["runs"].astype(float)
        )

        return agg[[
            "player_id", f"{prefix}_runs", f"{prefix}_balls", f"{prefix}_matches",
            f"{prefix}_sr", f"{prefix}_dot_pct", f"{prefix}_boundary_pct",
            f"{prefix}_dismissals", f"{prefix}_avg"
        ]]

    df_pressure = df[df["is_pressure"]]
    df_baseline = df[~df["is_pressure"]]

    bat_pressure = aggregate_batting(df_pressure, "pressure")
    bat_baseline = aggregate_batting(df_baseline, "baseline")

    df_ipl_pressure = df[df["is_pressure"] & df["is_ipl"]]
    df_t20i_pressure = df[df["is_pressure"] & df["is_t20i"]]
    bat_ipl = aggregate_batting(df_ipl_pressure, "ipl_pressure")[
        ["player_id", "ipl_pressure_balls", "ipl_pressure_sr", "ipl_pressure_runs"]
    ]
    bat_t20i = aggregate_batting(df_t20i_pressure, "t20i_pressure")[
        ["player_id", "t20i_pressure_balls", "t20i_pressure_sr", "t20i_pressure_runs"]
    ]

    df_pp = df[df["is_pressure"] & (df["match_phase"] == "powerplay")]
    df_mid = df[df["is_pressure"] & (df["match_phase"] == "middle")]
    df_death = df[df["is_pressure"] & (df["match_phase"] == "death")]
    df_chase = df[df["is_pressure"] & (df["innings"] == 2)]
    df_collapse = df[df["is_pressure"] & df["signal_collapse_defense"]]
    df_vs_pace = df[df["is_pressure"] & (df["pace_or_spin"] == "Pace")]
    df_vs_spin = df[df["is_pressure"] & (df["pace_or_spin"] == "Spin")]

    bat_pp = aggregate_batting(df_pp, "pp_pressure")[
        ["player_id", "pp_pressure_balls", "pp_pressure_sr", "pp_pressure_dot_pct"]
    ]
    bat_mid = aggregate_batting(df_mid, "mid_pressure")[
        ["player_id", "mid_pressure_balls", "mid_pressure_sr", "mid_pressure_dot_pct"]
    ]
    bat_death = aggregate_batting(df_death, "death_pressure")[
        ["player_id", "death_pressure_balls", "death_pressure_sr", "death_pressure_dot_pct"]
    ]
    bat_chase = aggregate_batting(df_chase, "chase_pressure")[
        ["player_id", "chase_pressure_balls", "chase_pressure_sr"]
    ]
    bat_collapse = aggregate_batting(df_collapse, "collapse_pressure")[
        ["player_id", "collapse_pressure_balls", "collapse_pressure_sr"]
    ]
    bat_vs_pace = aggregate_batting(df_vs_pace, "vs_pace_pressure")[
        ["player_id", "vs_pace_pressure_balls", "vs_pace_pressure_sr"]
    ]
    bat_vs_spin = aggregate_batting(df_vs_spin, "vs_spin_pressure")[
        ["player_id", "vs_spin_pressure_balls", "vs_spin_pressure_sr"]
    ]

    legal_pressure = df_pressure[df_pressure["is_legal_ball"]]
    match_pressure = legal_pressure.groupby(["striker_id", "match_id"]).agg(
        m_runs=("runs", "sum"),
        m_balls=("is_legal_ball", "sum")
    ).reset_index()
    match_pressure = match_pressure[match_pressure["m_balls"] > 0]
    match_pressure["m_sr"] = (match_pressure["m_runs"] / match_pressure["m_balls"]) * 100.0

    consistency = match_pressure.groupby("striker_id").agg(
        sr_std=("m_sr", "std"),
        sr_mean=("m_sr", "mean"),
        matches_scored=("m_runs", "count")
    ).reset_index().rename(columns={"striker_id": "player_id"})
    consistency["sr_cv"] = np.where(
        (consistency["sr_mean"] > 0) & (consistency["sr_std"].notnull()),
        consistency["sr_std"] / consistency["sr_mean"],
        1.0
    )
    consistency["consistency_score"] = np.clip(1.0 - (consistency["sr_cv"] / 2.0), 0.1, 1.0)
    consistency_cols = consistency[["player_id", "consistency_score", "sr_cv"]]

    m = roles_df[roles_df["eligible_as_batter"]].copy()
    m = m.merge(bat_pressure, on="player_id", how="left")
    m = m.merge(bat_baseline, on="player_id", how="left")
    m = m.merge(bat_ipl, on="player_id", how="left")
    m = m.merge(bat_t20i, on="player_id", how="left")
    m = m.merge(bat_pp, on="player_id", how="left")
    m = m.merge(bat_mid, on="player_id", how="left")
    m = m.merge(bat_death, on="player_id", how="left")
    m = m.merge(bat_chase, on="player_id", how="left")
    m = m.merge(bat_collapse, on="player_id", how="left")
    m = m.merge(bat_vs_pace, on="player_id", how="left")
    m = m.merge(bat_vs_spin, on="player_id", how="left")
    m = m.merge(consistency_cols, on="player_id", how="left")

    fill_zeros = [
        "pressure_runs", "pressure_balls", "pressure_matches", "pressure_sr",
        "pressure_dot_pct", "pressure_boundary_pct", "pressure_dismissals", "pressure_avg",
        "ipl_pressure_balls", "ipl_pressure_sr", "ipl_pressure_runs",
        "t20i_pressure_balls", "t20i_pressure_sr", "t20i_pressure_runs",
        "pp_pressure_balls", "pp_pressure_sr", "pp_pressure_dot_pct",
        "mid_pressure_balls", "mid_pressure_sr", "mid_pressure_dot_pct",
        "death_pressure_balls", "death_pressure_sr", "death_pressure_dot_pct",
        "chase_pressure_balls", "chase_pressure_sr",
        "collapse_pressure_balls", "collapse_pressure_sr",
        "vs_pace_pressure_balls", "vs_pace_pressure_sr",
        "vs_spin_pressure_balls", "vs_spin_pressure_sr",
        "baseline_runs", "baseline_balls", "baseline_sr", "baseline_dot_pct",
        "baseline_boundary_pct", "baseline_avg", "baseline_matches", "baseline_dismissals"
    ]
    for col in fill_zeros:
        if col in m.columns:
            m[col] = m[col].fillna(0.0)

    m["consistency_score"] = m["consistency_score"].fillna(0.50)

    # IPL/T20I weighted pressure rates (Auction Official scoring inputs)
    w_ipl, w_t20 = CONFIG.IPL_WEIGHT, CONFIG.T20I_WEIGHT
    m["weighted_pressure_sr"] = _weighted_rate(
        m["ipl_pressure_runs"], m["ipl_pressure_balls"],
        m["t20i_pressure_runs"], m["t20i_pressure_balls"],
        w_ipl, w_t20
    )
    # Fallback when no domain split: use combined legal-ball pressure SR
    no_domain = (m["ipl_pressure_balls"] + m["t20i_pressure_balls"]) <= 0
    m.loc[no_domain, "weighted_pressure_sr"] = m.loc[no_domain, "pressure_sr"]

    m["ipl_pressure_share"] = np.where(
        m["pressure_balls"] > 0, m["ipl_pressure_balls"] / m["pressure_balls"], 0.0
    )

    m["sr_uplift"] = m["weighted_pressure_sr"] - m["baseline_sr"]
    m["dot_reduction"] = m["baseline_dot_pct"] - m["pressure_dot_pct"]
    m["boundary_uplift"] = m["pressure_boundary_pct"] - m["baseline_boundary_pct"]
    m["avg_uplift"] = m["pressure_avg"] - m["baseline_avg"]

    conditions = [
        m["pressure_balls"] >= CONFIG.CONFIDENCE_HIGH_BALLS,
        m["pressure_balls"] >= CONFIG.CONFIDENCE_MED_BALLS
    ]
    m["sample_confidence"] = np.select(conditions, ["High", "Medium"], default="Low")

    # Display-only reliability (does not feed PressureScore)
    k = float(CONFIG.RELIABILITY_K_BATTER)
    m["reliability"] = np.round(m["pressure_balls"] / (m["pressure_balls"] + k), 3)

    logger.info(f"Batting metrics computed for {len(m)} eligible batters.")

    if save_parquet:
        out_parquet = PROCESSED_DATA_DIR / "metrics_batting.parquet"
        m.to_parquet(out_parquet, index=False)
        logger.info(f"Persisted batting metrics to {out_parquet}")

        qa_lines = [
            "# PressurePulse — Batting Metrics & Uplift Summary",
            "",
            "## Top uplift (min 100 legal pressure balls)",
            "| Player | Pressure Balls | Weighted SR | Baseline SR | SR Uplift | IPL% |",
            "|---|---|---|---|---|---|"
        ]
        top_uplift = m[m["pressure_balls"] >= 100].sort_values("sr_uplift", ascending=False).head(10)
        for _, r in top_uplift.iterrows():
            qa_lines.append(
                f"| {r['player_name']} | {int(r['pressure_balls'])} | {r['weighted_pressure_sr']:.1f} | "
                f"{r['baseline_sr']:.1f} | {r['sr_uplift']:+.1f} | {100 * r['ipl_pressure_share']:.0f}% |"
            )
        (QA_DIR / "batting_metrics_summary.md").write_text("\n".join(qa_lines), encoding="utf-8")

    return m


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    compute_batting_metrics()
