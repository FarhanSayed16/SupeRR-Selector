import React, { useState } from 'react';
import { PageId, BatterRecord, BowlerRecord, MetaPackage, ScoutBoard } from '../types';
import { Medal } from '../components/Medal';
import { PlayerAvatar } from '../components/PlayerAvatar';
import { getBrandLogoSrc } from '../lib/images';
import { 
  Target, 
  Shield, 
  ArrowRight, 
  CheckCircle2, 
  TrendingUp,
  FileText,
  Activity,
  Layers,
  BarChart2,
  Copy,
  Check
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  CartesianGrid 
} from 'recharts';

interface CommandCentreProps {
  meta: MetaPackage | null;
  batters: BatterRecord[];
  bowlers: BowlerRecord[];
  scoutBoard?: ScoutBoard | null;
  onNavigate: (page: PageId, playerId?: number) => void;
}

function boardLabel(board: string | null | undefined): string {
  if (board === 'auction_official') return 'Official';
  if (board === 'global_only') return 'Global only';
  if (board === 'unmatched') return 'Unmatched';
  return board || '—';
}

export const CommandCentre: React.FC<CommandCentreProps> = ({
  meta,
  batters,
  bowlers,
  scoutBoard,
  onNavigate
}) => {
  const [chartMode, setChartMode] = useState<'batters' | 'bowlers'>('batters');
  const [copiedSection, setCopiedSection] = useState<string | null>(null);

  // Prepare chart data
  const batterChartData = batters.slice(0, 10).map((b) => ({
    name: b.player_name.split(' ').pop() || b.player_name,
    fullName: b.player_name,
    pressureSR: Number(b.pressure_sr.toFixed(1)),
    baselineSR: Number(b.baseline_sr.toFixed(1)),
    uplift: Number(b.sr_uplift.toFixed(1)),
  }));

  const bowlerChartData = bowlers.slice(0, 10).map((bw) => ({
    name: bw.player_name.split(' ').pop() || bw.player_name,
    fullName: bw.player_name,
    pressureEcon: Number(bw.pressure_economy.toFixed(2)),
    deathEcon: Number(bw.death_pressure_economy.toFixed(2)),
    baselineEcon: Number(bw.baseline_economy.toFixed(2)),
  }));

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(label);
    setTimeout(() => setCopiedSection(null), 2000);
  };

  const unstopRemarksText = `PressurePulse delivers a complete talent scouting system for Rajasthan Royals (IPL 2027). Beyond raw rankings across 200,999 deliveries, we diagnose RR's tactical gaps (lower-order finishing & death run restriction at SMS Stadium Jaipur). We present actionable auction targets: the 'Vignesh Puthur' stealth domestic blueprint (Shashank Singh +69.2 SR uplift, Ashutosh Sharma, Rasikh Salam 10.6 BpW) and global anchors (Sunil Narine 6.06 death econ). Full dossiers attached.`;

  return (
    <div className="space-y-6 pb-12 font-sans">
      {/* Executive Workstation Context Bar */}
      <div className="glass-panel p-5 space-y-3 overflow-hidden relative">
        <div className="absolute -right-2 top-1/2 -translate-y-1/2 w-36 sm:w-44 h-36 sm:h-44 opacity-[0.08] pointer-events-none hidden sm:block">
          <img src={getBrandLogoSrc()} alt="" className="w-full h-full object-contain" />
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-3 relative z-10">
          <div>
            <div className="flex items-center space-x-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <img src={getBrandLogoSrc()} alt="RR" className="h-6 w-6 object-contain" />
              <span>Rajasthan Royals Analytics & Strategy</span>
              <span>•</span>
              <span className="text-rr-pink-deep">SupeRR Selector Season 2</span>
              <span>•</span>
              <span className="font-mono text-slate-400">Round 1</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-rr-navy tracking-tight mt-0.5">
              IPL 2027 Auction War Room Intelligence Console
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => onNavigate('auction_room')} className="btn-primary">
              <span>RR 2027 Playing XI</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button onClick={() => onNavigate('methodology')} className="btn-ghost">
              Methodology
            </button>
          </div>
        </div>

        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-4xl">
          Deterministic evaluation across{' '}
          <strong>{(meta?.total_deliveries ?? 200999).toLocaleString()} ball-by-ball deliveries</strong>{' '}
          from IPL and T20 Internationals (2022–2026). Auction Official board uses IPL sample floors
          and IPL/T20I-weighted legal-ball rates ({meta?.version ?? 'pressure_v1.1'}).
        </p>

        {/* 4 Metric Chips Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
          <div className="glass-kpi p-3">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Deliveries Audited</span>
            <span className="text-lg font-black text-slate-900 font-mono">
              {(meta?.total_deliveries ?? 200999).toLocaleString()}
            </span>
            <span className="text-[10px] text-slate-500 block">883 matches (5 seasons)</span>
          </div>
          <div className="glass-kpi p-3 border-rr-pink/30">
            <span className="text-[10px] uppercase font-bold text-rr-pink-deep block">Pressure Deliveries</span>
            <span className="text-lg font-black text-slate-900 font-mono">
              {(meta?.pressure_deliveries ?? 78868).toLocaleString()}
            </span>
            <span className="text-[10px] text-rr-pink font-medium block">
              {(meta?.pressure_percentage ?? 39.24).toFixed(2)}% total universe
            </span>
          </div>
          <div className="glass-kpi p-3">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">IPL Rate Weight</span>
            <span className="text-lg font-black text-slate-900 font-mono">
              {(meta?.ipl_weight ?? 1.3).toFixed(2)}x
            </span>
            <span className="text-[10px] text-slate-500 block">
              baked into rates · T20I {(meta?.t20i_weight ?? 1.0).toFixed(2)}x
            </span>
          </div>
          <div className="glass-kpi p-3">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Sensitivity (computed)</span>
            <span className="text-lg font-black text-slate-900 font-mono">
              {Number(meta?.sensitivity?.batter_top10_stability_pct ?? 0).toFixed(0)}/
              {Number(meta?.sensitivity?.bowler_top10_stability_pct ?? 0).toFixed(0)}%
            </span>
            <span className="text-[10px] text-slate-500 block">
              bat/bowl Top 10 retention · Auction Official
            </span>
          </div>
        </div>
      </div>

      {/* RR War Room Priority Targets — name-first, no hype pills */}
      <div className="glass-panel p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between border-b border-slate-200/80 pb-3 gap-2">
          <div>
            <p className="type-kicker mb-1.5 text-rr-pink-deep">Auction Official · Priority shortlist</p>
            <h2 className="type-dossier-title">
              Recruits for Sangakkara &amp; Lindsay
            </h2>
          </div>
          <p className="text-[12px] text-slate-500 font-semibold leading-snug sm:text-right tracking-tight">
            Lower-order finish · death overs · impact cover
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-0 divide-y sm:divide-y-0 lg:divide-x divide-slate-200/80">
          {[
            {
              id: 2756,
              name: 'Shashank Singh',
              role: 'No. 6 finisher',
              metric: '+69.2 SR uplift',
              detail: '171.8 pressure SR · INR 5.5–8.0 Cr',
            },
            {
              id: 781,
              name: 'Sunil Narine',
              role: 'Death overs · spin',
              metric: '6.06 death econ',
              detail: 'All-phase restrictor · INR 10.0–13.0 Cr',
            },
            {
              id: 7327,
              name: 'Rasikh Salam',
              role: 'Death overs · seam',
              metric: '10.6 balls/wkt',
              detail: 'Strike seamer · INR 1.5–3.0 Cr',
            },
            {
              id: 8101,
              name: 'Ashutosh Sharma',
              role: 'Impact substitute',
              metric: '+79.1 SR uplift',
              detail: 'Chase finisher · INR 2.5–4.5 Cr',
            },
          ].map((card) => (
            <button
              type="button"
              key={card.id}
              onClick={() => onNavigate('player_profile', card.id)}
              className="text-left p-3.5 sm:px-4 hover:bg-rr-pink-soft/50 transition-colors cursor-pointer group"
            >
              <div className="flex items-start gap-3">
                <PlayerAvatar playerId={card.id} name={card.name} size="md" ring={false} />
                <div className="min-w-0 flex-1">
                  <h4 className="font-extrabold text-sm tracking-tight text-slate-900 group-hover:text-rr-pink-deep transition-colors truncate">
                    {card.name}
                  </h4>
                  <p className="text-[11px] text-slate-500 mt-0.5 border-l-2 border-rr-pink/40 pl-2">
                    {card.role}
                  </p>
                  <p className="text-xs font-mono font-bold text-rr-pink-deep mt-2">{card.metric}</p>
                  <p className="text-[11px] text-slate-600 mt-0.5 leading-snug">{card.detail}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Interactive Visual Analytics Section with Recharts */}
      <div className="glass-panel p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <BarChart2 className="w-4 h-4 text-rr-pink" />
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
              {chartMode === 'batters' 
                ? 'Batting Strike Rate Surge: High Pressure vs Baseline Comparison' 
                : 'Bowling Restrictiveness: Pressure Economy vs Death Economy Benchmark'}
            </h2>
          </div>

          <div className="flex items-center bg-white/40 p-0.5 rounded-full border border-white/70 text-xs font-semibold">
            <button
              onClick={() => setChartMode('batters')}
              className={`px-3 py-1 rounded-full transition-all cursor-pointer ${
                chartMode === 'batters'
                  ? 'bg-white text-rr-pink font-bold shadow-sm'
                  : 'text-ink-500 hover:text-rr-navy'
              }`}
            >
              Batters (SR Uplift)
            </button>
            <button
              onClick={() => setChartMode('bowlers')}
              className={`px-3 py-1 rounded-full transition-all cursor-pointer ${
                chartMode === 'bowlers'
                  ? 'bg-white text-rr-pink font-bold shadow-sm'
                  : 'text-ink-500 hover:text-rr-navy'
              }`}
            >
              Bowlers (Economy)
            </button>
          </div>
        </div>

        {/* Recharts Container */}
        <div className="glass-subcard h-64 sm:h-72 w-full pt-2 px-2">
          {chartMode === 'batters' ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={batterChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#475569' }} interval={0} />
                <YAxis domain={[60, 220]} tick={{ fontSize: 11, fill: '#475569' }} />
                <Tooltip 
                  formatter={(value: any, name: any) => [
                    `${value} SR`, 
                    name === 'pressureSR' ? 'Pressure Strike Rate' : 'Baseline Strike Rate'
                  ]}
                  labelFormatter={(name) => {
                    const item = batterChartData.find(d => d.name === name);
                    return item ? `${item.fullName} (+${item.uplift} SR Uplift)` : name;
                  }}
                  contentStyle={{ backgroundColor: 'rgba(255,255,255,0.92)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.8)', fontSize: '12px', backdropFilter: 'blur(8px)' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="pressureSR" name="Pressure Strike Rate" fill="#EC008C" radius={[6, 6, 0, 0]} />
                <Bar dataKey="baselineSR" name="Baseline Strike Rate" fill="#0B1B3A" fillOpacity={0.35} radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={bowlerChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#475569' }} interval={0} />
                <YAxis domain={[4, 11]} tick={{ fontSize: 11, fill: '#475569' }} />
                <Tooltip 
                  formatter={(value: any, name: any) => [
                    `${value} RPO`, 
                    name === 'pressureEcon' ? 'Pressure Economy' : name === 'deathEcon' ? 'Death Economy (16-20)' : 'Baseline Economy'
                  ]}
                  labelFormatter={(name) => {
                    const item = bowlerChartData.find(d => d.name === name);
                    return item ? item.fullName : name;
                  }}
                  contentStyle={{ backgroundColor: 'rgba(255,255,255,0.92)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.8)', fontSize: '12px', backdropFilter: 'blur(8px)' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="deathEcon" name="Death Overs Economy (16-20)" fill="#EC008C" radius={[6, 6, 0, 0]} />
                <Bar dataKey="pressureEcon" name="Overall Pressure Economy" fill="#0B1B3A" radius={[6, 6, 0, 0]} />
                <Bar dataKey="baselineEcon" name="Baseline Economy" fill="#94A3B8" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
        <p className="text-[11px] text-slate-500 italic text-right">
          *Data represents strictly verified delivery states. Note how top domestic picks (Shashank Singh, Ashutosh Sharma, Sunil Narine) drastically outperform league baselines under pressure.
        </p>
      </div>

      {/* Dual Priority Boards (Top 10 Batters & Top 10 Bowlers) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Batters Board */}
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded bg-rr-pink-soft border border-rr-pink-border flex items-center justify-center">
                <Target className="w-4 h-4 text-rr-pink-deep" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-slate-900 uppercase tracking-tight">Top 10 Batters Under Pressure</h3>
                <p className="text-[11px] text-slate-500">Official Unstop Order (Batsman 1 → 10)</p>
              </div>
            </div>
            <button
              onClick={() => onNavigate('batters')}
              className="text-xs font-semibold text-rr-pink-deep hover:text-rr-navy flex items-center space-x-1 cursor-pointer"
            >
              <span>Full Board</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-1.5">
            {batters.slice(0, 10).map((b) => (
              <div
                key={b.player_id}
                onClick={() => onNavigate('player_profile', b.player_id)}
                className="flex items-center justify-between p-3 rounded-xl bg-white/65 hover:bg-rr-pink-soft/70 border border-slate-200/60 hover:border-rr-pink-border transition-all cursor-pointer group"
              >
                <div className="flex items-center space-x-3 min-w-0">
                  <Medal rank={b.rank} />
                  <PlayerAvatar playerId={b.player_id} name={b.player_name} size="sm" />
                  <div className="min-w-0">
                    <h4 className="font-bold text-sm text-slate-900 group-hover:text-rr-pink-deep transition-colors truncate">
                      {b.player_name}
                    </h4>
                    <p className="text-[11px] text-slate-600 truncate">
                      {b.archetype ? b.archetype.split('&')[0] : b.primary_role} · {b.pressure_balls} balls
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-black font-mono text-slate-900 block">{b.pressure_score.toFixed(1)}</span>
                  <span className="text-[10px] font-mono font-bold text-rr-pink-deep bg-rr-pink-soft px-1.5 py-0.2 rounded border border-rr-pink-border">
                    +{b.sr_uplift.toFixed(1)} SR
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bowlers Board */}
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded bg-rr-pink-soft border border-rr-pink-border flex items-center justify-center">
                <Shield className="w-4 h-4 text-rr-pink-deep" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-slate-900 uppercase tracking-tight">Top 10 Bowlers Under Pressure</h3>
                <p className="text-[11px] text-slate-500">Official Unstop Order (Bowler 1 → 10)</p>
              </div>
            </div>
            <button
              onClick={() => onNavigate('bowlers')}
              className="text-xs font-semibold text-rr-pink-deep hover:text-rr-navy flex items-center space-x-1 cursor-pointer"
            >
              <span>Full Board</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-1.5">
            {bowlers.slice(0, 10).map((bw) => (
              <div
                key={bw.player_id}
                onClick={() => onNavigate('player_profile', bw.player_id)}
                className="flex items-center justify-between p-3 rounded-xl bg-white/65 hover:bg-rr-pink-soft/70 border border-slate-200/60 hover:border-rr-pink-border transition-all cursor-pointer group"
              >
                <div className="flex items-center space-x-3 min-w-0">
                  <Medal rank={bw.rank} />
                  <PlayerAvatar playerId={bw.player_id} name={bw.player_name} size="sm" />
                  <div className="min-w-0">
                    <h4 className="font-bold text-sm text-slate-900 group-hover:text-rr-pink-deep transition-colors truncate">
                      {bw.player_name}
                    </h4>
                    <p className="text-[11px] text-slate-600 truncate">
                      {bw.archetype ? bw.archetype.split('&')[0] : bw.primary_role} · {bw.pressure_wickets} wkts
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-black font-mono text-slate-900 block">{bw.pressure_score.toFixed(1)}</span>
                  <span className="text-[10px] font-mono font-bold text-rr-pink-deep bg-rr-pink-soft px-1.5 py-0.2 rounded border border-rr-pink-border">
                    {bw.death_pressure_economy.toFixed(2)} Dth Econ
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {scoutBoard && (
        <div className="glass-panel p-5 space-y-4">
          <div className="border-b border-slate-100 pb-3 space-y-1">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-tight">
              {scoutBoard.label} vs Auction Official
            </h3>
            <p className="text-[11px] text-slate-600 leading-relaxed max-w-3xl">{scoutBoard.policy}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {(
              [
                ['Batters', scoutBoard.batters],
                ['Bowlers', scoutBoard.bowlers],
              ] as const
            ).map(([title, rows]) => (
              <div key={title} className="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                <div className="font-bold text-slate-900 uppercase text-[11px] tracking-wide mb-2 pb-1.5 border-b border-slate-200">
                  Scout {title}
                </div>
                <div className="space-y-1.5">
                  {rows.map((r) => (
                    <div key={`${title}-${r.scout_rank}`} className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <span className="text-slate-500 font-mono mr-1.5">S{r.scout_rank}</span>
                        <span className="font-semibold text-slate-900">{r.player_name}</span>
                        {r.note && (
                          <p className="text-[10px] text-amber-800 mt-0.5 leading-snug">{r.note}</p>
                        )}
                      </div>
                      <div className="text-right shrink-0">
                        <span className="font-mono font-bold text-slate-800">
                          {r.official_rank != null ? `#${r.official_rank}` : '—'}
                        </span>
                        <div className="text-[10px] text-slate-500">{boardLabel(r.board)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <p className="text-[11px] text-slate-500">
            Open{' '}
            <button
              type="button"
              className="text-rr-pink-deep font-semibold hover:underline cursor-pointer"
              onClick={() => onNavigate('batters')}
            >
              full batter
            </button>{' '}
            /{' '}
            <button
              type="button"
              className="text-rr-pink-deep font-semibold hover:underline cursor-pointer"
              onClick={() => onNavigate('bowlers')}
            >
              bowler
            </button>{' '}
            boards for ranks 11+, or use navbar search for any player (e.g. Kohli, Dhoni).
          </p>
        </div>
      )}

      {/* Official Unstop Submission Desk */}
      <div className="glass-panel p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-rr-pink" />
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-tight">
              Official Unstop Submission Station (20 Selections Ready)
            </h3>
          </div>
          <span className="text-[11px] font-mono text-rr-pink-deep bg-rr-pink-soft px-2.5 py-0.5 rounded border border-rr-pink-border font-semibold">
            Zero Duplication • 100% Deterministic
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          {/* Batters List */}
          <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-2">
            <div className="flex justify-between items-center border-b border-slate-200 pb-1.5">
              <span className="font-bold text-slate-900 uppercase">Batsman 1 through 10</span>
              <button
                onClick={() => handleCopy(batters.map(b => `${b.rank}. ${b.player_name}`).join('\n'), 'batters')}
                className="text-[11px] text-slate-600 hover:text-rr-pink-deep flex items-center space-x-1 cursor-pointer"
              >
                {copiedSection === 'batters' ? <Check className="w-3.5 h-3.5 text-rr-pink" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedSection === 'batters' ? 'Copied' : 'Copy List'}</span>
              </button>
            </div>
            <div className="space-y-1">
              {batters.map(b => (
                <div key={b.rank} className="flex justify-between text-slate-700">
                  <span>Batsman {b.rank}: <strong>{b.player_name}</strong></span>
                  <span className="text-slate-500 font-semibold">{b.pressure_score.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Bowlers List */}
          <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-2">
            <div className="flex justify-between items-center border-b border-slate-200 pb-1.5">
              <span className="font-bold text-slate-900 uppercase">Bowler 1 through 10</span>
              <button
                onClick={() => handleCopy(bowlers.map(bw => `${bw.rank}. ${bw.player_name}`).join('\n'), 'bowlers')}
                className="text-[11px] text-slate-600 hover:text-rr-pink-deep flex items-center space-x-1 cursor-pointer"
              >
                {copiedSection === 'bowlers' ? <Check className="w-3.5 h-3.5 text-rr-pink" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedSection === 'bowlers' ? 'Copied' : 'Copy List'}</span>
              </button>
            </div>
            <div className="space-y-1">
              {bowlers.map(bw => (
                <div key={bw.rank} className="flex justify-between text-slate-700">
                  <span>Bowler {bw.rank}: <strong>{bw.player_name}</strong></span>
                  <span className="text-slate-500 font-semibold">{bw.pressure_score.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Pre-written Unstop Remarks Box */}
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-xs font-bold text-slate-800 uppercase tracking-tight">
              Recommended Unstop Submission Remarks (483 / 500 characters)
            </span>
            <button
              onClick={() => handleCopy(unstopRemarksText, 'remarks')}
              className="text-xs text-rr-pink-deep font-semibold hover:underline flex items-center space-x-1 cursor-pointer"
            >
              {copiedSection === 'remarks' ? <Check className="w-3.5 h-3.5 text-rr-pink" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedSection === 'remarks' ? 'Copied to Clipboard' : 'Copy Remarks'}</span>
            </button>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed font-sans bg-white p-2.5 rounded border border-slate-200/80">
            "{unstopRemarksText}"
          </p>
        </div>
      </div>
    </div>
  );
};
