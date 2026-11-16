import React from 'react';
import { BookOpen, Scale, ShieldAlert, Cpu } from 'lucide-react';

export const Methodology: React.FC = () => {
  return (
    <div className="space-y-8 pb-12 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 sm:p-8 space-y-3 shadow-xs">
        <div className="inline-flex items-center space-x-2 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          <BookOpen className="w-4 h-4 text-emerald-700" />
          <span>Royals Analytics Evaluation Standard</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 uppercase tracking-tight">
          PressurePulse <span className="text-emerald-700">Methodology & Architecture</span>
        </h1>
        <p className="text-slate-600 text-xs sm:text-sm leading-relaxed">
          Transparent, fully reproducible analytics built to franchise war-room standards. Every rank is deterministically derived from delivery-level match events across IPL and men's T20 Internationals (2022–2026).
        </p>
      </div>

      {/* Section 1: Pressure Definition */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-6 space-y-4 shadow-xs">
        <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-emerald-700" />
          <span>1. Pressure Definition & Match Context Reconstruction</span>
        </h2>
        <div className="p-4 bg-slate-50 rounded-xl border-l-4 border-emerald-600 text-xs sm:text-sm text-slate-800 italic">
          "A delivery is defined as high-pressure when match context demands immediate high-leverage execution: specifically during steep chases (RRR &gt;= 9.5), death-over contests, severe batting collapses (&lt;=3 wickets in hand), or critical playoff knockout stages."
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          To calculate Required Run Rate (RRR) and balls remaining after every ball, our pipeline reconstructs the full state of every innings from delivery records, accounting for legal balls, extras (wides and no-balls do not consume balls), and DLS/rain-revised targets from official match metadata.
        </p>
      </div>

      {/* Section 2: Mathematical Formulations */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-6 space-y-4 shadow-xs">
        <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide flex items-center space-x-2">
          <Scale className="w-5 h-5 text-emerald-700" />
          <span>2. Transparent Scoring Formulations</span>
        </h2>

        {/* Batter Formula */}
        <div className="space-y-2.5 p-4 bg-slate-50 rounded-xl border border-slate-200">
          <h3 className="text-xs font-bold uppercase text-emerald-900">Batters Composite PressureScore (0–100)</h3>
          <p className="text-xs text-slate-900 font-mono bg-white p-2.5 rounded border border-slate-200/70">
            PressureScore = (0.40 × ClutchQuality + 0.25 × Uplift + 0.20 × Consistency + 0.15 × Volume) × IPL_Boost
          </p>
          <ul className="text-xs text-slate-600 list-disc list-inside space-y-1.5 pt-1 leading-relaxed">
            <li><strong>ClutchQuality (40%):</strong> Normalized Pressure Strike Rate (110–180), Boundary % (12–28%), and Batting Average.</li>
            <li><strong>Uplift (25%):</strong> Strike Rate Uplift = Pressure_SR − Baseline_SR. Evaluates true rise-to-the-occasion ability against non-pressure baseline.</li>
            <li><strong>Consistency (20%):</strong> Match-to-match reliability score derived from the inverse coefficient of variation of per-match strike rate.</li>
            <li><strong>Volume (15%):</strong> Sample depth curve ensuring stability across tournaments.</li>
            <li><strong>IPL_Boost:</strong> Up to +15% multiplier proportional to balls faced against premier IPL bowling attacks.</li>
          </ul>
        </div>

        {/* Bowler Formula */}
        <div className="space-y-2.5 p-4 bg-slate-50 rounded-xl border border-slate-200">
          <h3 className="text-xs font-bold uppercase text-emerald-900">Bowlers Composite PressureScore (0–100)</h3>
          <p className="text-xs text-slate-900 font-mono bg-white p-2.5 rounded border border-slate-200/70">
            PressureScore = (0.35 × Restrictiveness + 0.30 × WicketThreat + 0.15 × EconomyUplift + 0.10 × Consistency + 0.10 × Volume) × IPL_Boost
          </p>
          <ul className="text-xs text-slate-600 list-disc list-inside space-y-1.5 pt-1 leading-relaxed">
            <li><strong>Restrictiveness (35%):</strong> Overall pressure economy (6.0–11.5 benchmark) combined with Death Overs (16–20) economy and dot-ball %.</li>
            <li><strong>WicketThreat (30%):</strong> Balls per dismissal (11–24 balls/wkt) and total pressure wickets taken. Only wickets credited to bowler (Caught, Bowled, LBW, Stumped, Hit Wicket) are included; run-outs are excluded.</li>
            <li><strong>EconomyUplift (15%):</strong> Evaluates ability to resist the natural league-wide +2.5 RPO economy surge in death/pressure situations.</li>
            <li><strong>Consistency & Volume (20%):</strong> Per-match economy stability and volume depth.</li>
          </ul>
        </div>
      </div>

      {/* Section 3: Fairness & Eligibility */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-6 space-y-3 shadow-xs">
        <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide">
          3. Fairness, Eligibility & Duplicate Guards
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <span className="text-slate-900 font-bold block">Strict Sample Size Minimums:</span>
            <p className="text-slate-600 leading-relaxed">
              Batters must have faced at least 50 pressure balls and 40 baseline balls across &gt;=5 matches. Bowlers must have bowled at least 80 pressure balls and 60 baseline balls. This permanently filters out small-sample anomalies.
            </p>
          </div>
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <span className="text-slate-900 font-bold block">Zero Cross-List Overlap:</span>
            <p className="text-slate-600 leading-relaxed">
              As mandated by Rajasthan Royals and Unstop guidelines, no player may appear on both Top 10 lists. All-rounders who qualify in both categories are allocated to their highest relative percentile score.
            </p>
          </div>
        </div>
      </div>

      {/* Section 4: Limitations */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-6 space-y-3 shadow-xs">
        <div className="flex items-center space-x-2 text-slate-900">
          <ShieldAlert className="w-5 h-5 text-amber-700" />
          <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide">
            4. Scientific Limitations & Data Boundaries
          </h2>
        </div>
        <ul className="text-xs text-slate-600 list-disc list-inside space-y-2 leading-relaxed">
          <li><strong>Bowl Speed Missingness:</strong> `bowl_speed` is unrecorded on 38.7% of deliveries; hence it was relegated to an auxiliary context proxy rather than a hard scoring gate.</li>
          <li><strong>Auction Valuation Nuance:</strong> Player market prices and squad purse constraints are intentionally excluded from Round 1 player performance rankings (as specified in the official Round 1 problem statement).</li>
          <li><strong>Domain Adaptation:</strong> While T20 Internationals provide expansive global sample depth, an IPL weighting factor (1.30x) was incorporated to reflect the unique competitive intensity of Indian franchise cricket.</li>
        </ul>
      </div>
    </div>
  );
};
