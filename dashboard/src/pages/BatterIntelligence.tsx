import React, { useMemo, useState } from 'react';
import { BoardMode, ExcludedPlayer, PageId, BatterRecord } from '../types';
import { Medal } from '../components/Medal';
import { ConfidenceBadge } from '../components/ConfidenceBadge';
import { PlayerAvatar } from '../components/PlayerAvatar';
import { Target, Search, ArrowRight } from 'lucide-react';

interface BatterIntelligenceProps {
  batters: BatterRecord[];
  globalBatters: BatterRecord[];
  excluded: ExcludedPlayer[];
  onNavigate: (page: PageId, playerId?: number) => void;
}

function iplPct(b: BatterRecord): number {
  if (b.ipl_pressure_share != null) return Math.round(100 * Number(b.ipl_pressure_share));
  if (b.pressure_balls > 0 && b.ipl_pressure_balls != null) {
    return Math.round((100 * Number(b.ipl_pressure_balls)) / b.pressure_balls);
  }
  return 0;
}

export const BatterIntelligence: React.FC<BatterIntelligenceProps> = ({
  batters,
  globalBatters,
  excluded,
  onNavigate,
}) => {
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('All');
  const [board, setBoard] = useState<BoardMode>('auction');

  const source = board === 'auction' ? batters : globalBatters;
  const filtered = source.filter((b) => {
    const matchesSearch = b.player_name.toLowerCase().includes(search.toLowerCase());
    const matchesRole = roleFilter === 'All' || b.primary_role.includes(roleFilter);
    return matchesSearch && matchesRole;
  });

  const avgSr = useMemo(() => {
    if (!source.length) return 0;
    const vals = source.map((b) => Number(b.weighted_pressure_sr ?? b.pressure_sr));
    return vals.reduce((a, c) => a + c, 0) / vals.length;
  }, [source]);

  const avgUplift = useMemo(() => {
    if (!source.length) return 0;
    return source.reduce((a, c) => a + Number(c.sr_uplift), 0) / source.length;
  }, [source]);

  const excludedBatters = excluded.filter((e) => e.category === 'Batter');

  return (
    <div className="space-y-6 pb-12 font-sans">
      <div className="glass-panel p-5 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <div className="inline-flex items-center space-x-1.5 text-rr-pink-deep text-xs font-bold uppercase tracking-wider mb-1">
              <Target className="w-3.5 h-3.5 text-rr-pink" />
              <span>Rajasthan Royals Batting Recruitment Board</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              Top 10 Batters Under Pressure
            </h1>
            <p className="text-slate-600 text-xs sm:text-sm mt-0.5">
              {board === 'auction'
                ? 'Auction Official — IPL sample floors + IPL/T20I weighted legal-ball rates.'
                : 'Global Combined — no IPL floor (methodology context board).'}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-semibold">
              <button
                type="button"
                onClick={() => setBoard('auction')}
                className={`px-3 py-1.5 rounded-md cursor-pointer ${
                  board === 'auction' ? 'bg-rr-pink text-white font-bold' : 'text-slate-600'
                }`}
              >
                Auction Official
              </button>
              <button
                type="button"
                onClick={() => setBoard('global')}
                className={`px-3 py-1.5 rounded-md cursor-pointer ${
                  board === 'global' ? 'bg-rr-pink text-white font-bold' : 'text-slate-600'
                }`}
              >
                Global Combined
              </button>
            </div>
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Filter player..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-rr-pink focus:bg-white transition-all w-40 sm:w-48"
              />
            </div>
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-800 focus:outline-none focus:border-rr-pink focus:bg-white cursor-pointer font-medium"
            >
              <option value="All">All Roles</option>
              <option value="Batter">Pure Batter</option>
              <option value="Wicketkeeper">Wicketkeeper-Batter</option>
              <option value="All-Rounder">All-Rounder</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Board</span>
            <span className="font-bold text-slate-900">{board === 'auction' ? 'Auction Official' : 'Global'}</span>
          </div>
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Top 10 Avg Weighted SR</span>
            <span className="font-bold text-rr-pink-deep font-mono">{avgSr.toFixed(1)}</span>
          </div>
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Top 10 Avg Uplift</span>
            <span className="font-bold text-rr-pink-deep font-mono">+{avgUplift.toFixed(1)}</span>
          </div>
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Target Finish Void</span>
            <span className="font-bold text-slate-900">#6/#7 Slots</span>
          </div>
        </div>
      </div>

      <div className="glass-panel overflow-hidden">
        <div key={board} className="overflow-x-auto board-fade">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/80 text-slate-700 uppercase font-bold tracking-wider border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3 px-3 w-12 text-center">Rank</th>
                <th className="py-3 px-3">Player & Tactical Archetype</th>
                <th className="py-3 px-3 text-center">IPL%</th>
                <th className="py-3 px-3 text-right">Pressure Score</th>
                <th className="py-3 px-3 text-right">Weighted SR</th>
                <th className="py-3 px-3 text-right">PP / Mid / Death</th>
                <th className="py-3 px-3 text-right">SR Uplift</th>
                <th className="py-3 px-3 text-right">Chase SR</th>
                <th className="py-3 px-3 text-center">Rel.</th>
                <th className="py-3 px-3 text-center">Confidence</th>
                <th className="py-3 px-3 text-center">Dossier</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((b) => (
                <tr
                  key={`${board}-${b.player_id}`}
                  className="hover:bg-rr-pink-soft/40 transition-colors cursor-pointer group"
                  onClick={() => onNavigate('player_profile', b.player_id)}
                >
                  <td className="py-3 px-3 text-center">
                    <Medal rank={b.rank} />
                  </td>
                  <td className="py-3.5 px-3">
                    <div className="flex items-center space-x-3">
                      <PlayerAvatar playerId={b.player_id} name={b.player_name} size="sm" />
                      <div className="min-w-0">
                        <div className="font-bold text-slate-900 group-hover:text-rr-pink-deep text-sm transition-colors">
                          {b.player_name}
                        </div>
                        <div className="text-[11px] text-slate-600 font-medium leading-snug">
                          {b.archetype || b.primary_role}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-center">
                    <span className="inline-flex px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-rr-navy/5 text-rr-navy border border-slate-200">
                      {iplPct(b)}%
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right font-black text-xs text-slate-900 font-mono">
                    {Number(b.pressure_score).toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">
                    {Number(b.weighted_pressure_sr ?? b.pressure_sr).toFixed(1)}
                  </td>
                  <td className="py-3 px-3">
                    <div className="flex items-center justify-end gap-1">
                      <div className="phase-chip">
                        <span>PP</span>
                        <span>{Number(b.pp_pressure_sr ?? 0).toFixed(0)}</span>
                      </div>
                      <div className="phase-chip">
                        <span>Mid</span>
                        <span>{Number(b.mid_pressure_sr ?? 0).toFixed(0)}</span>
                      </div>
                      <div className="phase-chip">
                        <span>Death</span>
                        <span>{Number(b.death_pressure_sr).toFixed(0)}</span>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold">
                    <span className="inline-flex items-center text-rr-pink-deep bg-rr-pink-soft border border-rr-pink-border px-1.5 rounded text-[11px]">
                      +{Number(b.sr_uplift).toFixed(1)}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-medium text-slate-800">
                    {Number(b.chase_pressure_sr).toFixed(1)}
                  </td>
                  <td className="py-3 px-3">
                    <div className="mx-auto w-14">
                      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-rr-pink rounded-full"
                          style={{ width: `${Math.round(100 * Number(b.reliability ?? 0))}%` }}
                        />
                      </div>
                      <div className="text-center font-mono text-[10px] text-slate-600 mt-0.5">
                        {Math.round(100 * Number(b.reliability ?? 0))}%
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-center">
                    <ConfidenceBadge level={b.sample_confidence} />
                  </td>
                  <td className="py-3 px-3 text-center">
                    <button
                      type="button"
                      className="text-xs font-semibold text-rr-pink-deep group-hover:text-rr-navy p-1 rounded hover:bg-rr-pink-soft transition-colors flex items-center space-x-0.5 mx-auto"
                    >
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

      {board === 'auction' && excludedBatters.length > 0 && (
        <div className="glass-panel p-4 space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wide text-slate-900">
            Excluded from Auction Official (low IPL sample)
          </h3>
          <p className="text-[11px] text-slate-600">
            Present on Global Combined Top 10 but below the IPL pressure-ball floor.
          </p>
          <div className="flex flex-wrap gap-2">
            {excludedBatters.map((e) => (
              <span
                key={e.player_id}
                className="text-[11px] font-semibold px-2 py-1 rounded-full bg-amber-50 text-amber-900 border border-amber-200"
              >
                {e.player_name}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
