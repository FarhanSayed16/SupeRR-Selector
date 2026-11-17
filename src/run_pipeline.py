"""
PressurePulse — Master Pipeline Orchestrator
Single entry point to execute and reproduce the intelligence pipeline end-to-end.
"""

import sys
import time
from typing import Dict
from src.foundation.config import CONFIG, PROCESSED_DATA_DIR, QA_DIR
from src.foundation.manifest import setup_logging, write_run_manifest
from src.data_platform.warehouse import build_warehouse

logger = setup_logging()

def run_pipeline() -> int:
    """Executes all pipeline stages with error boundaries and manifest logging."""
    start_time = time.time()
    logger.info("==================================================")
    logger.info(f" Starting PressurePulse Pipeline ({CONFIG.PRESSURE_VERSION})")
    logger.info("==================================================")

    stage_statuses: Dict[str, str] = {}

    try:
        # Stage 1: Data Platform & Warehouse (Phase 05)
        logger.info(">>> Stage 1: Ingestion & Data Warehouse")
        warehouse_tables = build_warehouse()
        stage_statuses["01_warehouse"] = "SUCCESS"
        logger.info(f"Warehouse ready: {len(warehouse_tables['fact_delivery'])} deliveries loaded.")

        # Stage 2: Match State Reconstruction (Phase 07)
        logger.info(">>> Stage 2: Match State Reconstruction")
        from src.intelligence.state import reconstruct_match_states
        delivery_state_df = reconstruct_match_states(
            delivery_df=warehouse_tables["fact_delivery"],
            match_df=warehouse_tables["dim_match"]
        )
        stage_statuses["02_state_reconstruction"] = "SUCCESS"
        logger.info(f"State reconstruction ready: {len(delivery_state_df)} deliveries state-indexed.")

        # Stage 3: Pressure Definition Engine (Phase 08)
        logger.info(">>> Stage 3: Pressure Definition Engine")
        from src.intelligence.pressure import run_pressure_engine
        delivery_pressure_df, pressure_diagnostics = run_pressure_engine(state_df=delivery_state_df)
        stage_statuses["03_pressure_engine"] = "SUCCESS"
        logger.info(f"Pressure engine ready: {pressure_diagnostics['pressure_percentage']}% balls marked pressure.")

        # Stage 4: Role Classification (Phase 09)
        logger.info(">>> Stage 4: Player Role Classification")
        from src.intelligence.roles import classify_player_roles
        player_roles_df = classify_player_roles(
            delivery_df=delivery_pressure_df,
            xi_df=warehouse_tables["fact_xi"],
            player_df=warehouse_tables["dim_player"]
        )
        stage_statuses["04_role_classification"] = "SUCCESS"
        logger.info(f"Role classification ready: {player_roles_df['eligible_as_batter'].sum()} batters and {player_roles_df['eligible_as_bowler'].sum()} bowlers eligible.")

        # Stage 5: Batting Metrics (Phase 10)
        logger.info(">>> Stage 5: Batting Metrics")
        from src.intelligence.metrics_batting import compute_batting_metrics
        batting_metrics_df = compute_batting_metrics(
            delivery_df=delivery_pressure_df,
            roles_df=player_roles_df
        )
        stage_statuses["05_batting_metrics"] = "SUCCESS"
        logger.info(f"Batting metrics ready: {len(batting_metrics_df)} batters evaluated.")

        # Stage 6: Bowling Metrics (Phase 11)
        logger.info(">>> Stage 6: Bowling Metrics")
        from src.intelligence.metrics_bowling import compute_bowling_metrics
        bowling_metrics_df = compute_bowling_metrics(
            delivery_df=delivery_pressure_df,
            roles_df=player_roles_df
        )
        stage_statuses["06_bowling_metrics"] = "SUCCESS"
        logger.info(f"Bowling metrics ready: {len(bowling_metrics_df)} bowlers evaluated.")

        # Stage 7: Scoring & Top 10 Ranking (Phase 12 & 13)
        logger.info(">>> Stage 7: Scoring & Top 10 Ranking")
        from src.intelligence.ranking import run_ranking_pipeline
        from src.intelligence.validation import run_validation_and_freeze
        top10_batters_df, top10_bowlers_df = run_ranking_pipeline(
            batting_metrics_df=batting_metrics_df,
            bowling_metrics_df=bowling_metrics_df
        )
        freeze_meta = run_validation_and_freeze()
        stage_statuses["07_scoring_ranking"] = "SUCCESS"
        stage_statuses["07_rank_freeze"] = f"FROZEN_{freeze_meta['freeze_sha256'][:8]}"
        logger.info(f"Top 10 frozen with SHA256: {freeze_meta['freeze_sha256'][:8]}... #{1} Batter = {top10_batters_df.iloc[0]['player_name']}, #{1} Bowler = {top10_bowlers_df.iloc[0]['player_name']}")

        # Stage 8: Delivery & JSON/CSV Exports (Phase 14)
        logger.info(">>> Stage 8: Delivery & JSON/CSV Exports")
        from src.delivery.export import export_delivery_packages
        exported_packages = export_delivery_packages()
        stage_statuses["08_delivery_exports"] = "SUCCESS"
        logger.info(f"Delivery packages synchronized: {len(exported_packages)} JSON files in dashboard/public/data/")

        # Write execution manifest
        duration = time.time() - start_time
        manifest_path = write_run_manifest(
            stage_statuses=stage_statuses,
            metrics_summary={"total_duration_seconds": round(duration, 2)}
        )
        logger.info(f"Run manifest successfully written to {manifest_path}")
        logger.info(f"Pipeline completed successfully in {duration:.2f}s.")
        return 0

    except Exception as e:
        logger.error(f"FATAL PIPELINE ERROR: {e}", exc_info=True)
        stage_statuses["pipeline"] = f"FAILED: {str(e)}"
        write_run_manifest(stage_statuses=stage_statuses)
        return 1

if __name__ == "__main__":
    sys.exit(run_pipeline())
