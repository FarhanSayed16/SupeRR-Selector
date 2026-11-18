import React, { useMemo, useState } from 'react';
import { BoardMode, ExcludedPlayer, PageId, BowlerRecord } from '../types';
import { Medal } from '../components/Medal';
import { ConfidenceBadge } from '../components/ConfidenceBadge';
import { PlayerAvatar } from '../components/PlayerAvatar';
import { Shield, Search, ArrowRight } from 'lucide-react';

interface BowlerIntelligenceProps {
  bowlers: BowlerRecord[];
  globalBowlers: BowlerRecord[];
  excluded: ExcludedPlayer[];
  onNavigate: (page: PageId, playerId?: number) => void;
}

function iplPct(bw: BowlerRecord): number {
  if (bw.ipl_pressure_share != null) return Math.round(100 * Number(bw.ipl_pressure_share));
  if (bw.pressure_balls > 0 && bw.ipl_pressure_balls != null) {
    return Math.round((100 * Number(bw.ipl_pressure_balls)) / bw.pressure_balls);
  }
  return 0;
}

export const BowlerIntelligence: React.FC<BowlerIntelligenceProps> = ({
  bowlers,
  globalBowlers,
  excluded,
  onNavigate,
}) => {
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('All');
  const [board, setBoard] = useState<BoardMode>('auction');

  const source = board === 'auction' ? bowlers : globalBowlers;
  const filtered = source.filter((bw) => {
    const matchesSearch = bw.player_name.toLowerCase().includes(search.toLowerCase());
    const matchesRole = roleFilter === 'All' || bw.primary_role.includes(roleFilter);
    return matchesSearch && matchesRole;
  });

  const avgDeath = useMemo(() => {
    if (!source.length) return 0;
    return (
      source.reduce(
        (a, c) => a + Number(c.death_pressure_economy_capped ?? c.death_pressure_economy),
        0
      ) / source.length
    );
  }, [source]);

  const totalWkts = useMemo(
    () => source.reduce((a, c) => a + Number(c.pressure_wickets), 0),
    [source]
  );

  const excludedBowlers = excluded.filter((e) => e.category === 'Bowler');

  return (
    <div className="space-y-6 pb-12 font-sans">
      <div className="glass-panel p-5 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <div className="inline-flex items-center space-x-1.5 text-rr-pink-deep text-xs font-bold uppercase tracking-wider mb-1">
              <Shield className="w-3.5 h-3.5 text-rr-pink" />
              <span>Rajasthan Royals Bowling Recruitment Board</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              Full Bowler Pressure Board
            </h1>
            <p className="text-slate-600 text-xs sm:text-sm mt-0.5">
              {board === 'auction'
                ? `Auction Official — all ${source.length} eligible bowlers (Top 10 frozen).`
                : `Global Combined — all ${source.length} bowlers (no IPL floor).`}
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
                placeholder="Filter bowler..."
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
              <option value="Bowler">Pure Bowler</option>
              <option value="All-Rounder">Bowling All-Rounder</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Board</span>
            <span className="font-bold text-slate-900">{board === 'auction' ? 'Auction Official' : 'Global'}</span>
          </div>
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Board Death Econ</span>
            <span className="font-bold text-rr-pink-deep font-mono">{avgDeath.toFixed(2)} RPO</span>
          </div>
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Board Wickets</span>
            <span className="font-bold text-slate-900 font-mono">{totalWkts} Wickets</span>
          </div>
          <div className="glass-kpi p-2.5">
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Target Restrict Void</span>
            <span className="font-bold text-rr-pink-deep">Overs 17 & 19</span>
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
                <th className="py-3 px-3 text-right">Weighted Econ</th>
                <th className="py-3 px-3 text-right">PP / Mid / Death</th>
                <th className="py-3 px-3 text-right">Wickets</th>
                <th className="py-3 px-3 text-right">Balls/Wkt</th>
                <th className="py-3 px-3 text-right">Dot Ball %</th>
                <th className="py-3 px-3 text-center">Rel.</th>
                <th className="py-3 px-3 text-center">Confidence</th>
                <th className="py-3 px-3 text-center">Dossier</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((bw) => (
                <tr
                  key={`${board}-${bw.player_id}`}
                  className={`hover:bg-rr-pink-soft/40 transition-colors cursor-pointer group ${
                    bw.rank <= 10 ? 'bg-rr-pink-soft/15' : ''
                  }`}
                  onClick={() => onNavigate('player_profile', bw.player_id)}
                >
                  <td className="py-3 px-3 text-center">
                    <Medal rank={bw.rank} />
                  </td>
                  <td className="py-3 px-3">
                    <div className="flex items-center space-x-2.5">
                      <PlayerAvatar playerId={bw.player_id} name={bw.player_name} size="sm" />
                      <div className="min-w-0">
                        <div className="font-bold text-slate-900 group-hover:text-rr-pink-deep text-sm transition-colors">
                          {bw.player_name}
                        </div>
                        <div className="text-[11px] text-slate-600 font-medium leading-snug">
                          {bw.archetype || bw.primary_role}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-center">
                    <span className="inline-flex px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-rr-navy/5 text-rr-navy border border-slate-200">
                      {iplPct(bw)}%
                    </span>
                  </td>
                  <td className="py-3.5 px-3 text-right font-black text-xs text-slate-900 font-mono">
                    {Number(bw.pressure_score).toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">
                    {Number(bw.weighted_pressure_economy ?? bw.pressure_economy).toFixed(2)}
                  </td>
                  <td className="py-3 px-3">
                    <div className="flex items-center justify-end gap-1">
                      <div className="phase-chip">
                        <span>PP</span>
                        <span>{Number(bw.pp_pressure_economy ?? 0).toFixed(1)}</span>
                      </div>
                      <div className="phase-chip">
                        <span>Mid</span>
                        <span>{Number(bw.mid_pressure_economy ?? 0).toFixed(1)}</span>
                      </div>
                      <div className="phase-chip">
                        <span>Death</span>
                        <span>
                          {Number(
                            bw.death_pressure_economy_capped ?? bw.death_pressure_economy
                          ).toFixed(1)}
                        </span>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-right font-mono font-bold text-slate-900">
                    {bw.pressure_wickets}
                  </td>
                  <td className="py-3 px-3 text-right font-mono text-slate-700">
                    {Number(bw.pressure_balls_per_wicket).toFixed(1)}
                  </td>
                  <td className="py-3 px-3 text-right font-mono text-slate-700">
                    {Number(bw.pressure_dot_pct).toFixed(1)}%
                  </td>
                  <td className="py-3 px-3">
                    <div className="mx-auto w-14">
                      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-rr-pink rounded-full"
                          style={{ width: `${Math.round(100 * Number(bw.reliability ?? 0))}%` }}
                        />
                      </div>
                      <div className="text-center font-mono text-[10px] text-slate-600 mt-0.5">
                        {Math.round(100 * Number(bw.reliability ?? 0))}%
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-center">
                    <ConfidenceBadge level={bw.sample_confidence} />
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

      {board === 'auction' && excludedBowlers.length > 0 && (
        <div className="glass-panel p-4 space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wide text-slate-900">
            Excluded from Auction Official (low IPL sample)
          </h3>
          <p className="text-[11px] text-slate-600">
            Present on Global Combined Top 10 but below the IPL pressure-ball floor (e.g. 0% IPL).
          </p>
          <div className="flex flex-wrap gap-2">
            {excludedBowlers.map((e) => (
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
