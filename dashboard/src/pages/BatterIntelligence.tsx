import React, { useState } from 'react';
import { PageId, BatterRecord } from '../types';
import { Medal } from '../components/Medal';
import { ConfidenceBadge } from '../components/ConfidenceBadge';
import { Target, Search, ArrowRight, Zap, TrendingUp, BarChart3 } from 'lucide-react';

interface BatterIntelligenceProps {
  batters: BatterRecord[];
  onNavigate: (page: PageId, playerId?: number) => void;
}

export const BatterIntelligence: React.FC<BatterIntelligenceProps> = ({
  batters,
  onNavigate
}) => {
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('All');

  const filtered = batters.filter((b) => {
    const matchesSearch = b.player_name.toLowerCase().includes(search.toLowerCase());
    const matchesRole = roleFilter === 'All' || b.primary_role.includes(roleFilter);
    return matchesSearch && matchesRole;
  });

  return (
    <div className="space-y-6 pb-12 font-sans">
      {/* Page Header */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <div className="inline-flex items-center space-x-1.5 text-emerald-800 text-xs font-bold uppercase tracking-wider mb-1">
              <Target className="w-3.5 h-3.5 text-emerald-700" />
              <span>Rajasthan Royals Batting Recruitment Board</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              Top 10 Batters Under Pressure (IPL 2027 Auction Target Pool)
            </h1>
            <p className="text-slate-600 text-xs sm:text-sm mt-0.5">
              Ranked by composite PressureScore measuring clutch strike rate, positive uplift vs baseline, consistency, and volume depth.
            </p>
          </div>

          {/* Search & Filter Controls */}
          <div className="flex flex-wrap items-center gap-2.5">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Filter player..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-600 focus:bg-white transition-all w-40 sm:w-48"
              />
            </div>
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-800 focus:outline-none focus:border-emerald-600 focus:bg-white cursor-pointer font-medium"
            >
              <option value="All">All Roles</option>
              <option value="Batter">Pure Batter</option>
              <option value="Wicketkeeper">Wicketkeeper-Batter</option>
              <option value="All-Rounder">All-Rounder</option>
            </select>
          </div>
        </div>

        {/* Quick Analytical Benchmark Strips */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="bg-slate-50/80 p-2.5 rounded-lg border border-slate-200/70">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Cohort Size</span>
            <span className="font-bold text-slate-900 font-mono">379 Batters</span>
          </div>
          <div className="bg-slate-50/80 p-2.5 rounded-lg border border-slate-200/70">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Top 10 Avg SR</span>
            <span className="font-bold text-emerald-800 font-mono">172.9 Strike Rate</span>
          </div>
          <div className="bg-slate-50/80 p-2.5 rounded-lg border border-slate-200/70">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Top 10 Avg Uplift</span>
            <span className="font-bold text-emerald-800 font-mono">+57.5 vs Baseline</span>
          </div>
          <div className="bg-slate-50/80 p-2.5 rounded-lg border border-slate-200/70">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Target Finish Void</span>
            <span className="font-bold text-slate-900">#6/#7 Slots</span>
          </div>
        </div>
      </div>

      {/* Main Board Table */}
      <div className="bg-white border border-slate-200/90 rounded-xl overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/80 text-slate-700 uppercase font-bold tracking-wider border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3 px-3 w-12 text-center">Rank</th>
                <th className="py-3 px-3">Player & Tactical Archetype</th>
                <th className="py-3 px-3 text-right">Pressure Score</th>
                <th className="py-3 px-3 text-right">Pressure SR</th>
                <th className="py-3 px-3 text-right">Baseline SR</th>
                <th className="py-3 px-3 text-right">SR Uplift</th>
                <th className="py-3 px-3 text-right">Death SR (16-20)</th>
                <th className="py-3 px-3 text-right">Chase SR (Inn 2)</th>
                <th className="py-3 px-3 text-right">Dot Ball %</th>
                <th className="py-3 px-3 text-center">Confidence</th>
                <th className="py-3 px-3 text-center">Dossier</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((b) => (
                <tr 
                  key={b.player_id}
                  className="hover:bg-emerald-50/40 transition-colors cursor-pointer group"
                  onClick={() => onNavigate('player_profile', b.player_id)}
                >
                  <td className="py-3 px-3 text-center">
                    <Medal rank={b.rank} />
                  </td>
                  <td className="py-3 px-3">
                    <div className="font-bold text-slate-900 group-hover:text-emerald-900 text-xs transition-colors flex items-center space-x-1.5">
                      <span>{b.player_name}</span>
                    </div>
                    <div className="text-[10px] text-slate-500 font-medium">
                      {b.archetype || b.primary_role}
                    </div>
                  </td>
                  <td className="py-3 px-3 text-right font-black text-xs text-slate-900 font-mono">
                    {b.pressure_score.toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">
                    {b.pressure_sr.toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono text-slate-500">
                    {b.baseline_sr.toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold">
                    <span className="inline-flex items-center text-emerald-800 bg-emerald-50 border border-emerald-200 px-1.5 py-0.2 rounded text-[11px]">
                      +{b.sr_uplift.toFixed(1)}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-medium text-slate-800">
                    {b.death_pressure_sr.toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-medium text-slate-800">
                    {b.chase_pressure_sr.toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono text-slate-600">
                    {b.pressure_dot_pct.toFixed(1)}%
                  </td>
                  <td className="py-3 px-3 text-center">
                    <ConfidenceBadge level={b.sample_confidence} />
                  </td>
                  <td className="py-3 px-3 text-center">
                    <button className="text-xs font-semibold text-emerald-800 group-hover:text-emerald-950 p-1 rounded hover:bg-emerald-100 transition-colors flex items-center space-x-0.5 mx-auto">
                      <span>View</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
