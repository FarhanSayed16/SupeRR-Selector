import React from 'react';
import { PageId, BatterRecord, BowlerRecord } from '../types';
import { ConfidenceBadge } from '../components/ConfidenceBadge';
import { PlayerAvatar } from '../components/PlayerAvatar';
import { 
  ArrowLeft, 
  Target, 
  Shield, 
  Award, 
  Activity, 
  CheckCircle, 
  AlertTriangle, 
  Coins, 
  MapPin, 
  BarChart3, 
  Sparkles,
  ChevronDown
} from 'lucide-react';

interface PlayerProfileProps {
  playerId: number | null;
  batters: BatterRecord[];
  bowlers: BowlerRecord[];
  onNavigate: (page: PageId, playerId?: number) => void;
}

export const PlayerProfile: React.FC<PlayerProfileProps> = ({
  playerId,
  batters,
  bowlers,
  onNavigate
}) => {
  const batter = batters.find((b) => b.player_id === playerId);
  const bowler = bowlers.find((bw) => bw.player_id === playerId);
  const isBowler = bowler ? true : false;
  const player = (isBowler ? bowler : batter) || batters[0];

  if (!player) {
    return (
      <div className="text-slate-800 p-8 space-y-4">
        <p>Player not found.</p>
        <button
          onClick={() => onNavigate('batters')}
          className="px-4 py-2 bg-rr-pink-deep rounded text-xs font-bold text-white uppercase"
        >
          Return to Batters
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12 font-sans">
      {/* Top Action Bar with Quick Player Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200 ">
        <button
          onClick={() => onNavigate(isBowler ? 'bowlers' : 'batters')}
          className="inline-flex items-center space-x-2 text-xs font-bold text-slate-600 hover:text-rr-pink-deep transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to {isBowler ? 'Bowlers' : 'Batters'} Board</span>
        </button>

        {/* Quick Switch Dropdown */}
        <div className="flex items-center space-x-2 text-xs">
          <span className="text-[11px] text-slate-500 font-semibold uppercase">Quick Switch Dossier:</span>
          <select
            value={player.player_id}
            onChange={(e) => onNavigate('player_profile', Number(e.target.value))}
            className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-md text-xs font-bold text-slate-800 focus:outline-none focus:border-rr-pink cursor-pointer"
          >
            <optgroup label="Top 10 Batters">
              {batters.map((b) => (
                <option key={b.player_id} value={b.player_id}>
                  #{b.rank} {b.player_name} (Batter)
                </option>
              ))}
            </optgroup>
            <optgroup label="Top 10 Bowlers">
              {bowlers.map((bw) => (
                <option key={bw.player_id} value={bw.player_id}>
                  #{bw.rank} {bw.player_name} (Bowler)
                </option>
              ))}
            </optgroup>
          </select>
        </div>
      </div>

      {/* Hero Profile Banner */}
      <div className="glass-panel p-5 sm:p-6 relative overflow-hidden ">
        <div className="absolute right-0 top-0 w-80 h-80 bg-rr-pink-soft rounded-bl-full pointer-events-none opacity-50" />
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5 relative z-10">
          <div className="flex items-start space-x-4">
            <div className="relative">
              <PlayerAvatar playerId={player.player_id} name={player.player_name} size="xl" />
              <span className="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-rr-pink text-white text-xs font-black flex items-center justify-center border-2 border-white shadow">
                {player.rank}
              </span>
            </div>
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="text-[11px] uppercase font-bold text-rr-pink-deep tracking-wider">
                  Official Freeze Rank #{player.rank} • {isBowler ? 'Bowler' : 'Batter'}
                </span>
                <ConfidenceBadge level={player.sample_confidence} />
              </div>
              <h1 className="text-xl sm:text-3xl font-black text-slate-900 tracking-tight">
                {player.player_name}
              </h1>
              <div className="flex flex-wrap items-center gap-2 pt-0.5">
                <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rr-pink-soft border border-rr-pink-border text-rr-pink-deep">
                  {player.archetype || player.primary_role}
                </span>
                <span className="text-slate-500 text-xs font-mono">
                  • {player.pressure_balls} pressure deliveries audited
                </span>
              </div>
            </div>
          </div>

          {/* Hero Score Badge */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-right min-w-[130px]">
            <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">
              Composite PressureScore
            </span>
            <span className="text-2xl sm:text-3xl font-black text-slate-900 font-mono">
              {player.pressure_score.toFixed(1)}
            </span>
            <span className="text-[10px] text-rr-pink block font-semibold mt-0.5">
              Verified Unstop Top 10
            </span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Dual Panel: Pressure vs Baseline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* High Pressure Panel */}
        <div className="glass-panel border-rr-pink/25 p-5 space-y-3.5">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
            <div className="flex items-center space-x-2 text-rr-pink-deep">
              <Activity className="w-4 h-4 text-rr-pink" />
              <h3 className="font-bold text-xs uppercase tracking-wide text-slate-900">Under High Pressure (Match on the line)</h3>
            </div>
            <span className="text-xs font-mono text-rr-pink-deep font-bold bg-rr-pink-soft px-2 py-0.5 rounded border border-rr-pink-border">
              {player.pressure_balls} Deliveries
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {!isBowler ? (
              <>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Pressure Strike Rate</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BatterRecord).pressure_sr.toFixed(1)}</p>
                  <p className="text-[10px] text-rr-pink font-bold mt-0.5 font-mono">+{(player as BatterRecord).sr_uplift.toFixed(1)} vs Baseline</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Boundary Percentage</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BatterRecord).pressure_boundary_pct.toFixed(1)}%</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Four/Six conversion</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Death Overs SR (16–20)</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BatterRecord).death_pressure_sr.toFixed(1)}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Clutch finishing phase</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Chase SR (Innings 2)</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BatterRecord).chase_pressure_sr.toFixed(1)}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Target pursuit tempo</p>
                </div>
              </>
            ) : (
              <>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Pressure Economy</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BowlerRecord).pressure_economy.toFixed(2)}</p>
                  <p className="text-[10px] text-rr-pink font-bold mt-0.5 font-mono">
                    {(player as BowlerRecord).economy_uplift > 0 ? `+${(player as BowlerRecord).economy_uplift.toFixed(2)}` : (player as BowlerRecord).economy_uplift.toFixed(2)} vs Baseline
                  </p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Pressure Wickets</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BowlerRecord).pressure_wickets}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5 font-mono">{(player as BowlerRecord).pressure_balls_per_wicket.toFixed(1)} balls/wkt</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Death Economy (16–20)</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BowlerRecord).death_pressure_economy.toFixed(2)}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Death restrictiveness</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Dot-Ball Percentage</span>
                  <p className="text-lg font-black text-slate-900 mt-0.5 font-mono">{(player as BowlerRecord).pressure_dot_pct.toFixed(1)}%</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Dot choke rate</p>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Baseline Panel */}
        <div className="glass-panel p-5 space-y-3.5">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
            <div className="flex items-center space-x-2 text-slate-600">
              <BarChart3 className="w-4 h-4 text-slate-500" />
              <h3 className="font-bold text-xs uppercase tracking-wide text-slate-900">Baseline (Ordinary Situations)</h3>
            </div>
            <span className="text-xs font-mono text-slate-600 font-bold bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
              {player.baseline_balls} Deliveries
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {!isBowler ? (
              <>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Baseline Strike Rate</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BatterRecord).baseline_sr.toFixed(1)}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Uncontested overs tempo</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Baseline Boundary %</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BatterRecord).baseline_boundary_pct.toFixed(1)}%</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Standard four/six rate</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Baseline Dot %</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BatterRecord).baseline_dot_pct.toFixed(1)}%</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Non-pressure dot rate</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Total Baseline Runs</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BatterRecord).baseline_runs}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Career sample depth</p>
                </div>
              </>
            ) : (
              <>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Baseline Economy</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BowlerRecord).baseline_economy.toFixed(2)}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Standard phase economy</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Baseline Wickets</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BowlerRecord).baseline_wickets}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Standard dismissals</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Baseline Dot %</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BowlerRecord).baseline_dot_pct.toFixed(1)}%</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Baseline control</p>
                </div>
                <div className="bg-slate-50/80 p-3 rounded-lg border border-slate-200/70">
                  <span className="text-[10px] text-slate-500 uppercase font-semibold block">Total Baseline Balls</span>
                  <p className="text-lg font-black text-slate-700 mt-0.5 font-mono">{(player as BowlerRecord).baseline_balls}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">Career sample depth</p>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Rajasthan Royals War Room Tactical Fit & Scouting Dossier */}
      <div className="glass-panel p-5 sm:p-6 space-y-5 ">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
          <div className="flex items-center space-x-2 text-rr-pink-deep">
            <Award className="w-4 h-4 text-rr-pink" />
            <h3 className="font-bold text-sm uppercase tracking-wide text-slate-900">
              Official RR Scouting Dossier & Auction Strategy
            </h3>
          </div>
          <span className="text-xs font-mono font-bold text-rr-pink-deep bg-rr-pink-soft border border-rr-pink-border px-2.5 py-0.5 rounded-full w-fit">
            Target Slot: {player.rr_slot || 'Core Starter'}
          </span>
        </div>

        {/* Tactical Strengths & Vulnerabilities */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Strengths */}
          <div className="bg-rr-pink-soft/40 border border-rr-pink-border rounded-lg p-4 space-y-2">
            <div className="flex items-center space-x-2 text-rr-pink-deep">
              <CheckCircle className="w-4 h-4 text-rr-pink" />
              <h4 className="font-bold text-xs uppercase tracking-wider text-rr-pink-deep">
                Key Pressure Strengths & Superpowers
              </h4>
            </div>
            <ul className="space-y-1.5">
              {(player.strengths || [
                `Dominant strike execution under extreme leverage.`,
                `Substantial uplift over non-pressure baseline numbers.`
              ]).map((st, i) => (
                <li key={i} className="text-xs text-slate-700 flex items-start space-x-2">
                  <span className="text-rr-pink font-bold">•</span>
                  <span>{st}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Vulnerabilities */}
          <div className="bg-amber-50/40 border border-amber-200 rounded-lg p-4 space-y-2">
            <div className="flex items-center space-x-2 text-amber-800">
              <AlertTriangle className="w-4 h-4 text-amber-700" />
              <h4 className="font-bold text-xs uppercase tracking-wider text-amber-900">
                Scouting Vulnerabilities & Dismissal Risks
              </h4>
            </div>
            <ul className="space-y-1.5">
              {(player.vulnerabilities || [
                `Requires careful phase management to maximize leverage.`,
                `Boundary reliance can create brief dot-ball clusters.`
              ]).map((vb, i) => (
                <li key={i} className="text-xs text-slate-700 flex items-start space-x-2">
                  <span className="text-amber-700 font-bold">•</span>
                  <span>{vb}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Venue Fit & War Room Assessment */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 space-y-3">
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 space-y-1">
              <div className="flex items-center space-x-2 text-rr-pink-deep">
                <MapPin className="w-3.5 h-3.5 text-rr-pink" />
                <span className="text-xs uppercase font-bold text-slate-900">Sawai Mansingh Stadium & Venue Fit</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                {player.venue_fit || 'Excels on true surfaces and exploits Jaipur dimensions through precision placement.'}
              </p>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 space-y-1">
              <div className="flex items-center space-x-2 text-rr-pink-deep">
                <Sparkles className="w-3.5 h-3.5 text-rr-pink" />
                <span className="text-xs uppercase font-bold text-slate-900">War Room Assessment for Kumar Sangakkara & Giles Lindsay</span>
              </div>
              <p className="text-xs text-slate-700 italic leading-relaxed">
                "{player.scouting_summary || player.rr_tactical_fit || 'High-leverage specialist who provides immediate strategic uplift to Rajasthan Royals.'}"
              </p>
            </div>
          </div>

          {/* Auction Economics Card */}
          <div className="rounded-2xl p-4 flex flex-col justify-between space-y-3 text-white bg-gradient-to-br from-rr-purple via-rr-navy to-rr-navy border border-white/20 shadow-lg">
            <div>
              <div className="flex items-center space-x-1.5 text-pink-200 mb-2">
                <Coins className="w-3.5 h-3.5" />
                <span className="text-[10px] font-bold uppercase tracking-wider">Auction Valuation</span>
              </div>
              <div className="space-y-2">
                <div>
                  <span className="text-[10px] text-pink-200 uppercase block">Acquisition Tier</span>
                  <span className="text-xs font-bold text-white">{player.auction_tier || 'Prime Target'}</span>
                </div>
                <div>
                  <span className="text-[10px] text-pink-200 uppercase block">Target Price Bracket</span>
                  <span className="text-sm font-black text-amber-300 font-mono">{player.target_price_inr || 'INR 4.0 Cr – 7.0 Cr'}</span>
                </div>
                <div>
                  <span className="text-[10px] text-pink-200 uppercase block">Max Bidding Ceiling</span>
                  <span className="text-xs font-mono font-bold text-white">{player.max_bid_ceiling_inr || 'INR 8.0 Cr'}</span>
                </div>
              </div>
            </div>

            {player.fallback_targets && player.fallback_targets.length > 0 && (
              <div className="border-t border-rr-navy pt-2">
                <span className="text-[9px] text-pink-300 uppercase block font-semibold">Contingency Backups</span>
                <span className="text-[10px] text-pink-100 font-medium">
                  {player.fallback_targets.join(', ')}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
