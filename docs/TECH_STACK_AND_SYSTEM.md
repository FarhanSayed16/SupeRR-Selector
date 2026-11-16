# PressurePulse — Technical Stack, System Design & Deployment

**Product name:** PressurePulse (SupeRR Selector Season 2 · Round 1)  
**Goal:** A complete, deployable analytics system — not a one-off notebook — that Rajasthan Royals can open, explore, and trust.  
**Companion docs:**  
- [`DOCS_INDEX.md`](./DOCS_INDEX.md) — map of all planning docs  
- [`MASTER_PLAN.md`](./MASTER_PLAN.md) — **execution checklist** (25 phases + gates)  
- [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) — problem, data gaps, methodology, submission rules  
- [`BACKEND_PLAN.md`](./BACKEND_PLAN.md) — full backend modules, services, features, build order (no code)  
- [`FRONTEND_PLAN.md`](./FRONTEND_PLAN.md) — pages, navigation, design system, motion, UI structure (no code)  

**This doc:** Exact technical stack, architecture, dashboard/deploy overview, and production path.

---

## 1. Confirmation — what we are building

Yes — the plan is a **full system**, not only a PDF:

| Layer | Deliverable |
|-------|-------------|
| Data engine | Reproducible Python pipeline on the official RR data pack |
| Pressure intelligence | Defined Pressure Index + batter/bowler ratings |
| Rankings | Official Top 10 batters + Top 10 bowlers (exportable) |
| Dashboard | RR-branded interactive web app (live URL for Unstop + RR review) |
| Report | Methodology PDF/PPTX generated from the same pipeline outputs |
| Deployment | Public (or shareable) production URL RR can open without setup |
| Ops hygiene | `.gitignore` for proprietary CSVs, README, env samples, run scripts |

**Unstop still needs:** dropdown rankings + PDF/PPTX. The dashboard is the war-room face of the same system.

---

## 2. Technical stack (final choices)

### 2.1 Stack at a glance

| Concern | Choice | Version target | Why |
|---------|--------|----------------|-----|
| Language (analytics) | **Python** | 3.11+ | Best fit for cricket ball-by-ball wrangling |
| Dataframes | **pandas** + **pyarrow** | latest stable | Fast CSV/Parquet IO (~201k balls is fine) |
| Numerics | **numpy**, **scipy** | latest stable | Metrics, bootstrap CIs |
| Optional ML | **scikit-learn** | latest stable | Only if uplift/consistency models help; keep interpretable |
| API (optional) | **FastAPI** + **uvicorn** | latest stable | Serve rankings/search if not static-only |
| Frontend | **React 18** + **Vite** + **TypeScript** | current | Production-grade dashboard RR can click through |
| Styling | **Tailwind CSS** | v3/v4 | RR brand tokens (pink / navy / gold) |
| Charts | **Recharts** (+ **ECharts** if needed for heatmaps) | latest | Clean sports-analytics visuals |
| Routing / UI state | **React Router** | v6+ | Multi-page Command Centre |
| Icons | **lucide-react** | latest | Clean, not emoji-heavy |
| Report build | **HTML/CSS → PDF** (Playwright/Chromium) or **python-docx + export** | — | Matches methodology from same numbers |
| Package mgmt (FE) | **npm** / **pnpm** | — | Vite standard |
| Package mgmt (BE/analytics) | **pip** + `requirements.txt` (or uv) | — | Simple, reproducible |
| Hosting (dashboard) | **Vercel** | — | Fast shareable URL, free tier OK |
| Hosting (API, if used) | **Railway / Render / Fly.io** | — | Only if dynamic API is needed |
| Analytics data in prod | **Precomputed JSON / Parquet → static assets** | — | No need to ship raw proprietary CSVs to the browser |
| Version control | **Git** + private remote | — | Never publish raw data pack publicly |
| CI (light) | GitHub Actions: lint + build dashboard | — | Catch breakages before RR opens the link |

### 2.2 Why this stack (and what we rejected)

| Alternative | Decision |
|-------------|----------|
| Streamlit-only | Faster, but looks less “franchise war room.” Use only as emergency fallback. |
| Next.js full-stack | Extra complexity for little gain before 18 Nov deadline. Vite SPA + static JSON is enough. |
| Pure Jupyter submission | Not a system RR can browse; notebooks stay internal for exploration. |
| Heavy ML black box | Risks disqualification narrative (“not transparent”). Prefer scored formulas + optional sklearn. |
| Shipping raw CSVs to frontend | Violates competition data rules + bloated bundle. Always ship **aggregates only**. |

### 2.3 Brand / design tokens (from RR UI reference)

Use CSS variables in the dashboard:

```css
:root {
  --rr-pink: #EC008C;      /* primary CTA / accents */
  --rr-pink-deep: #C4006E;
  --rr-navy: #0B1B3A;      /* dark panels, headers */
  --rr-purple: #2A1450;    /* premium player panels */
  --rr-gold: #D4A017;      /* sparse highlights */
  --rr-white: #FFFFFF;
  --rr-surface: #F7F4F8;   /* light page bg — not flat grey SaaS */
  --rr-text: #0B1B3A;
  --rr-muted: #5C6578;
}
```

**UI rules for the product**

- One composition per page (Command Centre ≠ cluttered BI board)
- RR pink for primary actions; navy/purple for depth; gold sparingly
- Diagonal stripe / energy patterns allowed in hero headers (match RR site feel)
- Charts: high contrast, readable on pink and navy panels
- No generic purple-gradient “AI startup” look

---

## 3. System architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                     PRESSUREPULSE SYSTEM                        │
├──────────────────────┬──────────────────────┬───────────────────┤
│  A. DATA LAYER       │  B. INTEL ENGINE     │  C. DELIVERY      │
│                      │                      │                   │
│  Official RR pack    │  State reconstruction│  React dashboard  │
│  (local, private)    │  Pressure Index      │  (Vercel URL)     │
│                      │  Batter/Bowler scores│                   │
│  Optional public     │  Ranking + CI        │  Methodology PDF  │
│  enrichment (squad)  │  Exports (JSON/CSV)  │  Unstop form      │
└──────────────────────┴──────────────────────┴───────────────────┘
```

### Data flow (end-to-end)

```text
Raw CSVs (private)
    → Python pipeline (`src/`)
        → processed Parquet / feature tables
            → player scores + Top 10 tables
                → `dashboard/public/data/*.json`  (aggregates only)
                → `outputs/report/` charts + tables
                    → Vite build → Vercel
                    → PDF report → Unstop upload
```

**RR experience:** open live URL → Command Centre → drill into batter/bowler intelligence → open player card → read methodology tab. No local Python needed for reviewers.

---

## 4. Repository structure (build exactly this)

```text
SupeRR Selector/
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── TECH_STACK_AND_SYSTEM.md      ← this file
│   ├── projectdetails.md
│   ├── RRSitedata.md
│   ├── 1794678506882-9180.jpeg
│   └── dataset/.../Data Pack/        ← PRIVATE raw CSVs + problem PDF
│
├── data/
│   ├── raw/                          ← symlink or copy of pack (gitignored)
│   ├── processed/                    ← engineered tables (gitignored or aggregates only)
│   └── external/                     ← optional public enrichment CSVs
│
├── src/                              ← Python intel engine
│   ├── __init__.py
│   ├── config.py                     ← paths, thresholds, brand constants
│   ├── load.py                       ← read & validate 6 CSVs
│   ├── state.py                      ← innings state reconstruction
│   ├── pressure.py                   ← Pressure Index definition
│   ├── metrics_batting.py
│   ├── metrics_bowling.py
│   ├── ranking.py                    ← eligibility, scores, Top 10
│   ├── validation.py                 ← sensitivity, bootstrap, QA checks
│   ├── export_dashboard.py           ← write JSON for frontend
│   ├── export_report.py              ← tables/charts for PDF
│   └── run_pipeline.py               ← single entry: python -m src.run_pipeline
│
├── notebooks/                        ← exploration only (not source of truth)
│   └── 01_eda.ipynb
│
├── outputs/
│   ├── rankings/
│   │   ├── top10_batters.csv
│   │   ├── top10_bowlers.csv
│   │   └── full_player_scores.csv
│   ├── charts/
│   ├── report/
│   │   └── PressurePulse_Methodology.pdf
│   └── qa/
│       └── validation_summary.json
│
├── dashboard/                        ← React + Vite + TS app
│   ├── public/
│   │   └── data/                     ← generated JSON (safe aggregates)
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── styles/
│   │   │   └── tokens.css
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── CommandCentre.tsx
│   │   │   ├── BatterIntelligence.tsx
│   │   │   ├── BowlerIntelligence.tsx
│   │   │   ├── PressureLab.tsx
│   │   │   ├── PlayerProfile.tsx
│   │   │   ├── AuctionRoom.tsx       ← RR fit narrative
│   │   │   └── Methodology.tsx
│   │   ├── lib/
│   │   │   └── data.ts               ← load JSON
│   │   └── types/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── api/                              ← OPTIONAL FastAPI (only if needed)
│   └── main.py
│
├── scripts/
│   ├── setup_env.sh / setup_env.ps1
│   ├── run_all.ps1                   ← pipeline → copy JSON → optional build
│   └── build_report.ps1
│
├── .gitignore                        ← raw data, .env, caches, node_modules
├── requirements.txt
├── README.md                         ← how RR / judges run or view the system
└── LICENSE / NOTICE                  ← competition data usage note
```

---

## 5. Dashboard product spec (what RR will see)

### 5.1 Pages / modules

| # | Page | Purpose | Key widgets |
|---|------|---------|-------------|
| 1 | **Command Centre** | Landing / hero for RR brand + headline findings | Top 10 preview, pressure definition one-liner, CTA into labs |
| 2 | **Batter Intelligence** | Full batter rankings & filters | Rank table, uplift chart, sample-size badges, IPL vs T20I toggle |
| 3 | **Bowler Intelligence** | Full bowler rankings & filters | Economy under pressure, wicket rate, death-over view |
| 4 | **Pressure Lab** | Prove the definition | Pressure vs baseline distributions, threshold slider (read-only or client filter on precomputed bins) |
| 5 | **Player Profile** | Deep dive one player | Baseline vs pressure cards, match timeline, role, confidence |
| 6 | **RR Auction Room** | Squad narrative | How Top picks fill RR gaps (public squad context) |
| 7 | **Methodology** | Transparency for analysts | Formulas, eligibility, limitations, reproducibility notes |

### 5.2 UX principles

- Mobile usable, desktop-first (analysts review on laptop)
- Fast load: precomputed JSON, no 40MB CSV in browser
- Every Top 10 claim clickable to evidence
- Confidence labels: High / Medium / Low sample
- Export buttons: CSV of current view (from aggregates)

### 5.3 JSON contracts (pipeline → dashboard)

Generate at least:

| File | Contents |
|------|----------|
| `meta.json` | Build timestamp, data seasons, pressure definition version, pipeline git hash |
| `top10_batters.json` | Rank, player_id, name, scores, sample, confidence |
| `top10_bowlers.json` | Same for bowlers |
| `players_index.json` | Searchable list (id, name, roles, scores) |
| `player_{id}.json` *or* `players_detail.json` | Per-player evidence payloads |
| `pressure_summary.json` | Distributions, % balls labelled pressure, stage breakdowns |
| `rr_fit.json` | Narrative bullets per Top pick |

Keep individual files small; prefer one `players_detail.json` if total &lt; ~2–3 MB.

---

## 6. Python intel engine — module responsibilities

| Module | Responsibility | Output |
|--------|----------------|--------|
| `load.py` | Read CSVs, dtype fixes, key integrity | Clean frames |
| `state.py` | Cumulative score/wickets/balls; chase target & RRR | Ball-level state table |
| `pressure.py` | Composite Pressure Index + binary `is_pressure` | Labelled balls |
| `metrics_batting.py` | SR, dots, boundaries, dismissals in/out pressure | Batter metrics |
| `metrics_bowling.py` | Economy, dots, wickets in/out pressure | Bowler metrics |
| `ranking.py` | Eligibility, PressureScore, Top 10 cut | Ranking tables |
| `validation.py` | Sensitivity, bootstrap, leakage checks | QA JSON |
| `export_dashboard.py` | Write dashboard JSON | `dashboard/public/data/*` |
| `export_report.py` | Charts + PDF inputs | `outputs/report/*` |
| `run_pipeline.py` | Orchestrate all steps | Exit 0 only if QA gates pass |

### Config knobs (`config.py`) — document every default in Methodology

- Pressure thresholds (RRR, wickets left, overs band, knockout weight)
- Min balls faced / bowled in pressure
- Min matches
- IPL weight vs T20I weight
- Recency weights (e.g. 2025–26 &gt; 2022)
- Super-over include/exclude

---

## 7. Environment setup

### 7.1 Prerequisites

- Windows 10/11 (your machine) or Mac/Linux
- Python 3.11+
- Node.js 20+
- Git
- (Optional) Vercel CLI for deploy

### 7.2 Python

```powershell
cd "d:\SupeRR Selector"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 7.3 `requirements.txt` (planned)

```text
pandas>=2.2
numpy>=1.26
pyarrow>=15
scipy>=1.11
scikit-learn>=1.4
matplotlib>=3.8
seaborn>=0.13
plotly>=5.18
jinja2>=3.1
python-docx>=1.1
fastapi>=0.110          # optional
uvicorn>=0.27           # optional
pydantic>=2.6
tqdm>=4.66
```

### 7.4 Dashboard

```powershell
cd dashboard
npm install
npm run dev          # local http://localhost:5173
npm run build        # production bundle
```

### 7.5 One-command local demo

`scripts/run_all.ps1` should:

1. Activate venv  
2. Run `python -m src.run_pipeline`  
3. Confirm JSON landed in `dashboard/public/data`  
4. Optionally `npm run build`  

---

## 8. Deployment plan (until RR can open it)

### 8.1 Recommended production path

| Step | Action | Result |
|------|--------|--------|
| 1 | Run pipeline locally | Fresh rankings + JSON |
| 2 | Commit **aggregates only** + dashboard code | Safe for remote |
| 3 | Deploy `dashboard/` to **Vercel** | Live HTTPS URL |
| 4 | Paste URL into Unstop “dashboard link” | Judges / RR open instantly |
| 5 | Upload PDF methodology | Formal submission artifact |

### 8.2 Vercel setup (frontend)

1. Create Vercel project pointing at `dashboard/`  
2. Build command: `npm run build`  
3. Output directory: `dist`  
4. Env: none required if fully static JSON  
5. Custom note in README: “Data shown are derived aggregates; raw pack not hosted.”

### 8.3 Optional API deploy

Only if you need live search beyond static JSON:

- Deploy `api/` to Railway/Render  
- Point Vite `VITE_API_URL` to that host  
- CORS allow Vercel domain only  

**Default recommendation:** skip API for Round 1; static JSON is enough and more reliable.

### 8.4 What RR / judges need

| Audience | What you give them |
|----------|--------------------|
| Unstop form | Top 10 dropdowns + PDF + dashboard URL |
| RR Analytics (review) | Same live URL + methodology clarity |
| You (local) | Full raw data + pipeline to regenerate |

No RR staff should need to install Python to evaluate Round 1.

### 8.5 Security & competition compliance

- `.gitignore`: `data/raw/`, full `ball_by_ball.csv`, `__MACOSX`, `.venv`, `.env`, large processed dumps  
- README warning: data pack is competition-only  
- Public repo (if any): **code + aggregates**, never full proprietary CSVs  
- Do not scrape or republish RR site assets illegally; use your own UI inspired by brand colours  

---

## 9. End-to-end “what exactly is to be done” (build checklist)

### Phase 0 — Foundations (half day)

- [ ] Create folder layout above  
- [ ] `requirements.txt`, `package.json`, `.gitignore`, root `README.md`  
- [ ] Copy/symlink data pack into `data/raw` (gitignored)  
- [ ] Brand tokens file in dashboard  

### Phase 1 — Intel engine (core)

- [ ] `load.py` + schema validation report  
- [ ] `state.py` chase/defend reconstruction  
- [ ] `pressure.py` v1 definition + labelled % summary  
- [ ] Batting & bowling metrics  
- [ ] Ranking + eligibility → draft Top 15  
- [ ] Validation / sensitivity  

### Phase 2 — Exports

- [ ] Official Top 10 CSV/JSON  
- [ ] Dashboard JSON pack  
- [ ] Chart assets for report  

### Phase 3 — Dashboard

- [ ] Vite + React + TS + Tailwind scaffold  
- [ ] Command Centre (RR hero)  
- [ ] Batter / Bowler intelligence pages  
- [ ] Pressure Lab  
- [ ] Player profile  
- [ ] Auction Room + Methodology  
- [ ] Wire all pages to JSON  

### Phase 4 — Report

- [ ] Methodology PDF from same numbers as dashboard  
- [ ] Cross-check Unstop names vs IDs vs PDF  

### Phase 5 — Deploy & submit

- [ ] Vercel production deploy  
- [ ] Smoke-test on phone + desktop  
- [ ] Fill Unstop rankings (exact order)  
- [ ] Upload PDF; paste dashboard URL  
- [ ] Optional journey video  

### Phase 6 — Freeze

- [ ] Tag release `v1.0-round1`  
- [ ] Store submission screenshots  
- [ ] Do not change rankings after form submit  

---

## 10. Definition of done (system complete)

The system is complete when all are true:

1. `python -m src.run_pipeline` regenerates identical Top 10s  
2. Dashboard on Vercel loads without errors and shows those Top 10s  
3. Methodology PDF explains pressure, metrics, fairness, limits  
4. Unstop dropdowns match PDF and dashboard  
5. Raw data pack is not publicly exposed  
6. RR reviewer can understand Pressure Lab without reading code  
7. README tells a stranger how to view (URL) and how you regenerate (pipeline)  

---

## 11. Timeline vs deadline (practical)

**Round 1 deadline:** 18 Nov 2026, 11:59 PM IST  

| Day | Focus |
|-----|--------|
| Day 1 | Pipeline: state + pressure + draft rankings |
| Day 2 | Harden rankings + validation + JSON export |
| Day 3 | Dashboard pages + RR branding |
| Day 4 | PDF + Vercel deploy + Unstop submit buffer |

If time slips: **freeze rankings + PDF first**, then ship a thinner dashboard (Command Centre + Top 10 + Methodology) rather than missing the form deadline.

---

## 12. Mapping docs — how to use them

| File | Use when |
|------|----------|
| [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) | What RR asked, data inventory, methodology blueprint, submission rules |
| [`TECH_STACK_AND_SYSTEM.md`](./TECH_STACK_AND_SYSTEM.md) | How we build, stack, architecture, dashboard, deploy |
| `projectdetails.md` | Unstop form fields / prizes / timelines reference |
| `RRSitedata.md` | RR site IA / tone reference |
| UI jpeg | Colour & layout inspiration |

---

## 13. Final answer — technical stack summary

**Analytics:** Python 3.11 · pandas · numpy · scipy · (optional scikit-learn)  
**App:** React · Vite · TypeScript · Tailwind · Recharts · React Router  
**Delivery:** Precomputed JSON aggregates · Methodology PDF  
**Deploy:** Vercel (dashboard) · local pipeline for regeneration  
**Optional:** FastAPI if dynamic API becomes necessary  

That is the complete system plan: from private data pack → pressure engine → RR-branded dashboard → production URL → Unstop submission, ready for Rajasthan Royals to open and work with.
