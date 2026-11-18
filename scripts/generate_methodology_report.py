"""
PressurePulse — Final Unstop Round 1 submission PDF (concise, complete).
Upload: outputs/submission_pack/PressurePulse_Methodology.pdf
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RR_PINK = colors.HexColor("#EC008C")
RR_NAVY = colors.HexColor("#0B1B3A")
RR_PURPLE = colors.HexColor("#2A1450")
SLATE_DARK = colors.HexColor("#1E293B")
SLATE_LIGHT = colors.HexColor("#F8FAFC")
SLATE_BORDER = colors.HexColor("#CBD5E1")
TEXT_MUTED = colors.HexColor("#64748B")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._footer(n)
            super().showPage()
        super().save()

    def _footer(self, page_count: int):
        self.saveState()
        self.setStrokeColor(SLATE_BORDER)
        self.setLineWidth(0.5)
        self.line(54, 42, 541, 42)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(TEXT_MUTED)
        self.drawString(
            54,
            30,
            "PressurePulse • SupeRR Selector S2 Round 1 • Prepared for RR Analytics",
        )
        self.drawRightString(541, 30, f"Page {self._pageNumber} of {page_count}")
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(RR_NAVY)
            self.drawString(54, 805, "PRESSUREPULSE — IPL 2027 AUCTION INTELLIGENCE")
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(541, 805, "Auction Official freeze")
            self.line(54, 797, 541, 797)
        self.restoreState()


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "T", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=20,
            leading=24, textColor=RR_NAVY, spaceAfter=2,
        ),
        "sub": ParagraphStyle(
            "S", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10,
            leading=13, textColor=RR_PINK, spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=12,
            leading=15, textColor=RR_NAVY, spaceBefore=8, spaceAfter=4,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.5,
            leading=12, textColor=RR_PURPLE, spaceBefore=6, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "B", parent=base["Normal"], fontName="Helvetica", fontSize=8.5,
            leading=11.5, textColor=SLATE_DARK, spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "M", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8,
            leading=11, textColor=RR_NAVY, spaceAfter=4,
        ),
        "th": ParagraphStyle(
            "TH", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.5,
            leading=9, textColor=colors.white, alignment=1,
        ),
        "td": ParagraphStyle(
            "TD", parent=base["Normal"], fontName="Helvetica", fontSize=7.5,
            leading=9, textColor=SLATE_DARK,
        ),
        "tdc": ParagraphStyle(
            "TDC", parent=base["Normal"], fontName="Helvetica", fontSize=7.5,
            leading=9, textColor=SLATE_DARK, alignment=1,
        ),
        "tdb": ParagraphStyle(
            "TDB", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.5,
            leading=9, textColor=RR_NAVY, alignment=1,
        ),
    }


def _table(data, widths, header_color):
    t = Table(data, colWidths=widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), header_color),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SLATE_LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.4, SLATE_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def build_pdf() -> Path:
    s = _styles()
    top10_bat = pd.read_csv("outputs/rankings/top10_batters.csv")
    top10_bowl = pd.read_csv("outputs/rankings/top10_bowlers.csv")
    with open("outputs/rankings/frozen_top10_fingerprint.json", encoding="utf-8") as f:
        freeze = json.load(f)

    sha = freeze["freeze_sha256"]
    sens = freeze.get("sensitivity") or {}
    audit = freeze.get("audit_checks") or {}

    story = []
    story.append(Paragraph("PRESSUREPULSE", s["title"]))
    story.append(
        Paragraph(
            "RAJASTHAN ROYALS AUCTION INTELLIGENCE — IPL 2027",
            s["sub"],
        )
    )
    story.append(
        Paragraph(
            "<b>SupeRR Selector Season 2 • Round 1</b> — Most reliable players under pressure",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            f"Dataset: IPL &amp; T20I 2022–2026 • 200,999 deliveries • Board: <b>Auction Official</b> "
            f"({freeze.get('pressure_version', 'pressure_v1.1')}) • Freeze SHA: <font face='Courier' size='7'>{sha[:24]}…</font>",
            s["meta"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.4, color=RR_PINK, spaceBefore=2, spaceAfter=8))

    # 1. Executive
    story.append(Paragraph("1. What we solved", s["h1"]))
    story.append(
        Paragraph(
            "RR needs auction targets who <b>raise their game when the match is on the line</b> — not just career averages. "
            "PressurePulse rebuilds pre-delivery match state, tags high-leverage balls, scores each player against their own "
            "non-pressure baseline, and freezes a reproducible Top 10 batters + Top 10 bowlers list for IPL 2027.",
            s["body"],
        )
    )

    # Tables
    story.append(Paragraph("Official Top 10 Batters (Auction Official)", s["h2"]))
    bat_rows = [[
        Paragraph("R", s["th"]), Paragraph("Player", s["th"]), Paragraph("Role", s["th"]),
        Paragraph("P.Balls", s["th"]), Paragraph("P.SR", s["th"]), Paragraph("Base SR", s["th"]),
        Paragraph("Uplift", s["th"]), Paragraph("Score", s["th"]),
    ]]
    for _, r in top10_bat.iterrows():
        bat_rows.append([
            Paragraph(str(int(r["rank"])), s["tdb"]),
            Paragraph(str(r["player_name"]), s["td"]),
            Paragraph(str(r["primary_role"]), s["td"]),
            Paragraph(str(int(r["pressure_balls"])), s["tdc"]),
            Paragraph(f"{r['pressure_sr']:.1f}", s["tdc"]),
            Paragraph(f"{r['baseline_sr']:.1f}", s["tdc"]),
            Paragraph(f"+{r['sr_uplift']:.1f}", s["tdb"]),
            Paragraph(f"{r['pressure_score']:.1f}", s["tdb"]),
        ])
    story.append(_table(bat_rows, [22, 108, 88, 42, 38, 42, 40, 38], RR_NAVY))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Official Top 10 Bowlers (Auction Official)", s["h2"]))
    bowl_rows = [[
        Paragraph("R", s["th"]), Paragraph("Player", s["th"]), Paragraph("Role", s["th"]),
        Paragraph("P.Balls", s["th"]), Paragraph("P.Econ", s["th"]), Paragraph("Death", s["th"]),
        Paragraph("Wkts", s["th"]), Paragraph("Score", s["th"]),
    ]]
    for _, r in top10_bowl.iterrows():
        bowl_rows.append([
            Paragraph(str(int(r["rank"])), s["tdb"]),
            Paragraph(str(r["player_name"]), s["td"]),
            Paragraph(str(r["primary_role"]), s["td"]),
            Paragraph(str(int(r["pressure_balls"])), s["tdc"]),
            Paragraph(f"{r['pressure_economy']:.2f}", s["tdc"]),
            Paragraph(f"{r['death_pressure_economy']:.2f}", s["tdc"]),
            Paragraph(str(int(r["pressure_wickets"])), s["tdb"]),
            Paragraph(f"{r['pressure_score']:.1f}", s["tdb"]),
        ])
    story.append(_table(bowl_rows, [22, 108, 88, 42, 40, 40, 36, 38], RR_PURPLE))

    story.append(PageBreak())

    # 2. Method
    story.append(Paragraph("2. Pressure definition (not death overs alone)", s["h1"]))
    story.append(
        Paragraph(
            "A delivery is <b>high-pressure</b> when pre-ball context demands high-leverage execution: "
            "steep chase (RRR ≥ 9.5), death overs (16–20), collapse (≤3 wickets in hand), or knockout stages. "
            "Of <b>200,999</b> legal-context deliveries, <b>78,868 (39.24%)</b> are pressure. "
            "Material share sits outside death (powerplay ~10%, middle ~34%) — collapse defence and rising RRR, not only slog overs.",
            s["body"],
        )
    )

    story.append(Paragraph("3. Scoring & fairness", s["h1"]))
    story.append(
        Paragraph(
            "<b>Batters (0–100):</b> 40% clutch quality + 25% SR uplift vs own baseline + 20% consistency + 15% volume.<br/>"
            "<b>Bowlers (0–100):</b> 35% restrictiveness (econ + death soft-cap) + 30% wicket threat + 15% economy uplift + "
            "10% consistency + 10% volume.<br/>"
            "<b>Rates:</b> legal balls only; IPL weighted <b>1.30×</b>, T20I <b>1.00×</b> inside rates.<br/>"
            "<b>Eligibility (Auction Official):</b> batters ≥50 pressure / ≥40 baseline / ≥5 matches / ≥40 IPL pressure balls; "
            "bowlers ≥80 / ≥60 / ≥5 / ≥60 IPL. <b>Zero</b> batter–bowler cross-list overlap.",
            s["body"],
        )
    )

    story.append(Paragraph("4. Validation & reproducibility", s["h1"]))
    story.append(
        Paragraph(
            f"Pressure vs baseline sets are disjoint (leakage = {audit.get('leakage_count', 0)}). "
            f"Sensitivity: Top 10 retention batters <b>{sens.get('batter_top10_stability_pct', 'n/a')}%</b>, "
            f"bowlers <b>{sens.get('bowler_top10_stability_pct', 'n/a')}%</b> across RRR∈{{9.0,10.0}} and death-start∈{{15,17}}. "
            f"IPL-only Top 12 overlap: bat {sens.get('ipl_overlap_batters', 'n/a')}/10, bowl {sens.get('ipl_overlap_bowlers', 'n/a')}/10. "
            f"Regen: <font face='Courier' size='7.5'>python -m src.run_pipeline</font> → SHA <font face='Courier' size='7'>{sha}</font>.",
            s["body"],
        )
    )

    # 5. RR fit — the Unstop "how they strengthen RR" requirement
    story.append(Paragraph("5. How these picks strengthen RR (IPL 2027)", s["h1"]))
    story.append(
        Paragraph(
            "Retained core (Jaiswal, Samson, Parag, Jurel, Hetmyer, Sandeep) already covers top order and death seam. "
            "Gaps: <b>lower-order finishing</b>, <b>death / middle restrict</b> at SMS, and <b>impact cover</b>. "
            "Season 1 pattern (Vignesh Puthur): prefer high-leverage value over brand inflation.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Shashank Singh / Ashutosh Sharma / Rinku / DK / Pant:</b> finishers &amp; keepers who lift SR under pressure "
            "(Shashank +73 SR uplift; Ashutosh +93) — solve chase volatility after top-order fails.<br/>"
            "• <b>Rohit / Iyer / SKY / Stoinis / Naman:</b> high-floor middle / experience / float roles for Jaipur chases.<br/>"
            "• <b>Narine / Santner / Kuldeep / Rashid / Hasaranga / Varun:</b> spin choke for SMS square boundaries "
            "(Narine death econ 6.06 — elite purse priority).<br/>"
            "• <b>Bumrah / Pathirana / Rasikh / Zampa:</b> death seam + wrist-spin strike options; Rasikh is the "
            "domestic ‘Puthur-style’ death seam value pick.<br/>"
            "• <b>Projected XI sketch:</b> Jaiswal, Rohit*, Samson (C/WK), Parag, Hetmyer, Shashank*, Jurel, Narine*, "
            "Sandeep, Rasikh*, Kuldeep* | Impact: Ashutosh* (* = scouted from this board).",
            s["body"],
        )
    )

    story.append(Paragraph("6. Limits (stated plainly)", s["h1"]))
    story.append(
        Paragraph(
            "Auction Official privileges IPL sample floors — some T20I-only standouts sit on the Global Combined board only. "
            "Auction prices are scouting bands, not market forecasts. Rankings measure pressure reliability, not franchise "
            "retention status or purse maths.",
            s["body"],
        )
    )

    out = Path("outputs/report/PressurePulse_Methodology.pdf")
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(out), pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=50,
    )
    doc.build(story, canvasmaker=NumberedCanvas)

    pack = Path("outputs/submission_pack")
    pack.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, pack / "PressurePulse_Methodology.pdf")
    # Convenience copy at repo root for quick Unstop upload
    shutil.copy2(out, Path("PressurePulse_Round1_Submission.pdf"))
    print(f"OK {out} | pack copy | PressurePulse_Round1_Submission.pdf")
    return out


if __name__ == "__main__":
    build_pdf()
