# PressurePulse — Documentation Index & Execution Map

**Use this file** to know which document to open for which decision.  
**Use [`MASTER_PLAN.md`](./MASTER_PLAN.md)** as the day-to-day phase checklist until the project is fully shipped.

---

## 1. Document set (source of truth)

| # | Document | What it owns | When to open it |
|---|----------|--------------|-----------------|
| 1 | [`MASTER_PLAN.md`](./MASTER_PLAN.md) | **Final execution checklist** — phases, sub-phases, gates | Every working session |
| 2 | [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) | Problem statement, deliverables, data inventory, gaps, methodology intent, Unstop rules | Clarifying *what RR asked* |
| 3 | [`TECH_STACK_AND_SYSTEM.md`](./TECH_STACK_AND_SYSTEM.md) | Stack choices, system architecture, repo layout, deploy path | Setup, tooling, hosting |
| 4 | [`BACKEND_PLAN.md`](./BACKEND_PLAN.md) | Backend layers, services, modules, features, handoffs (no code) | Building the intel engine |
| 5 | [`FRONTEND_PLAN.md`](./FRONTEND_PLAN.md) | Pages, nav, design system, motion, UI structure (no code) | Building the dashboard |
| 5b | [`UI_GLASSMORPHIC_PLAN.md`](./UI_GLASSMORPHIC_PLAN.md) | **Locked RR Glass theme** — tokens, recipes, page mapping | Visual redesign / UI polish |
| 5c | [`ANALYSIS_HARDENING_PLAN.md`](./ANALYSIS_HARDENING_PLAN.md) | **pressure_v1.1** — Auction Official floors, weighted rates, sensitivity | Metric/score truth & re-freeze |
| 6 | [`projectdetails.md`](./projectdetails.md) | Unstop page scrape — timelines, prizes, form fields | Submission form fields |
| 7 | [`RRSitedata.md`](./RRSitedata.md) | RR website IA / tone reference | Brand & content cues |
| 8 | `1794678506882-9180.jpeg` | RR UI colour / layout reference | Visual design checks |
| 9 | Data Pack PDF + CSVs under `docs/dataset/.../Data Pack/` | Official problem PDF + proprietary data | Analysis only; keep private |

---

## 2. How the docs relate

```text
                    ┌─────────────────────────┐
                    │      MASTER_PLAN        │
                    │  (execute & check off)  │
                    └───────────┬─────────────┘
                                │ references
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
   PROJECT_PLAN          TECH_STACK_AND_SYSTEM     (submission
   (why / what)          (how / stack / deploy)     dates/form)
          │                     │
          ├──────────┬──────────┤
          ▼          ▼          ▼
     BACKEND_PLAN  FRONTEND_PLAN  brand refs
     (engine)      (dashboard)    (RR site + jpeg)
```

**Rule:** If MASTER_PLAN and a detail doc disagree on *process order*, follow MASTER_PLAN.  
**Rule:** If MASTER_PLAN and the Round 1 PDF disagree on *competition requirements*, follow the **official PDF** and update MASTER_PLAN.

---

## 3. Official competition anchors (do not lose)

| Item | Value |
|------|--------|
| Competition | SupeRR Selector Season 2 |
| Round | Round 1 — Reliable players under pressure |
| Required lists | Top 10 batters + Top 10 bowlers |
| Required upload | Methodology PDF or PPTX |
| Optional | Dashboard URL + journey video |
| Round 1 deadline | 18 Nov 2026, 11:59 PM IST |
| Registration deadline | 16 Nov 2026, 11:59 PM IST |
| Participation | Individual only |
| Data | Official pack = IPL + T20I from 2022 (private) |

---

## 4. Product name & stacks (locked for execution)

| Layer | Decision |
|-------|----------|
| Product | **PressurePulse** |
| Analytics | Python 3.11 + pandas / numpy / scipy (+ optional sklearn) |
| Dashboard | React + Vite + TypeScript + Tailwind + Recharts |
| Delivery to UI | Precomputed JSON aggregates only |
| Hosting | Vercel (dashboard) |
| Report | PDF/PPTX from frozen pipeline numbers |
| Optional API | Deferred unless needed |

---

## 5. Execution protocol

1. Open [`MASTER_PLAN.md`](./MASTER_PLAN.md).  
2. Work only inside the **current phase** (and its sub-phases).  
3. Check off sub-phases as done.  
4. Do not skip a **Phase Gate** — fix blockers first.  
5. Deep-dive into BACKEND / FRONTEND / TECH docs when a sub-phase needs detail.  
6. After Phase Gate passes, move to the next phase.  
7. At the end, run the **Final Master Gate** before Unstop submit.

---

## 6. Status legend (for MASTER_PLAN checkboxes)

| Mark | Meaning |
|------|---------|
| `[ ]` | Not started |
| `[~]` | In progress (optional manual mark) |
| `[x]` | Done and verified |
| `[!]` | Blocked — note why next to the item |

---

## 7. What “project complete” means

All of the following are true:

- Official Top 10 batters and Top 10 bowlers frozen and reproducible  
- Methodology PDF/PPTX matches those ranks  
- Dashboard live on shareable URL, RR-branded, all planned pages working  
- Unstop form filled (dropdowns + upload + optional links)  
- Raw data pack never published  
- MASTER_PLAN Final Master Gate fully checked  

---

## 8. Final Deliverables & Artifacts Map

| Artifact | File Path | Format & Design Standard |
| :--- | :--- | :--- |
| **Methodology Report** | `outputs/submission_pack/PressurePulse_Methodology.pdf` | Publication-Grade 2-Page PDF with brand styling, math formulas & tables |
| **Visual Scouting Dossier** | `outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.pdf` | 6-Page Executive Scouting Dossier with player cards & auction blueprints |
| **Scouting Markdown Dossier** | `outputs/submission_pack/RR_WAR_ROOM_SCOUTING_DOSSIER.md` | Complete 20-player scouting intelligence and tactical breakdown |
| **Unstop Submission Guide** | `outputs/submission_pack/UNSTOP_SUBMISSION_FORM_GUIDE.md` | Dropdown-by-dropdown instructions with 483-char remarks |
| **Machine-Readable Roster** | `outputs/submission_pack/submission_roster.json` | Verified JSON payload of Top 10 Batters & Bowlers |
| **Scouting Data Package** | `outputs/submission_pack/scouting_dossiers.json` | Structured JSON with archetypes, valuations & venue ratings |
| **Interactive Dashboard** | `dashboard/dist` | Production-compiled React 19 + Tailwind v4 + TS application |

---

*This index is Document 1 of 2 execution docs. Document 2 is `MASTER_PLAN.md`.*
