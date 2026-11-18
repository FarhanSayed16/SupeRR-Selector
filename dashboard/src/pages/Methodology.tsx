import React, { useEffect, useState } from 'react';
import { BookOpen, Scale, ShieldAlert, Cpu } from 'lucide-react';
import { MetaPackage, MethodologyPackage } from '../types';
import { fetchMethodology } from '../lib/data';

interface MethodologyProps {
  meta?: MetaPackage | null;
}

export const Methodology: React.FC<MethodologyProps> = ({ meta }) => {
  const [pack, setPack] = useState<MethodologyPackage | null>(null);

  useEffect(() => {
    fetchMethodology()
      .then(setPack)
      .catch(() => setPack(null));
  }, []);

  const iplW = pack?.ipl_weight ?? meta?.ipl_weight ?? 1.3;
  const t20W = pack?.t20i_weight ?? meta?.t20i_weight ?? 1.0;
  const batFloor = pack?.min_ipl_pressure_balls_batter ?? meta?.min_ipl_pressure_balls_batter ?? 40;
  const bowlFloor = pack?.min_ipl_pressure_balls_bowler ?? meta?.min_ipl_pressure_balls_bowler ?? 60;
  const batMin = pack?.min_batter_pressure_balls ?? 50;
  const bowlMin = pack?.min_bowler_pressure_balls ?? 80;
  const sha = meta?.freeze_sha256;
  const version = pack?.pressure_version ?? meta?.version ?? 'pressure_v1.1';

  return (
    <div className="space-y-8 pb-12 max-w-5xl mx-auto">
      <div className="glass-panel p-6 sm:p-8 space-y-3">
        <div className="inline-flex items-center space-x-2 text-rr-pink-deep text-xs font-bold uppercase tracking-wider">
          <BookOpen className="w-4 h-4 text-rr-pink" />
          <span>Royals Analytics Evaluation Standard</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 uppercase tracking-tight">
          PressurePulse <span className="text-rr-pink">Methodology & Architecture</span>
        </h1>
        <p className="text-slate-600 text-xs sm:text-sm leading-relaxed">
          Transparent, fully reproducible analytics ({version}). Every Auction Official rank is
          deterministically derived from delivery-level match events across IPL and men&apos;s T20
          Internationals (2022–2026).
        </p>
        {sha && (
          <p className="text-[11px] font-mono text-slate-500">
            Freeze SHA256: {sha.slice(0, 16)}… · Board: Auction Official
          </p>
        )}
      </div>

      <div className="glass-panel p-6 space-y-4">
        <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-rr-pink" />
          <span>1. Pressure Definition & Match Context Reconstruction</span>
        </h2>
        <div className="p-4 bg-slate-50 rounded-xl border-l-4 border-rr-pink text-xs sm:text-sm text-slate-800 italic">
          {pack?.definition_sentence ||
            'A delivery is defined as high-pressure when match context demands immediate high-leverage execution: specifically during steep chases (RRR >= 9.5), death-over contests, severe batting collapses (<=3 wickets in hand), or critical playoff knockout stages.'}
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          The pipeline reconstructs innings state after every ball (RRR, balls remaining, wickets in
          hand), accounting for legal balls and extras. Super overs are gated by config
          (currently excluded from pressure).
        </p>
      </div>

      <div className="glass-panel p-6 space-y-4">
        <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide flex items-center space-x-2">
          <Scale className="w-5 h-5 text-rr-pink" />
          <span>2. Transparent Scoring Formulations ({version})</span>
        </h2>

        <div className="space-y-2.5 p-4 bg-slate-50 rounded-xl border border-slate-200">
          <h3 className="text-xs font-bold uppercase text-rr-pink-deep">
            Batters Composite PressureScore (0–100)
          </h3>
          <p className="text-xs text-slate-900 font-mono bg-white p-2.5 rounded border border-slate-200/70">
            PressureScore = 0.40 × ClutchQuality + 0.25 × Uplift + 0.20 × Consistency + 0.15 × Volume
          </p>
          <ul className="text-xs text-slate-600 list-disc list-inside space-y-1.5 pt-1 leading-relaxed">
            <li>
              <strong>Rates:</strong> Legal-ball SR/dot%/boundary%; IPL deliveries weighted {iplW}x
              and T20I {t20W}x inside the rate (no separate post-hoc boost).
            </li>
            <li>
              <strong>ClutchQuality (40%):</strong> Normalized weighted pressure SR, boundary %, and
              batting average.
            </li>
            <li>
              <strong>Uplift (25%):</strong> Weighted Pressure SR − Baseline SR.
            </li>
            <li>
              <strong>Consistency (20%) / Volume (15%):</strong> Match stability and sample depth.
            </li>
          </ul>
        </div>

        <div className="space-y-2.5 p-4 bg-slate-50 rounded-xl border border-slate-200">
          <h3 className="text-xs font-bold uppercase text-rr-pink-deep">
            Bowlers Composite PressureScore (0–100)
          </h3>
          <p className="text-xs text-slate-900 font-mono bg-white p-2.5 rounded border border-slate-200/70">
            PressureScore = 0.35 × Restrictiveness + 0.30 × WicketThreat + 0.15 × EconomyUplift + 0.10
            × Consistency + 0.10 × Volume
          </p>
          <ul className="text-xs text-slate-600 list-disc list-inside space-y-1.5 pt-1 leading-relaxed">
            <li>
              <strong>Rates:</strong> Legal-ball economy with the same IPL {iplW}x / T20I {t20W}x
              bake-in; death economy soft-capped when death sample is thin.
            </li>
            <li>
              <strong>Restrictiveness (35%):</strong> Weighted pressure economy + capped death econ +
              dot %.
            </li>
            <li>
              <strong>WicketThreat (30%):</strong> Balls per dismissal and pressure wickets (run-outs
              excluded).
            </li>
          </ul>
        </div>
      </div>

      <div className="glass-panel p-6 space-y-3">
        <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide">
          3. Boards, Eligibility & Duplicate Guards
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <span className="text-slate-900 font-bold block">Auction Official (primary freeze)</span>
            <p className="text-slate-600 leading-relaxed">
              Batters: ≥{batMin} pressure balls, ≥40 baseline, ≥5 matches, and ≥{batFloor} IPL
              pressure legal balls. Bowlers: ≥{bowlMin} pressure balls, ≥60 baseline, ≥5 matches,
              and ≥{bowlFloor} IPL pressure legal balls.
            </p>
          </div>
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <span className="text-slate-900 font-bold block">Global Combined + overlap guard</span>
            <p className="text-slate-600 leading-relaxed">
              Secondary board without IPL floors (methodology context). No player may appear on both
              Top 10 lists — all-rounders resolve to their stronger relative percentile.
            </p>
          </div>
        </div>
        {pack?.board_policy && (
          <p className="text-[11px] text-slate-500 leading-relaxed">{pack.board_policy}</p>
        )}
      </div>

      <div className="glass-panel p-6 space-y-3">
        <div className="flex items-center space-x-2 text-slate-900">
          <ShieldAlert className="w-5 h-5 text-amber-700" />
          <h2 className="text-lg font-black text-slate-900 uppercase tracking-wide">
            4. Scientific Limitations & Data Boundaries
          </h2>
        </div>
        <ul className="text-xs text-slate-600 list-disc list-inside space-y-2 leading-relaxed">
          <li>
            <strong>Bowl Speed Missingness:</strong> `bowl_speed` is unrecorded on a large share of
            deliveries; treated as auxiliary context, not a scoring gate.
          </li>
          <li>
            <strong>Auction Valuation:</strong> Market prices and purse constraints are excluded from
            Round 1 performance ranks.
          </li>
          <li>
            <strong>Domain Adaptation:</strong> IPL balls enter rates at {iplW}x vs T20I {t20W}x so
            franchise intensity is baked into SR/economy — not a separate +15% score multiplier.
          </li>
        </ul>
      </div>
    </div>
  );
};
