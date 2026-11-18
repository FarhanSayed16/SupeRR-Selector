export type PageId =
  | 'command_centre'
  | 'batters'
  | 'bowlers'
  | 'pressure_lab'
  | 'player_profile'
  | 'auction_room'
  | 'methodology'
  | 'about';

export interface MetaPackage {
  product_name: string;
  subtitle: string;
  version: string;
  board?: string;
  build_timestamp: string;
  freeze_sha256: string;
  seasons_covered: string[];
  total_deliveries: number;
  pressure_deliveries: number;
  pressure_percentage: number;
  ipl_weight: number;
  t20i_weight?: number;
  min_ipl_pressure_balls_batter?: number;
  min_ipl_pressure_balls_bowler?: number;
  sensitivity?: {
    batter_top10_stability_pct?: number;
    bowler_top10_stability_pct?: number;
    ipl_overlap_batters?: number;
    ipl_overlap_bowlers?: number;
    computed?: boolean;
    [key: string]: unknown;
  };
  disclaimer: string;
}

export type BoardMode = 'auction' | 'global';

export interface ExcludedPlayer {
  player_id: number;
  player_name: string;
  category: string;
  exclusion_reason: string;
  rank?: number;
  pressure_score?: number;
  ipl_pressure_balls?: number;
}

export interface BatterRecord {
  rank: number;
  player_id: number;
  player_name: string;
  primary_role: string;
  pressure_score: number;
  pressure_runs: number;
  pressure_balls: number;
  pressure_matches: number;
  pressure_sr: number;
  pressure_dot_pct: number;
  pressure_boundary_pct: number;
  pressure_dismissals: number;
  pressure_avg: number;
  baseline_runs: number;
  baseline_balls: number;
  baseline_sr: number;
  baseline_dot_pct: number;
  baseline_boundary_pct: number;
  baseline_avg: number;
  sr_uplift: number;
  dot_reduction: number;
  boundary_uplift: number;
  avg_uplift: number;
  death_pressure_sr: number;
  death_pressure_balls?: number;
  chase_pressure_sr: number;
  sample_confidence: 'High' | 'Medium' | 'Low';
  ipl_pressure_balls?: number;
  ipl_pressure_share?: number;
  weighted_pressure_sr?: number;
  pp_pressure_balls?: number;
  pp_pressure_sr?: number;
  pp_pressure_dot_pct?: number;
  mid_pressure_balls?: number;
  mid_pressure_sr?: number;
  mid_pressure_dot_pct?: number;
  death_pressure_dot_pct?: number;
  collapse_pressure_balls?: number;
  collapse_pressure_sr?: number;
  vs_pace_pressure_balls?: number;
  vs_pace_pressure_sr?: number;
  vs_spin_pressure_balls?: number;
  vs_spin_pressure_sr?: number;
  reliability?: number;
  adjusted_display_score?: number;
  board?: string;
  squad_role?: string;
  rr_tactical_fit?: string;
  synergy_score?: number;
  archetype?: string;
  rr_slot?: string;
  auction_tier?: string;
  target_price_inr?: string;
  max_bid_ceiling_inr?: string;
  fallback_targets?: string[];
  strengths?: string[];
  vulnerabilities?: string[];
  venue_fit?: string;
  scouting_summary?: string;
}

export interface BowlerRecord {
  rank: number;
  player_id: number;
  player_name: string;
  primary_role: string;
  pressure_score: number;
  pressure_balls: number;
  pressure_overs: number;
  pressure_runs: number;
  pressure_wickets: number;
  pressure_matches: number;
  pressure_dots: number;
  pressure_economy: number;
  pressure_dot_pct: number;
  pressure_bowling_avg: number;
  pressure_balls_per_wicket: number;
  baseline_balls: number;
  baseline_runs: number;
  baseline_wickets: number;
  baseline_economy: number;
  baseline_dot_pct: number;
  baseline_bowling_avg: number;
  economy_uplift: number;
  dot_uplift: number;
  wicket_rate_uplift: number;
  death_pressure_economy: number;
  death_pressure_wickets: number;
  death_pressure_balls?: number;
  chase_pressure_economy: number;
  chase_pressure_wickets: number;
  sample_confidence: 'High' | 'Medium' | 'Low';
  ipl_pressure_balls?: number;
  ipl_pressure_share?: number;
  weighted_pressure_economy?: number;
  death_pressure_economy_capped?: number;
  pp_pressure_balls?: number;
  pp_pressure_economy?: number;
  pp_pressure_dot_pct?: number;
  pp_pressure_wickets?: number;
  mid_pressure_balls?: number;
  mid_pressure_economy?: number;
  mid_pressure_dot_pct?: number;
  mid_pressure_wickets?: number;
  death_pressure_dot_pct?: number;
  reliability?: number;
  adjusted_display_score?: number;
  board?: string;
  squad_role?: string;
  rr_tactical_fit?: string;
  synergy_score?: number;
  archetype?: string;
  rr_slot?: string;
  auction_tier?: string;
  target_price_inr?: string;
  max_bid_ceiling_inr?: string;
  fallback_targets?: string[];
  strengths?: string[];
  vulnerabilities?: string[];
  venue_fit?: string;
  scouting_summary?: string;
}

export interface PlayerIndexItem {
  player_id: number;
  player_name: string;
  primary_role: string;
  is_batter: boolean;
  is_bowler: boolean;
  rank?: number;
  pressure_score?: number;
  bowler_rank?: number;
  bowler_pressure_score?: number;
  board?: string;
}

export interface ScoutBoardEntry {
  scout_rank: number;
  player_name: string;
  official_rank: number | null;
  official_pressure_score: number | null;
  board: string | null;
  note?: string | null;
}

export interface ScoutBoard {
  label: string;
  policy: string;
  batters: ScoutBoardEntry[];
  bowlers: ScoutBoardEntry[];
}

export type PlayerDetailMap = Record<
  string,
  { batting?: BatterRecord; bowling?: BowlerRecord }
>;

export interface PressureSummary {
  pressure_version: string;
  definition_sentence: string;
  total_deliveries: number;
  pressure_deliveries: number;
  baseline_deliveries: number;
  pressure_percentage: number;
  ipl_pressure_percentage: number;
  t20i_pressure_percentage: number;
  phase_distribution_count: Record<string, number>;
  phase_distribution_percentage: Record<string, number>;
  signal_activation_counts: Record<string, number>;
  pressure_band_counts?: Record<string, number>;
  pressure_band_percentage?: Record<string, number>;
  pressure_band_thresholds?: {
    low_max?: number;
    medium_max?: number;
    note?: string;
  };
}

export interface MethodologyPackage {
  pressure_version: string;
  official_board?: string;
  definition_sentence: string;
  chase_high_rrr: number;
  chase_critical_rrr: number;
  death_overs: string;
  collapse_wickets: number;
  min_batter_pressure_balls: number;
  min_bowler_pressure_balls: number;
  min_baseline_balls_batter?: number;
  min_baseline_balls_bowler?: number;
  min_ipl_pressure_balls_batter?: number;
  min_ipl_pressure_balls_bowler?: number;
  ipl_weight?: number;
  t20i_weight?: number;
  include_super_overs?: boolean;
  board_policy?: string;
  prime_note?: string;
  scoring_weights_batter: Record<string, any>;
  scoring_weights_bowler: Record<string, any>;
}
