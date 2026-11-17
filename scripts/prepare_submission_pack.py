"""
PressurePulse — Submission Pack Builder (Phase 24)
Assembles all official Unstop submission assets into outputs/submission_pack/.
"""

import json
import shutil
from pathlib import Path
import pandas as pd

def prepare_pack():
    pack_dir = Path("outputs/submission_pack")
    pack_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy frozen PDF report
    pdf_src = Path("outputs/report/PressurePulse_Methodology.pdf")
    pdf_dst = pack_dir / "PressurePulse_Methodology.pdf"
    if pdf_src.exists():
        shutil.copy2(pdf_src, pdf_dst)

    # 2. Load frozen rankings
    top10_bat = pd.read_csv("outputs/rankings/top10_batters.csv")
    top10_bowl = pd.read_csv("outputs/rankings/top10_bowlers.csv")
    with open("outputs/rankings/frozen_top10_fingerprint.json", "r") as f:
        freeze_meta = json.load(f)

    # 3. Create Unstop Form Guide
    guide_lines = [
        "# PressurePulse — Official Unstop Round 1 Submission Guide",
        "",
        "> **SupeRR Selector Season 2: Help Shape Rajasthan Royals' IPL 2027 Auction Strategy**  ",
        f"> **Freeze SHA256:** `{freeze_meta['freeze_sha256']}`  ",
        "> **Deadline:** 18 Nov 2026, 11:59 PM IST",
        "",
        "---",
        "",
        "## 1. Batsmen Dropdown Selections (Rank 1 through 10)",
        "Select these exact players in rank order from the Unstop dropdowns:",
        ""
    ]

    for _, r in top10_bat.iterrows():
        guide_lines.append(f"- **Batsman {r['rank']}:** `{r['player_name']}` (Score: {r['pressure_score']:.1f} | {r['primary_role']})")

    guide_lines.extend([
        "",
        "---",
        "",
        "## 2. Bowlers Dropdown Selections (Rank 1 through 10)",
        "Select these exact players in rank order from the Unstop dropdowns:",
        ""
    ])

    for _, r in top10_bowl.iterrows():
        guide_lines.append(f"- **Bowler {r['rank']}:** `{r['player_name']}` (Score: {r['pressure_score']:.1f} | {r['primary_role']})")

    guide_lines.extend([
        "",
        "---",
        "",
        "## 3. Upload Your Report (Mandatory)",
        f"- **File to upload:** `{pdf_dst.resolve()}`",
        "- **File Format:** PDF (2-page publication grade document with tables and brand styling)",
        "",
        "---",
        "",
        "## 4. Dashboard Link (Optional, Max 500 Chars)",
        "- **Paste your live Vercel URL:** `https://your-pressurepulse-deployment.vercel.app` (or local/preview link)",
        "",
        "---",
        "",
        "## 5. Suggested Remarks for Unstop Submission",
        "```text",
        "PressurePulse is an end-to-end auction intelligence engine developed for Rajasthan Royals. Across 200,999 ball-by-ball deliveries (IPL & T20I 2022–2026), our composite Pressure Index isolates high-leverage deliveries across all match phases (43.7% outside death overs) and scores players on clutch quality, positive uplift against their own baseline, and consistency. The attached report details the methodology, fairness constraints, and tactical squad fit for the IPL 2027 auction.",
        "```",
        "",
        "---",
        "",
        "## 6. Optional Journey Reel / Post",
        "If sharing on LinkedIn, YouTube, or Instagram:",
        "- **Tags required:** `@rajasthanroyals` and `@unstop.world`",
        "- **Suggested Caption:** *Unveiling PressurePulse: Our data-driven player reliability model for Rajasthan Royals' IPL 2027 Auction Strategy in SupeRR Selector Season 2!*"
    ])

    (pack_dir / "UNSTOP_SUBMISSION_FORM_GUIDE.md").write_text("\n".join(guide_lines), encoding="utf-8")

    # 4. JSON Roster for automated matching
    submission_roster = {
        "freeze_sha256": freeze_meta["freeze_sha256"],
        "batters_1_to_10": top10_bat[["rank", "player_id", "player_name", "pressure_score"]].to_dict(orient="records"),
        "bowlers_1_to_10": top10_bowl[["rank", "player_id", "player_name", "pressure_score"]].to_dict(orient="records")
    }
    with open(pack_dir / "submission_roster.json", "w", encoding="utf-8") as f:
        json.dump(submission_roster, f, indent=2)

    print(f"Prepared submission pack in {pack_dir}")

if __name__ == "__main__":
    prepare_pack()
