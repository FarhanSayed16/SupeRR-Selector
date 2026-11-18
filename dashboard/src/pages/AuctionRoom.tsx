import React, { useState } from 'react';
import { PageId, BatterRecord, BowlerRecord } from '../types';
import { PlayerAvatar } from '../components/PlayerAvatar';
import { getBrandLogoSrc } from '../lib/images';
import { 
  Award, 
  Target, 
  Shield, 
  Users, 
  Briefcase, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Compass,
  PieChart as PieIcon,
  DollarSign
} from 'lucide-react';

interface AuctionRoomProps {
  batters: BatterRecord[];
  bowlers: BowlerRecord[];
  onNavigate: (page: PageId, playerId?: number) => void;
}

export const AuctionRoom: React.FC<AuctionRoomProps> = ({
  batters,
  bowlers,
  onNavigate
}) => {
  const [activeTab, setActiveTab] = useState<'lineup' | 'field_pitch' | 'budget'>('field_pitch');

  const playingXI = [
    { slot: '1', playerId: 9001, name: 'Yashasvi Jaiswal', shortName: 'Jaiswal', role: 'LH Explosive Opener', type: 'Retained Core', pos: 'Deep Extra Cover', x: 22, y: 28, note: 'Top-Order Firepower' },
    { slot: '2', playerId: 126, name: 'Rohit Sharma', shortName: 'Rohit', role: 'Powerplay Enforcer (183.4 SR)', type: 'Auction Target', pos: 'Mid-Wicket', x: 38, y: 18, note: '+52.1 SR Uplift' },
    { slot: '3', playerId: 9002, name: 'Sanju Samson (C/WK)', shortName: 'Samson', role: 'Captain & Anchor', type: 'Retained Core', pos: 'Wicketkeeper', x: 50, y: 78, note: 'Tactical Anchor' },
    { slot: '4', playerId: 9003, name: 'Riyan Parag', shortName: 'Parag', role: 'Spin Dominator & Middle Overs', type: 'Retained Core', pos: 'Cover', x: 72, y: 26, note: 'Middle Overs Spine' },
    { slot: '5', playerId: 9004, name: 'Shimron Hetmyer', shortName: 'Hetmyer', role: 'LH Death Finisher', type: 'Retained Core', pos: 'Deep Square', x: 78, y: 62, note: 'Boundary Hitter' },
    { slot: '6', playerId: 2756, name: 'Shashank Singh', shortName: 'Shashank', role: 'Clutch Finisher (+69.2 Uplift)', type: 'Auction Target', pos: 'Long-on', x: 58, y: 14, note: '171.8 Pressure SR' },
    { slot: '7', playerId: 9005, name: 'Dhruv Jurel', shortName: 'Jurel', role: 'Clutch WK/Finisher', type: 'Retained Core', pos: 'Point', x: 24, y: 52, note: 'Pressure Adaptability' },
    { slot: '8', playerId: 781, name: 'Sunil Narine', shortName: 'Narine', role: 'Mystery Choke (6.06 Death Econ)', type: 'Auction Target', pos: 'Mid-off', x: 34, y: 66, note: 'All-Phase Restrictor' },
    { slot: '9', playerId: 9006, name: 'Sandeep Sharma', shortName: 'Sandeep', role: 'Death Knuckle Specialist', type: 'Retained Core', pos: 'Mid-on', x: 50, y: 40, note: 'Defensive Seam' },
    { slot: '10', playerId: 7327, name: 'Rasikh Salam', shortName: 'Rasikh', role: 'Death Wicket Machine (10.6 BpW)', type: 'Auction Target', pos: 'Fine Leg', x: 68, y: 82, note: 'Strike Seamer' },
    { slot: '11', playerId: 3644, name: 'Kuldeep Yadav', shortName: 'Kuldeep', role: 'Attacking Wrist Spin', type: 'Auction Target', pos: 'Deep Mid-Wicket', x: 84, y: 44, note: 'Wicket Threat' },
    { slot: 'Sub', playerId: 8101, name: 'Ashutosh Sharma', shortName: 'Ashutosh', role: 'Impact Finisher (+79.1 Uplift)', type: 'Impact Sub', pos: 'Dugout', x: 12, y: 86, note: 'Crisis 360-Hitter' },
  ];

  return (
    <div className="space-y-6 pb-12 font-sans">
      {/* Header */}
      <div className="glass-panel p-5 space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center space-x-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <img src={getBrandLogoSrc()} alt="RR" className="h-6 w-6 object-contain" />
              <span>Rajasthan Royals War Room</span>
              <span>•</span>
              <span className="text-rr-pink-deep">Auction Official Board</span>
              <span>•</span>
              <span className="font-mono text-slate-400">IPL 2027</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight mt-0.5">
              Projected RR 2027 Squad & Tactical War Room Blueprint
            </h1>
          </div>

          <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setActiveTab('field_pitch')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                activeTab === 'field_pitch'
                  ? 'bg-white text-rr-pink-deep font-bold '
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Field & Pitch View
            </button>
            <button
              onClick={() => setActiveTab('lineup')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                activeTab === 'lineup'
                  ? 'bg-white text-rr-pink-deep font-bold '
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Squad Cards
            </button>
            <button
              onClick={() => setActiveTab('budget')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                activeTab === 'budget'
                  ? 'bg-white text-rr-pink-deep font-bold '
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Purse Allocation
            </button>
          </div>
        </div>

        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-4xl">
          In Season 1, Rajasthan Royals backed our analytical recommendation of <strong>Vignesh Puthur</strong>, securing him at the IPL auction. For Season 2, we present a full <strong>Strategic Recruitment Strategy</strong> engineered for Head Coach Kumar Sangakkara and Director of Strategy Giles Lindsay, translating 200,999 deliveries into actionable auction blueprints.
        </p>
      </div>

      {/* Main Dynamic View: Field / Lineup / Budget */}
      {activeTab === 'field_pitch' && (
        <div className="glass-panel p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
                <Compass className="w-4 h-4 text-rr-pink" />
                <span>Tactical Field Map: Projected RR 2027 Playing XI</span>
              </h2>
              <p className="text-[11px] text-slate-500">
                Spatial distribution optimized for Sawai Mansingh Stadium (Jaipur) boundary dimensions.
              </p>
            </div>
            <div className="flex items-center space-x-3 text-xs">
              <span className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-rr-pink"></span>
                <span className="text-slate-700 font-medium">Auction Target / Impact (6)</span>
              </span>
              <span className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-rr-navy"></span>
                <span className="text-slate-700 font-medium">Retained Core (6)</span>
              </span>
            </div>
          </div>

          {/* Stable HTML field map with avatar markers */}
          <div className="relative w-full aspect-[16/10] sm:aspect-[16/9] max-h-[560px] rounded-xl border border-rr-navy/10 overflow-hidden bg-gradient-to-b from-rr-pink-soft via-[#fce7f3] to-[#ede9fe]">
            <svg viewBox="0 0 1000 600" className="absolute inset-0 w-full h-full" aria-hidden>
              <ellipse cx="500" cy="300" rx="470" ry="275" fill="#FDF2F8" stroke="#F9A8D4" strokeWidth="3" />
              <ellipse cx="500" cy="300" rx="270" ry="160" fill="#FCE7F3" stroke="#F472B6" strokeWidth="2" strokeDasharray="6 6" />
              <rect x="475" y="210" width="50" height="180" rx="4" fill="#FEF3C7" stroke="#FDE68A" strokeWidth="2" />
              <line x1="480" y1="225" x2="520" y2="225" stroke="#D97706" strokeWidth="3" />
              <line x1="480" y1="375" x2="520" y2="375" stroke="#D97706" strokeWidth="3" />
              <line x1="470" y1="235" x2="530" y2="235" stroke="#FFFFFF" strokeWidth="2" />
              <line x1="470" y1="365" x2="530" y2="365" stroke="#FFFFFF" strokeWidth="2" />
            </svg>

            {playingXI.map((p) => {
              const isScouted = p.type.includes('Target') || p.type.includes('Impact');
              return (
                <div
                  key={p.slot}
                  className="absolute z-10 flex flex-col items-center -translate-x-1/2 -translate-y-1/2"
                  style={{ left: `${p.x}%`, top: `${p.y}%` }}
                  title={`${p.name} · ${p.role}`}
                >
                  <div
                    className={`relative rounded-full p-0.5 shadow-lg ${
                      isScouted ? 'bg-rr-pink ring-2 ring-rr-pink' : 'bg-rr-navy ring-2 ring-white/90'
                    }`}
                  >
                    <PlayerAvatar playerId={p.playerId} name={p.name} size="sm" ring={false} />
                    <span
                      className={`absolute -bottom-1 -right-1 w-5 h-5 rounded-full text-[9px] font-black flex items-center justify-center border border-white ${
                        isScouted ? 'bg-rr-pink text-white' : 'bg-rr-navy text-white'
                      }`}
                    >
                      {p.slot === 'Sub' ? 'S' : p.slot}
                    </span>
                  </div>
                  <span
                    className={`mt-1 max-w-[88px] truncate px-1.5 py-0.5 rounded text-[10px] font-bold text-white shadow-sm ${
                      isScouted ? 'bg-rr-pink' : 'bg-rr-navy/90'
                    }`}
                  >
                    {p.shortName}
                  </span>
                </div>
              );
            })}
          </div>

          <p className="text-[11px] text-slate-500 text-center">
            Numbered markers show the projected XI. Pink markers are auction recruits addressing RR structural voids; navy markers are retained core.
          </p>
        </div>
      )}

      {activeTab === 'lineup' && (
        <div className="glass-panel p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
            <div>
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
                <Users className="w-4 h-4 text-rr-pink" />
                <span>Projected RR 2027 Playing XI & Impact Substitution</span>
              </h2>
              <p className="text-[11px] text-slate-500">
                12-Man tactical sheet integrating elite auction targets with retained core.
              </p>
            </div>
            <span className="text-xs font-mono text-rr-pink-deep bg-rr-pink-soft px-2.5 py-0.5 rounded border border-rr-pink-border font-semibold">
              Balanced Left/Right & Seam/Spin Ratios
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {playingXI.map((item) => {
              const isScouted = item.type.includes('Target') || item.type.includes('Impact');
              return (
                <div
                  key={item.slot}
                  className={`rounded-xl p-3.5 space-y-2.5 transition-all border ${
                    isScouted
                      ? 'bg-rr-pink-soft/60 border-rr-pink-border'
                      : 'bg-white/70 border-slate-200/70'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <PlayerAvatar playerId={item.playerId} name={item.name} size="md" />
                    <div className="min-w-0 flex-1">
                      <div className="flex justify-between items-center gap-2">
                        <span className="font-mono text-[10px] font-black text-slate-500">#{item.slot}</span>
                        <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
                          isScouted
                            ? 'bg-white text-rr-pink-deep border border-rr-pink-border'
                            : 'bg-slate-100 text-slate-600 border border-slate-200'
                        }`}>
                          {item.type}
                        </span>
                      </div>
                      <h4 className="font-bold text-slate-900 text-sm truncate mt-0.5">{item.name}</h4>
                    </div>
                  </div>
                  <p className="text-[11px] text-slate-600 font-medium leading-snug">{item.role}</p>
                  <div className="pt-1.5 border-t border-slate-200/60 flex justify-between items-center gap-2 text-[10px]">
                    <span className="text-slate-500 truncate">{item.pos}</span>
                    <span className="font-semibold text-rr-pink-deep shrink-0">{item.note}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeTab === 'budget' && (
        <div className="glass-panel p-5 space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
            <div>
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
                <DollarSign className="w-4 h-4 text-rr-pink" />
                <span>Rajasthan Royals IPL 2027 Auction Purse Model</span>
              </h2>
              <p className="text-[11px] text-slate-500">
                Purse modeling based on official INR 120 Cr franchise cap and retention structures.
              </p>
            </div>
            <span className="text-xs font-mono text-rr-pink-deep bg-rr-pink-soft px-2.5 py-0.5 rounded border border-rr-pink-border font-semibold">
              Available Auction Purse: INR 41.0 Cr
            </span>
          </div>

          {/* Budget Visual Progress Bars */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
              <span className="text-[10px] uppercase font-bold text-slate-500 block">Total Franchise Cap</span>
              <span className="text-xl font-black text-slate-900 font-mono">INR 120.0 Cr</span>
              <span className="text-[10px] text-slate-500 block mt-0.5">BCCI IPL 2027 Guidelines</span>
            </div>
            <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
              <span className="text-[10px] uppercase font-bold text-slate-500 block">Retained Core Deductions</span>
              <span className="text-xl font-black text-slate-700 font-mono">INR 79.0 Cr</span>
              <span className="text-[10px] text-slate-500 block mt-0.5">Samson, Jaiswal, Parag, Hetmyer, Sandeep</span>
            </div>
            <div className="bg-rr-pink-soft p-3.5 rounded-lg border border-rr-pink-border">
              <span className="text-[10px] uppercase font-bold text-rr-pink-deep block">Target Purse for Recruits</span>
              <span className="text-xl font-black text-rr-pink-deep font-mono">INR 22.0 Cr</span>
              <span className="text-[10px] text-rr-pink font-medium block mt-0.5">Leaves INR 19 Cr for squad depth</span>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-900 uppercase">Target Spend Allocation Matrix</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-700 font-bold uppercase text-[10px]">
                  <tr>
                    <th className="py-2.5 px-3">Target Recruit</th>
                    <th className="py-2.5 px-3">RR Tactical Slot</th>
                    <th className="py-2.5 px-3 text-right">Target Range</th>
                    <th className="py-2.5 px-3 text-right">Ceiling Bid</th>
                    <th className="py-2.5 px-3">Contingency Backup</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Sunil Narine (O)</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">#8 Mystery Death Anchor</td>
                    <td className="py-2 px-3 text-right text-rr-pink-deep font-bold">INR 10.0–13.0 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 15.0 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Mitchell Santner / Kuldeep Yadav</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Shashank Singh</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">#6 Clutch Finisher</td>
                    <td className="py-2 px-3 text-right text-rr-pink-deep font-bold">INR 5.5–8.0 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 9.5 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Naman Dhir / Vijay Shankar</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Rasikh Salam</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">#10 Death Wicket Machine</td>
                    <td className="py-2 px-3 text-right text-rr-pink-deep font-bold">INR 1.5–3.0 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 4.0 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Mohit Sharma / Tushar Deshpande</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Ashutosh Sharma</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">Impact Weapon Finisher</td>
                    <td className="py-2 px-3 text-right text-rr-pink-deep font-bold">INR 2.5–4.5 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 5.5 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Ramandeep Singh / Abdul Samad</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Strategic Focus Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Batting Strategy */}
        <div className="glass-panel p-5 space-y-3 ">
          <div className="flex items-center space-x-2 text-rr-pink-deep">
            <Target className="w-4 h-4 text-rr-pink" />
            <h2 className="font-bold text-xs uppercase text-slate-900 tracking-wide">
              Batting Gap: Lower-Order Death Finishing (Overs 16–20)
            </h2>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            RR's retained top order (Jaiswal, Samson, Parag) is world-class, but data highlights match volatility when chasing 12+ RRR in the final 4 overs. Our scouting model targets proven clutch finishers:
          </p>
          <div className="space-y-1.5 pt-1">
            {batters.slice(0, 5).map((b) => (
              <div
                key={b.player_id}
                onClick={() => onNavigate('player_profile', b.player_id)}
                className="p-2.5 bg-slate-50/70 border border-slate-200/60 hover:bg-rr-pink-soft/60 hover:border-rr-pink-border rounded-lg transition-all cursor-pointer group"
              >
                <div className="flex justify-between items-center gap-2">
                  <div className="flex items-center space-x-2.5 min-w-0">
                    <PlayerAvatar playerId={b.player_id} name={b.player_name} size="sm" />
                    <div className="space-y-0.5 min-w-0">
                      <span className="font-bold text-slate-900 text-xs group-hover:text-rr-pink-deep transition-colors block truncate">
                        #{b.rank} {b.player_name}
                      </span>
                      <span className="text-[10px] text-slate-500 block truncate">
                        {b.archetype || b.primary_role}
                      </span>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-xs font-mono font-bold text-rr-pink-deep block">
                      +{b.sr_uplift.toFixed(1)} SR
                    </span>
                    <span className="text-[10px] text-slate-600 font-semibold font-mono">
                      {b.target_price_inr || 'Valued Target'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bowling Strategy */}
        <div className="glass-panel p-5 space-y-3 ">
          <div className="flex items-center space-x-2 text-rr-pink-deep">
            <Shield className="w-4 h-4 text-rr-pink" />
            <h2 className="font-bold text-xs uppercase text-slate-900 tracking-wide">
              Bowling Gap: Death Restrictiveness & Choke Spin
            </h2>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            In modern 200+ T20 games, championship margins are won defending overs 16–20. At Sawai Mansingh Stadium (Jaipur), long square boundaries demand restrictive bowlers who create dot balls and choke run rates:
          </p>
          <div className="space-y-1.5 pt-1">
            {bowlers.slice(0, 5).map((bw) => (
              <div
                key={bw.player_id}
                onClick={() => onNavigate('player_profile', bw.player_id)}
                className="p-2.5 bg-slate-50/70 border border-slate-200/60 hover:bg-rr-pink-soft/60 hover:border-rr-pink-border rounded-lg transition-all cursor-pointer group"
              >
                <div className="flex justify-between items-center gap-2">
                  <div className="flex items-center space-x-2.5 min-w-0">
                    <PlayerAvatar playerId={bw.player_id} name={bw.player_name} size="sm" />
                    <div className="space-y-0.5 min-w-0">
                      <span className="font-bold text-slate-900 text-xs group-hover:text-rr-pink-deep transition-colors block truncate">
                        #{bw.rank} {bw.player_name}
                      </span>
                      <span className="text-[10px] text-slate-500 block truncate">
                        {bw.archetype || bw.primary_role}
                      </span>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-xs font-mono font-bold text-rr-pink-deep block">
                      {bw.death_pressure_economy.toFixed(2)} Death Econ
                    </span>
                    <span className="text-[10px] text-slate-600 font-semibold font-mono">
                      {bw.target_price_inr || 'Valued Target'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* War Room Acquisition Bidding Strategies */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass-panel border-rr-pink/25 p-5 space-y-3 ">
          <div className="flex items-center space-x-2 text-rr-pink-deep">
            <Sparkles className="w-4 h-4 text-rr-pink" />
            <h3 className="font-bold text-xs uppercase tracking-wide text-slate-900">
              The 'Vignesh Puthur' Stealth Value Strategy
            </h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Target high-performing domestic gems before market bidding inflates their cost. This mirrors RR's successful Season 1 signing of Vignesh Puthur:
          </p>
          <ul className="space-y-1.5 text-xs text-slate-700 pt-1 font-mono">
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Shashank Singh:</strong> #6 Finisher (+69.2 SR)</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 5.5–8.0 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Ashutosh Sharma:</strong> Crisis 360-Hitter (+79.1 SR)</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 2.5–4.5 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Rasikh Salam:</strong> Death Seamer (10.6 BpW)</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 1.5–3.0 Cr</span>
            </li>
            <li className="flex justify-between pb-0.5 font-sans">
              <span><strong>Matheesha Pathirana:</strong> Death Seam (Auction Official)</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 5.0–8.0 Cr</span>
            </li>
          </ul>
          <div className="bg-rr-pink-soft/60 p-2.5 rounded border border-rr-pink-border text-[11px] text-rr-pink-deep font-medium font-sans">
            <strong>War Room Impact:</strong> Secures 4 Auction Official clutch targets for ~INR 16–20 Cr, preserving purse for marquee rounds. (0% IPL Global names stay off this list.)
          </div>
        </div>

        <div className="glass-panel p-5 space-y-3 ">
          <div className="flex items-center space-x-2 text-slate-900">
            <Briefcase className="w-4 h-4 text-rr-pink" />
            <h3 className="font-bold text-xs uppercase tracking-wide text-slate-900">
              Elite Anchor & Championship Closer Strategy
            </h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Deploy heavyweight purse reserves to guarantee game-changing match winners in marquee rounds:
          </p>
          <ul className="space-y-1.5 text-xs text-slate-700 pt-1 font-mono">
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Sunil Narine:</strong> Global Death Choke Anchor</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 10.0–13.0 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Rohit Sharma:</strong> Powerplay Crisis Aggressor</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 12.0–16.0 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Jasprit Bumrah:</strong> Pace Benchmark</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 18.0–22.0 Cr</span>
            </li>
            <li className="flex justify-between pb-0.5 font-sans">
              <span><strong>Rinku Singh:</strong> Ultimate Chase Finisher</span>
              <span className="text-rr-pink-deep font-mono font-bold">INR 9.0–13.0 Cr</span>
            </li>
          </ul>
          <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-[11px] text-slate-700 font-medium font-sans">
            <strong>War Room Impact:</strong> Guarantees Rajasthan an untouchable bowling clamp or fear-inducing batting lineup for the 2027-2029 IPL cycle.
          </div>
        </div>
      </div>
    </div>
  );
};
