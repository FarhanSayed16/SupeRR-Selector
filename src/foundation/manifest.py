"""
PressurePulse — Logging & Run Manifest Writer (L0)
Generates structured execution manifests to ensure reproducible pipelines.
"""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from src.foundation.config import CONFIG, QA_DIR

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """Configures unified logging to stdout and file."""
    logger = logging.getLogger("PressurePulse")
    logger.setLevel(log_level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    QA_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(QA_DIR / "pipeline_run.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def get_git_commit() -> str:
    """Returns current git commit hash if available."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return "uncommitted_workspace"

def write_run_manifest(
    stage_statuses: Dict[str, str],
    metrics_summary: Dict[str, Any] = None,
    output_path: Path = QA_DIR / "run_manifest.json"
) -> Path:
    """Writes a machine-readable run manifest with timestamps and configuration."""
    manifest = {
        "pipeline_name": "PressurePulse",
        "pressure_version": CONFIG.PRESSURE_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "python_version": sys.version,
        "config": {
            "IPL_WEIGHT": CONFIG.IPL_WEIGHT,
            "T20I_WEIGHT": CONFIG.T20I_WEIGHT,
            "INCLUDE_SUPER_OVERS": CONFIG.INCLUDE_SUPER_OVERS,
            "MIN_PRESSURE_BALLS_FACED": CONFIG.MIN_PRESSURE_BALLS_FACED,
            "MIN_PRESSURE_BALLS_BOWLED": CONFIG.MIN_PRESSURE_BALLS_BOWLED,
            "CHASE_HIGH_RRR": CONFIG.CHASE_HIGH_RRR,
            "CHASE_CRITICAL_RRR": CONFIG.CHASE_CRITICAL_RRR,
            "KNOCKOUT_MULTIPLIER": CONFIG.KNOCKOUT_MULTIPLIER
        },
        "stage_statuses": stage_statuses,
        "metrics_summary": metrics_summary or {}
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return output_path
