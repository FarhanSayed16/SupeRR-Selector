# PressurePulse — Data Warehouse Quality & Integrity Report

## 1. Table Inventories & Row Counts
| Table | Type | Records | Columns | Parquet File |
|---|---|---|---|---|
| `dim_competition` | Dimension | 141 | 7 | `dim_competition.parquet` |
| `dim_team` | Dimension | 38 | 2 | `dim_team.parquet` |
| `dim_player` | Dimension | 1,217 | 2 | `dim_player.parquet` |
| `dim_match` | Dimension | 883 | 26 | `dim_match.parquet` |
| `fact_playing_eleven` | Fact | 28,381 | 9 | `fact_playing_eleven.parquet` |
| `fact_delivery` | Fact | 200,999 | 40 | `fact_delivery.parquet` |

## 2. Integrity Checks & Hygiene Results
- **Orphan Matches in Delivery Log:** 0 (Pass)
- **Orphan Players in Delivery Log:** 0 (Pass)
- **Duplicate Deliveries on (match, innings, overid, over_ball_num):** 0 (Clean)
- **Negative Runs Scored:** 0 (Clean)

## 3. Contextual Enrichment & Flags Added
- **IPL Matches Flagged:** 371 matches across 5 IPL seasons.
- **T20I Matches Flagged:** 482 matches across 134 T20I competitions.
- **Knockout Matches Flagged:** 31 playoff/knockout fixtures.

## 4. Total Delivery Scoring Verification
- **Total Deliveries Processed:** 200,999
- **Total Runs Recorded (Bat + Extras):** 284,257
- **Total Wickets Recorded:** 10,881

**Conclusion:** Clean warehouse built with 100% referential integrity and persisted as Parquet.