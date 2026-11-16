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
  build_timestamp: string;
  freeze_sha256: string;
  seasons_covered: string[];
  total_deliveries: number;
  pressure_deliveries: number;
  pressure_percentage: number;
  ipl_weight: number;
  disclaimer: string;
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
  chase_pressure_sr: number;
  sample_confidence: 'High' | 'Medium' | 'Low';
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
  chase_pressure_economy: number;
  chase_pressure_wickets: number;
  sample_confidence: 'High' | 'Medium' | 'Low';
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
}

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
}

export interface MethodologyPackage {
  pressure_version: string;
  definition_sentence: string;
  chase_high_rrr: number;
  chase_critical_rrr: number;
  death_overs: string;
  collapse_wickets: number;
  min_batter_pressure_balls: number;
  min_bowler_pressure_balls: number;
  scoring_weights_batter: Record<string, any>;
  scoring_weights_bowler: Record<string, any>;
}
