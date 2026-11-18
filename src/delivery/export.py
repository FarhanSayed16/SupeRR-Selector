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
    global_bat = pd.read_csv(RANKINGS_DIR / "top10_batters_global.csv")
    global_bowl = pd.read_csv(RANKINGS_DIR / "top10_bowlers_global.csv")
    excluded_path = RANKINGS_DIR / "excluded_low_ipl_sample.csv"
    excluded_df = pd.read_csv(excluded_path) if excluded_path.exists() else pd.DataFrame()

    with open(RANKINGS_DIR / "frozen_top10_fingerprint.json", "r", encoding="utf-8") as f:
        freeze_meta = json.load(f)
    with open(QA_DIR / "pressure_summary.json", "r", encoding="utf-8") as f:
        pressure_summary = json.load(f)

    # 1. Meta Package
    meta_pkg = {
        "product_name": "PressurePulse",
        "subtitle": "Rajasthan Royals Auction Intelligence System (IPL 2027)",
        "version": CONFIG.PRESSURE_VERSION,
        "board": "auction_official",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "freeze_sha256": freeze_meta["freeze_sha256"],
        "seasons_covered": ["2022", "2023", "2024", "2025", "2026"],
        "total_deliveries": pressure_summary["total_deliveries"],
        "pressure_deliveries": pressure_summary["pressure_deliveries"],
        "pressure_percentage": pressure_summary["pressure_percentage"],
        "ipl_weight": CONFIG.IPL_WEIGHT,
        "t20i_weight": CONFIG.T20I_WEIGHT,
        "min_ipl_pressure_balls_batter": CONFIG.MIN_IPL_PRESSURE_BALLS_BATTER,
        "min_ipl_pressure_balls_bowler": CONFIG.MIN_IPL_PRESSURE_BALLS_BOWLER,
        "sensitivity": freeze_meta.get("sensitivity"),
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
            "pressure_score": float(r["pressure_score"]),
            "board": "auction_official",
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
                "pressure_score": float(r["pressure_score"]),
                "board": "auction_official",
            })

    # 5. Detailed Player Profiles — full Auction boards (search / dossier)
    profiles = {}
    for rec in full_bat.to_dict(orient="records"):
        profiles[str(rec["player_id"])] = {"batting": rec}
    for rec in full_bowl.to_dict(orient="records"):
        pid = str(rec["player_id"])
        if pid not in profiles:
            profiles[pid] = {"bowling": rec}
        else:
            profiles[pid]["bowling"] = rec

    # Global-only players (e.g. zero IPL sample) — searchable, not Official
    full_bat_global = pd.read_csv(RANKINGS_DIR / "full_batter_rankings_global.csv")
    full_bowl_global = pd.read_csv(RANKINGS_DIR / "full_bowler_rankings_global.csv")
    for _, r in full_bat_global.iterrows():
        pid = int(r["player_id"])
        if any(p["player_id"] == pid for p in players_index):
            continue
        players_index.append({
            "player_id": pid,
            "player_name": r["player_name"],
            "primary_role": r["primary_role"],
            "is_batter": True,
            "is_bowler": False,
            "rank": int(r["rank"]),
            "pressure_score": float(r["pressure_score"]),
            "board": "global",
        })
        profiles[str(pid)] = {"batting": r.to_dict()}
    for _, r in full_bowl_global.iterrows():
        pid = int(r["player_id"])
        existing = next((p for p in players_index if p["player_id"] == pid), None)
        if existing:
            if not existing.get("is_bowler"):
                existing["is_bowler"] = True
                existing["bowler_rank"] = int(r["rank"])
                existing["bowler_pressure_score"] = float(r["pressure_score"])
            if "bowling" not in profiles.get(str(pid), {}):
                profiles.setdefault(str(pid), {})["bowling"] = r.to_dict()
            continue
        players_index.append({
            "player_id": pid,
            "player_name": r["player_name"],
            "primary_role": r["primary_role"],
            "is_batter": False,
            "is_bowler": True,
            "rank": int(r["rank"]),
            "pressure_score": float(r["pressure_score"]),
            "board": "global",
        })
        profiles[str(pid)] = {"bowling": r.to_dict()}

    # Human scout board — opinion overlay; never mutates Official freeze
    def _official_rank(df: pd.DataFrame, name: str):
        hit = df[df["player_name"].str.fullmatch(name, case=False, na=False)]
        if len(hit):
            return int(hit.iloc[0]["rank"]), float(hit.iloc[0]["pressure_score"]), "auction_official"
        return None, None, None

    scout_batters = [
        "Shashank Singh", "Ashutosh Sharma", "Rinku Singh", "Shreyas Iyer",
        "Suryakumar Yadav", "Rohit Sharma", "Marcus Stoinis", "Naman Dhir",
        "Rishabh Pant", "Riza",
    ]
    scout_bowlers = [
        "Sunil Narine", "Jasprit Bumrah", "Rashid Khan", "Mitchell Santner",
        "Kuldeep Yadav", "Varun Chakravarthy", "Matheesha Pathirana", "Rasikh Salam",
        "Mohammad Nawaz", "Matthew Humphreys",
    ]
    scout_bat_rows = []
    for i, name in enumerate(scout_batters, 1):
        of_rank, of_score, board = _official_rank(full_bat, name)
        note = None
        if name == "Riza":
            note = "Name unmatched on Auction Official; not Mohammad Rizwan in eligible set."
            board = "unmatched"
        elif of_rank is None:
            g = full_bat_global[full_bat_global["player_name"].str.fullmatch(name, case=False, na=False)]
            if len(g):
                of_rank, of_score, board = int(g.iloc[0]["rank"]), float(g.iloc[0]["pressure_score"]), "global_only"
                note = "Below Auction Official IPL sample floor — Global board only."
            else:
                board = "unmatched"
                note = "Not found in ranked boards."
        scout_bat_rows.append({
            "scout_rank": i, "player_name": name,
            "official_rank": of_rank, "official_pressure_score": of_score, "board": board, "note": note,
        })
    scout_bowl_rows = []
    for i, name in enumerate(scout_bowlers, 1):
        of_rank, of_score, board = _official_rank(full_bowl, name)
        note = None
        if of_rank is None:
            g = full_bowl_global[full_bowl_global["player_name"].str.fullmatch(name, case=False, na=False)]
            if len(g):
                of_rank, of_score, board = int(g.iloc[0]["rank"]), float(g.iloc[0]["pressure_score"]), "global_only"
                note = "Below Auction Official IPL sample floor — Global board only."
            else:
                board = "unmatched"
                note = "Not found in ranked boards."
        scout_bowl_rows.append({
            "scout_rank": i, "player_name": name,
            "official_rank": of_rank, "official_pressure_score": of_score, "board": board, "note": note,
        })
    scout_board = {
        "label": "Scout Board (human opinion)",
        "policy": (
            "Auction Official Top 10 stays frozen. This board is a side-by-side scout opinion "
            "for war-room debate — it does not rewrite PressureScore or the freeze SHA."
        ),
        "batters": scout_bat_rows,
        "bowlers": scout_bowl_rows,
    }

    # 6. Methodology JSON Package
    methodology_pkg = {
        "pressure_version": CONFIG.PRESSURE_VERSION,
        "official_board": "auction_official",
        "definition_sentence": pressure_summary["definition_sentence"],
        "chase_high_rrr": CONFIG.CHASE_HIGH_RRR,
        "chase_critical_rrr": CONFIG.CHASE_CRITICAL_RRR,
        "death_overs": "16-20",
        "collapse_wickets": CONFIG.COLLAPSE_WICKETS_LOST,
        "min_batter_pressure_balls": CONFIG.MIN_PRESSURE_BALLS_FACED,
        "min_bowler_pressure_balls": CONFIG.MIN_PRESSURE_BALLS_BOWLED,
        "min_baseline_balls_batter": CONFIG.MIN_BASELINE_BALLS_FACED,
        "min_baseline_balls_bowler": CONFIG.MIN_BASELINE_BALLS_BOWLED,
        "min_ipl_pressure_balls_batter": CONFIG.MIN_IPL_PRESSURE_BALLS_BATTER,
        "min_ipl_pressure_balls_bowler": CONFIG.MIN_IPL_PRESSURE_BALLS_BOWLER,
        "ipl_weight": CONFIG.IPL_WEIGHT,
        "t20i_weight": CONFIG.T20I_WEIGHT,
        "include_super_overs": CONFIG.INCLUDE_SUPER_OVERS,
        "scoring_weights_batter": {
            "clutch_quality": 0.40,
            "uplift_vs_baseline": 0.25,
            "consistency": 0.20,
            "volume_depth": 0.15,
            "rate_basis": "IPL/T20I weighted legal-ball SR"
        },
        "scoring_weights_bowler": {
            "restrictiveness_and_death_econ": 0.35,
            "wicket_taking_threat": 0.30,
            "uplift_and_resistance": 0.15,
            "consistency": 0.10,
            "volume_depth": 0.10,
            "rate_basis": "IPL/T20I weighted legal-ball economy; death econ soft-capped"
        },
        "board_policy": (
            "Auction Official is the primary freeze (IPL sample floors + weighted rates). "
            "Global Combined is a secondary board without IPL floors for methodology context."
        ),
        "prime_note": (
            "P.R.I.M.E. display layer: innings phase (PP/mid/death) is role context; "
            "match-state signals define pressure. Phase, pace/spin, collapse, and reliability "
            "fields are evidence-only and do not change PressureScore or the freeze SHA."
        ),
    }

    global_bat_records = global_bat.to_dict(orient="records")
    global_bowl_records = global_bowl.to_dict(orient="records")
    excluded_keep = [
        "player_id", "player_name", "category", "exclusion_reason", "rank",
        "pressure_score", "ipl_pressure_balls", "ipl_pressure_share", "primary_role",
    ]
    if len(excluded_df):
        cols = [c for c in excluded_keep if c in excluded_df.columns]
        excluded_records = excluded_df[cols].to_dict(orient="records")
    else:
        excluded_records = []

    # Files to serialize
    artifacts = {
        "meta.json": meta_pkg,
        "top10_batters.json": top10_bat_records,
        "top10_bowlers.json": top10_bowl_records,
        "top10_batters_global.json": global_bat_records,
        "top10_bowlers_global.json": global_bowl_records,
        "full_batter_rankings.json": full_bat.to_dict(orient="records"),
        "full_bowler_rankings.json": full_bowl.to_dict(orient="records"),
        "full_batter_rankings_global.json": full_bat_global.to_dict(orient="records"),
        "full_bowler_rankings_global.json": full_bowl_global.to_dict(orient="records"),
        "excluded_low_ipl_sample.json": excluded_records,
        "players_index.json": players_index,
        "players_detail.json": profiles,
        "scout_board.json": scout_board,
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
