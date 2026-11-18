import React, { useState } from 'react';
import { MetaPackage, PressureSummary } from '../types';
import { 
  Activity, 
  ShieldCheck, 
  Layers, 
  Sliders, 
  Flame, 
  CheckCircle2, 
  AlertCircle,
  Trophy
} from 'lucide-react';

interface PressureLabProps {
  summary: PressureSummary | null;
  meta?: MetaPackage | null;
}

export const PressureLab: React.FC<PressureLabProps> = ({ summary, meta }) => {
  // Interactive Simulation State
  const [innings, setInnings] = useState<1 | 2>(2);
  const [over, setOver] = useState<number>(17);
  const [target, setTarget] = useState<number>(192);
  const [currentScore, setCurrentScore] = useState<number>(154);
  const [wicketsLost, setWicketsLost] = useState<number>(5);
  const [isKnockout, setIsKnockout] = useState<boolean>(true);

  if (!summary) {
    return <div className="text-slate-700 p-8">Loading Pressure Lab diagnostics...</div>;
  }

  const sens = meta?.sensitivity;
  const batStab = Number(sens?.batter_top10_stability_pct ?? 0);
  const bowlStab = Number(sens?.bowler_top10_stability_pct ?? 0);
  const phasePct = summary.phase_distribution_percentage || {};
  const phaseCount = summary.phase_distribution_count || {};
  const ppPct = Number(phasePct.powerplay ?? 0);
  const midPct = Number(phasePct.middle ?? 0);
  const deathPct = Number(phasePct.death ?? 0);
  const outsideDeathPct = ppPct + midPct;
  const phaseCards = [
    {
      key: 'powerplay',
      label: 'Powerplay (Overs 1–6)',
      pct: ppPct,
      count: Number(phaseCount.powerplay ?? 0),
      blurb: 'Triggered by early collapse defense & aggressive target setups.',
    },
    {
      key: 'middle',
      label: 'Middle Overs (Overs 7–15)',
      pct: midPct,
      count: Number(phaseCount.middle ?? 0),
      blurb: 'Steep RRR and wicket-cluster pressure in the rebuild window.',
    },
    {
      key: 'death',
      label: 'Death Overs (Overs 16–20)',
      pct: deathPct,
      count: Number(phaseCount.death ?? 0),
      blurb: 'Extreme execution phase where matches are closed out or lost.',
    },
  ];

  // Simulation Calculations
  const ballsBowled = Math.min(120, Math.floor(over) * 6);
  const ballsRemaining = Math.max(1, 120 - ballsBowled);
  const runsNeeded = Math.max(0, target - currentScore);
  const rrr = Number(((runsNeeded / ballsRemaining) * 6).toFixed(1));
  const crr = Number(((currentScore / Math.max(1, ballsBowled)) * 6).toFixed(1));

  // Determine active signals
  const isDeath = over >= 16;
  const isPowerplay = over <= 6;
  const isCollapse = (isPowerplay && wicketsLost >= 3) || (10 - wicketsLost <= 3 && ballsRemaining >= 12);
  const isChaseTight = innings === 2 && (rrr >= 11.5 || (over >= 10 && rrr >= 9.5) || (ballsRemaining <= 30 && runsNeeded <= 55));
  const isDeathContest = isDeath && (innings === 1 || (innings === 2 && runsNeeded > 5));

  // Compute leverage score
  let calculatedLeverage = 1.0;
  if (isChaseTight) calculatedLeverage += 0.65;
  if (isDeathContest) calculatedLeverage += 0.45;
  if (isCollapse) calculatedLeverage += 0.40;
  if (isKnockout) calculatedLeverage += 0.30;
  calculatedLeverage = Math.min(2.5, calculatedLeverage);

  let statusColor = "text-slate-700 bg-slate-100 border-slate-300";
  let statusText = "STANDARD CONTEXT (1.00x)";
  if (calculatedLeverage >= 2.1) {
    statusColor = "text-rr-navy bg-rr-pink-soft border-rr-pink/50";
    statusText = "MAXIMUM CRUNCH LEVERAGE (2.20x+)";
  } else if (calculatedLeverage >= 1.6) {
    statusColor = "text-rr-pink-deep bg-rr-pink-soft border-rr-pink-border";
    statusText = "HIGH-STAKES CLUTCH (1.60x–2.10x)";
  } else if (calculatedLeverage >= 1.25) {
    statusColor = "text-amber-900 bg-amber-50 border-amber-300";
    statusText = "CONTESTED LEVERAGE (1.25x–1.60x)";
  }

  const signals = [
    {
      name: "Chase Tightness (Innings 2)",
      desc: "Triggered when Required Run Rate >= 9.5 in final 10 overs, or RRR >= 11.5 anytime, or <= 30 balls remaining needing <= 55 runs.",
      count: summary.signal_activation_counts?.chase_tightness ?? 0,
      badge: "Steep Chases",
      color: "border-rr-pink-border bg-rr-pink-soft text-rr-pink-deep"
    },
    {
      name: "Collapse & Survival (Innings 1 & 2)",
      desc: "Triggered during severe top-order collapse (>=3 wickets lost before Over 8) or tail exposure (<=3 wickets in hand with >=12 balls left).",
      count: summary.signal_activation_counts?.collapse_defense ?? 0,
      badge: "Crisis Defense",
      color: "border-amber-200 bg-amber-50 text-amber-900"
    },
    {
      name: "Death Overs Contest (Overs 16-20)",
      desc: "Target setting in Innings 1 or active contested chase in Innings 2 (where remaining runs required > 5).",
      count: summary.signal_activation_counts?.death_contest ?? 0,
      badge: "High Leverage",
      color: "border-slate-200 bg-slate-100 text-slate-800"
    },
    {
      name: "Knockout Playoff Leverage",
      desc: "Qualifiers, Eliminators, and Finals under active game state pressure, magnified by tournament context.",
      count: summary.signal_activation_counts?.knockout_leverage ?? 0,
      badge: "Trophy Stakes",
      color: "border-rr-pink-border bg-rr-pink-soft text-rr-pink-deep"
    },
    {
      name: "Super Overs",
      desc: "100% maximum pressure clutch tie-breakers (Innings 3 and 4).",
      count: summary.signal_activation_counts?.super_overs ?? 0,
      badge: "Ultra Clutch",
      color: "border-rose-200 bg-rose-50 text-rose-800"
    }
  ];

  return (
    <div className="space-y-6 pb-12 font-sans">
      {/* Manifesto Header */}
      <div className="glass-panel p-5 space-y-3">
        <div className="flex items-center space-x-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
          <Activity className="w-3.5 h-3.5 text-rr-pink" />
          <span>Empirical Validation Engine • {summary.pressure_version}</span>
        </div>
        <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
          How We Formulate, Quantify & Verify Match Pressure
        </h1>
        <div className="p-3.5 rounded-lg bg-slate-50 border-l-4 border-rr-pink text-slate-800 text-xs sm:text-sm leading-relaxed italic">
          "{summary.definition_sentence}"
        </div>
        <p className="text-xs text-slate-600 leading-relaxed max-w-4xl">
          Pressure in T20 cricket is multidimensional. It cannot be reduced to overs 16–20 alone. Our composite formulation isolates high-leverage deliveries across the entire match timeline where individual decision quality directly swings win probability.
        </p>
      </div>

      {/* Interactive Scenario Simulator */}
      <div className="glass-panel p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
          <div className="flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-rr-pink" />
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
              Live Game Situation Simulator (Interactive Engine)
            </h2>
          </div>
          <span className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded border ${statusColor}`}>
            {statusText}
          </span>
        </div>

        {/* Input Controls Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 pt-1">
          {/* Innings & Tournament */}
          <div className="space-y-3 bg-slate-50/70 p-3.5 rounded-lg border border-slate-200/60">
            <div>
              <label className="text-[10px] uppercase font-bold text-slate-600 block mb-1">Innings Phase</label>
              <div className="flex gap-2 text-xs">
                <button
                  onClick={() => setInnings(1)}
                  className={`flex-1 py-1 rounded font-semibold transition-all ${
                    innings === 1 ? 'bg-rr-pink-deep text-white ' : 'bg-white text-slate-700 border border-slate-200'
                  }`}
                >
                  1st (Target Setting)
                </button>
                <button
                  onClick={() => setInnings(2)}
                  className={`flex-1 py-1 rounded font-semibold transition-all ${
                    innings === 2 ? 'bg-rr-pink-deep text-white ' : 'bg-white text-slate-700 border border-slate-200'
                  }`}
                >
                  2nd (Run Chase)
                </button>
              </div>
            </div>

            <div>
              <label className="text-[10px] uppercase font-bold text-slate-600 block mb-1">Stakes / Tournament Context</label>
              <button
                onClick={() => setIsKnockout(!isKnockout)}
                className={`w-full py-1.5 px-3 rounded text-xs font-semibold flex items-center justify-between transition-all ${
                  isKnockout ? 'bg-rr-pink-soft text-rr-pink-deep border border-rr-pink-border' : 'bg-white text-slate-700 border border-slate-200'
                }`}
              >
                <span className="flex items-center space-x-1.5">
                  <Trophy className="w-3.5 h-3.5 text-rr-pink" />
                  <span>IPL Playoff / Knockout Final</span>
                </span>
                <span className="font-mono text-[10px] font-bold">{isKnockout ? '+0.30x LEV' : 'LEAGUE'}</span>
              </button>
            </div>
          </div>

          {/* Over & Wickets */}
          <div className="space-y-3 bg-slate-50/70 p-3.5 rounded-lg border border-slate-200/60">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[10px] uppercase font-bold text-slate-600">Over Completed: Over {over}</span>
                <span className="font-mono font-bold text-slate-900">{ballsRemaining} balls left</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="20" 
                value={over} 
                onChange={(e) => setOver(Number(e.target.value))}
                className="w-full accent-rr-pink cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[10px] uppercase font-bold text-slate-600">Wickets Down: {wicketsLost}</span>
                <span className="font-mono font-bold text-slate-900">{10 - wicketsLost} wickets in hand</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="9" 
                value={wicketsLost} 
                onChange={(e) => setWicketsLost(Number(e.target.value))}
                className="w-full accent-rr-pink cursor-pointer"
              />
            </div>
          </div>

          {/* Target & Score */}
          <div className="space-y-3 bg-slate-50/70 p-3.5 rounded-lg border border-slate-200/60">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[10px] uppercase font-bold text-slate-600">Target Score: {target}</span>
                <span className="font-mono text-slate-500 text-[10px]">Par: 185</span>
              </div>
              <input 
                type="range" 
                min="130" 
                max="240" 
                value={target} 
                onChange={(e) => setTarget(Number(e.target.value))}
                className="w-full accent-rr-pink cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[10px] uppercase font-bold text-slate-600">Current Score: {currentScore}/{wicketsLost}</span>
                <span className="font-mono text-rr-pink-deep font-bold text-[10px]">Need {runsNeeded}</span>
              </div>
              <input 
                type="range" 
                min="50" 
                max={target} 
                value={currentScore} 
                onChange={(e) => setCurrentScore(Number(e.target.value))}
                className="w-full accent-rr-pink cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* Real-Time Mathematical Output Bar */}
        <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Required Run Rate</span>
            <span className={`text-lg font-black font-mono ${rrr >= 12 ? 'text-rose-700' : 'text-slate-900'}`}>
              {innings === 2 ? `${rrr} RPO` : 'Setting Target'}
            </span>
            <span className="text-[10px] text-slate-500 block">Needs {runsNeeded} runs from {ballsRemaining} balls</span>
          </div>

          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Ball Leverage Multiplier</span>
            <span className="text-lg font-black font-mono text-rr-pink-deep">
              {calculatedLeverage.toFixed(2)}x
            </span>
            <span className="text-[10px] text-rr-pink font-medium block">Domain scale 1.00x–2.50x</span>
          </div>

          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Active Signal Triggers</span>
            <span className="text-xs font-bold text-slate-900 block mt-1">
              {[
                isChaseTight ? 'Chase' : null,
                isDeathContest ? 'Death' : null,
                isCollapse ? 'Collapse' : null,
                isKnockout ? 'Playoff' : null
              ].filter(Boolean).join(' + ') || 'Baseline Phase'}
            </span>
            <span className="text-[10px] text-slate-500 block">Empirical signal detection</span>
          </div>

          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">RR Target Specialist</span>
            <span className="text-xs font-bold text-rr-pink-deep block mt-1">
              {isDeath ? 'Shashank Singh / Sunil Narine' : 'Rohit Sharma / Rasikh Salam'}
            </span>
            <span className="text-[10px] text-slate-500 block">Optimal tactical match</span>
          </div>
        </div>
      </div>

      {/* Core Diagnostic Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="glass-panel p-4 ">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Total Pressure Balls</span>
          <div className="text-2xl font-black text-slate-900 mt-0.5 font-mono">
            {summary.pressure_deliveries?.toLocaleString()}
          </div>
          <p className="text-[11px] text-rr-pink font-semibold mt-0.5">
            {summary.pressure_percentage}% of audited deliveries
          </p>
        </div>

        <div className="glass-panel p-4 ">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Baseline Comparator Pool</span>
          <div className="text-2xl font-black text-slate-900 mt-0.5 font-mono">
            {summary.baseline_deliveries?.toLocaleString()}
          </div>
          <p className="text-[11px] text-slate-600 font-semibold mt-0.5">
            {(100 - summary.pressure_percentage).toFixed(1)}% fair baseline pool
          </p>
        </div>

        <div className="glass-panel p-4 ">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Top 10 Sensitivity (computed)</span>
          <div className="text-2xl font-black text-slate-900 mt-0.5 font-mono">
            {batStab.toFixed(1)}% / {bowlStab.toFixed(1)}%
          </div>
          <p className="text-[11px] text-rr-pink font-semibold mt-0.5">
            Batter / bowler mean retention across RRR &amp; death-start shifts
          </p>
        </div>
      </div>

      {/* Proof that Pressure is NOT just Death Overs */}
      <div className="glass-panel p-5 space-y-4 ">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-rr-pink-soft text-rr-pink-deep border border-rr-pink-border">
            <ShieldCheck className="w-4 h-4 text-rr-pink" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
              Proof: The Definition Is NOT Just "Death Overs Renamed"
            </h2>
            <p className="text-[11px] text-slate-500">
              Distribution of high-pressure deliveries across match phases
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {phaseCards.map((p) => (
            <div key={p.key} className="bg-slate-50 border border-slate-200 rounded-lg p-3 space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-800 font-bold uppercase text-[10px]">{p.label}</span>
                <span className="text-rr-pink-deep font-bold font-mono">{p.pct.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                <div
                  className="bg-rr-pink h-full rounded-full transition-[width] duration-700 ease-out"
                  style={{ width: `${Math.min(100, p.pct)}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-500">{p.count.toLocaleString()} balls · {p.blurb}</p>
            </div>
          ))}
        </div>

        <div className="p-3 bg-rr-pink-soft/70 border border-rr-pink-border rounded-lg text-xs text-rr-pink-deep font-medium">
          <strong>Key Analytical Takeaway:</strong> A full{' '}
          <strong>{outsideDeathPct.toFixed(1)}%</strong> of all high-pressure deliveries occur{' '}
          <em>outside</em> the death overs. Phase is role context; pressure is match-state.
        </div>
      </div>

      {summary.pressure_band_counts && (
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-rr-pink" />
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
              Pressure Intensity Bands (display only)
            </h2>
          </div>
          <p className="text-[11px] text-slate-600">
            {summary.pressure_band_thresholds?.note ||
              'Splits pressure_index on labelled pressure deliveries into low / medium / high. Not a re-rank.'}
          </p>
          <div className="grid grid-cols-3 gap-3 text-xs">
            {(['low', 'medium', 'high'] as const).map((band) => (
              <div key={band} className="bg-slate-50 border border-slate-200 rounded-lg p-3">
                <span className="text-[10px] uppercase font-semibold text-slate-500 block">{band} intensity</span>
                <p className="font-mono font-black text-slate-900 text-lg mt-0.5">
                  {(summary.pressure_band_counts?.[band] ?? 0).toLocaleString()}
                </p>
                <p className="text-[10px] text-slate-500">
                  {summary.pressure_band_percentage?.[band] ?? 0}% of pressure balls
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Signal Architecture */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
          <Layers className="w-4 h-4 text-rr-pink" />
          <span>The 5 Pressure Signals (Composite Formula)</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {signals.map((s, idx) => (
            <div key={idx} className="glass-subcard p-4 space-y-1.5 ">
              <div className="flex justify-between items-start">
                <span className={`text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded border ${s.color}`}>
                  {s.badge}
                </span>
                <span className="text-xs font-mono text-slate-500 font-bold">{s.count?.toLocaleString()} balls</span>
              </div>
              <h3 className="text-xs font-bold text-slate-900 pt-0.5">{s.name}</h3>
              <p className="text-[11px] text-slate-600 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
