"""
PressurePulse — Backend Delivery & Export Service (L3)
Generates static JSON aggregates for the React dashboard and report assets.
Ensures zero proprietary delivery-level records are published.
"""

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
import pandas as pd
from src.foundation.config import (
    CONFIG, RANKINGS_DIR, PROCESSED_DATA_DIR,
    DASHBOARD_DATA_DIR, DASHBOARD_EXPORT_DIR, QA_DIR
)

logger = logging.getLogger(__name__)

# RR Tactical Squad Needs Context (Derived from Public RR 2026/2027 Auction Roster analysis)
RR_FIT_NARRATIVES = {
    # Batters
    1: { # Rohit Sharma
        "squad_role": "Elite Pressure Opener / Powerplay Anchor",
        "rr_tactical_fit": "Provides senior opening stability alongside Yashasvi Jaiswal; proven match-winner in high-intensity knockout chases.",
        "synergy_score": 96
    },
    2: { # Shashank Singh
        "squad_role": "High-Impact Number 6 Finisher",
        "rr_tactical_fit": "Direct solution to RR's lower-middle order death finishing; exceptional boundary conversion rate (+69.2 SR uplift in tight chases).",
        "synergy_score": 98
    },
    3: { # Naman Dhir
        "squad_role": "Versatile Number 3/4 Dynamic Hitter",
        "rr_tactical_fit": "High strike rate against both high pace and spin; flexible top-order aggressor who elevates run rate in middle overs.",
        "synergy_score": 92
    },
    4: { # Ashutosh Sharma
        "squad_role": "Specialist Number 7 Clutch Finisher",
        "rr_tactical_fit": "Extraordinary tail-end rescue ability (79.1 SR uplift in critical chases); fills the exact finisher slot needed at Sawai Mansingh Stadium.",
        "synergy_score": 97
    },
    5: { # Dinesh Karthik
        "squad_role": "Veteran Finisher / Wicketkeeping Depth",
        "rr_tactical_fit": "Unmatched death over strike rate (170.6 SR under pressure); invaluable mentor and high-leverage execution specialist.",
        "synergy_score": 90
    },
    6: { # Rishabh Pant
        "squad_role": "Middle-Order Counter-Attacker",
        "rr_tactical_fit": "Elite left-handed middle order destructor; turns lost matches around from collapse situations with 47.1 SR uplift.",
        "synergy_score": 94
    },
    7: { # Sai Sudharsan
        "squad_role": "Anchor with High-Gear Finishing Gear",
        "rr_tactical_fit": "Technically immaculate left-hander who absorbs early pressure without dropping scoring tempo in qualifiers.",
        "synergy_score": 93
    },
    8: { # Vijay Shankar
        "squad_role": "Pace-Hitting Middle-Order Floater",
        "rr_tactical_fit": "Substantial boundary-hitting uplift (+69.6 SR) against high-speed pace bowling in middle-to-death overs.",
        "synergy_score": 88
    },
    9: { # Suryakumar Yadav
        "squad_role": "360-Degree Match Winner",
        "rr_tactical_fit": "Highest volume pressure sample in cricket history (1,033 balls); delivers 177.8 SR under extreme pressure.",
        "synergy_score": 99
    },
    10: { # Rinku Singh
        "squad_role": "Proven Death Finisher",
        "rr_tactical_fit": "World-class chase execution record (903 balls, 161.4 SR); extreme psychological advantage in final 3 overs.",
        "synergy_score": 98
    },
    # Bowlers
    101: { # Sunil Narine
        "squad_role": "Mystery Spin Enforcer / Death Restrictor",
        "rr_tactical_fit": "Unrivalled 6.06 death over economy under pressure; pair with RR's spin battery to choke middle-to-death scoring.",
        "synergy_score": 98
    },
    102: { # Mohammad Nawaz
        "squad_role": "Left-Arm Orthodox Choke Specialist",
        "rr_tactical_fit": "Sub-6.0 economy under pressure (5.98) with lethal arm-ball variation; controls powerplay and middle phase chokes.",
        "synergy_score": 91
    },
    103: { # Sufiyan Muqeem
        "squad_role": "Left-Arm Wrist Spin Weapon",
        "rr_tactical_fit": "Lowest recorded pressure economy in the dataset (5.30) with 56.2% dot balls; high-upside auction target for RR war room.",
        "synergy_score": 95
    },
    104: { # Abrar Ahmed
        "squad_role": "Attacking Leg-Spin / Mystery Spinner",
        "rr_tactical_fit": "Consistent wicket-taker (24 wickets at 5.89 economy in pressure); unreadable variations on dry Jaipur tracks.",
        "synergy_score": 92
    },
    105: { # Kuldeep Yadav
        "squad_role": "Premier Left-Arm Wrist Spinner",
        "rr_tactical_fit": "Elite wicket-taking strike rate in middle overs (51 pressure wickets); breaks critical partnerships under siege.",
        "synergy_score": 96
    },
    106: { # Jasprit Bumrah
        "squad_role": "World-Leading Death / Super-Over Bowler",
        "rr_tactical_fit": "Unrivalled 7.41 death economy and 53 pressure wickets across 780 balls; the gold standard of bowling under pressure.",
        "synergy_score": 100
    },
    107: { # Rasikh Salam
        "squad_role": "Domestic Death Overs Slower-Ball Specialist",
        "rr_tactical_fit": "High-value Indian domestic pace bowler taking a wicket every 10.6 balls under pressure; ideal auction budget multiplier.",
        "synergy_score": 97
    },
    108: { # Rashid Khan
        "squad_role": "Global Elite Franchise Wicket-Taker",
        "rr_tactical_fit": "96 pressure wickets (dataset record) with an 8.36 death economy; unmatched experience in tournament knockouts.",
        "synergy_score": 99
    },
    109: { # Mitchell Santner
        "squad_role": "Economical Finger Spin / Defending Anchor",
        "rr_tactical_fit": "Sub-7.0 economy under pressure (6.91) across 563 balls; exceptional boundary-prevention accuracy.",
        "synergy_score": 93
    },
    110: { # Varun Chakravarthy
        "squad_role": "Middle-Over Breakthrough Mystery Bowler",
        "rr_tactical_fit": "66 pressure wickets at 13.3 balls per dismissal; forces false strokes when batsmen attempt to accelerate.",
        "synergy_score": 95
    }
}

def export_delivery_packages() -> Dict[str, Path]:
    """Generates all JSON payloads for dashboard and report."""
    logger.info("Exporting JSON delivery packages...")

    DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Load frozen rankings and QA summaries
    top10_bat = pd.read_csv(RANKINGS_DIR / "top10_batters.csv")
    top10_bowl = pd.read_csv(RANKINGS_DIR / "top10_bowlers.csv")
    full_bat = pd.read_csv(RANKINGS_DIR / "full_batter_rankings.csv")
    full_bowl = pd.read_csv(RANKINGS_DIR / "full_bowler_rankings.csv")
    
    with open(RANKINGS_DIR / "frozen_top10_fingerprint.json", "r", encoding="utf-8") as f:
        freeze_meta = json.load(f)
    with open(QA_DIR / "pressure_summary.json", "r", encoding="utf-8") as f:
        pressure_summary = json.load(f)

    # 1. Meta Package
    meta_pkg = {
        "product_name": "PressurePulse",
        "subtitle": "Rajasthan Royals Auction Intelligence System (IPL 2027)",
        "version": CONFIG.PRESSURE_VERSION,
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "freeze_sha256": freeze_meta["freeze_sha256"],
        "seasons_covered": ["2022", "2023", "2024", "2025", "2026"],
        "total_deliveries": pressure_summary["total_deliveries"],
        "pressure_deliveries": pressure_summary["pressure_deliveries"],
        "pressure_percentage": pressure_summary["pressure_percentage"],
        "ipl_weight": CONFIG.IPL_WEIGHT,
        "disclaimer": "Proprietary Rajasthan Royals data pack evaluated strictly under SupeRR Selector competition terms."
    }

    # 2. Enrich Top 10 Batters with RR Fit
    top10_bat_records = []
    for _, r in top10_bat.iterrows():
        rec = r.to_dict()
        fit = RR_FIT_NARRATIVES.get(int(r["rank"]), {})
        rec.update(fit)
        top10_bat_records.append(rec)

    # 3. Enrich Top 10 Bowlers with RR Fit
    top10_bowl_records = []
    for _, r in top10_bowl.iterrows():
        rec = r.to_dict()
        fit = RR_FIT_NARRATIVES.get(100 + int(r["rank"]), {})
        rec.update(fit)
        top10_bowl_records.append(rec)

    # 4. Searchable Players Index
    players_index = []
    for _, r in full_bat.iterrows():
        players_index.append({
            "player_id": int(r["player_id"]),
            "player_name": r["player_name"],
            "primary_role": r["primary_role"],
            "is_batter": True,
            "is_bowler": False,
            "rank": int(r["rank"]),
            "pressure_score": float(r["pressure_score"])
        })
    for _, r in full_bowl.iterrows():
        # Check if already present as all-rounder
        existing = next((p for p in players_index if p["player_id"] == int(r["player_id"])), None)
        if existing:
            existing["is_bowler"] = True
            existing["bowler_rank"] = int(r["rank"])
            existing["bowler_pressure_score"] = float(r["pressure_score"])
        else:
            players_index.append({
                "player_id": int(r["player_id"]),
                "player_name": r["player_name"],
                "primary_role": r["primary_role"],
                "is_batter": False,
                "is_bowler": True,
                "rank": int(r["rank"]),
                "pressure_score": float(r["pressure_score"])
            })

    # 5. Detailed Player Profiles (Top 20 from both sides)
    profiles = {}
    for rec in top10_bat_records + full_bat.iloc[10:20].to_dict(orient="records"):
        pid = str(rec["player_id"])
        if pid not in profiles:
            profiles[pid] = {"batting": rec}
        else:
            profiles[pid]["batting"] = rec

    for rec in top10_bowl_records + full_bowl.iloc[10:20].to_dict(orient="records"):
        pid = str(rec["player_id"])
        if pid not in profiles:
            profiles[pid] = {"bowling": rec}
        else:
            profiles[pid]["bowling"] = rec

    # 6. Methodology JSON Package
    methodology_pkg = {
        "pressure_version": CONFIG.PRESSURE_VERSION,
        "definition_sentence": pressure_summary["definition_sentence"],
        "chase_high_rrr": CONFIG.CHASE_HIGH_RRR,
        "chase_critical_rrr": CONFIG.CHASE_CRITICAL_RRR,
        "death_overs": "16-20",
        "collapse_wickets": CONFIG.COLLAPSE_WICKETS_LOST,
        "min_batter_pressure_balls": CONFIG.MIN_PRESSURE_BALLS_FACED,
        "min_bowler_pressure_balls": CONFIG.MIN_PRESSURE_BALLS_BOWLED,
        "scoring_weights_batter": {
            "clutch_quality": 0.40,
            "uplift_vs_baseline": 0.25,
            "consistency": 0.20,
            "volume_depth": 0.15,
            "ipl_multiplier_max": "+15%"
        },
        "scoring_weights_bowler": {
            "restrictiveness_and_death_econ": 0.35,
            "wicket_taking_threat": 0.30,
            "uplift_and_resistance": 0.15,
            "consistency": 0.10,
            "volume_depth": 0.10,
            "ipl_multiplier_max": "+15%"
        }
    }

    # Files to serialize
    artifacts = {
        "meta.json": meta_pkg,
        "top10_batters.json": top10_bat_records,
        "top10_bowlers.json": top10_bowl_records,
        "players_index.json": players_index,
        "players_detail.json": profiles,
        "pressure_summary.json": pressure_summary,
        "methodology.json": methodology_pkg
    }

    # Write to both dashboard/public/data and outputs/dashboard_export
    for fname, payload in artifacts.items():
        for target_dir in [DASHBOARD_DATA_DIR, DASHBOARD_EXPORT_DIR]:
            p = target_dir / fname
            with open(p, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, default=str)

    logger.info(f"Synchronized {len(artifacts)} JSON packages to {DASHBOARD_DATA_DIR} and {DASHBOARD_EXPORT_DIR}")
    return artifacts

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    export_delivery_packages()
