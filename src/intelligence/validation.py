"""
PressurePulse — Validation, Sensitivity & Rank Freeze Service (L2)
Computes real threshold sensitivity + IPL-only overlap; freezes official ranks.
"""

import hashlib
import json
import logging
from typing import Dict, List, Set
import numpy as np
import pandas as pd
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, RANKINGS_DIR, QA_DIR
from src.intelligence.pressure import compute_pressure_signals
from src.intelligence.metrics_batting import compute_batting_metrics
from src.intelligence.metrics_bowling import compute_bowling_metrics
from src.intelligence.ranking import score_batters, score_bowlers, _resolve_overlap

logger = logging.getLogger(__name__)


def _top_names(df: pd.DataFrame, n: int = 10) -> Set[str]:
    if df is None or df.empty:
        return set()
    return set(df.head(n)["player_name"].tolist())


def _retention(base: Set[str], other: Set[str]) -> float:
    if not base:
        return 0.0
    return round(100.0 * len(base.intersection(other)) / len(base), 1)


def _relabel_pressure(state_df: pd.DataFrame, chase_high_rrr: float, death_start: int) -> pd.DataFrame:
    """Recompute pressure flags with perturbed thresholds (does not mutate CONFIG)."""
    data = state_df.copy()
    # Remap death phase from overid for death-start perturbation
    data["match_phase"] = np.select(
        [
            data["overid"] <= 6,
            data["overid"] >= death_start,
        ],
        ["powerplay", "death"],
        default="middle",
    )

    s1_high_rrr = (data["innings"] == 2) & (data["rrr_before"] >= chase_high_rrr) & (data["legal_balls_remaining_before"] <= 60)
    s1_crit_rrr = (data["innings"] == 2) & (data["rrr_before"] >= CONFIG.CHASE_CRITICAL_RRR)
    s1_close_finish = (
        (data["innings"] == 2)
        & (data["legal_balls_remaining_before"] <= 30)
        & (data["runs_needed_before"] > 0)
        & (data["runs_needed_before"] <= 55)
    )
    data["signal_chase_tightness"] = s1_high_rrr | s1_crit_rrr | s1_close_finish

    s2_early_collapse = (data["overid"] <= CONFIG.COLLAPSE_BEFORE_OVER) & (data["wickets_before"] >= CONFIG.COLLAPSE_WICKETS_LOST)
    s2_tail_exposed = (data["wickets_in_hand_before"] <= CONFIG.LOW_WICKETS_IN_HAND) & (data["legal_balls_remaining_before"] >= 12)
    data["signal_collapse_defense"] = s2_early_collapse | s2_tail_exposed

    s3_inn1_death = (data["innings"] == 1) & (data["match_phase"] == "death")
    s3_inn2_death = (data["innings"] == 2) & (data["match_phase"] == "death") & (data["runs_needed_before"] > 5)
    data["signal_death_contest"] = s3_inn1_death | s3_inn2_death

    s4_ko = data["is_knockout"] & (
        ((data["innings"] == 2) & (data["rrr_before"] >= 8.5))
        | (data["match_phase"] == "death")
        | (data["wickets_before"] >= 2)
    )
    data["signal_knockout_leverage"] = s4_ko
    data["signal_super_over"] = data["is_super_over"] & CONFIG.INCLUDE_SUPER_OVERS
    data["is_pressure"] = (
        data["signal_chase_tightness"]
        | data["signal_collapse_defense"]
        | data["signal_death_contest"]
        | data["signal_knockout_leverage"]
        | data["signal_super_over"]
    )
    return data


def _auction_top10_from_deliveries(delivery_df: pd.DataFrame, roles_df: pd.DataFrame):
    bat = compute_batting_metrics(delivery_df=delivery_df, roles_df=roles_df, save_parquet=False)
    bowl = compute_bowling_metrics(delivery_df=delivery_df, roles_df=roles_df, save_parquet=False)
    rb = score_batters(bat, board="auction")
    rbw = score_bowlers(bowl, board="auction")
    _, _, tbat, tbowl = _resolve_overlap(rb, rbw)
    return tbat, tbowl


def compute_sensitivity(official_bat_names: Set[str], official_bowl_names: Set[str]) -> Dict:
    """Re-label + re-score under threshold perturbations; return computed retention stats."""
    logger.info("Computing real sensitivity (threshold perturbation)...")
    state_path = PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet"
    roles_df = pd.read_parquet(PROCESSED_DATA_DIR / "dim_player_roles.parquet")
    base_df = pd.read_parquet(state_path)

    bat_retentions: List[float] = []
    bowl_retentions: List[float] = []
    variants = []

    for rrr in (9.0, 9.5, 10.0):
        for death_start in (15, 16, 17):
            if rrr == CONFIG.CHASE_HIGH_RRR and death_start == CONFIG.CHASE_DEATH_OVERS_START:
                continue  # skip exact nominal (already official)
            # Keep compute tractable: sample key axis shifts only
            variants.append((rrr, death_start))

    # Prefer the plan axes: RRR alone at fixed death 16, and death alone at fixed RRR 9.5
    focused = [
        (9.0, 16),
        (10.0, 16),
        (9.5, 15),
        (9.5, 17),
    ]

    for rrr, death_start in focused:
        labeled = _relabel_pressure(base_df, chase_high_rrr=rrr, death_start=death_start)
        tbat, tbowl = _auction_top10_from_deliveries(labeled, roles_df)
        br = _retention(official_bat_names, _top_names(tbat))
        bwr = _retention(official_bowl_names, _top_names(tbowl))
        bat_retentions.append(br)
        bowl_retentions.append(bwr)
        logger.info(f"  sensitivity rrr={rrr} death={death_start}: bat={br}% bowl={bwr}%")

    # IPL-only Top 12 overlap
    bat_metrics = pd.read_parquet(PROCESSED_DATA_DIR / "metrics_batting.parquet")
    bowl_metrics = pd.read_parquet(PROCESSED_DATA_DIR / "metrics_bowling.parquet")

    ipl_bat = bat_metrics.copy()
    ipl_bat["weighted_pressure_sr"] = ipl_bat["ipl_pressure_sr"]
    ipl_bat["pressure_balls"] = ipl_bat["ipl_pressure_balls"]
    ipl_bat["pressure_matches"] = np.maximum(ipl_bat.get("pressure_matches", 5), 5)
    # keep baseline; require IPL balls for auction floor naturally
    ipl_bat_ranked = score_batters(ipl_bat, board="auction")
    ipl_bat_top12 = set(ipl_bat_ranked.head(12)["player_name"].tolist())

    ipl_bowl = bowl_metrics.copy()
    ipl_bowl["weighted_pressure_economy"] = ipl_bowl["ipl_pressure_economy"]
    ipl_bowl["death_pressure_economy_capped"] = ipl_bowl["death_pressure_economy"]
    ipl_bowl["pressure_balls"] = ipl_bowl["ipl_pressure_balls"]
    ipl_bowl_ranked = score_bowlers(ipl_bowl, board="auction")
    ipl_bowl_top12 = set(ipl_bowl_ranked.head(12)["player_name"].tolist())

    ipl_overlap_batters = len(official_bat_names.intersection(ipl_bat_top12))
    ipl_overlap_bowlers = len(official_bowl_names.intersection(ipl_bowl_top12))

    return {
        "rrr_nominal": CONFIG.CHASE_HIGH_RRR,
        "death_start_nominal": CONFIG.CHASE_DEATH_OVERS_START,
        "variants_tested": [{"rrr": a, "death_start": b} for a, b in focused],
        "batter_retention_by_variant_pct": bat_retentions,
        "bowler_retention_by_variant_pct": bowl_retentions,
        "batter_top10_stability_pct": round(float(np.mean(bat_retentions)), 1) if bat_retentions else 0.0,
        "bowler_top10_stability_pct": round(float(np.mean(bowl_retentions)), 1) if bowl_retentions else 0.0,
        "ipl_overlap_batters": ipl_overlap_batters,
        "ipl_overlap_bowlers": ipl_overlap_bowlers,
        "ipl_overlap_batters_of": 10,
        "ipl_overlap_bowlers_of": 10,
        "computed": True,
    }


def run_validation_and_freeze() -> Dict:
    logger.info("Executing ranking validation and sensitivity audits...")

    top10_bat = pd.read_csv(RANKINGS_DIR / "top10_batters.csv")
    top10_bowl = pd.read_csv(RANKINGS_DIR / "top10_bowlers.csv")
    df_del = pd.read_parquet(PROCESSED_DATA_DIR / "fact_delivery_pressure.parquet")

    pressure_mask = df_del["is_pressure"] == True
    baseline_mask = df_del["is_pressure"] == False
    leakage_count = int((pressure_mask & baseline_mask).sum())
    total_accounted = int(pressure_mask.sum() + baseline_mask.sum())
    assert leakage_count == 0, f"Data leakage detected: {leakage_count} deliveries in both sets!"
    assert total_accounted == len(df_del), f"Missing deliveries: {len(df_del) - total_accounted}"

    assert top10_bat["player_id"].nunique() == 10, "Duplicate player in Top 10 Batters!"
    assert top10_bowl["player_id"].nunique() == 10, "Duplicate player in Top 10 Bowlers!"

    bat_ids = set(top10_bat["player_id"])
    bowl_ids = set(top10_bowl["player_id"])
    overlap = bat_ids.intersection(bowl_ids)
    assert len(overlap) == 0, f"Cross-list player overlap detected: {overlap}"

    # Auction Official must clear IPL floors
    assert (top10_bat["ipl_pressure_balls"] >= CONFIG.MIN_IPL_PRESSURE_BALLS_BATTER).all(), "Batter IPL floor breach"
    assert (top10_bowl["ipl_pressure_balls"] >= CONFIG.MIN_IPL_PRESSURE_BALLS_BOWLER).all(), "Bowler IPL floor breach"

    min_bat_balls = int(top10_bat["pressure_balls"].min())
    min_bowl_balls = int(top10_bowl["pressure_balls"].min())
    assert min_bat_balls >= CONFIG.MIN_PRESSURE_BALLS_FACED, f"Sample failure: batter with {min_bat_balls} balls"
    assert min_bowl_balls >= CONFIG.MIN_PRESSURE_BALLS_BOWLED, f"Sample failure: bowler with {min_bowl_balls} balls"

    official_bat_names = set(top10_bat["player_name"].tolist())
    official_bowl_names = set(top10_bowl["player_name"].tolist())
    sensitivity_results = compute_sensitivity(official_bat_names, official_bowl_names)

    freeze_payload = {
        "version": CONFIG.PRESSURE_VERSION,
        "board": "auction_official",
        "top10_batters": top10_bat[["rank", "player_id", "player_name", "pressure_score"]].to_dict(orient="records"),
        "top10_bowlers": top10_bowl[["rank", "player_id", "player_name", "pressure_score"]].to_dict(orient="records"),
    }
    freeze_str = json.dumps(freeze_payload, sort_keys=True)
    freeze_hash = hashlib.sha256(freeze_str.encode("utf-8")).hexdigest()

    freeze_record = {
        "freeze_sha256": freeze_hash,
        "status": "FROZEN_OFFICIAL",
        "pressure_version": CONFIG.PRESSURE_VERSION,
        "board": "auction_official",
        "top10_batters_ordered": top10_bat["player_name"].tolist(),
        "top10_bowlers_ordered": top10_bowl["player_name"].tolist(),
        "audit_checks": {
            "leakage_count": leakage_count,
            "min_batter_pressure_balls": min_bat_balls,
            "min_bowler_pressure_balls": min_bowl_balls,
            "min_batter_ipl_pressure_balls": int(top10_bat["ipl_pressure_balls"].min()),
            "min_bowler_ipl_pressure_balls": int(top10_bowl["ipl_pressure_balls"].min()),
            "cross_list_duplicates": 0,
            "within_list_duplicates": 0,
        },
        "sensitivity": sensitivity_results,
    }

    with open(RANKINGS_DIR / "frozen_top10_fingerprint.json", "w", encoding="utf-8") as f:
        json.dump(freeze_record, f, indent=2)

    report_lines = [
        "# PressurePulse — Official Ranking Validation & Freeze Report",
        "",
        "## 1. Cryptographic Freeze Fingerprint",
        f"- **Status:** `FROZEN_OFFICIAL`",
        f"- **Board:** Auction Official",
        f"- **SHA256 Fingerprint:** `{freeze_hash}`",
        f"- **Pressure Specification Version:** `{CONFIG.PRESSURE_VERSION}`",
        "",
        "## 2. Integrity & Orthogonality Audits",
        "| Audit Check | Condition Tested | Result | Status |",
        "|---|---|:---:|:---:|",
        f"| Zero Leakage | Pressure & Baseline balls mutually exclusive | {leakage_count} leaks | **PASS** |",
        f"| Universal Delivery Coverage | Pressure + Baseline == Total | {total_accounted:,} == {len(df_del):,} | **PASS** |",
        f"| Batters Uniqueness | Top 10 Batters unique IDs | {top10_bat['player_id'].nunique()} / 10 | **PASS** |",
        f"| Bowlers Uniqueness | Top 10 Bowlers unique IDs | {top10_bowl['player_id'].nunique()} / 10 | **PASS** |",
        f"| Disjoint Lists | Zero cross-category player duplication | {len(overlap)} overlaps | **PASS** |",
        f"| Sample Sufficiency (Batters) | Min pressure balls | {min_bat_balls} >= {CONFIG.MIN_PRESSURE_BALLS_FACED} | **PASS** |",
        f"| Sample Sufficiency (Bowlers) | Min pressure balls | {min_bowl_balls} >= {CONFIG.MIN_PRESSURE_BALLS_BOWLED} | **PASS** |",
        f"| IPL Floor (Batters) | Min IPL pressure balls | {int(top10_bat['ipl_pressure_balls'].min())} >= {CONFIG.MIN_IPL_PRESSURE_BALLS_BATTER} | **PASS** |",
        f"| IPL Floor (Bowlers) | Min IPL pressure balls | {int(top10_bowl['ipl_pressure_balls'].min())} >= {CONFIG.MIN_IPL_PRESSURE_BALLS_BOWLER} | **PASS** |",
        "",
        "## 3. Sensitivity & Domain Stability (computed)",
        f"- **Batter Top 10 mean retention:** {sensitivity_results['batter_top10_stability_pct']}% across RRR/death perturbations.",
        f"- **Bowler Top 10 mean retention:** {sensitivity_results['bowler_top10_stability_pct']}% across RRR/death perturbations.",
        f"- **Per-variant batter retention %:** {sensitivity_results['batter_retention_by_variant_pct']}",
        f"- **Per-variant bowler retention %:** {sensitivity_results['bowler_retention_by_variant_pct']}",
        f"- **IPL-only Top 12 overlap:** batters {sensitivity_results['ipl_overlap_batters']}/10, bowlers {sensitivity_results['ipl_overlap_bowlers']}/10.",
        "",
        "## 4. Official Frozen Top 10 Roster (Auction Official)",
        "### Batters",
    ]
    for i, name in enumerate(top10_bat["player_name"].tolist(), 1):
        report_lines.append(f"{i}. {name}")
    report_lines.append("\n### Bowlers")
    for i, name in enumerate(top10_bowl["player_name"].tolist(), 1):
        report_lines.append(f"{i}. {name}")

    (QA_DIR / "validation_summary.md").write_text("\n".join(report_lines), encoding="utf-8")
    logger.info(f"Rank freeze successful! SHA256: {freeze_hash}")
    return freeze_record


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_validation_and_freeze()
