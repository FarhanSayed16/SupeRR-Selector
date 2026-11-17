"""
PressurePulse — Central Configuration & Methodology Constants (L0)
Single source of truth for all paths, thresholds, weights, and policies.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List

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
    PRESSURE_VERSION: str = "pressure_v1"
    RANDOM_SEED: int = 42

    # Competition weights for auction relevance
    # IPL is direct auction domain (weighted higher); T20I provides global sample
    IPL_WEIGHT: float = 1.30
    T20I_WEIGHT: float = 1.00

    # Match Inclusions/Exclusions
    INCLUDE_SUPER_OVERS: bool = False  # Super overs analyzed in clutch subset, excluded from base rates
    MAX_REGULAR_INNINGS: int = 2

    # Pressure Definition Thresholds (pressure_v1)
    # Chase leverage
    CHASE_HIGH_RRR: float = 9.5         # Required Run Rate >= 9.5
    CHASE_CRITICAL_RRR: float = 11.5    # Required Run Rate >= 11.5
    CHASE_DEATH_OVERS_START: int = 16   # Overs 16-20
    CHASE_BALLS_REMAINING_LOW: int = 30 # <= 30 balls remaining
    
    # Collapse leverage (Innings 1 & 2)
    COLLAPSE_WICKETS_LOST: int = 3      # Lost >= 3 wickets
    COLLAPSE_BEFORE_OVER: int = 8       # within first 8 overs
    LOW_WICKETS_IN_HAND: int = 3        # <= 3 wickets in hand remaining
    
    # Knockout boost
    KNOCKOUT_MULTIPLIER: float = 1.15

    # Eligibility Gates (Tuned for fair sample size)
    MIN_PRESSURE_BALLS_FACED: int = 30
    MIN_BASELINE_BALLS_FACED: int = 60
    MIN_BATTER_MATCHES: int = 5

    MIN_PRESSURE_BALLS_BOWLED: int = 30
    MIN_BASELINE_BALLS_BOWLED: int = 60
    MIN_BOWLER_MATCHES: int = 5

    # Role Classification Thresholds
    # Pure Batter: balls_faced >= 50 and balls_bowled < 30
    # Pure Bowler: balls_bowled >= 50 and balls_faced < 30
    # All-Rounder: meets both or hybrid
    MIN_BALLS_FACED_FOR_BATTER: int = 40
    MIN_BALLS_BOWLED_FOR_BOWLER: int = 40

    # Confidence Thresholds
    CONFIDENCE_HIGH_BALLS: int = 90
    CONFIDENCE_MED_BALLS: int = 45

CONFIG = PipelineConfig()
