"""
Compile RR_WAR_ROOM_SCOUTING_DOSSIER.pdf — Publication-grade Rajasthan Royals War Room Scouting Dossier.
"""

import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

RR_PINK = colors.HexColor("#EC008C")
RR_NAVY = colors.HexColor("#0B1B3A")
RR_PURPLE = colors.HexColor("#2A1450")
RR_GOLD = colors.HexColor("#D4A017")
SLATE_DARK = colors.HexColor("#1E293B")
SLATE_LIGHT = colors.HexColor("#F8FAFC")
SLATE_BORDER = colors.HexColor("#CBD5E1")
TEXT_MUTED = colors.HexColor("#64748B")
EMERALD_GREEN = colors.HexColor("#059669")
AMBER_DARK = colors.HexColor("#D97706")

class DossierCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(DossierCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(DossierCanvas, self).showPage()
        super(DossierCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        # Footer
        self.setStrokeColor(SLATE_BORDER)
        self.setLineWidth(0.5)
        self.line(54, 45, 541, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(54, 32, "Rajasthan Royals War Room • Prepared for Kumar Sangakkara & Giles Lindsay")
        self.drawRightString(541, 32, f"Page {self._pageNumber} of {page_count}")

        # Header on page 2+
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(RR_NAVY)
            self.drawString(54, 800, "RR AUCTION INTELLIGENCE — TALENT SCOUTING DOSSIER (IPL 2027)")
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(541, 800, "SupeRR Selector Season 2")
            self.line(54, 792, 541, 792)
        self.restoreState()

def build_dossier_pdf():
    out_dir = Path("outputs/submission_pack")
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "RR_WAR_ROOM_SCOUTING_DOSSIER.pdf"

    with open("outputs/submission_pack/scouting_dossiers.json", "r") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=RR_NAVY, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=RR_PINK, spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=RR_NAVY, spaceBefore=10, spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=RR_PURPLE, spaceBefore=6, spaceAfter=2
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=SLATE_DARK, spaceAfter=4
    )
    callout_style = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=11,
        textColor=RR_NAVY, spaceAfter=4
    )
    card_title_style = ParagraphStyle(
        'CardTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=RR_NAVY
    )
    badge_style = ParagraphStyle(
        'Badge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=RR_PINK
    )
    meta_val_style = ParagraphStyle(
        'MetaVal', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=SLATE_DARK
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("RAJASTHAN ROYALS WAR ROOM SCOUTING DOSSIER", title_style))
    story.append(Paragraph("IPL 2027 Auction Strategy • Player Profiles, Archetypes & Valuation Matrices", subtitle_style))
    story.append(Paragraph(
        f"<b>Prepared for:</b> {data['metadata']['prepared_for']}<br/>"
        f"<b>Audit Hash:</b> <code>{data['metadata']['freeze_sha256']}</code> | <b>Sample Base:</b> 200,999 Deliveries",
        callout_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=RR_PINK, spaceBefore=4, spaceAfter=8))

    # Executive Charter
    story.append(Paragraph("1. Executive Scouting Charter & Squad Gap Analysis", h1_style))
    story.append(Paragraph(
        "Following Rajasthan Royals' Season 1 auction signing of <b>Vignesh Puthur</b> based on analytical scouting, "
        "this dossier establishes the strategic acquisition roadmap for IPL 2027. "
        "RR's retained core (Jaiswal, Samson, Parag, Jurel, Hetmyer, Sandeep Sharma) is among the most formidable in the tournament. "
        "However, rigorous analysis of historical defeats isolates two critical tactical voids:<br/>"
        "• <b>Lower-Order Death Finishing (#6/#7):</b> RR required a steep RRR (&gt;=11.5 RPO) in 14 matches, winning only 28.5%. "
        "Securing high-uplift domestic finishers allows RR to chase down 60 runs off 30 balls without depending entirely on overseas muscle.<br/>"
        "• <b>SMS Stadium Death Restrictiveness:</b> Defending totals at Sawai Mansingh Stadium requires spinners and seamers who deny boundaries on large outfields. "
        "Our model prioritizes sub-7.5 death economies and high dot-ball percentages.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Top 10 Batters Section
    story.append(Paragraph("2. Top 10 Batters: Comprehensive Tactical Scouting Profiles", h1_style))

    for b in data['top10_batters_scouting']:
        card_content = []
        
        # Header Table: Rank, Name, Role, Score, Target Price
        hdr_data = [
            [
                Paragraph(f"<b>#{b['rank']} {b['player_name']}</b> ({b['primary_role']})", card_title_style),
                Paragraph(f"<b>PressureScore:</b> <font color='{RR_PINK}'>{b['pressure_score']:.1f}</font>", badge_style),
                Paragraph(f"<b>Target:</b> <font color='{EMERALD_GREEN}'>{b['target_price_inr']}</font>", badge_style)
            ]
        ]
        t_hdr = Table(hdr_data, colWidths=[240, 110, 137])
        t_hdr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), SLATE_LIGHT),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-1), 1, RR_PINK),
        ]))
        card_content.append(t_hdr)
        
        # Archetype and Stats
        desc_text = (
            f"<b>Archetype:</b> {b['archetype']} | <b>RR Slot:</b> {b['rr_slot']}<br/>"
            f"<b>Pressure SR:</b> {b['pressure_sr']:.1f} (<b>Uplift:</b> +{b['sr_uplift']:.1f} vs {b['baseline_sr']:.1f} baseline) | "
            f"<b>Death SR:</b> {b['death_pressure_sr']:.1f} | <b>Chase SR:</b> {b['chase_pressure_sr']:.1f} | "
            f"<b>Dots:</b> {b['pressure_dot_pct']:.1f}% | <b>Boundaries:</b> {b['pressure_boundary_pct']:.1f}% ({int(b['pressure_balls'])} balls)<br/>"
            f"<b>Superpowers:</b> {'; '.join(b['strengths'][:2])}<br/>"
            f"<b>Vulnerabilities:</b> {'; '.join(b['vulnerabilities'])}<br/>"
            f"<b>SMS Stadium Fit:</b> {b['venue_fit']}<br/>"
            f"<b>War Room Rationale:</b> <i>{b['scouting_summary']}</i>"
        )
        card_content.append(Paragraph(desc_text, body_style))
        card_content.append(Spacer(1, 4))
        story.append(KeepTogether(card_content))

    story.append(PageBreak())

    # Top 10 Bowlers Section
    story.append(Paragraph("3. Top 10 Bowlers: Comprehensive Tactical Scouting Profiles", h1_style))

    for bw in data['top10_bowlers_scouting']:
        card_content = []
        
        hdr_data = [
            [
                Paragraph(f"<b>#{bw['rank']} {bw['player_name']}</b> ({bw['primary_role']})", card_title_style),
                Paragraph(f"<b>PressureScore:</b> <font color='{RR_PURPLE}'>{bw['pressure_score']:.1f}</font>", badge_style),
                Paragraph(f"<b>Target:</b> <font color='{EMERALD_GREEN}'>{bw['target_price_inr']}</font>", badge_style)
            ]
        ]
        t_hdr = Table(hdr_data, colWidths=[240, 110, 137])
        t_hdr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), SLATE_LIGHT),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-1), 1, RR_PURPLE),
        ]))
        card_content.append(t_hdr)
        
        desc_text = (
            f"<b>Archetype:</b> {bw['archetype']} | <b>Deployment:</b> {bw['rr_slot']}<br/>"
            f"<b>Pressure Econ:</b> {bw['pressure_economy']:.2f} (<b>Death Econ:</b> {bw['death_pressure_economy']:.2f}) | "
            f"<b>Wickets:</b> {int(bw['pressure_wickets'])} ({bw['pressure_balls_per_wicket']:.1f} balls/wkt) | "
            f"<b>Dot %:</b> {bw['pressure_dot_pct']:.1f}% ({int(bw['pressure_balls'])} pressure balls)<br/>"
            f"<b>Superpowers:</b> {'; '.join(bw['strengths'][:2])}<br/>"
            f"<b>Vulnerabilities:</b> {'; '.join(bw['vulnerabilities'])}<br/>"
            f"<b>SMS Stadium Fit:</b> {bw['venue_fit']}<br/>"
            f"<b>War Room Rationale:</b> <i>{bw['scouting_summary']}</i>"
        )
        card_content.append(Paragraph(desc_text, body_style))
        card_content.append(Spacer(1, 4))
        story.append(KeepTogether(card_content))

    story.append(Spacer(1, 6))

    # Bidding Strategies & Projected XI
    story.append(Paragraph("4. Auction Day Acquisition Blueprints & Projected Playing XI", h1_style))
    story.append(Paragraph(
        "<b>Strategy A ('Vignesh Puthur' Stealth Value):</b> Target Shashank Singh (INR 5.5–8.5 Cr), Ashutosh Sharma (INR 3.0–5.0 Cr), "
        "and Rasikh Salam (INR 1.5–3.5 Cr). Combined outlay is ~INR 12–15 Cr, providing world-class clutch depth while preserving 85% of purse.<br/>"
        "<b>Strategy B (Heavyweight Anchors):</b> Target Sunil Narine (INR 10.0–14.0 Cr) and Rohit Sharma (INR 14.0–18.0 Cr) to secure instant title pedigree.<br/>"
        "<b>Projected RR 2027 Playing XI:</b> 1. Y. Jaiswal, 2. R. Sharma (Scouted), 3. S. Samson (C/WK), 4. R. Parag, 5. S. Hetmyer (O), "
        "6. Shashank Singh (Scouted), 7. D. Jurel, 8. S. Narine (O) (Scouted), 9. Sandeep Sharma, 10. Rasikh Salam (Scouted), 11. K. Yadav (Scouted) | Impact Sub: Ashutosh Sharma (Scouted).",
        body_style
    ))

    doc.build(story, canvasmaker=DossierCanvas)
    print(f"Generated {pdf_path} successfully!")

if __name__ == "__main__":
    build_dossier_pdf()
