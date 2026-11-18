"""
PressurePulse — Central Configuration & Methodology Constants (L0)
Single source of truth for all paths, thresholds, weights, and policies.
"""

from pathlib import Path
from dataclasses import dataclass


# Base Directories
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

OUTPUTS_DIR = ROOT_DIR / "outputs"
RANKINGS_DIR = OUTPUTS_DIR / "rankings"
QA_DIR = OUTPUTS_DIR / "qa"
REPORT_DIR = OUTPUTS_DIR / "report"
CHARTS_DIR = OUTPUTS_DIR / "charts"
DASHBOARD_EXPORT_DIR = OUTPUTS_DIR / "dashboard_export"
DASHBOARD_DATA_DIR = ROOT_DIR / "dashboard" / "public" / "data"


@dataclass(frozen=True)
class PipelineConfig:
    # Versioning
    PRESSURE_VERSION: str = "pressure_v1.1"
    RANDOM_SEED: int = 42

    # Competition weights baked into IPL/T20I blended rates (Auction Official)
    IPL_WEIGHT: float = 1.30
    T20I_WEIGHT: float = 1.00

    # Match Inclusions/Exclusions
    INCLUDE_SUPER_OVERS: bool = False
    MAX_REGULAR_INNINGS: int = 2

    # Pressure Definition Thresholds
    CHASE_HIGH_RRR: float = 9.5
    CHASE_CRITICAL_RRR: float = 11.5
    CHASE_DEATH_OVERS_START: int = 16
    CHASE_BALLS_REMAINING_LOW: int = 30

    COLLAPSE_WICKETS_LOST: int = 3
    COLLAPSE_BEFORE_OVER: int = 8
    LOW_WICKETS_IN_HAND: int = 3

    # Ranking eligibility (shared by roles soft-gate + ranking hard-gate)
    MIN_PRESSURE_BALLS_FACED: int = 50
    MIN_BASELINE_BALLS_FACED: int = 40
    MIN_BATTER_MATCHES: int = 5

    MIN_PRESSURE_BALLS_BOWLED: int = 80
    MIN_BASELINE_BALLS_BOWLED: int = 60
    MIN_BOWLER_MATCHES: int = 5

    # Auction Official IPL sample floors
    MIN_IPL_PRESSURE_BALLS_BATTER: int = 40
    MIN_IPL_PRESSURE_BALLS_BOWLER: int = 60

    # Soft-cap death economy when sample is thin
    MIN_DEATH_BALLS_FOR_FULL_WEIGHT: int = 30

    # Role Classification Thresholds
    MIN_BALLS_FACED_FOR_BATTER: int = 40
    MIN_BALLS_BOWLED_FOR_BOWLER: int = 40

    # Confidence Thresholds
    CONFIDENCE_HIGH_BALLS: int = 90
    CONFIDENCE_MED_BALLS: int = 45

    # P.R.I.M.E. display-only reliability shrinkage (does not affect freeze score)
    RELIABILITY_K_BATTER: int = 40
    RELIABILITY_K_BOWLER: int = 60


CONFIG = PipelineConfig()
