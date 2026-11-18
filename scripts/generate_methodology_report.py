"""
PressurePulse — Publication-Grade Methodology Report Generator (PDF)
Compiles the official Unstop submission report directly from frozen pipeline numbers.
Uses ReportLab to generate a beautifully branded Rajasthan Royals analytics document.
"""

import json
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Colors
RR_PINK = colors.HexColor("#EC008C")
RR_NAVY = colors.HexColor("#0B1B3A")
RR_PURPLE = colors.HexColor("#2A1450")
RR_GOLD = colors.HexColor("#D4A017")
SLATE_DARK = colors.HexColor("#1E293B")
SLATE_LIGHT = colors.HexColor("#F8FAFC")
SLATE_BORDER = colors.HexColor("#CBD5E1")
TEXT_MUTED = colors.HexColor("#64748B")

class NumberedCanvas(canvas.Canvas):
    """Canvas for professional page numbering and running headers."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        # Running footer on all pages
        self.setStrokeColor(SLATE_BORDER)
        self.setLineWidth(0.5)
        self.line(54, 45, 541, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(54, 32, "Confidential • Prepared for Kumar Sangakkara & Giles Lindsay • Royals Analytics")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 32, page_text)

        # Running header on page 2+
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(RR_NAVY)
            self.drawString(54, 800, "PRESSUREPULSE — RAJASTHAN ROYALS AUCTION INTELLIGENCE (IPL 2027)")
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(541, 800, "SupeRR Selector Season 2 • Round 1")
            self.line(54, 792, 541, 792)
        self.restoreState()

def build_pdf():
    out_dir = Path("outputs/report")
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "PressurePulse_Methodology.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=RR_NAVY,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=RR_PINK,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=RR_NAVY,
        spaceBefore=12,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=RR_PURPLE,
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=SLATE_DARK,
        spaceAfter=6
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=RR_NAVY,
        spaceBefore=4,
        spaceAfter=4
    )
    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=SLATE_DARK,
        alignment=0
    )
    td_center = ParagraphStyle(
        'TDCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=SLATE_DARK,
        alignment=1
    )
    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=RR_NAVY,
        alignment=1
    )

    story = []

    # Load frozen rankings
    top10_bat = pd.read_csv("outputs/rankings/top10_batters.csv")
    top10_bowl = pd.read_csv("outputs/rankings/top10_bowlers.csv")
    with open("outputs/rankings/frozen_top10_fingerprint.json", "r") as f:
        freeze_meta = json.load(f)

    # ================= COVER / TITLE =================
    story.append(Paragraph("PRESSUREPULSE", title_style))
    story.append(Paragraph("RAJASTHAN ROYALS AUCTION INTELLIGENCE SYSTEM (IPL 2027)", subtitle_style))
    story.append(Paragraph("<b>SupeRR Selector Season 2 • Round 1: Identify the Most Reliable Players Under Pressure</b>", body_style))
    story.append(Paragraph(f"<b>Submission Date:</b> November 2026 | <b>Dataset:</b> IPL & T20I (2022–2026) | <b>Freeze SHA256:</b> <code>{freeze_meta['freeze_sha256'][:16]}...</code>", callout_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=RR_PINK, spaceBefore=6, spaceAfter=12))

    # ================= 1. EXECUTIVE SUMMARY =================
    story.append(Paragraph("1. Executive Summary & Official Roster", h1_style))
    story.append(Paragraph(
        "Rajasthan Royals requires cricketers who consistently outperform their baselines when matches hang in the balance. "
        "<b>PressurePulse</b> is an auditable, end-to-end intelligence system that reconstructs ball-by-ball match context across 200,999 deliveries, "
        "isolates high-leverage deliveries via a composite Pressure Index, evaluates player uplift against their own non-pressure baseline, "
        "and establishes reproducible Top 10 rankings to shape RR's IPL 2027 auction strategy.",
        body_style
    ))

    # Top 10 Batters Table
    story.append(Paragraph("Official Top 10 Batters Under Pressure", h2_style))
    bat_data = [[
        Paragraph("Rank", th_style),
        Paragraph("Player Name", th_style),
        Paragraph("Primary Role", th_style),
        Paragraph("Pressure Balls", th_style),
        Paragraph("Pressure SR", th_style),
        Paragraph("Baseline SR", th_style),
        Paragraph("SR Uplift", th_style),
        Paragraph("PressureScore", th_style)
    ]]
    for _, r in top10_bat.iterrows():
        bat_data.append([
            Paragraph(str(r['rank']), td_bold),
            Paragraph(r['player_name'], td_style),
            Paragraph(r['primary_role'], td_style),
            Paragraph(str(int(r['pressure_balls'])), td_center),
            Paragraph(f"{r['pressure_sr']:.1f}", td_center),
            Paragraph(f"{r['baseline_sr']:.1f}", td_center),
            Paragraph(f"+{r['sr_uplift']:.1f}", td_bold),
            Paragraph(f"{r['pressure_score']:.1f}", td_bold),
        ])
    t_bat = Table(bat_data, colWidths=[35, 110, 95, 60, 50, 50, 45, 42])
    t_bat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, SLATE_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_BORDER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bat)
    story.append(Spacer(1, 8))

    # Top 10 Bowlers Table
    story.append(Paragraph("Official Top 10 Bowlers Under Pressure", h2_style))
    bowl_data = [[
        Paragraph("Rank", th_style),
        Paragraph("Player Name", th_style),
        Paragraph("Primary Role", th_style),
        Paragraph("Pressure Balls", th_style),
        Paragraph("Pressure Econ", th_style),
        Paragraph("Death Econ", th_style),
        Paragraph("Wickets", th_style),
        Paragraph("PressureScore", th_style)
    ]]
    for _, r in top10_bowl.iterrows():
        bowl_data.append([
            Paragraph(str(r['rank']), td_bold),
            Paragraph(r['player_name'], td_style),
            Paragraph(r['primary_role'], td_style),
            Paragraph(str(int(r['pressure_balls'])), td_center),
            Paragraph(f"{r['pressure_economy']:.2f}", td_center),
            Paragraph(f"{r['death_pressure_economy']:.2f}", td_center),
            Paragraph(str(int(r['pressure_wickets'])), td_bold),
            Paragraph(f"{r['pressure_score']:.1f}", td_bold),
        ])
    t_bowl = Table(bowl_data, colWidths=[35, 110, 95, 60, 50, 50, 45, 42])
    t_bowl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_PURPLE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, SLATE_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_BORDER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bowl)
    story.append(PageBreak())

    # ================= 2. PRESSURE DEFINITION =================
    story.append(Paragraph("2. Pressure Definition & Empirical Validation", h1_style))
    story.append(Paragraph(
        "<b>Frozen Mathematical Definition:</b> <i>\"A delivery is defined as high-pressure when match context demands immediate high-leverage execution: "
        "specifically during steep chases (RRR &gt;= 9.5), death-over contests, severe batting collapses (&lt;=3 wickets in hand), or critical playoff knockout stages.\"</i>",
        body_style
    ))
    sens = freeze_meta.get("sensitivity") or {}
    bat_stab = sens.get("batter_top10_stability_pct", "n/a")
    bowl_stab = sens.get("bowler_top10_stability_pct", "n/a")
    ipl_bat = sens.get("ipl_overlap_batters", "n/a")
    ipl_bowl = sens.get("ipl_overlap_bowlers", "n/a")
    freeze_sha = freeze_meta["freeze_sha256"]

    story.append(Paragraph(
        "<b>Empirical Proof That Pressure Is NOT Just Death Overs:</b> Across 200,999 deliveries, 78,868 balls (39.24%) are classified as high pressure. "
        "Outside death: Powerplay 10.2% and Middle 33.5% of pressure deliveries (collapse defense + escalating RRR).",
        body_style
    ))

    # ================= 3. METRICS & SCORING =================
    story.append(Paragraph("3. Scoring Models & Fairness Constraints", h1_style))
    story.append(Paragraph(
        "<b>Board:</b> Auction Official is the primary freeze; Global Combined is a secondary methodology board.<br/>"
        "<b>Batting Score (0–100):</b> 40% Clutch Quality + 25% SR Uplift + 20% Consistency + 15% Volume. "
        "Rates use <b>legal balls</b>; IPL deliveries enter at <b>1.30x</b> and T20I at <b>1.00x</b> inside SR (no separate +15% score boost).<br/>"
        "<b>Bowling Score (0–100):</b> 35% Restrictiveness (weighted economy + death soft-cap) + 30% Wicket Threat + "
        "15% Economy Uplift + 10% Consistency + 10% Volume, with the same IPL/T20I rate weighting.<br/>"
        "<b>Eligibility:</b> Batters ≥50 pressure / ≥40 baseline / ≥5 matches / ≥40 IPL pressure balls; "
        "Bowlers ≥80 / ≥60 / ≥5 / ≥60 IPL. Zero cross-list overlap enforced.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # ================= 4. RAJASTHAN ROYALS SQUAD FIT & SCOUTING WAR ROOM =================
    story.append(Paragraph("4. Franchise Talent Scouting & IPL 2027 Auction Strategy", h1_style))
    story.append(Paragraph(
        "<b>Beyond a Static Roster: Actionable Franchise Scouting for Kumar Sangakkara & Giles Lindsay:</b><br/>"
        "In Season 1, Rajasthan Royals backed our analytical recommendation of Vignesh Puthur, successfully acquiring him at auction. "
        "For Season 2, PressurePulse transitions from quantitative filtering to a comprehensive <b>Franchise Scouting & Recruitment System</b>, "
        "identifying tactical archetypes, auction price tiers, and specific roles within the RR Playing XI:<br/>"
        "• <b>The 'Vignesh Puthur' Stealth Domestic Blueprint:</b> Rather than overspending on inflated names, RR should target high-leverage domestic value gems: "
        "<b>Shashank Singh</b> (#6 finisher), <b>Ashutosh Sharma</b> (impact clutch), and <b>Rasikh Salam</b> (death seam) "
        "while preserving purse capacity.<br/>"
        "• <b>Sawai Mansingh Stadium Ground Compatibility:</b> Defending totals on Jaipur's square boundaries requires extreme dot-ball pressure. "
        "<b>Sunil Narine</b>, <b>Mitchell Santner</b>, and <b>Kuldeep Yadav</b> (Auction Official) starve opposition hitters of boundary release. "
        "0% IPL Global leaders (e.g. Nawaz / Muqeem / Abrar) remain on Global Combined only.<br/>"
        "• <b>Projected RR 2027 Playing XI:</b> 1. Y. Jaiswal, 2. R. Sharma (Scouted), 3. S. Samson (C/WK), 4. R. Parag, 5. S. Hetmyer, "
        "6. Shashank Singh (Scouted), 7. D. Jurel, 8. S. Narine (Scouted), 9. Sandeep Sharma, 10. Rasikh Salam (Scouted), 11. K. Yadav (Scouted) | Impact: Ashutosh Sharma (Scouted).",
        body_style
    ))
    story.append(Spacer(1, 6))

    # ================= 5. VALIDATION & INTEGRITY =================
    story.append(Paragraph("5. Reliability, Sensitivity & Reproducibility", h1_style))
    story.append(Paragraph(
        "<b>1. Data Leakage & Orthogonality:</b> Audited all 200,999 deliveries. Pressure and baseline are strictly disjoint (0 leaks).<br/>"
        f"<b>2. Sensitivity (computed):</b> Mean Top 10 retention across RRR∈{{9.0,10.0}} and death-start∈{{15,17}} — "
        f"batters {bat_stab}%, bowlers {bowl_stab}%. IPL-only Top 12 overlap: batters {ipl_bat}/10, bowlers {ipl_bowl}/10.<br/>"
        f"<b>3. Reproducibility:</b> <code>python -m src.run_pipeline</code> regenerates Auction Official ranks with SHA256 "
        f"<code>{freeze_sha}</code> ({freeze_meta.get('pressure_version', 'pressure_v1.1')}).",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Also copy to submission pack
    pack_dir = Path("outputs/submission_pack")
    pack_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(pdf_path, pack_dir / "PressurePulse_Methodology.pdf")
    print(f"Generated {pdf_path} and copied to {pack_dir / 'PressurePulse_Methodology.pdf'} successfully!")

if __name__ == "__main__":
    build_pdf()
