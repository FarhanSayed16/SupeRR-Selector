import React from 'react';
import { Info, Shield } from 'lucide-react';
import { MetaPackage } from '../types';

export const About: React.FC<{ meta: MetaPackage | null }> = ({ meta }) => {
  return (
    <div className="space-y-8 pb-12 max-w-4xl mx-auto">
      <div className="glass-panel p-6 sm:p-8 space-y-4 ">
        <div className="inline-flex items-center space-x-2 text-rr-pink-deep text-xs font-bold uppercase tracking-wider">
          <Info className="w-4 h-4 text-rr-pink" />
          <span>Competition Information & Compliance</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 uppercase tracking-tight">
          About <span className="text-rr-pink">PressurePulse</span>
        </h1>
        <p className="text-slate-600 text-xs sm:text-sm leading-relaxed">
          Developed for <strong>SupeRR Selector Season 2: Help Shape Rajasthan Royals' IPL 2027 Auction Strategy</strong>, hosted on Unstop by Rajasthan Royals.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-slate-500 text-xs uppercase font-semibold">Competition Stage</span>
            <p className="text-sm font-bold text-slate-900">Round 1: Identify the Most Reliable Players Under Pressure</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-slate-500 text-xs uppercase font-semibold">Organisers</span>
            <p className="text-sm font-bold text-slate-900">Rajasthan Royals × Unstop</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-slate-500 text-xs uppercase font-semibold">Participation</span>
            <p className="text-sm font-bold text-slate-900">Individual Entry</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-slate-500 text-xs uppercase font-semibold">Submission Deadline</span>
            <p className="text-sm font-bold text-slate-900">18 Nov 2026, 11:59 PM IST</p>
          </div>
        </div>
      </div>

      <div className="glass-panel p-6 space-y-3 ">
        <h2 className="text-base font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
          <Shield className="w-5 h-5 text-rr-pink" />
          <span>Proprietary Data Usage & Security</span>
        </h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          The dataset used in this model was provided by Rajasthan Royals for the SupeRR Selector competition. In strict adherence to competition rules, raw delivery-level CSVs are kept strictly private on local analytical workstations. Only derived statistical aggregates and model rankings are exposed to this dashboard.
        </p>
        <div className="p-3 bg-slate-50 rounded-lg text-xs font-mono text-slate-700 border border-slate-200">
          Rank Freeze SHA256: {meta?.freeze_sha256 || '5cdd7b7451b5a6672dbfadccc3c36a9777ec5bafaec589339e22ba307202d272'}
        </div>
      </div>
    </div>
  );
};
