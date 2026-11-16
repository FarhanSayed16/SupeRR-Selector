# PressurePulse — Complete Frontend Implementation Plan

**Scope:** Frontend only — pages, navigation, design system, motion, components, scalability.  
**No code in this document** — structures, headings, and what must exist on screen.  
**Product:** RR-branded Pressure Intelligence dashboard for SupeRR Selector Season 2.  
**Related docs:** [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) · [`TECH_STACK_AND_SYSTEM.md`](./TECH_STACK_AND_SYSTEM.md) · [`BACKEND_PLAN.md`](./BACKEND_PLAN.md)

---

## 1. Frontend mission

Build a **professional, franchise-grade war-room dashboard** that Rajasthan Royals analysts and Unstop judges can open on a live URL and immediately understand:

- What “pressure” means in this system  
- Who the Top 10 batters and bowlers are  
- Why each pick is backed by evidence  
- How picks could strengthen RR for IPL 2027  

The UI must feel like **Rajasthan Royals digital** — pink energy, navy depth, gold accents — not a generic analytics template. It must be **highly scalable**: new players, seasons, and modules should plug in without redesigning the shell.

---

## 2. Product experience principles

| Principle | Meaning for UI |
|-----------|----------------|
| Brand first | First viewport reads as RR / PressurePulse, not a blank BI tool |
| One job per page | Each route has one primary analyst task |
| Evidence over decoration | Every claim links to a chart, metric, or player proof |
| War-room clarity | Dense data is allowed; clutter and competing CTAs are not |
| Motion with purpose | Transitions guide hierarchy; no noisy loops |
| Mobile usable, desktop primary | Analysts review on laptop; phone must still work |
| Scalable shell | Layout, nav, tokens, and data contracts stay stable as content grows |
| Accessible contrast | Pink/navy/white combinations stay readable |

---

## 3. Design system (visual foundation)

### 3.1 Theme direction

**Name:** Royals War-Room Dark + Pink Signal  

- Dominant surfaces: midnight navy / deep purple  
- Signal colour: royal pink for CTAs, active states, key numbers  
- Sparse gold for rank #1 / premium highlights only  
- Light “evidence panels” (white / soft surface) for heavy tables and infographics — same pattern as RR “in numbers” sections  
- Diagonal stripe / velocity motif in heroes and section headers (subtle, not wallpaper noise)

**Avoid**

- Generic purple-on-white SaaS look  
- Cream + terracotta editorial look  
- Neon glow overload  
- Emoji as UI  
- Too many rounded-full pills  
- Multi-layer muddy shadows  

---

### 3.2 Colour system (tokens)

| Token role | Direction | Usage |
|------------|-----------|--------|
| Primary pink | Hot magenta / RR pink | Primary buttons, active nav, links, key highlights |
| Pink deep | Darker pink | Hover / pressed states |
| Navy | Midnight blue | App chrome, side nav, footers |
| Purple deep | Dark purple | Premium player panels, hero gradients |
| Gold | Royal gold | Rank 1 badge, sparse “elite” markers |
| Surface light | Near-white soft tint | Tables, methodology long-read, “in numbers” blocks |
| Surface dark | Navy/purple | Default app background |
| Text primary (on dark) | White | Headings on dark |
| Text primary (on light) | Navy | Headings on light panels |
| Text muted | Cool grey-blue | Captions, meta |
| Success / confidence high | Clear green (restrained) | High confidence badges |
| Warning / confidence mid | Amber | Medium sample |
| Danger / confidence low | Soft red | Low sample / caution |
| Border subtle | Low-contrast line | Card edges without heavy boxing |

**Rule:** Pink is the *signal*, navy is the *stage*, gold is the *medal* — never equal volume of all three.

---

### 3.3 Typography

| Role | Character | Use |
|------|-----------|-----|
| Display | Bold, athletic sans (expressive, not Inter/Roboto default stack) | Hero titles, Command Centre brand line |
| Heading | Strong sans, tight tracking | Page H1/H2, section titles |
| Body | Clean readable sans | Explanations, methodology |
| Data / numerals | Tabular figures, slightly condensed OK | Rank tables, SR, economy, scores |
| Label / overline | Small caps or uppercase micro labels | “TOP 10”, “PRESSURE LAB”, “IPL WEIGHTED” |

**Hierarchy rules**

- One display moment per page (usually top)  
- Numbers in tables must align and scan faster than prose  
- Methodology page allows longer reading measure; intel pages stay scannable  

---

### 3.4 Iconography

**Style:** Professional outlined / duotone icons (consistent stroke), sports-analytics tone.  
**Library direction:** Single icon set across the app (e.g. Lucide-class consistency) — no mixed cartoon packs.

**Icon domains to plan**

| Domain | Example concepts |
|--------|------------------|
| Nav | Command centre, bat, ball, flask/lab, user, auction gavel, book |
| Metrics | Trend up, target, clock, wicket stump, flame (pressure), shield |
| Status | Check, alert, info, lock (frozen ranks) |
| Actions | Filter, download, share, search, expand |
| Confidence | Signal bars / shield levels — not traffic-light chaos |

**Rules**

- Icons support labels; never icon-only for critical actions on first visit  
- Active nav = pink icon + label  
- Decorative icons in hero only if they reinforce cricket/pressure meaning  

---

### 3.5 Spacing, radius, elevation

| Token | Direction |
|-------|-----------|
| Spacing scale | Tight war-room density on tables; generous hero breathing room |
| Radius | Moderate (professional cards) — not pill-everything |
| Elevation | Soft separation on dark UI; stronger on light evidence panels |
| Grid | 12-column desktop; stacked single column mobile |
| Max content width | Wide for tables (analyst), constrained for methodology prose |

**Cards policy**

- Cards allowed for interactive units (player rank row, metric tile, filter group)  
- Hero is **not** a collage of mini-cards  
- If removing border/shadow doesn’t hurt understanding, don’t use a card  

---

### 3.6 Imagery & motifs

- Hero: brand wordmark + pressure tagline + subtle diagonal energy (RR reference language)  
- Player panels: dark premium background, large numerals, optional silhouette/placeholder avatar  
- Empty / loading: branded skeleton shapes, not blank white flashes  
- No heavy stock photo clutter competing with data  

---

## 4. Information architecture & navigation

### 4.1 Primary navigation (always available)

| Order | Nav item | Route concept | Primary job |
|------:|----------|---------------|-------------|
| 1 | Command Centre | `/` | Land, brand, headline findings |
| 2 | Batters | `/batters` | Explore batter pressure rankings |
| 3 | Bowlers | `/bowlers` | Explore bowler pressure rankings |
| 4 | Pressure Lab | `/pressure-lab` | Understand & trust the definition |
| 5 | Auction Room | `/auction-room` | RR squad-fit narrative |
| 6 | Methodology | `/methodology` | Full transparency for analysts |
| — | Player Profile | `/players/:id` | Deep dive (reached from lists, not always top-level) |

**Optional secondary**

| Item | Purpose |
|------|---------|
| About / Disclaimer | Data pack use, competition context |
| Download ranks | Export Top 10 CSV from aggregates |
| Freeze badge | Shows pipeline version / build time |

---

### 4.2 Navigation chrome layout

**Desktop**

- Top bar: PressurePulse wordmark + RR-inspired mark + primary nav links + search players  
- Subtle pink underline / pill for active route  
- Right cluster: data version chip, “Ranks frozen” indicator  

**Tablet**

- Compact top nav or collapsible secondary items  

**Mobile**

- Sticky top brand bar  
- Bottom tab bar **or** hamburger drawer for the six primary destinations  
- Player search in drawer / overlay  

---

### 4.3 Global search

- Search players by name from any page  
- Results show role badges (Batter / Bowler / Both) + headline PressureScore  
- Selecting a result opens Player Profile  
- Keyboard-friendly (analysts love `/` to focus search — plan as enhancement)  

---

### 4.4 Breadcrumbs & wayfinding

- List → Player: `Batters / #3 Player Name`  
- Auction Room → Player deep links preserve context  
- Back affordance on profile (“Back to Batters”) with scroll restoration where possible  

---

## 5. Full page inventory

### Page 01 — Command Centre (Home)

**Purpose:** First impression + executive summary for RR.  
**Mood:** Brand-led hero, then decisive findings (not a widget dump).

**Sections (in order)**

1. **Hero composition**
   - Brand: PressurePulse × Rajasthan Royals signal  
   - One headline about reliable players under pressure  
   - One supporting sentence (IPL + T20I 2022–26 coverage)  
   - CTA group: “View Top Batters” · “View Top Bowlers” · “Open Pressure Lab”  
   - Dominant visual plane (gradient / diagonal motif / subtle cricket energy) — full-bleed feel  
2. **Headline rankings strip**
   - Top 3 batters + Top 3 bowlers preview (not full tables)  
   - Rank medals; gold only on #1  
3. **Pressure in one glance**
   - Definition one-liner  
   - 3–4 signal chips (chase tightness, wickets left, death contest, knockouts)  
   - Link into Pressure Lab  
4. **System confidence bar**
   - Data seasons covered  
   - Pipeline / pressure version  
   - High-level QA status (“Sensitivity stable” style message)  
5. **RR auction teaser**
   - Short bridge into Auction Room (“How these picks strengthen RR”)  
6. **Footer strip**
   - Disclaimer: derived aggregates; competition context  

**Animations on this page**

- Hero text fade/slide-up on load  
- Rank preview stagger-in  
- Soft parallax or gradient shift on hero (subtle)  
- CTA hover pink lift  

---

### Page 02 — Batter Intelligence

**Purpose:** Full batter universe under pressure; filter, compare, open profiles.

**Sections**

1. Page header — title, short remit, IPL-weighted vs Combined toggle  
2. **KPI row** — eligible batters count, median uplift, % pressure balls (batting context)  
3. **Filter / control rail**
   - Competition view (IPL weighted / Combined / IPL only if available)  
   - Confidence filter  
   - Min sample quick filters  
   - Search within table  
4. **Official Top 10 board**
   - Ranked cards or premium table  
   - Columns concept: Rank, Player, PressureScore, Uplift, SR under pressure, Balls, Confidence, RR-fit tag  
5. **Extended rankings** (11+)
   - Scalable virtualised/paginated table for growth  
6. **Compare tray** (optional enhancement)
   - Pin up to 3 batters for side-by-side metric comparison  
7. Empty / low-data states with clear messaging  

**Interactions**

- Row click → Player Profile  
- Sort by score / uplift / volume  
- Export current Top 10 view  

---

### Page 03 — Bowler Intelligence

**Purpose:** Mirror of Batter Intelligence for bowling — same IA, bowling metrics.

**Sections**

1. Header + competition toggle  
2. KPI row (economy under pressure, wicket rate, eligible bowlers)  
3. Filters (pace/spin supporting filter if data exported)  
4. Official Top 10 board  
5. Extended rankings  
6. Compare tray  

**Metric columns concept:** Rank, Player, PressureScore, Uplift, Economy (P), Wicket rate (P), Balls, Confidence  

**Design note:** Keep layout symmetry with Batters so RR staff learn once, use twice.

---

### Page 04 — Pressure Lab

**Purpose:** Make the definition credible and interactive — the trust page.

**Sections**

1. **Definition manifesto**
   - What counts as pressure (human language)  
   - What does *not* count  
2. **Signal cards**
   - Each signal explained with icon + plain English + “why it matters”  
3. **Coverage diagnostics**
   - Share of balls labelled pressure  
   - Split: IPL vs T20I, phase (PP/middle/death), stage (league/knockout)  
4. **Baseline vs pressure contrast**
   - Visual proof the label changes the performance distribution  
5. **Sensitivity panel**
   - Show that Top 10 remains largely stable when thresholds nudge (from backend QA export)  
   - Read-only scenario chips (not a live recompute engine unless API exists)  
6. **Methodology deep-link**
   - CTA to full Methodology page  

**Tone:** Scientific but RR-branded — flask/lab iconography, not cold grey enterprise.

---

### Page 05 — Player Profile

**Purpose:** Evidence pack for one player — the page judges click from Top 10.

**Layout**

1. **Identity header**
   - Name, role badges, rank in batter and/or bowler lists if applicable  
   - Confidence badge  
   - Competition scope chips  
2. **Score hero**
   - PressureScore large numeral  
   - Uplift vs baseline  
   - Volume under pressure  
3. **Baseline vs Pressure dual panel**
   - Side-by-side metric tiles  
4. **Situation breakdown**
   - Phase charts, chase slices, knockout exposure (as available)  
5. **Consistency**
   - Match/season reliability view  
6. **RR fit note**
   - Short narrative from Auction Room data if present  
7. **Related players**
   - Nearby ranks (±2) for context  

**States**

- Loading skeleton matching header + tiles  
- Not found  
- Low sample caution banner  

---

### Page 06 — Auction Room (RR Fit)

**Purpose:** Bridge analytics → franchise decision narrative for IPL 2027.

**Sections**

1. Hero — “Strengthening Rajasthan Royals”  
2. **Role need board** (conceptual gaps: finisher, death bowler, etc. — narrative, clearly labelled as analysis view)  
3. **Pick cards for Top batters & bowlers**
   - Why this player  
   - Pressure proof (2 numbers + link to profile)  
   - Role fit line  
4. **Squad composition lens**
   - Domestic vs overseas flavour if enrichment exists  
   - All-rounder value callouts  
5. **Disclaimer**
   - Round 1 is pressure reliability, not full auction optimiser  

**Visual:** Dark premium + pink CTAs; feels closer to RR “Match Centre / spotlight” energy.

---

### Page 07 — Methodology

**Purpose:** Full transparency; readable long-form for RR Analytics.

**Sections**

1. Overview & reproducibility statement  
2. Data coverage  
3. Pressure definition (formal)  
4. Feature / state reconstruction summary  
5. Metrics dictionary (batting & bowling)  
6. Scoring & eligibility  
7. Fairness: IPL vs T20I, sample sizes  
8. Validation & limitations  
9. How to read the dashboard  
10. Appendix links / version freeze info  

**Design:** Light evidence surface for reading comfort; sticky mini-TOC on desktop; print-friendly friendly spacing.

---

### Page 08 — About / Disclaimer (small)

**Purpose:** Competition context, data usage note, credits, contact/submit reminder.

**Contents**

- SupeRR Selector Season 2 context  
- Aggregates-only public data statement  
- Build version  
- Optional journey/social link placeholder  

---

### System pages / states (must plan)

| State | Behaviour |
|-------|-----------|
| Global loading | Branded splash or route skeleton |
| Data fetch error | Retry + message; never blank crash |
| Empty filter result | Clear reset filters CTA |
| 404 route | Brand 404 with link home |
| Offline / stale | Optional “last built at” warning |

---

## 6. Component architecture (scalable UI kit)

Plan components in layers — **atoms → molecules → organisms → templates**.

### 6.1 Foundation components

- App shell (nav + content + footer)  
- Brand mark / wordmark  
- Button (primary pink, secondary outline, ghost)  
- Icon button  
- Badge / chip (role, confidence, competition)  
- Rank medal  
- Tooltip  
- Tabs  
- Toggle group (IPL / Combined)  
- Inputs: search, select, checkbox filters  
- Skeleton loaders  
- Empty state block  
- Modal / drawer (mobile filters, compare tray)  
- Toast (export success)  

### 6.2 Data components

- KPI stat tile  
- Metric dual compare (baseline vs pressure)  
- Ranking table (desktop)  
- Ranking card list (mobile)  
- Sparkline / mini trend  
- Distribution chart wrapper  
- Phase breakdown chart  
- Confidence meter  
- Player avatar placeholder  
- Freeze / version chip  

### 6.3 Domain organisms

- Top10Board  
- ExtendedRankTable  
- FilterRail  
- PressureSignalCard  
- PlayerIdentityHeader  
- AuctionPickCard  
- MethodologySection  
- GlobalPlayerSearch  

### 6.4 Page templates

- `WarRoomTemplate` — dark intel pages (Batters, Bowlers, Lab, Auction)  
- `EvidenceReadTemplate` — light long-read (Methodology)  
- `HeroLandingTemplate` — Command Centre  
- `ProfileTemplate` — Player  

**Scalability rule:** New pages should reuse templates + organisms; avoid one-off layouts per screen.

---

## 7. Motion, transitions & micro-interactions

### 7.1 Motion principles

| Principle | Application |
|-----------|-------------|
| Purposeful | Enter/exit explain hierarchy |
| Fast enough | Feel snappy on tables; slower only on hero |
| Reduced motion | Honour OS “reduce motion” — fade instead of big moves |
| Consistent easings | One entrance curve, one exit curve across app |
| No infinite distraction | No looping neon; cricket energy ≠ casino |

### 7.2 Required transition map

| Interaction | Motion plan |
|-------------|-------------|
| Route change | Short fade + slight vertical settle of page content |
| Nav active state | Pink underline / pill morph |
| Hero load | Stagger: brand → headline → CTA → preview strip |
| Rank rows enter | Staggered fade-up (Top 10), then table |
| Hover on rank row / card | Lift + border pink hint + cursor pointer |
| Button press | Scale down slightly + colour deepen |
| Filter apply | Table cross-fade; KPIs count-up optional |
| Chart appear on scroll | Once-per-view reveal (Pressure Lab, Profile) |
| Player profile open | Image/header fade; numbers count-up once |
| Modal / drawer | Slide from right (desktop filters) / bottom sheet (mobile) |
| Search overlay | Quick fade + focus trap |
| Export success | Toast slide-in |

### 7.3 Signature animations (2–3 intentional “presence” moments)

1. **Command Centre hero** — brand presence entrance  
2. **Pressure Lab signal cards** — sequential reveal proving definition seriousness  
3. **Top 10 medal lock-in** — subtle rank number emphasis when Official board loads  

Everything else stays quieter support motion.

### 7.4 Chart animation

- Bars/lines animate on first view  
- Tooltips instant  
- No continuous redraw churn on scroll  

---

## 8. Responsive & layout breakpoints

| Breakpoint | Behaviour |
|------------|-----------|
| Mobile | Single column; bottom/drawer nav; cards instead of wide tables; sticky CTAs sparingly |
| Tablet | 2-column KPI/filter; tables with horizontal scroll if needed |
| Desktop | Full war-room: filter rail + main stage; sticky TOC on Methodology |
| Wide | Cap readable prose; allow tables to use extra width |

**Touch targets:** Adequate for mobile rank cards and nav tabs.

---

## 9. Frontend folder structure (planning map)

```text
dashboard/
├── public/
│   ├── data/                 ← backend JSON aggregates only
│   ├── brand/                ← marks, favicon, og image
│   └── patterns/             ← optional diagonal motif assets
├── src/
│   ├── app/                  ← router shell, providers
│   ├── pages/                ← one module per route
│   ├── layouts/              ← WarRoom / Evidence / Hero / Profile
│   ├── components/
│   │   ├── foundation/
│   │   ├── data/
│   │   └── domain/
│   ├── features/             ← batters, bowlers, pressure-lab, auction, methodology
│   ├── design-system/        ← tokens, typography, icon map, motion tokens
│   ├── lib/                  ← data loaders, formatters, rank helpers
│   ├── types/                ← contracts matching backend JSON
│   ├── hooks/                ← filters, search, media query, reduced motion
│   └── styles/               ← global + token styles
└── (config files)
```

**Feature folders** keep each domain scalable (batters feature owns its table config, column defs, copy).

---

## 10. Data consumption plan (frontend side)

### 10.1 Sources

- Static JSON from backend delivery layer (default)  
- Optional API later without changing page IA  

### 10.2 Frontend data responsibilities

- Load meta + rankings + lab summaries on app start or per-route  
- Cache in memory for session  
- Format numbers (1 decimal economy, integer balls, signed uplift)  
- Never invent metrics client-side that contradict frozen ranks  
- Client filters only slice already-exported aggregates  

### 10.3 Loading strategy

| Route | Data needed first |
|-------|-------------------|
| Command Centre | meta, top10 both, pressure one-liner stats |
| Batters / Bowlers | full list + top10 for that role |
| Pressure Lab | pressure_summary + sensitivity summary |
| Player | player detail payload |
| Auction Room | rr_fit + top10 |
| Methodology | methodology package / static content keyed to version |

---

## 11. Content & microcopy guidelines

- Voice: confident, analytical, franchise-respectful  
- Prefer “under pressure” / “baseline” language consistently  
- Show units: SR, economy, balls, matches  
- Confidence always explained on first badge click/tooltip  
- Disclaimers short and visible, not buried only in footer  
- Auction Room must not overclaim (“guaranteed signing”)  

---

## 12. Accessibility & professionalism checklist

- [ ] Colour contrast sufficient for pink-on-navy and text-on-pink buttons  
- [ ] Focus states visible for keyboard users  
- [ ] Charts not colour-only (patterns/labels too)  
- [ ] Reduced motion path  
- [ ] Alt text for brand/meaningful images  
- [ ] Tables have clear headers  
- [ ] Form controls labelled (search/filters)  

---

## 13. Performance & scalability plan

| Concern | Plan |
|---------|------|
| Bundle size | Code-split by route |
| Large rank lists | Pagination or virtualisation |
| Charts | Lazy-load chart library on Lab/Profile |
| Images | Few, optimised; CSS motifs preferred |
| Data growth | JSON contracts versioned; UI reads `meta.pressure_version` |
| New modules | Add feature folder + nav item + template reuse |
| Design drift | Tokens only — no one-off hex in random components |

**Scalable app definition here:** same shell can absorb IPL 2027 refresh data, more players, extra lab signals, and Round 2 modules without redesigning navigation or tokens.

---

## 14. Quality bar before RR review

- [ ] All primary routes reachable from nav  
- [ ] Top 10 on UI matches backend freeze / PDF  
- [ ] Player profiles open for every Top 10 name  
- [ ] Pressure Lab explains definition without reading Methodology  
- [ ] Mobile doesn’t break tables into unusable mush  
- [ ] Animations feel premium, not laggy  
- [ ] Brand reads RR within first viewport  
- [ ] Empty/error states look intentional  
- [ ] Lighthouse-level basics: no console errors, fast first paint on Vercel  

---

## 15. Frontend build sequence (implementation order)

### Phase F1 — Design system & shell

1. Tokens (colour, type, space, motion)  
2. Icon map  
3. App shell + responsive nav  
4. Route stubs for all pages  

### Phase F2 — Command Centre + shared data components

5. KPI tiles, badges, rank medals  
6. Home hero + Top 3 previews  
7. Global search  

### Phase F3 — Intelligence pages

8. Batter Intelligence full  
9. Bowler Intelligence full  
10. Shared ranking table/card system  

### Phase F4 — Trust & depth

11. Pressure Lab  
12. Player Profile  
13. Methodology  

### Phase F5 — Narrative & polish

14. Auction Room  
15. Motion pass + reduced motion  
16. Empty/error/404  
17. Responsive hardening  
18. Deploy preview for RR/Unstop link  

---

## 16. Definition of done (frontend)

Frontend is complete when:

1. All planned pages exist and navigate cleanly.  
2. Design system is consistent (pink signal / navy stage / gold medals).  
3. Official Top 10s are visible, filterable, and link to evidence profiles.  
4. Pressure Lab makes the definition understandable.  
5. Auction Room tells RR-fit story without overclaiming.  
6. Motion and transitions feel professional and purposeful.  
7. App is responsive, accessible enough for review, and deployed on a shareable URL.  
8. UI stays scalable: new JSON builds refresh content without structural rewrites.  

---

## 17. Doc map

| Doc | Role |
|-----|------|
| `PROJECT_PLAN.md` | Competition problem & submission |
| `BACKEND_PLAN.md` | Engine modules & exports FE consumes |
| `TECH_STACK_AND_SYSTEM.md` | Stack & deploy |
| **`FRONTEND_PLAN.md`** | Pages, nav, design, motion, UI structure (this file) |

---

## 18. One-page frontend summary

**Shell:** RR war-room chrome with clear primary nav and player search.  
**Pages:** Command Centre · Batters · Bowlers · Pressure Lab · Player Profile · Auction Room · Methodology · About.  
**Look:** Navy/purple stage, pink signals, gold for #1, light evidence panels for dense proof.  
**Icons:** One professional set; cricket + analytics metaphors.  
**Motion:** Route fades, hero stagger, rank hover lift, lab reveals, profile number emphasis — plus reduced-motion fallback.  
**Scale:** Tokenised design system, feature folders, route code-split, JSON contracts, reusable templates.

That is the complete frontend plan — every page, navigation, design language, and motion system — ready to build as a professional, highly scalable RR-facing application.
