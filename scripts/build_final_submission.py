"""Build final Unstop Round 1 submission PDF + cleaned MD from frozen ranks."""
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
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RR_PINK = colors.HexColor("#EC008C")
RR_NAVY = colors.HexColor("#0B1B3A")
RR_PURPLE = colors.HexColor("#2A1450")
SLATE = colors.HexColor("#1E293B")
LIGHT = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#CBD5E1")
MUTED = colors.HexColor("#64748B")


class FooterCanvas(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._states = []

    def showPage(self):
        self._states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._states)
        for st in self._states:
            self.__dict__.update(st)
            self.saveState()
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(48, 40, 547, 40)
            self.setFont("Helvetica", 7.5)
            self.setFillColor(MUTED)
            self.drawString(48, 28, "PressurePulse · SupeRR Selector Season 2 · Round 1 · Confidential")
            self.drawRightString(547, 28, f"{self._pageNumber} / {n}")
            if self._pageNumber > 1:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(RR_NAVY)
                self.drawString(48, 810, "PRESSUREPULSE — RR AUCTION INTELLIGENCE (IPL 2027)")
                self.setFont("Helvetica", 8)
                self.setFillColor(MUTED)
                self.drawRightString(547, 810, "Auction Official")
                self.line(48, 802, 547, 802)
            self.restoreState()
            super().showPage()
        super().save()


def styles():
    b = getSampleStyleSheet()
    return {
        "brand": ParagraphStyle("brand", parent=b["Normal"], fontName="Helvetica-Bold",
                                fontSize=22, leading=26, textColor=RR_NAVY, spaceAfter=2),
        "sub": ParagraphStyle("sub", parent=b["Normal"], fontName="Helvetica-Bold",
                              fontSize=11, leading=14, textColor=RR_PINK, spaceAfter=4),
        "tag": ParagraphStyle("tag", parent=b["Normal"], fontName="Helvetica",
                              fontSize=9, leading=12, textColor=SLATE, spaceAfter=8),
        "h1": ParagraphStyle("h1", parent=b["Normal"], fontName="Helvetica-Bold",
                             fontSize=12, leading=15, textColor=RR_NAVY, spaceBefore=10, spaceAfter=4),
        "h2": ParagraphStyle("h2", parent=b["Normal"], fontName="Helvetica-Bold",
                             fontSize=9.5, leading=12, textColor=RR_PURPLE, spaceBefore=6, spaceAfter=3),
        "body": ParagraphStyle("body", parent=b["Normal"], fontName="Helvetica",
                               fontSize=8.5, leading=11.5, textColor=SLATE, spaceAfter=4),
        "bullet": ParagraphStyle("bullet", parent=b["Normal"], fontName="Helvetica",
                                 fontSize=8.5, leading=11.5, textColor=SLATE, leftIndent=10, spaceAfter=2),
        "th": ParagraphStyle("th", parent=b["Normal"], fontName="Helvetica-Bold",
                             fontSize=7, leading=9, textColor=colors.white, alignment=1),
        "td": ParagraphStyle("td", parent=b["Normal"], fontName="Helvetica",
                             fontSize=7, leading=9, textColor=SLATE),
        "tdc": ParagraphStyle("tdc", parent=b["Normal"], fontName="Helvetica",
                              fontSize=7, leading=9, textColor=SLATE, alignment=1),
        "tdb": ParagraphStyle("tdb", parent=b["Normal"], fontName="Helvetica-Bold",
                              fontSize=7, leading=9, textColor=RR_NAVY, alignment=1),
        "meta_k": ParagraphStyle("mk", parent=b["Normal"], fontName="Helvetica-Bold",
                                 fontSize=7.5, leading=9, textColor=MUTED),
        "meta_v": ParagraphStyle("mv", parent=b["Normal"], fontName="Helvetica",
                                 fontSize=7.5, leading=9, textColor=SLATE),
    }


def table(data, widths, header):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def build():
    s = styles()
    bat = pd.read_csv("outputs/rankings/top10_batters.csv")
    bowl = pd.read_csv("outputs/rankings/top10_bowlers.csv")
    freeze = json.loads(Path("outputs/rankings/frozen_top10_fingerprint.json").read_text(encoding="utf-8"))
    sha = freeze["freeze_sha256"]
    sens = freeze.get("sensitivity") or {}
    audit = freeze.get("audit_checks") or {}
    ver = freeze.get("pressure_version", "pressure_v1.1")

    story = []
    story.append(Paragraph("PRESSUREPULSE", s["brand"]))
    story.append(Paragraph("Rajasthan Royals Auction Intelligence — IPL 2027", s["sub"]))
    story.append(Paragraph(
        "SupeRR Selector Season 2 · Round 1 — Most reliable players under pressure",
        s["tag"],
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=RR_PINK, spaceBefore=0, spaceAfter=8))

    meta = [
        [Paragraph("Field", s["th"]), Paragraph("Value", s["th"])],
        [Paragraph("Dataset", s["meta_k"]), Paragraph("IPL &amp; T20I, 2022–2026", s["meta_v"])],
        [Paragraph("Deliveries", s["meta_k"]),
         Paragraph("200,999 (pressure: 78,868 · 39.24%)", s["meta_v"])],
        [Paragraph("Board", s["meta_k"]),
         Paragraph(f"<b>Auction Official</b> ({ver})", s["meta_v"])],
        [Paragraph("Freeze SHA256", s["meta_k"]),
         Paragraph(f"<font face='Courier' size='6.5'>{sha}</font>", s["meta_v"])],
        [Paragraph("Status", s["meta_k"]),
         Paragraph(str(freeze.get("status", "FROZEN_OFFICIAL")), s["meta_v"])],
    ]
    mt = Table(meta, colWidths=[90, 400])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), RR_NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(mt)

    story.append(Paragraph("1. What we solved", s["h1"]))
    story.append(Paragraph(
        "Rajasthan Royals needs auction targets who <b>raise their game when the match is on the line</b> — "
        "not career averages alone. PressurePulse rebuilds pre-delivery match state, tags high-leverage balls, "
        "scores each player against their own non-pressure baseline, and freezes a reproducible "
        "<b>Top 10 batters + Top 10 bowlers</b> list for IPL 2027.",
        s["body"],
    ))

    story.append(Paragraph("2. Official Top 10 Batters", s["h1"]))
    bat_data = [[
        Paragraph("R", s["th"]), Paragraph("Player", s["th"]), Paragraph("Role", s["th"]),
        Paragraph("P.Balls", s["th"]), Paragraph("P.SR", s["th"]), Paragraph("Base", s["th"]),
        Paragraph("Uplift", s["th"]), Paragraph("Score", s["th"]),
    ]]
    for _, r in bat.iterrows():
        bat_data.append([
            Paragraph(str(int(r["rank"])), s["tdb"]),
            Paragraph(str(r["player_name"]), s["td"]),
            Paragraph(str(r["primary_role"]), s["td"]),
            Paragraph(str(int(r["pressure_balls"])), s["tdc"]),
            Paragraph(f"{r['pressure_sr']:.1f}", s["tdc"]),
            Paragraph(f"{r['baseline_sr']:.1f}", s["tdc"]),
            Paragraph(f"+{r['sr_uplift']:.1f}", s["tdb"]),
            Paragraph(f"{r['pressure_score']:.1f}", s["tdb"]),
        ])
    story.append(table(bat_data, [20, 100, 95, 42, 38, 38, 40, 38], RR_NAVY))

    story.append(Paragraph("3. Official Top 10 Bowlers", s["h1"]))
    bowl_data = [[
        Paragraph("R", s["th"]), Paragraph("Player", s["th"]), Paragraph("Role", s["th"]),
        Paragraph("P.Balls", s["th"]), Paragraph("P.Econ", s["th"]), Paragraph("Death", s["th"]),
        Paragraph("Wkts", s["th"]), Paragraph("Score", s["th"]),
    ]]
    for _, r in bowl.iterrows():
        bowl_data.append([
            Paragraph(str(int(r["rank"])), s["tdb"]),
            Paragraph(str(r["player_name"]), s["td"]),
            Paragraph(str(r["primary_role"]), s["td"]),
            Paragraph(str(int(r["pressure_balls"])), s["tdc"]),
            Paragraph(f"{r['pressure_economy']:.2f}", s["tdc"]),
            Paragraph(f"{r['death_pressure_economy']:.2f}", s["tdc"]),
            Paragraph(str(int(r["pressure_wickets"])), s["tdb"]),
            Paragraph(f"{r['pressure_score']:.1f}", s["tdb"]),
        ])
    story.append(table(bowl_data, [20, 100, 95, 42, 40, 40, 36, 38], RR_PURPLE))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Pressure definition", s["h1"]))
    story.append(Paragraph(
        "A delivery is <b>high-pressure</b> when pre-ball context demands high-leverage execution: "
        "steep chase (RRR ≥ 9.5), death overs (16–20), collapse (≤3 wickets in hand), or knockout stages. "
        "Of <b>200,999</b> deliveries, <b>78,868 (39.24%)</b> are pressure. A material share sits outside death "
        "(powerplay ~10%, middle ~34%) — collapse defence and rising RRR, not slog overs alone.",
        s["body"],
    ))

    story.append(Paragraph("5. Scoring &amp; fairness", s["h1"]))
    story.append(Paragraph(
        "<b>Batters (0–100):</b> 40% clutch quality + 25% SR uplift vs own baseline + 20% consistency + 15% volume.<br/>"
        "<b>Bowlers (0–100):</b> 35% restrictiveness (economy + death soft-cap) + 30% wicket threat + "
        "15% economy uplift + 10% consistency + 10% volume.<br/>"
        "<b>Rates:</b> legal balls only; IPL <b>1.30×</b>, T20I <b>1.00×</b>.<br/>"
        "<b>Eligibility:</b> batters ≥50 / ≥40 / ≥5 matches / ≥40 IPL pressure balls; "
        "bowlers ≥80 / ≥60 / ≥5 / ≥60 IPL. Zero batter–bowler cross-list overlap.",
        s["body"],
    ))

    story.append(Paragraph("6. Validation &amp; reproducibility", s["h1"]))
    story.append(Paragraph(
        f"Pressure vs baseline leakage = <b>{audit.get('leakage_count', 0)}</b>. "
        f"Top 10 sensitivity retention: batters <b>{sens.get('batter_top10_stability_pct', 'n/a')}%</b>, "
        f"bowlers <b>{sens.get('bowler_top10_stability_pct', 'n/a')}%</b>. "
        f"IPL-only Top 12 overlap: bat <b>{sens.get('ipl_overlap_batters', 'n/a')}/10</b>, "
        f"bowl <b>{sens.get('ipl_overlap_bowlers', 'n/a')}/10</b>. "
        f"Reproducible via <font face='Courier' size='7.5'>python -m src.run_pipeline</font> "
        f"(SHA <font face='Courier' size='6.5'>{sha[:28]}…</font>).",
        s["body"],
    ))

    story.append(Paragraph("7. How these picks strengthen RR", s["h1"]))
    story.append(Paragraph(
        "Retained core (Jaiswal, Samson, Parag, Jurel, Hetmyer, Sandeep) covers top order and death seam. "
        "Gaps: lower-order finishing, death/middle restrict at SMS, and impact cover. "
        "Season 1 pattern (Vignesh Puthur): prefer high-leverage value over brand inflation.",
        s["body"],
    ))
    for line in [
        "<b>Shashank / Ashutosh / Rinku / DK / Pant</b> — finishers &amp; keepers who lift SR under pressure "
        "(Shashank +73; Ashutosh +93); solve chase volatility after top-order fails.",
        "<b>Rohit / Iyer / SKY / Stoinis / Naman</b> — high-floor middle, experience, and float roles for Jaipur chases.",
        "<b>Narine / Santner / Kuldeep / Rashid / Hasaranga / Varun</b> — spin choke for SMS square boundaries "
        "(Narine death econ 6.06).",
        "<b>Bumrah / Pathirana / Rasikh / Zampa</b> — death seam and wrist-spin strike; Rasikh is the domestic "
        "death-seam value pick.",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Projected XI:</b> Jaiswal, Rohit*, Samson (C/WK), Parag, Hetmyer, Shashank*, Jurel, Narine*, "
        "Sandeep, Rasikh*, Kuldeep* · <b>Impact:</b> Ashutosh* · (* scouted from this board)",
        s["body"],
    ))

    story.append(Paragraph("8. Limits", s["h1"]))
    story.append(Paragraph(
        "Auction Official privileges IPL sample floors — some T20I-only standouts remain on Global Combined only. "
        "These rankings measure pressure reliability, not retention status or purse maths.",
        s["body"],
    ))

    # Write PDF
    pdf_path = Path("PressurePulse_Round1_Submission.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path), pagesize=A4,
        leftMargin=48, rightMargin=48, topMargin=44, bottomMargin=48,
    )
    doc.build(story, canvasmaker=FooterCanvas)

    pack = Path("outputs/submission_pack")
    pack.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_path, pack / "PressurePulse_Methodology.pdf")
    shutil.copy2(pdf_path, pack / "PressurePulse_Round1_Submission.pdf")
    shutil.copy2(pdf_path, Path("outputs/report/PressurePulse_Methodology.pdf"))

    # Clean MD (submission body only — no Unstop meta)
    bat_md = "\n".join(
        f"| {int(r['rank'])} | {r['player_name']} | {r['primary_role']} | "
        f"{int(r['pressure_balls'])} | {r['pressure_sr']:.1f} | {r['baseline_sr']:.1f} | "
        f"+{r['sr_uplift']:.1f} | {r['pressure_score']:.1f} |"
        for _, r in bat.iterrows()
    )
    bowl_md = "\n".join(
        f"| {int(r['rank'])} | {r['player_name']} | {r['primary_role']} | "
        f"{int(r['pressure_balls'])} | {r['pressure_economy']:.2f} | "
        f"{r['death_pressure_economy']:.2f} | {int(r['pressure_wickets'])} | "
        f"{r['pressure_score']:.1f} |"
        for _, r in bowl.iterrows()
    )
    md = f"""# PRESSUREPULSE
## Rajasthan Royals Auction Intelligence — IPL 2027

**SupeRR Selector Season 2 · Round 1** — Most reliable players under pressure

| Field | Value |
|---|---|
| Dataset | IPL & T20I, 2022–2026 |
| Deliveries | 200,999 (pressure: 78,868 · 39.24%) |
| Board | **Auction Official** (`{ver}`) |
| Freeze SHA256 | `{sha}` |
| Status | {freeze.get('status', 'FROZEN_OFFICIAL')} |

---

## 1. What we solved

Rajasthan Royals needs auction targets who **raise their game when the match is on the line** — not career averages alone. PressurePulse rebuilds pre-delivery match state, tags high-leverage balls, scores each player against their own non-pressure baseline, and freezes a reproducible **Top 10 batters + Top 10 bowlers** list for IPL 2027.

---

## 2. Official Top 10 Batters

| Rank | Player | Role | Pressure balls | Pressure SR | Baseline SR | SR uplift | Score |
|---:|---|---|---:|---:|---:|---:|---:|
{bat_md}

---

## 3. Official Top 10 Bowlers

| Rank | Player | Role | Pressure balls | Pressure econ | Death econ | Wickets | Score |
|---:|---|---|---:|---:|---:|---:|---:|
{bowl_md}

---

## 4. Pressure definition

A delivery is **high-pressure** when pre-ball context demands high-leverage execution:

- steep chase (**RRR ≥ 9.5**)
- death overs (**16–20**)
- collapse (**≤ 3 wickets in hand**)
- knockout / playoff stages

Of **200,999** deliveries, **78,868 (39.24%)** are pressure. A material share sits **outside death** (powerplay ~10%, middle ~34%) — collapse defence and rising RRR, not slog overs alone.

---

## 5. Scoring & fairness

**Batters (0–100):** 40% clutch quality + 25% SR uplift vs own baseline + 20% consistency + 15% volume

**Bowlers (0–100):** 35% restrictiveness (economy + death soft-cap) + 30% wicket threat + 15% economy uplift + 10% consistency + 10% volume

**Rates:** legal balls only; IPL **1.30×**, T20I **1.00×**

**Eligibility:** batters ≥50 / ≥40 / ≥5 matches / ≥40 IPL pressure balls; bowlers ≥80 / ≥60 / ≥5 / ≥60 IPL. Zero batter–bowler cross-list overlap.

---

## 6. Validation & reproducibility

| Check | Result |
|---|---|
| Pressure ↔ baseline leakage | **{audit.get('leakage_count', 0)}** |
| Batter Top 10 sensitivity retention | **{sens.get('batter_top10_stability_pct', 'n/a')}%** |
| Bowler Top 10 sensitivity retention | **{sens.get('bowler_top10_stability_pct', 'n/a')}%** |
| IPL-only Top 12 overlap | bat **{sens.get('ipl_overlap_batters', 'n/a')}/10**, bowl **{sens.get('ipl_overlap_bowlers', 'n/a')}/10** |

Regen: `python -m src.run_pipeline` → SHA `{sha}`

---

## 7. How these picks strengthen RR

Retained core (Jaiswal, Samson, Parag, Jurel, Hetmyer, Sandeep) covers top order and death seam. Gaps: lower-order finishing, death/middle restrict at SMS, and impact cover. Season 1 pattern (Vignesh Puthur): prefer high-leverage value over brand inflation.

- **Shashank / Ashutosh / Rinku / DK / Pant** — finishers & keepers who lift SR under pressure (Shashank +73; Ashutosh +93); solve chase volatility after top-order fails.
- **Rohit / Iyer / SKY / Stoinis / Naman** — high-floor middle, experience, and float roles for Jaipur chases.
- **Narine / Santner / Kuldeep / Rashid / Hasaranga / Varun** — spin choke for SMS square boundaries (Narine death econ **6.06**).
- **Bumrah / Pathirana / Rasikh / Zampa** — death seam and wrist-spin strike; Rasikh is the domestic death-seam value pick.

**Projected XI:** Jaiswal, Rohit*, Samson (C/WK), Parag, Hetmyer, Shashank*, Jurel, Narine*, Sandeep, Rasikh*, Kuldeep* · **Impact:** Ashutosh* · (* scouted from this board)

---

## 8. Limits

Auction Official privileges IPL sample floors — some T20I-only standouts remain on Global Combined only. These rankings measure **pressure reliability**, not retention status or purse maths.

---

*PressurePulse · SupeRR Selector Season 2 · Round 1 · Auction Official freeze*
"""
    Path("PressurePulse_Round1_Submission.md").write_text(md, encoding="utf-8")
    (pack / "PressurePulse_Round1_Submission.md").write_text(md, encoding="utf-8")

    # Unstop form cheat-sheet (separate — not the submission report)
    guide = Path("outputs/submission_pack/UNSTOP_FORM_CHEATSHEET.md")
    guide.write_text(
        f"""# Unstop form cheat-sheet (do not upload this file)

## Upload this PDF
`PressurePulse_Round1_Submission.pdf`

## Batters 1→10
{chr(10).join(f"{int(r['rank'])}. {r['player_name']}" for _, r in bat.iterrows())}

## Bowlers 1→10
{chr(10).join(f"{int(r['rank'])}. {r['player_name']}" for _, r in bowl.iterrows())}

## Remarks
PressurePulse scores IPL/T20I players on high-leverage deliveries (78,868 of 200,999 balls), not career averages. Auction Official Top 10s are frozen (SHA a819c0e6). Priority RR fits: Shashank/Ashutosh finishers, Narine death restrict, Rasikh domestic death seam — full method + XI sketch in the PDF.
""",
        encoding="utf-8",
    )

    print(f"FINAL PDF: {pdf_path.resolve()}")
    print(f"pages ready for Unstop upload")


if __name__ == "__main__":
    build()
