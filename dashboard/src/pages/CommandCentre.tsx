import React, { useState } from 'react';
import { PageId, BatterRecord, BowlerRecord, MetaPackage } from '../types';
import { Medal } from '../components/Medal';
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
  onNavigate: (page: PageId, playerId?: number) => void;
}

export const CommandCentre: React.FC<CommandCentreProps> = ({
  meta,
  batters,
  bowlers,
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
      <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center space-x-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <span>Rajasthan Royals Analytics & Strategy</span>
              <span>•</span>
              <span className="text-emerald-800">SupeRR Selector Season 2</span>
              <span>•</span>
              <span className="font-mono text-slate-400">Round 1</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight mt-0.5">
              IPL 2027 Auction War Room Intelligence Console
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate('auction_room')}
              className="px-3.5 py-1.5 rounded-md bg-emerald-800 hover:bg-emerald-900 text-white text-xs font-bold tracking-tight shadow-xs transition-colors cursor-pointer flex items-center space-x-1.5"
            >
              <span>RR 2027 Playing XI</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate('methodology')}
              className="px-3.5 py-1.5 rounded-md bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold tracking-tight transition-colors cursor-pointer"
            >
              Methodology
            </button>
          </div>
        </div>

        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-4xl">
          Deterministic evaluation across <strong>200,999 ball-by-ball deliveries</strong> from IPL and T20 Internationals (2022–2026). Engineered for Head Coach Kumar Sangakkara and Director of Strategy Giles Lindsay to solve Rajasthan Royals' lower-order death finishing deficit and death overs run leakage.
        </p>

        {/* 4 Metric Chips Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
          <div className="bg-slate-50/80 border border-slate-200/80 rounded-lg p-3">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Deliveries Audited</span>
            <span className="text-lg font-black text-slate-900 font-mono">200,999</span>
            <span className="text-[10px] text-slate-500 block">883 matches (5 seasons)</span>
          </div>
          <div className="bg-slate-50/80 border border-emerald-200 rounded-lg p-3">
            <span className="text-[10px] uppercase font-bold text-emerald-800 block">Pressure Deliveries</span>
            <span className="text-lg font-black text-slate-900 font-mono">78,906</span>
            <span className="text-[10px] text-emerald-700 font-medium block">39.26% total universe</span>
          </div>
          <div className="bg-slate-50/80 border border-slate-200/80 rounded-lg p-3">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Outside Death Overs</span>
            <span className="text-lg font-black text-slate-900 font-mono">43.7%</span>
            <span className="text-[10px] text-slate-500 block">PP: 10.2% | Mid: 33.5%</span>
          </div>
          <div className="bg-slate-50/80 border border-slate-200/80 rounded-lg p-3">
            <span className="text-[10px] uppercase font-bold text-slate-500 block">Auction Domain Weight</span>
            <span className="text-lg font-black text-slate-900 font-mono">1.30x</span>
            <span className="text-[10px] text-slate-500 block">IPL vs 1.00x T20I</span>
          </div>
        </div>
      </div>

      {/* RR War Room Priority Targets Directive */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-2.5 gap-2">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-emerald-600"></div>
            <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Strategic Scouting Directives: Key Auction Recruits for Kumar Sangakkara
            </h2>
          </div>
          <span className="text-[11px] font-mono text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 font-semibold">
            Targeting RR Structural Deficits
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div 
            onClick={() => onNavigate('player_profile', 2756)}
            className="p-3 bg-slate-50/80 hover:bg-emerald-50/50 border border-slate-200/70 hover:border-emerald-300 rounded-lg transition-all cursor-pointer group"
          >
            <div className="flex justify-between items-start">
              <span className="text-[9px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-1.5 py-0.5 rounded border border-emerald-200">
                #6 Finisher Solution
              </span>
              <span className="text-xs font-mono font-bold text-emerald-800">+69.2 SR</span>
            </div>
            <h4 className="font-bold text-xs text-slate-900 group-hover:text-emerald-900 transition-colors mt-1.5">
              Shashank Singh
            </h4>
            <p className="text-[10px] text-slate-500">171.8 Pressure SR • Est. INR 5.5–8.0 Cr</p>
          </div>

          <div 
            onClick={() => onNavigate('player_profile', 781)}
            className="p-3 bg-slate-50/80 hover:bg-emerald-50/50 border border-slate-200/70 hover:border-emerald-300 rounded-lg transition-all cursor-pointer group"
          >
            <div className="flex justify-between items-start">
              <span className="text-[9px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-1.5 py-0.5 rounded border border-emerald-200">
                Death Choke Anchor
              </span>
              <span className="text-xs font-mono font-bold text-emerald-800">6.06 Econ</span>
            </div>
            <h4 className="font-bold text-xs text-slate-900 group-hover:text-emerald-900 transition-colors mt-1.5">
              Sunil Narine
            </h4>
            <p className="text-[10px] text-slate-500">All-Phase Restrictor • Est. INR 10.0–13.0 Cr</p>
          </div>

          <div 
            onClick={() => onNavigate('player_profile', 2753)}
            className="p-3 bg-slate-50/80 hover:bg-emerald-50/50 border border-slate-200/70 hover:border-emerald-300 rounded-lg transition-all cursor-pointer group"
          >
            <div className="flex justify-between items-start">
              <span className="text-[9px] font-bold uppercase tracking-wider bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded border border-slate-200">
                Death Seam Wickets
              </span>
              <span className="text-xs font-mono font-bold text-emerald-800">10.6 BpW</span>
            </div>
            <h4 className="font-bold text-xs text-slate-900 group-hover:text-emerald-900 transition-colors mt-1.5">
              Rasikh Salam
            </h4>
            <p className="text-[10px] text-slate-500">Strike Bowler • Est. INR 1.5–3.0 Cr</p>
          </div>

          <div 
            onClick={() => onNavigate('player_profile', 2768)}
            className="p-3 bg-slate-50/80 hover:bg-emerald-50/50 border border-slate-200/70 hover:border-emerald-300 rounded-lg transition-all cursor-pointer group"
          >
            <div className="flex justify-between items-start">
              <span className="text-[9px] font-bold uppercase tracking-wider bg-amber-100 text-amber-900 px-1.5 py-0.5 rounded border border-amber-200">
                Impact Sub Clutch
              </span>
              <span className="text-xs font-mono font-bold text-emerald-800">+79.1 SR</span>
            </div>
            <h4 className="font-bold text-xs text-slate-900 group-hover:text-emerald-900 transition-colors mt-1.5">
              Ashutosh Sharma
            </h4>
            <p className="text-[10px] text-slate-500">Crisis 360 Finisher • Est. INR 2.5–4.5 Cr</p>
          </div>
        </div>
      </div>

      {/* Interactive Visual Analytics Section with Recharts */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <BarChart2 className="w-4 h-4 text-emerald-700" />
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
              {chartMode === 'batters' 
                ? 'Batting Strike Rate Surge: High Pressure vs Baseline Comparison' 
                : 'Bowling Restrictiveness: Pressure Economy vs Death Economy Benchmark'}
            </h2>
          </div>

          <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setChartMode('batters')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                chartMode === 'batters' 
                  ? 'bg-white text-emerald-900 font-bold shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Batters (SR Uplift)
            </button>
            <button
              onClick={() => setChartMode('bowlers')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                chartMode === 'bowlers' 
                  ? 'bg-white text-emerald-900 font-bold shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Bowlers (Economy)
            </button>
          </div>
        </div>

        {/* Recharts Container */}
        <div className="h-64 sm:h-72 w-full pt-2">
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
                  contentStyle={{ backgroundColor: '#FFFFFF', borderRadius: '8px', border: '1px solid #E2E8F0', fontSize: '12px' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="pressureSR" name="Pressure Strike Rate" fill="#064E3B" radius={[4, 4, 0, 0]} />
                <Bar dataKey="baselineSR" name="Baseline Strike Rate" fill="#94A3B8" radius={[4, 4, 0, 0]} />
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
                  contentStyle={{ backgroundColor: '#FFFFFF', borderRadius: '8px', border: '1px solid #E2E8F0', fontSize: '12px' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="deathEcon" name="Death Overs Economy (16-20)" fill="#064E3B" radius={[4, 4, 0, 0]} />
                <Bar dataKey="pressureEcon" name="Overall Pressure Economy" fill="#0D9488" radius={[4, 4, 0, 0]} />
                <Bar dataKey="baselineEcon" name="Baseline Economy" fill="#94A3B8" radius={[4, 4, 0, 0]} />
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
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                <Target className="w-4 h-4 text-emerald-800" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-slate-900 uppercase tracking-tight">Top 10 Batters Under Pressure</h3>
                <p className="text-[11px] text-slate-500">Official Unstop Order (Batsman 1 → 10)</p>
              </div>
            </div>
            <button
              onClick={() => onNavigate('batters')}
              className="text-xs font-semibold text-emerald-800 hover:text-emerald-950 flex items-center space-x-1 cursor-pointer"
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
                className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50/70 hover:bg-emerald-50/50 border border-slate-200/60 hover:border-emerald-300 transition-all cursor-pointer group"
              >
                <div className="flex items-center space-x-2.5">
                  <Medal rank={b.rank} />
                  <div>
                    <h4 className="font-bold text-xs text-slate-900 group-hover:text-emerald-900 transition-colors">
                      {b.player_name}
                    </h4>
                    <p className="text-[10px] text-slate-500">
                      {b.archetype ? b.archetype.split('&')[0] : b.primary_role} • {b.pressure_balls} balls
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-black font-mono text-slate-900 block">{b.pressure_score.toFixed(1)}</span>
                  <span className="text-[10px] font-mono font-bold text-emerald-800 bg-emerald-50 px-1.5 py-0.2 rounded border border-emerald-200">
                    +{b.sr_uplift.toFixed(1)} SR
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bowlers Board */}
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                <Shield className="w-4 h-4 text-emerald-800" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-slate-900 uppercase tracking-tight">Top 10 Bowlers Under Pressure</h3>
                <p className="text-[11px] text-slate-500">Official Unstop Order (Bowler 1 → 10)</p>
              </div>
            </div>
            <button
              onClick={() => onNavigate('bowlers')}
              className="text-xs font-semibold text-emerald-800 hover:text-emerald-950 flex items-center space-x-1 cursor-pointer"
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
                className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50/70 hover:bg-emerald-50/50 border border-slate-200/60 hover:border-emerald-300 transition-all cursor-pointer group"
              >
                <div className="flex items-center space-x-2.5">
                  <Medal rank={bw.rank} />
                  <div>
                    <h4 className="font-bold text-xs text-slate-900 group-hover:text-emerald-900 transition-colors">
                      {bw.player_name}
                    </h4>
                    <p className="text-[10px] text-slate-500">
                      {bw.archetype ? bw.archetype.split('&')[0] : bw.primary_role} • {bw.pressure_wickets} wkts
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-black font-mono text-slate-900 block">{bw.pressure_score.toFixed(1)}</span>
                  <span className="text-[10px] font-mono font-bold text-emerald-800 bg-emerald-50 px-1.5 py-0.2 rounded border border-emerald-200">
                    {bw.death_pressure_economy.toFixed(2)} Dth Econ
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Official Unstop Submission Desk */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-700" />
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-tight">
              Official Unstop Submission Station (20 Selections Ready)
            </h3>
          </div>
          <span className="text-[11px] font-mono text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200 font-semibold">
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
                className="text-[11px] text-slate-600 hover:text-emerald-800 flex items-center space-x-1 cursor-pointer"
              >
                {copiedSection === 'batters' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
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
                className="text-[11px] text-slate-600 hover:text-emerald-800 flex items-center space-x-1 cursor-pointer"
              >
                {copiedSection === 'bowlers' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
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
              className="text-xs text-emerald-800 font-semibold hover:underline flex items-center space-x-1 cursor-pointer"
            >
              {copiedSection === 'remarks' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
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
