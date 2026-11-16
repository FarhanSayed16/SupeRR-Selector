# PressurePulse — Rajasthan Royals Auction Intelligence (IPL 2027)

> **SupeRR Selector Season 2 · Round 1: Identify the Most Reliable Players Under Pressure**  
> Developed for Rajasthan Royals × Unstop Challenge.

---

## 1. Executive Summary

**PressurePulse** is an end-to-end cricket analytics intelligence engine and war-room dashboard designed to quantify and rank player reliability under high-pressure T20 match situations. Utilizing historical ball-by-ball match data from IPL and T20 Internationals (2022–2026), the system reconstructs innings states, isolates high-leverage deliveries using a composite Pressure Index, measures performance uplift against each player's baseline, and outputs ranked **Top 10 Batters** and **Top 10 Bowlers** to inform Rajasthan Royals' IPL 2027 auction strategy.

---

## 2. Deliverables Summary

- **Top 10 Batters Under Pressure:** Ranked 1 to 10 with performance uplift, volume filters, and confidence intervals.
- **Top 10 Bowlers Under Pressure:** Ranked 1 to 10 evaluated on economy, dot-ball %, and wicket rate in pressure phases.
- **Methodology Report (PDF):** Mathematical definitions, baseline metrics, fairness criteria, player cards, and RR squad fit narrative.
- **Interactive Dashboard:** Franchise-grade war-room dashboard hosted on Vercel.

---

## 3. Repository Structure

```text
SupeRR Selector/
├── docs/                     # Strategic and planning documentation
│   ├── DOCS_INDEX.md         # Master index of documentation
│   ├── MASTER_PLAN.md        # 25-phase execution checklist and gates
│   ├── PROJECT_PLAN.md       # Problem statement, data inventory, and methodology
│   ├── TECH_STACK_AND_SYSTEM.md # Architecture, design tokens, and deploy guide
│   ├── BACKEND_PLAN.md       # Backend services, modules, and data handoffs
│   ├── FRONTEND_PLAN.md      # UI pages, wireframes, and design tokens
│   └── projectdetails.md     # Unstop competition guidelines & form fields
├── data/
│   ├── raw/                  # Official RR data pack (Private & Gitignored)
│   ├── processed/            # Derived analytical tables (Local/Gitignored)
│   └── external/             # Optional public enrichment data
├── src/                      # Python Pressure Intelligence Engine
│   ├── foundation/           # Config, logging, constants
│   ├── data_platform/        # Ingestion, cleaning, schema validation
│   ├── intelligence/         # State reconstruction, pressure index, metrics, ranking
│   ├── delivery/             # JSON & CSV export services for UI & report
│   └── run_pipeline.py       # Single-command orchestrator entry point
├── dashboard/                # React + Vite + TypeScript war-room dashboard
├── outputs/
│   ├── rankings/             # Official frozen Top 10 CSVs
│   ├── charts/               # Methodology report figures
│   ├── report/               # Final PDF methodology report
│   └── qa/                   # Pipeline validation & audit logs
├── NOTICE                    # Proprietary data usage notice
└── README.md                 # This file
```

---

## 4. Proprietary Data & Compliance Notice

The dataset provided under `data/raw/` is proprietary Rajasthan Royals data provided strictly for the SupeRR Selector Season 2 competition. Raw delivery-level CSVs are strictly gitignored and must never be exposed publicly. All public-facing deliverables and web dashboards operate exclusively on precomputed, aggregated JSON files.

---

## 5. Quickstart & Execution

### 5.1 Analytics Pipeline (Python 3.11+)
```bash
# Setup virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run full intelligence pipeline
python -m src.run_pipeline
```

### 5.2 Frontend Dashboard (Node.js 20+)
```bash
cd dashboard
npm install
npm run dev
```

---

## 6. Official Submission Tracker & Deliverables Inventory

| Component | Status | Location / Artifact |
| :--- | :---: | :--- |
| **Top 10 Batters** | ✅ Frozen | `outputs/rankings/top10_batters.csv` |
| **Top 10 Bowlers** | ✅ Frozen | `outputs/rankings/top10_bowlers.csv` |
| **Methodology Report (2-Page PDF)** | ✅ Compiled | `outputs/submission_pack/PressurePulse_Methodology.pdf` |
| **Visual Scouting Dossier (6-Page PDF)** | ✅ Compiled | `outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.pdf` |
| **Scouting Markdown Dossier** | ✅ Generated | `outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.md` |
| **Machine-Readable Scouting Data** | ✅ Exported | `outputs/submission_pack/scouting_dossiers.json` |
| **Submission Form & Dropdown Guide** | ✅ Ready | `outputs/submission_pack/UNSTOP_SUBMISSION_FORM_GUIDE.md` |
| **Interactive Dashboard (Web App)** | ✅ Built | `dashboard/dist` (Production bundle ready for Vercel) |
| **Audit Fingerprint (SHA256)** | ✅ Verified | `5cdd7b7451b5a6672dbfadccc3c36a9777ec5bafaec589339e22ba307202d272` |
