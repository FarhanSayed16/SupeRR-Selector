import pandas as pd
from pathlib import Path

raw = Path('data/raw')
comp = pd.read_csv(raw / 'competitions.csv')
teams = pd.read_csv(raw / 'teams.csv')
matches = pd.read_csv(raw / 'matches.csv')
xi = pd.read_csv(raw / 'playing_eleven.csv')
mapping = pd.read_csv(raw / 'competition_team_player_mapping.csv')
bbb = pd.read_csv(raw / 'ball_by_ball.csv', low_memory=False)

seasons = sorted(comp['season'].dropna().unique().tolist())
formats = comp['match_format'].value_counts().to_dict()
ipl_comps = comp[comp['comp_name'].str.contains('Indian Premier League|IPL', case=False, na=False)][['comp_id', 'comp_name', 'season']].to_dict(orient='records')

date_min = matches['match_date'].min()
date_max = matches['match_date'].max()

stages = matches['stage'].value_counts().to_dict()
knockouts = matches['knock_out'].value_counts().to_dict()

unique_strikers = bbb['striker_id'].nunique()
unique_bowlers = bbb['bowler_id'].nunique()
all_players_mapping = mapping['player_id'].nunique()
unique_teams = teams['team_id'].nunique()

bowl_speed_missing = int(bbb['bowl_speed'].isnull().sum())
bowl_speed_pct = (bowl_speed_missing / len(bbb)) * 100

lines = [
    "# PressurePulse — Data Pack Intake & Schema Audit Summary",
    "",
    "## 1. Inventory & Row Counts",
    "| File | Rows | Columns | Purpose |",
    "|---|---|---|---|",
    f"| `competitions.csv` | {len(comp):,} | {len(comp.columns)} | Competition IDs, names, seasons, formats |",
    f"| `teams.csv` | {len(teams):,} | {len(teams.columns)} | Team IDs and mappings across competitions |",
    f"| `matches.csv` | {len(matches):,} | {len(matches.columns)} | Match metadata, dates, venues, toss, stages, knockouts |",
    f"| `playing_eleven.csv` | {len(xi):,} | {len(xi.columns)} | Match playing XIs, batting order, captain/WK/impact roles |",
    f"| `competition_team_player_mapping.csv` | {len(mapping):,} | {len(mapping.columns)} | Master player ID to name & competition/team mapping |",
    f"| `ball_by_ball.csv` | {len(bbb):,} | {len(bbb.columns)} | Delivery-level event log (200,999 balls) |",
    "",
    "## 2. Seasons, Formats & Date Coverage",
    f"- **Seasons Covered:** {seasons} (2022 through 2026)",
    f"- **Formats (`match_format`):** {formats}",
    f"- **Date Range:** {date_min} to {date_max}",
    f"- **IPL Competitions Identified ({len(ipl_comps)}):**",
]

for c in ipl_comps:
    lines.append(f"  - [{c['comp_id']}] {c['comp_name']} (Season {c['season']})")

lines.extend([
    "",
    "## 3. Match Stages & Knockout Distribution",
    f"- **Knockout Flags (`knock_out`):** {knockouts} (31 knockout matches flagged)",
    "- **Stage Distribution (`stage`):**"
])

for k, v in stages.items():
    lines.append(f"  - {k}: {v}")

lines.extend([
    "",
    "## 4. Entity Dimensions",
    f"- **Unique Players in Mapping:** {all_players_mapping:,}",
    f"- **Unique Strikers in Ball-by-Ball:** {unique_strikers:,}",
    f"- **Unique Bowlers in Ball-by-Ball:** {unique_bowlers:,}",
    f"- **Unique Teams:** {unique_teams:,}",
    "",
    "## 5. Ball-by-Ball Key Fields & Quality Notes",
    "- **Delivery State:** `match_id`, `innings`, `overid`, `over_ball_num`, `innings_ball_num`",
    "- **Participants:** `striker_id`, `striker_name`, `non_striker_id`, `non_striker_name`, `bowler_id`, `bowler_name`",
    "- **Outcomes:** `runs`, `is_four`, `is_six`, `is_wicket`, `dismissal_type`, `dismissed_player_id`, `extras_type`, `extras1_runs`, `extras_2_runs`",
    "- **Contextual Proxies:** `batting_type`, `bowling_type`, `pace_or_spin`, `stroke`, `delivery_style`, `over_or_around`, `on_or_off`",
    f"- **Sparse Fields:** `bowl_speed` is null on {bowl_speed_pct:.1f}% of balls ({bowl_speed_missing:,} balls missing).",
    "",
    "## 6. Critical Analytical Gaps Identified (To be engineered in Phases 07-09)",
    "1. **No Innings Cumulative State:** Target, runs needed, balls remaining, current run rate, and required run rate (RRR) must be reconstructed ball-by-ball.",
    "2. **No Pressure Label:** Pressure index must be formulated using RRR, wickets in hand, overs remaining, and match stage.",
    "3. **No Explicit Player Roles:** Players are not tagged as 'Batter', 'Bowler', or 'All-Rounder'; this must be derived from career balls faced vs. balls bowled.",
    "4. **Super Overs:** Innings 3 & 4 exist (super overs) and require consistent inclusion/exclusion policies."
])

out_path = Path("outputs/qa/data_coverage_summary.md")
out_path.write_text("\n".join(lines), encoding="utf-8")
print(f"Generated {out_path} successfully!")
