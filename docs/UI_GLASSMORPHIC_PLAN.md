# PressurePulse — RR Glassmorphic UI Plan (Locked)

**Theme name:** RR Glass  
**Status:** Locked for implementation  
**References:** AirWatch-style glassmorphism (frosted panels, floating pill nav, KPI strip) recolored for Rajasthan Royals  
**Companion:** [`FRONTEND_PLAN.md`](./FRONTEND_PLAN.md)

---

## 1. Design decision

| Keep from references | Adapt for RR |
|----------------------|--------------|
| Frosted translucent panels + backdrop blur | Soft pink → lavender → navy atmospheric wash (not sky blue) |
| Floating pill nav, white active pill | Pink icon/label on active; navy brand text |
| Large rounded glass cards + nested white subcards | Same structure |
| Soft shadows, high radius, generous padding | Same |
| Status chip (API ACTIVE pattern) | `RANKS FROZEN` / pipeline SHA chip |
| KPI strip + hero CTAs | Primary CTA = RR pink |

**Not used:** Turf-green palette · solid dark war-room chrome · literal AirWatch sky photo

---

## 2. Colour tokens

| Token | Value | Use |
|-------|-------|-----|
| `--rr-pink` | `#EC008C` | Primary CTA, active accents, key numbers |
| `--rr-pink-deep` | `#C4006E` | Hover / pressed |
| `--rr-pink-soft` | `#FDF2F8` | Soft pink washes / badges |
| `--rr-navy` | `#0B1B3A` | Titles, primary text |
| `--rr-purple` | `#2A1450` | Atmospheric gradient depth |
| `--rr-gold` | `#D4A017` | Rank #1 only |
| `--glass-fill` | `rgba(255,255,255,0.62)` | Panel fill |
| `--glass-border` | `rgba(255,255,255,0.7)` | 1px edge |
| `--text-muted` | `#64748B` | Captions |
| Chart primary | `#EC008C` | Pressure series |
| Chart secondary | `#0B1B3A` | Contrast series |
| Chart muted | `#94A3B8` | Baseline |

---

## 3. Component recipes

| Recipe | Spec |
|--------|------|
| `.glass-panel` | Frosted fill, blur, thin white border, radius 20–24px, soft shadow |
| `.glass-nav` | Floating frosted bar, sticky |
| `.glass-kpi` | Compact glass metric card with icon |
| `.glass-subcard` | Near-opaque white nested card inside glass |
| `.btn-primary` | Solid RR pink, white text, rounded-xl |
| `.btn-ghost` | Transparent / light glass border, navy text |
| `.nav-pill-active` | White solid + shadow + pink text |
| `.status-chip` | Soft pill + pulsing pink/green dot |

---

## 4. Page mapping

| Page | Glass treatment |
|------|-----------------|
| Command Centre | Hero glass + KPI strip + glass boards + nested chart subcard |
| Batters / Bowlers | Page header glass + filter rail + ranking glass table/cards |
| Pressure Lab | Signal glass cards + diagnostics panels |
| Player Profile | Identity glass header + dual metric subcards |
| Auction Room | Narrative glass + pick cards |
| Methodology / About | Readable glass long-form panels |

---

## 5. Motion

- Route content fade/settle  
- Nav pill transition  
- Card hover lift + brighter border  
- `prefers-reduced-motion`: fades only  

---

## 6. Do / Don’t

**Do:** Navy on glass for readability · pink as signal only · gold for #1 · nested white for dense tables  
**Don’t:** Emerald/turf leftovers · neon glow · sky-blue AirWatch clone · equal pink/navy/gold volume  
