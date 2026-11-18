import React, { useMemo, useState } from 'react';
import { PageId, BatterRecord, BowlerRecord, PlayerDetailMap } from '../types';
import { ConfidenceBadge } from '../components/ConfidenceBadge';
import { PlayerAvatar } from '../components/PlayerAvatar';
import { ArrowLeft, Activity, Coins, BarChart3, Layers, Crosshair, Shield } from 'lucide-react';

type DossierTab = 'pressure' | 'baseline' | 'prime' | 'dossier';
type RoleView = 'bat' | 'bowl';

/** Highlight SR / % / INR / numeric tokens for scouting lists */
function emphasizeMetrics(text: string): React.ReactNode[] {
  const re =
    /(\d+(?:\.\d+)?(?:\s*(?:SR|Cr|cr|RPO|BpW|bpw|%))?|INR\s*[\d.,]+(?:\s*[–-]\s*INR\s*[\d.,]+)?(?:\s*Cr)?|\+\d+(?:\.\d+)?)/gi;
  const nodes: React.ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) nodes.push(text.slice(last, m.index));
    nodes.push(
      <span key={`m-${i++}`} className="metric-hot">
        {m[0]}
      </span>
    );
    last = m.index + m[0].length;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes.length ? nodes : [text];
}

function MetricTile({
  label,
  value,
  hint,
  hot,
}: {
  label: string;
  value: string;
  hint?: string;
  hot?: boolean;
}) {
  return (
    <div className="metric-tile">
      <span className="metric-tile-label">{label}</span>
      <p className={`metric-tile-value ${hot ? 'text-rr-pink-deep' : ''}`}>{value}</p>
      {hint ? <p className={`metric-tile-hint ${hot ? 'text-rr-pink font-semibold' : ''}`}>{hint}</p> : null}
    </div>
  );
}

interface PlayerProfileProps {
  playerId: number | null;
  batters: BatterRecord[];
  bowlers: BowlerRecord[];
  details?: PlayerDetailMap;
  onNavigate: (page: PageId, playerId?: number) => void;
}

export const PlayerProfile: React.FC<PlayerProfileProps> = ({
  playerId,
  batters,
  bowlers,
  details = {},
  onNavigate,
}) => {
  const detail = playerId != null ? details[String(playerId)] : undefined;
  const batter =
    batters.find((b) => b.player_id === playerId) ||
    (detail?.batting as BatterRecord | undefined);
  const bowler =
    bowlers.find((bw) => bw.player_id === playerId) ||
    (detail?.bowling as BowlerRecord | undefined);

  const [role, setRole] = useState<RoleView>('bat');
  const [tab, setTab] = useState<DossierTab>('pressure');

  // Reset view when navigating to another player
  React.useEffect(() => {
    const next: RoleView =
      bowler && (!batter || Number(bowler.pressure_score) >= Number(batter.pressure_score))
        ? 'bowl'
        : 'bat';
    setRole(next);
    setTab('pressure');
  }, [playerId, batter, bowler]);

  const dual = Boolean(batter && bowler);
  const isBowler = dual ? role === 'bowl' : Boolean(bowler) && !batter;
  const player = (isBowler ? bowler : batter) ?? bowler ?? null;

  const switchList = useMemo(() => {
    const rows: { id: number; label: string }[] = [];
    batters.slice(0, 30).forEach((b) =>
      rows.push({ id: b.player_id, label: `#${b.rank} ${b.player_name} · Bat` })
    );
    bowlers.slice(0, 30).forEach((bw) =>
      rows.push({ id: bw.player_id, label: `#${bw.rank} ${bw.player_name} · Bowl` })
    );
    return rows;
  }, [batters, bowlers]);

  if (!player) {
    return (
      <div className="glass-panel p-8 space-y-4">
        <p className="type-body">Player not found in ranked boards.</p>
        <button
          type="button"
          onClick={() => onNavigate('batters')}
          className="px-4 py-2 bg-rr-pink-deep rounded-full text-xs font-bold text-white uppercase cursor-pointer"
        >
          Return to Batters
        </button>
      </div>
    );
  }

  const ppBalls = Number(
    isBowler
      ? (player as BowlerRecord).pp_pressure_balls ?? 0
      : (player as BatterRecord).pp_pressure_balls ?? 0
  );
  const midBalls = Number(
    isBowler
      ? (player as BowlerRecord).mid_pressure_balls ?? 0
      : (player as BatterRecord).mid_pressure_balls ?? 0
  );
  const deathBalls = Number(
    isBowler
      ? (player as BowlerRecord).death_pressure_balls ?? 0
      : (player as BatterRecord).death_pressure_balls ?? 0
  );
  const phaseTotal = Math.max(1, ppBalls + midBalls + deathBalls);
  const relPct = Math.round(100 * Number((player as BatterRecord | BowlerRecord).reliability ?? 0));
  const adj = (player as BatterRecord | BowlerRecord).adjusted_display_score;

  const tabs: { id: DossierTab; label: string }[] = [
    { id: 'pressure', label: 'Pressure' },
    { id: 'baseline', label: 'Baseline' },
    { id: 'prime', label: 'P.R.I.M.E.' },
    { id: 'dossier', label: 'Dossier' },
  ];

  return (
    <div className="space-y-5 pb-12 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 glass-panel px-4 py-3">
        <button
          type="button"
          onClick={() => onNavigate(isBowler ? 'bowlers' : 'batters')}
          className="inline-flex items-center space-x-2 text-xs font-bold text-slate-600 hover:text-rr-pink-deep transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to {isBowler ? 'Bowlers' : 'Batters'} board</span>
        </button>
        <div className="flex items-center gap-2 text-xs">
          <span className="type-kicker hidden sm:inline">Jump to</span>
          <select
            value={player.player_id}
            onChange={(e) => onNavigate('player_profile', Number(e.target.value))}
            className="px-2.5 py-1.5 bg-white border border-slate-200 rounded-full text-xs font-semibold text-slate-800 focus:outline-none focus:border-rr-pink cursor-pointer max-w-[16rem]"
          >
            {switchList.map((r) => (
              <option key={`${r.id}-${r.label}`} value={r.id}>
                {r.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Hero */}
      <div className="glass-panel p-5 sm:p-7 relative overflow-hidden">
        <div className="absolute -right-8 -top-10 w-56 h-56 rounded-full bg-rr-pink-soft/70 pointer-events-none blur-2xl" />
        <div className="relative z-10 flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div className="flex items-start gap-4 sm:gap-5 min-w-0">
            <div className="relative shrink-0">
              <PlayerAvatar playerId={player.player_id} name={player.player_name} size="xl" />
              <span className="absolute -bottom-1 -right-1 min-w-7 h-7 px-1 rounded-full bg-rr-pink text-white text-xs font-black flex items-center justify-center border-2 border-white shadow">
                {player.rank}
              </span>
            </div>
            <div className="min-w-0 space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <span className="type-kicker text-rr-pink-deep">
                  {player.rank <= 10 ? 'Official freeze' : 'Board'} rank #{player.rank}
                </span>
                <ConfidenceBadge level={player.sample_confidence} />
              </div>
              <h1 className="type-hero-name truncate">{player.player_name}</h1>
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rr-pink-soft border border-rr-pink-border text-rr-pink-deep">
                  {player.archetype || player.primary_role}
                </span>
                <span className="text-slate-500 text-xs font-mono">
                  {player.pressure_balls} pressure balls audited
                </span>
              </div>
              {dual && (
                <div className="dossier-tabs mt-1" role="tablist" aria-label="Role view">
                  <button
                    type="button"
                    role="tab"
                    aria-selected={role === 'bat'}
                    className="dossier-tab inline-flex items-center gap-1"
                    onClick={() => setRole('bat')}
                  >
                    <Crosshair className="w-3 h-3" /> Batting
                  </button>
                  <button
                    type="button"
                    role="tab"
                    aria-selected={role === 'bowl'}
                    className="dossier-tab inline-flex items-center gap-1"
                    onClick={() => setRole('bowl')}
                  >
                    <Shield className="w-3 h-3" /> Bowling
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="shrink-0 rounded-2xl border border-slate-200/90 bg-white/70 px-5 py-4 min-w-[9.5rem] text-right">
            <span className="type-kicker block mb-1.5">PressureScore</span>
            <div className="type-score-display">{Number(player.pressure_score).toFixed(1)}</div>
            <p className="text-[10px] text-rr-pink font-semibold mt-1.5">
              {player.rank <= 10 ? 'Verified Unstop Top 10' : 'Full board dossier'}
            </p>
            {adj != null && (
              <p className="text-[10px] text-slate-500 font-mono mt-1">Adj. display {adj.toFixed(1)}</p>
            )}
          </div>
        </div>

        <div className="relative z-10 mt-6 pt-4 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="dossier-tabs" role="tablist" aria-label="Dossier sections">
            {tabs.map((t) => (
              <button
                key={t.id}
                type="button"
                role="tab"
                aria-selected={tab === t.id}
                className="dossier-tab"
                onClick={() => setTab(t.id)}
              >
                {t.label}
              </button>
            ))}
          </div>
          <p className="text-[11px] text-slate-500 max-w-sm sm:text-right">
            Use tabs to move between pressure evidence, baseline, role-phase context, and bid guidance.
          </p>
        </div>
      </div>

      {tab === 'pressure' && (
        <div className="glass-panel border-rr-pink/20 p-5 sm:p-6 space-y-4 page-enter">
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-rr-pink" />
              <div>
                <p className="type-kicker text-rr-pink-deep">Match on the line</p>
                <h2 className="type-dossier-title">Under high pressure</h2>
              </div>
            </div>
            <span className="text-xs font-mono text-rr-pink-deep font-bold bg-rr-pink-soft px-2.5 py-1 rounded-full border border-rr-pink-border">
              {player.pressure_balls} balls
            </span>
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {!isBowler ? (
              <>
                <MetricTile
                  label="Pressure SR"
                  value={Number((player as BatterRecord).pressure_sr).toFixed(1)}
                  hint={`+${Number((player as BatterRecord).sr_uplift).toFixed(1)} vs baseline`}
                  hot
                />
                <MetricTile
                  label="Boundary %"
                  value={`${Number((player as BatterRecord).pressure_boundary_pct).toFixed(1)}%`}
                  hint="Four / six conversion"
                />
                <MetricTile
                  label="Death SR (16–20)"
                  value={Number((player as BatterRecord).death_pressure_sr).toFixed(1)}
                  hint="Clutch finishing phase"
                  hot
                />
                <MetricTile
                  label="Chase SR"
                  value={Number((player as BatterRecord).chase_pressure_sr).toFixed(1)}
                  hint="Innings 2 tempo"
                />
              </>
            ) : (
              <>
                <MetricTile
                  label="Pressure econ"
                  value={Number((player as BowlerRecord).pressure_economy).toFixed(2)}
                  hint={`${Number((player as BowlerRecord).economy_uplift) >= 0 ? '+' : ''}${Number((player as BowlerRecord).economy_uplift).toFixed(2)} vs baseline`}
                  hot
                />
                <MetricTile
                  label="Pressure wickets"
                  value={String((player as BowlerRecord).pressure_wickets)}
                  hint={`${Number((player as BowlerRecord).pressure_balls_per_wicket).toFixed(1)} balls/wkt`}
                />
                <MetricTile
                  label="Death econ"
                  value={Number((player as BowlerRecord).death_pressure_economy).toFixed(2)}
                  hint="Overs 16–20"
                  hot
                />
                <MetricTile
                  label="Dot-ball %"
                  value={`${Number((player as BowlerRecord).pressure_dot_pct).toFixed(1)}%`}
                  hint="Dot choke rate"
                />
              </>
            )}
          </div>
        </div>
      )}

      {tab === 'baseline' && (
        <div className="glass-panel p-5 sm:p-6 space-y-4 page-enter">
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-slate-500" />
              <div>
                <p className="type-kicker">Ordinary situations</p>
                <h2 className="type-dossier-title">Baseline contrast</h2>
              </div>
            </div>
            <span className="text-xs font-mono text-slate-600 font-bold bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
              {player.baseline_balls} balls
            </span>
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {!isBowler ? (
              <>
                <MetricTile label="Baseline SR" value={Number((player as BatterRecord).baseline_sr).toFixed(1)} hint="Uncontested tempo" />
                <MetricTile label="Boundary %" value={`${Number((player as BatterRecord).baseline_boundary_pct).toFixed(1)}%`} />
                <MetricTile label="Dot %" value={`${Number((player as BatterRecord).baseline_dot_pct).toFixed(1)}%`} />
                <MetricTile label="Baseline runs" value={String((player as BatterRecord).baseline_runs)} hint="Sample depth" />
              </>
            ) : (
              <>
                <MetricTile label="Baseline econ" value={Number((player as BowlerRecord).baseline_economy).toFixed(2)} />
                <MetricTile label="Baseline wickets" value={String((player as BowlerRecord).baseline_wickets)} />
                <MetricTile label="Dot %" value={`${Number((player as BowlerRecord).baseline_dot_pct).toFixed(1)}%`} />
                <MetricTile label="Baseline balls" value={String((player as BowlerRecord).baseline_balls)} hint="Sample depth" />
              </>
            )}
          </div>
        </div>
      )}

      {tab === 'prime' && (
        <div className="glass-panel p-5 sm:p-6 space-y-5 page-enter">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-rr-pink" />
              <div>
                <p className="type-kicker">Phase ≠ pressure</p>
                <h2 className="type-dossier-title">P.R.I.M.E. role context</h2>
              </div>
            </div>
            <span className="font-mono text-[11px] font-bold text-slate-800 bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-full">
              Reliability {relPct}%
            </span>
          </div>

          <div className="space-y-2">
            <div className="flex h-2.5 rounded-full overflow-hidden bg-slate-100 border border-slate-200">
              <div className="bg-rr-navy/70" style={{ width: `${(100 * ppBalls) / phaseTotal}%` }} />
              <div className="bg-rr-pink/70" style={{ width: `${(100 * midBalls) / phaseTotal}%` }} />
              <div className="bg-rr-pink-deep" style={{ width: `${(100 * deathBalls) / phaseTotal}%` }} />
            </div>
            <div className="flex flex-wrap gap-3 text-[10px] text-slate-500 font-semibold">
              <span>PP {ppBalls}</span>
              <span>Mid {midBalls}</span>
              <span>Death {deathBalls}</span>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            {!isBowler ? (
              <>
                <MetricTile label="Powerplay SR" value={Number((player as BatterRecord).pp_pressure_sr ?? 0).toFixed(1)} hint={`${ppBalls} balls`} />
                <MetricTile label="Middle SR" value={Number((player as BatterRecord).mid_pressure_sr ?? 0).toFixed(1)} hint={`${midBalls} balls`} />
                <MetricTile label="Death SR" value={Number((player as BatterRecord).death_pressure_sr ?? 0).toFixed(1)} hint={`${deathBalls} balls`} hot />
              </>
            ) : (
              <>
                <MetricTile label="PP econ" value={Number((player as BowlerRecord).pp_pressure_economy ?? 0).toFixed(2)} hint={`${ppBalls} balls`} />
                <MetricTile label="Mid econ" value={Number((player as BowlerRecord).mid_pressure_economy ?? 0).toFixed(2)} hint={`${midBalls} balls`} />
                <MetricTile
                  label="Death econ"
                  value={Number(
                    (player as BowlerRecord).death_pressure_economy_capped ??
                      (player as BowlerRecord).death_pressure_economy
                  ).toFixed(2)}
                  hint={`${deathBalls} balls`}
                  hot
                />
              </>
            )}
          </div>

          {!isBowler && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <MetricTile
                label="Vs pace"
                value={`${Number((player as BatterRecord).vs_pace_pressure_sr ?? 0).toFixed(1)} SR`}
                hint={`${Number((player as BatterRecord).vs_pace_pressure_balls ?? 0)} balls`}
                hot
              />
              <MetricTile
                label="Vs spin"
                value={`${Number((player as BatterRecord).vs_spin_pressure_sr ?? 0).toFixed(1)} SR`}
                hint={`${Number((player as BatterRecord).vs_spin_pressure_balls ?? 0)} balls`}
                hot
              />
              <MetricTile
                label="Collapse"
                value={`${Number((player as BatterRecord).collapse_pressure_sr ?? 0).toFixed(1)} SR`}
                hint={`${Number((player as BatterRecord).collapse_pressure_balls ?? 0)} balls`}
              />
            </div>
          )}

          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-rr-pink rounded-full" style={{ width: `${relPct}%` }} />
          </div>
          <p className="text-[10px] text-slate-500">
            Reliability {relPct}% is display-only shrinkage. Official PressureScore and freeze SHA stay unchanged.
          </p>
        </div>
      )}

      {tab === 'dossier' && (
        <div className="glass-panel p-5 sm:p-7 space-y-6 page-enter">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between border-b border-slate-200/80 pb-4 gap-3">
            <div>
              <p className="type-kicker mb-1.5">Auction Official dossier</p>
              <h2 className="type-dossier-title">Scouting note &amp; bid guidance</h2>
            </div>
            <p className="text-[12px] text-slate-600 max-w-sm sm:text-right leading-snug">
              <span className="type-kicker block mb-1">Slot</span>
              <span className="font-mono text-[12px] font-semibold text-rr-navy">
                {player.rr_slot || 'Core starter'}
              </span>
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10">
            <div className="dossier-col-strength">
              <h4 className="type-section type-section-strength mb-3">Strengths under pressure</h4>
              <ol className="space-y-3 list-decimal list-outside ml-4">
                {(player.strengths || [
                  'Dominant strike execution under extreme leverage.',
                  'Substantial uplift over non-pressure baseline numbers.',
                ]).map((st, i) => (
                  <li key={i} className="type-body pl-1">
                    {emphasizeMetrics(st)}
                  </li>
                ))}
              </ol>
            </div>
            <div className="dossier-col-risk">
              <h4 className="type-section type-section-risk mb-3">Risks to manage</h4>
              <ol className="space-y-3 list-decimal list-outside ml-4">
                {(player.vulnerabilities || [
                  'Requires careful phase management to maximize leverage.',
                  'Boundary reliance can create brief dot-ball clusters.',
                ]).map((vb, i) => (
                  <li key={i} className="type-body pl-1">
                    {emphasizeMetrics(vb)}
                  </li>
                ))}
              </ol>
            </div>
          </div>

          <div className="border-t border-slate-200/80 pt-5 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 space-y-5">
              <div>
                <h4 className="type-section mb-2">Sawai Mansingh · venue fit</h4>
                <p className="type-body">
                  {player.venue_fit ||
                    'Excels on true surfaces and exploits Jaipur dimensions through precision placement.'}
                </p>
              </div>
              <div>
                <h4 className="type-section mb-2">Note for Sangakkara &amp; Lindsay</h4>
                <p className="type-note border-l-[3px] border-rr-pink pl-4">
                  {player.scouting_summary ||
                    player.rr_tactical_fit ||
                    'High-leverage specialist who provides immediate strategic uplift to Rajasthan Royals.'}
                </p>
              </div>
            </div>

            <div className="dossier-bid p-4 space-y-3.5">
              <div className="flex items-center gap-1.5">
                <Coins className="w-3.5 h-3.5 text-rr-pink" />
                <span className="type-kicker">Bid range</span>
              </div>
              <div>
                <span className="type-kicker block mb-0.5">Tier</span>
                <span className="text-[13px] font-semibold text-rr-navy">
                  {player.auction_tier || 'Prime target'}
                </span>
              </div>
              <div>
                <span className="type-kicker block mb-0.5">Target</span>
                <span className="text-lg font-mono font-bold text-rr-pink-deep leading-tight">
                  {player.target_price_inr || 'INR 4.0 Cr – 7.0 Cr'}
                </span>
              </div>
              <div>
                <span className="type-kicker block mb-0.5">Ceiling</span>
                <span className="text-[12px] font-mono font-medium text-slate-600">
                  {player.max_bid_ceiling_inr || 'INR 8.0 Cr'}
                </span>
              </div>
              {player.fallback_targets && player.fallback_targets.length > 0 && (
                <div className="border-t border-rr-navy/10 pt-2.5">
                  <span className="type-kicker block mb-0.5">Fallbacks</span>
                  <span className="text-[12px] text-slate-600 leading-snug">
                    {player.fallback_targets.join(', ')}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
