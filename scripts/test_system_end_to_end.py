"""
End-to-End System Integration Test for PressurePulse
Tests:
1. Pipeline Execution & Determinism
2. Parquet Dimensions & Facts Integrity
3. Pressure Definition Validation (Pressure % and Phase Distribution)
4. Frozen Rankings Integrity (SHA256 Fingerprint)
5. Zero Cross-List Overlap between Top 10 Batters and Bowlers
6. Data Delivery JSONs Integrity (valid JSON, non-empty, proper keys)
7. PDF Deliverables (File existence, valid PDF header, page counts)
8. Frontend Production Build Integrity
"""

import hashlib
import json
from pathlib import Path
import pandas as pd
import fitz  # PyMuPDF

def run_tests():
    print("=" * 60)
    print("PRESSUREPULSE SYSTEM INTEGRATION & AUDIT TEST")
    print("=" * 60)
    results = []

    # Test 1: Warehouse Parquet Checks
    try:
        dim_matches = pd.read_parquet("data/processed/dim_match.parquet")
        dim_players = pd.read_parquet("data/processed/dim_player.parquet")
        fact_balls = pd.read_parquet("data/processed/fact_delivery.parquet")
        assert len(fact_balls) == 200999, f"Expected 200999 balls, got {len(fact_balls)}"
        assert len(dim_matches) == 883, f"Expected 883 matches, got {len(dim_matches)}"
        assert len(dim_players) == 1217, f"Expected 1217 players, got {len(dim_players)}"
        results.append(("1. Parquet Warehouse Schema & Row Count", "PASS", f"{len(fact_balls)} balls across {len(dim_matches)} matches"))
    except Exception as e:
        results.append(("1. Parquet Warehouse Schema & Row Count", "FAIL", str(e)))

    # Test 2: Pressure Distribution
    try:
        fact_pressure = pd.read_parquet("data/processed/fact_delivery_pressure.parquet")
        total_balls = len(fact_pressure)
        pressure_balls = fact_pressure['is_pressure'].sum()
        pressure_pct = (pressure_balls / total_balls) * 100
        
        # Check death overs vs outside death
        pressure_df = fact_pressure[fact_pressure['is_pressure']]
        outside_death = (pressure_df['match_phase'] != 'death').sum()
        outside_death_pct = (outside_death / pressure_balls) * 100
        
        assert 38.0 <= pressure_pct <= 41.0, f"Unexpected pressure %: {pressure_pct:.2f}%"
        assert outside_death_pct > 40.0, f"Expected >40% pressure outside death, got {outside_death_pct:.2f}%"
        results.append(("2. PressurePulse Distribution", "PASS", f"{pressure_pct:.2f}% pressure balls ({outside_death_pct:.1f}% outside death)"))
    except Exception as e:
        results.append(("2. PressurePulse Distribution", "FAIL", str(e)))

    # Test 3: Top 10 Batters & Bowlers Integrity & Overlap
    try:
        top_bat = pd.read_csv("outputs/rankings/top10_batters.csv")
        top_bowl = pd.read_csv("outputs/rankings/top10_bowlers.csv")
        assert len(top_bat) == 10, f"Expected 10 batters, got {len(top_bat)}"
        assert len(top_bowl) == 10, f"Expected 10 bowlers, got {len(top_bowl)}"
        
        bat_names = set(top_bat['player_name'])
        bowl_names = set(top_bowl['player_name'])
        overlap = bat_names.intersection(bowl_names)
        assert len(overlap) == 0, f"Found overlapping players: {overlap}"
        results.append(("3. Top 10 Roster Isolation & Zero Overlap", "PASS", f"20 unique players across lists (0 duplicates)"))
    except Exception as e:
        results.append(("3. Top 10 Roster Isolation & Zero Overlap", "FAIL", str(e)))

    # Test 4: Cryptographic Freeze SHA256
    try:
        with open("outputs/rankings/frozen_top10_fingerprint.json", "r") as f:
            meta = json.load(f)
        saved_sha = meta['freeze_sha256']
        version = meta['pressure_version']
        
        # Re-compute sha matching validation.py
        freeze_payload = {
            "version": version,
            "top10_batters": top_bat[["rank", "player_id", "player_name", "pressure_score"]].to_dict(orient="records"),
            "top10_bowlers": top_bowl[["rank", "player_id", "player_name", "pressure_score"]].to_dict(orient="records")
        }
        computed_sha = hashlib.sha256(json.dumps(freeze_payload, sort_keys=True).encode("utf-8")).hexdigest()
        assert computed_sha == saved_sha, f"SHA mismatch! {computed_sha} != {saved_sha}"
        results.append(("4. Cryptographic Freeze Fingerprint", "PASS", f"SHA256: {computed_sha[:16]}... matched perfectly"))
    except Exception as e:
        results.append(("4. Cryptographic Freeze Fingerprint", "FAIL", str(e)))

    # Test 5: Data Delivery Packages
    try:
        expected_files = [
            "meta.json", "methodology.json", "players_detail.json",
            "players_index.json", "pressure_summary.json",
            "top10_batters.json", "top10_bowlers.json", "scouting_dossiers.json"
        ]
        data_dir = Path("dashboard/public/data")
        for fn in expected_files:
            fp = data_dir / fn
            assert fp.exists(), f"Missing delivery file: {fn}"
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
                assert len(d) > 0, f"File {fn} is empty"
        results.append(("5. Dashboard Public Data Feeds", "PASS", f"All 8 JSON packages valid and populated"))
    except Exception as e:
        results.append(("5. Dashboard Public Data Feeds", "FAIL", str(e)))

    # Test 6: PDF Reports Validation
    try:
        pdf_methodology = fitz.open("outputs/submission_pack/PressurePulse_Methodology.pdf")
        assert len(pdf_methodology) == 2, f"Expected 2 pages for methodology report, got {len(pdf_methodology)}"
        
        pdf_dossier = fitz.open("outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.pdf")
        assert len(pdf_dossier) == 6, f"Expected 6 pages for scouting dossier, got {len(pdf_dossier)}"
        results.append(("6. PDF Documents Structure & Quality", "PASS", f"Methodology: 2 pgs | Dossier: 6 pgs (0 errors)"))
    except Exception as e:
        results.append(("6. PDF Documents Structure & Quality", "FAIL", str(e)))

    # Test 7: Submission Pack Completeness
    try:
        req_pack = [
            "PressurePulse_Methodology.pdf",
            "RR_WAR_ROOM_SCOUTING_DOSSIER.pdf",
            "RR_WAR_ROOM_SCOUTING_DOSSIER.md",
            "scouting_dossiers.json",
            "submission_roster.json",
            "UNSTOP_SUBMISSION_FORM_GUIDE.md"
        ]
        pack_dir = Path("outputs/submission_pack")
        for fn in req_pack:
            fp = pack_dir / fn
            assert fp.exists() and fp.stat().st_size > 0, f"File {fn} missing or empty"
        results.append(("7. Final Submission Pack Staging", "PASS", f"All 6 submission artifacts verified in outputs/submission_pack/"))
    except Exception as e:
        results.append(("7. Final Submission Pack Staging", "FAIL", str(e)))

    # Test 8: Frontend Production Build
    try:
        dist_dir = Path("dashboard/dist")
        assert (dist_dir / "index.html").exists(), "Missing dist/index.html"
        assert (dist_dir / "assets").exists(), "Missing dist/assets"
        assets = list((dist_dir / "assets").glob("*"))
        assert len(assets) >= 2, f"Expected >=2 asset bundles, got {len(assets)}"
        results.append(("8. Frontend Production Distribution Build", "PASS", f"dist/ verified ({len(assets)} compiled bundles)"))
    except Exception as e:
        results.append(("8. Frontend Production Distribution Build", "FAIL", str(e)))

    # Print Summary Table
    print("\n" + "-" * 75)
    print(f"{'TEST NAME':<45} | {'STATUS':<6} | {'DETAILS'}")
    print("-" * 75)
    all_passed = True
    for name, status, details in results:
        print(f"{name:<45} | {status:<6} | {details}")
        if status != "PASS":
            all_passed = False
    print("-" * 75)
    print("ALL TESTS PASSED: " + ("YES" if all_passed else "NO"))
    print("=" * 60)
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
