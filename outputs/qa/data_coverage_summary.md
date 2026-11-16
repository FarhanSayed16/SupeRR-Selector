# PressurePulse — Data Pack Intake & Schema Audit Summary

## 1. Inventory & Row Counts
| File | Rows | Columns | Purpose |
|---|---|---|---|
| `competitions.csv` | 141 | 4 | Competition IDs, names, seasons, formats |
| `teams.csv` | 353 | 3 | Team IDs and mappings across competitions |
| `matches.csv` | 883 | 22 | Match metadata, dates, venues, toss, stages, knockouts |
| `playing_eleven.csv` | 28,381 | 9 | Match playing XIs, batting order, captain/WK/impact roles |
| `competition_team_player_mapping.csv` | 6,413 | 6 | Master player ID to name & competition/team mapping |
| `ball_by_ball.csv` | 200,999 | 33 | Delivery-level event log (200,999 balls) |

## 2. Seasons, Formats & Date Coverage
- **Seasons Covered:** ['2022', '2022/23', '2023', '2023/24', '2024', '2024/25', '2025', '2026'] (2022 through 2026)
- **Formats (`match_format`):** {'T20I': 134, 'T20': 7}
- **Date Range:** 2022-01-22 to 2026-11-01
- **IPL Competitions Identified (5):**
  - [1358] IPL 2022 (Season 2022)
  - [1715] IPL 2023 (Season 2023)
  - [2193] IPL 2024 (Season 2024)
  - [2725] IPL 2025 (Season 2025)
  - [3298] IPL 2026 (Season 2026)

## 3. Match Stages & Knockout Distribution
- **Knockout Flags (`knock_out`):** {0: 852, 1: 31} (31 knockout matches flagged)
- **Stage Distribution (`stage`):**
  - League: 620
  - Others: 226
  - Final: 12
  - Qualifier: 10
  - Super 4: 6
  - Eliminator: 5
  - Semi Final: 4

## 4. Entity Dimensions
- **Unique Players in Mapping:** 1,217
- **Unique Strikers in Ball-by-Ball:** 888
- **Unique Bowlers in Ball-by-Ball:** 647
- **Unique Teams:** 38

## 5. Ball-by-Ball Key Fields & Quality Notes
- **Delivery State:** `match_id`, `innings`, `overid`, `over_ball_num`, `innings_ball_num`
- **Participants:** `striker_id`, `striker_name`, `non_striker_id`, `non_striker_name`, `bowler_id`, `bowler_name`
- **Outcomes:** `runs`, `is_four`, `is_six`, `is_wicket`, `dismissal_type`, `dismissed_player_id`, `extras_type`, `extras1_runs`, `extras_2_runs`
- **Contextual Proxies:** `batting_type`, `bowling_type`, `pace_or_spin`, `stroke`, `delivery_style`, `over_or_around`, `on_or_off`
- **Sparse Fields:** `bowl_speed` is unrecorded / 0.0 on 38.7% of balls (77,861 balls). Use as secondary proxy only, not required gate.

## 6. Critical Analytical Gaps Identified (To be engineered in Phases 07-09)
1. **No Innings Cumulative State:** Target, runs needed, balls remaining, current run rate, and required run rate (RRR) must be reconstructed ball-by-ball.
2. **No Pressure Label:** Pressure index must be formulated using RRR, wickets in hand, overs remaining, and match stage.
3. **No Explicit Player Roles:** Players are not tagged as 'Batter', 'Bowler', or 'All-Rounder'; this must be derived from career balls faced vs. balls bowled.
4. **Super Overs:** Innings 3 & 4 exist (super overs) and require consistent inclusion/exclusion policies.