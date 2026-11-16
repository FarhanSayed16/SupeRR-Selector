import React, { useState } from 'react';
import { PageId, BatterRecord, BowlerRecord } from '../types';
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
    { slot: '1', name: 'Yashasvi Jaiswal', role: 'LH Explosive Opener', type: 'Retained Core', pos: 'Deep Extra Cover', x: 28, y: 32, note: 'Top-Order Firepower' },
    { slot: '2', name: 'Rohit Sharma (Scouted)', role: 'Powerplay Enforcer (183.4 SR)', type: 'Auction Target #1', pos: 'Slip / Mid-Wicket', x: 42, y: 25, note: '+52.1 SR Uplift Target' },
    { slot: '3', name: 'Sanju Samson (C/WK)', role: 'Captain & Anchor', type: 'Retained Core', pos: 'Wicketkeeper', x: 50, y: 76, note: 'Tactical Anchor' },
    { slot: '4', name: 'Riyan Parag', role: 'Spin Dominator & Middle Overs', type: 'Retained Core', pos: 'Long-off / Cover', x: 68, y: 30, note: 'Middle Overs Spine' },
    { slot: '5', name: 'Shimron Hetmyer (O)', role: 'LH Death Finisher', type: 'Retained Core', pos: 'Deep Square Leg', x: 74, y: 65, note: 'Boundary Hitter' },
    { slot: '6', name: 'Shashank Singh (Scouted)', role: 'Clutch Finisher (+69.2 Uplift)', type: 'Auction Target #2', pos: 'Long-on', x: 56, y: 20, note: '171.8 Pressure SR' },
    { slot: '7', name: 'Dhruv Jurel', role: 'Clutch WK/Finisher', type: 'Retained Core', pos: 'Point', x: 30, y: 55, note: 'Pressure Adaptability' },
    { slot: '8', name: 'Sunil Narine (O) (Scouted)', role: 'Mystery Choke (6.06 Death Econ)', type: 'Auction Target #1', pos: 'Short 3rd / Mid-off', x: 38, y: 65, note: 'All-Phase Restrictor' },
    { slot: '9', name: 'Sandeep Sharma', role: 'Death Knuckle Specialist', type: 'Retained Core', pos: 'Mid-on', x: 48, y: 38, note: 'Defensive Seam Anchor' },
    { slot: '10', name: 'Rasikh Salam (Scouted)', role: 'Death Wicket Machine (10.6 BpW)', type: 'Auction Target #7', pos: 'Deep Fine Leg', x: 66, y: 80, note: 'Strike Seamer' },
    { slot: '11', name: 'Kuldeep Yadav (Scouted)', role: 'Attacking Wrist Spin', type: 'Auction Target #5', pos: 'Deep Mid-Wicket', x: 80, y: 46, note: 'Middle Wicket Threat' },
    { slot: 'Sub', name: 'Ashutosh Sharma (Scouted)', role: 'Impact Finisher (+79.1 Uplift)', type: 'Impact Sub Target', pos: 'Dugout Impact Weapon', x: 15, y: 85, note: 'Crisis 360-Hitter' }
  ];

  return (
    <div className="space-y-6 pb-12 font-sans">
      {/* Header */}
      <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center space-x-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <span>Rajasthan Royals War Room</span>
              <span>•</span>
              <span className="text-emerald-800">Recruitment Strategy</span>
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
                  ? 'bg-white text-emerald-900 font-bold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Field & Pitch View
            </button>
            <button
              onClick={() => setActiveTab('lineup')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                activeTab === 'lineup'
                  ? 'bg-white text-emerald-900 font-bold shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Squad Cards
            </button>
            <button
              onClick={() => setActiveTab('budget')}
              className={`px-3 py-1 rounded-md transition-all cursor-pointer ${
                activeTab === 'budget'
                  ? 'bg-white text-emerald-900 font-bold shadow-xs'
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
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
                <Compass className="w-4 h-4 text-emerald-700" />
                <span>Tactical Field Map: Projected RR 2027 Playing XI</span>
              </h2>
              <p className="text-[11px] text-slate-500">
                Spatial distribution optimized for Sawai Mansingh Stadium (Jaipur) boundary dimensions.
              </p>
            </div>
            <div className="flex items-center space-x-3 text-xs">
              <span className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                <span className="text-slate-700 font-medium">Scouted Auction Target (5)</span>
              </span>
              <span className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
                <span className="text-slate-700 font-medium">Retained Core (6)</span>
              </span>
            </div>
          </div>

          {/* SVG Cricket Ground Graphic */}
          <div className="relative w-full aspect-[16/10] sm:aspect-[16/9] max-h-[520px] bg-emerald-950/5 rounded-xl border border-emerald-900/10 overflow-hidden flex items-center justify-center p-4">
            {/* Outfield Grass SVG */}
            <svg viewBox="0 0 1000 600" className="w-full h-full drop-shadow-xs">
              {/* Outer boundary oval */}
              <ellipse cx="500" cy="300" rx="470" ry="275" fill="#ECFDF5" stroke="#A7F3D0" strokeWidth="3" />
              {/* 30-yard inner circle */}
              <ellipse cx="500" cy="300" rx="270" ry="160" fill="#F0FDF4" stroke="#6EE7B7" strokeWidth="2" strokeDasharray="6 6" />
              {/* Pitch strip in center */}
              <rect x="475" y="210" width="50" height="180" rx="4" fill="#FEF3C7" stroke="#FDE68A" strokeWidth="2" />
              {/* Stumps lines */}
              <line x1="480" y1="225" x2="520" y2="225" stroke="#D97706" strokeWidth="3" />
              <line x1="480" y1="375" x2="520" y2="375" stroke="#D97706" strokeWidth="3" />
              {/* Crease markings */}
              <line x1="470" y1="235" x2="530" y2="235" stroke="#FFFFFF" strokeWidth="2" />
              <line x1="470" y1="365" x2="530" y2="365" stroke="#FFFFFF" strokeWidth="2" />

              {/* Position Markers */}
              {playingXI.map((p, idx) => {
                const isScouted = p.type.includes('Scouted') || p.type.includes('Target');
                const posX = (p.x / 100) * 1000;
                const posY = (p.y / 100) * 600;

                return (
                  <g key={idx} className="cursor-pointer group">
                    <circle 
                      cx={posX} 
                      cy={posY} 
                      r={isScouted ? "16" : "14"} 
                      fill={isScouted ? "#064E3B" : "#334155"} 
                      stroke="#FFFFFF" 
                      strokeWidth="2.5"
                      className="filter drop-shadow-sm transition-transform group-hover:scale-125"
                    />
                    <text 
                      x={posX} 
                      y={posY + 4} 
                      textAnchor="middle" 
                      fill="#FFFFFF" 
                      fontSize="10" 
                      fontWeight="bold" 
                      fontFamily="JetBrains Mono"
                    >
                      {p.slot}
                    </text>
                    {/* Tooltip Tag */}
                    <g className="transition-opacity">
                      <rect 
                        x={posX - 70} 
                        y={posY - 32} 
                        width="140" 
                        height="20" 
                        rx="4" 
                        fill={isScouted ? "#064E3B" : "#1E293B"} 
                        opacity="0.9"
                      />
                      <text 
                        x={posX} 
                        y={posY - 18} 
                        textAnchor="middle" 
                        fill="#FFFFFF" 
                        fontSize="9" 
                        fontWeight="600"
                      >
                        {p.name.split(' (')[0]}
                      </text>
                    </g>
                  </g>
                );
              })}
            </svg>
          </div>

          <p className="text-[11px] text-slate-500 italic text-center">
            *Numbered tokens represent projected playing formation. Green tokens indicate high-pressure auction recruits addressing structural voids.
          </p>
        </div>
      )}

      {activeTab === 'lineup' && (
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
            <div>
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
                <Users className="w-4 h-4 text-emerald-700" />
                <span>Projected RR 2027 Playing XI & Impact Substitution</span>
              </h2>
              <p className="text-[11px] text-slate-500">
                12-Man tactical sheet integrating elite auction targets with retained core.
              </p>
            </div>
            <span className="text-xs font-mono text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200 font-semibold">
              Balanced Left/Right & Seam/Spin Ratios
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {playingXI.map((item, idx) => {
              const isScouted = item.type.includes('Scouted') || item.type.includes('Target');
              return (
                <div 
                  key={idx} 
                  className={`rounded-lg p-3 space-y-1.5 transition-all border ${
                    isScouted 
                      ? 'bg-emerald-50/60 border-emerald-300' 
                      : 'bg-slate-50/70 border-slate-200/70'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs font-black text-slate-900">Slot #{item.slot}</span>
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                      isScouted 
                        ? 'bg-emerald-200/60 text-emerald-900 border border-emerald-300' 
                        : 'bg-white text-slate-600 border border-slate-200'
                    }`}>
                      {item.type}
                    </span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-xs">{item.name}</h4>
                  <p className="text-[10px] text-slate-600 font-medium">{item.role}</p>
                  <div className="pt-1 border-t border-slate-200/50 flex justify-between items-center text-[10px]">
                    <span className="text-slate-500 font-mono">{item.pos}</span>
                    <span className="font-semibold text-emerald-800">{item.note}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeTab === 'budget' && (
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
            <div>
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide flex items-center space-x-2">
                <DollarSign className="w-4 h-4 text-emerald-700" />
                <span>Rajasthan Royals IPL 2027 Auction Purse Model</span>
              </h2>
              <p className="text-[11px] text-slate-500">
                Purse modeling based on official INR 120 Cr franchise cap and retention structures.
              </p>
            </div>
            <span className="text-xs font-mono text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200 font-semibold">
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
            <div className="bg-emerald-50 p-3.5 rounded-lg border border-emerald-200">
              <span className="text-[10px] uppercase font-bold text-emerald-800 block">Target Purse for Recruits</span>
              <span className="text-xl font-black text-emerald-900 font-mono">INR 22.0 Cr</span>
              <span className="text-[10px] text-emerald-700 font-medium block mt-0.5">Leaves INR 19 Cr for squad depth</span>
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
                    <td className="py-2 px-3 text-right text-emerald-800 font-bold">INR 10.0–13.0 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 15.0 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Mitchell Santner / Mohammad Nawaz</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Shashank Singh</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">#6 Clutch Finisher</td>
                    <td className="py-2 px-3 text-right text-emerald-800 font-bold">INR 5.5–8.0 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 9.5 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Naman Dhir / Vijay Shankar</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Rasikh Salam</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">#10 Death Wicket Machine</td>
                    <td className="py-2 px-3 text-right text-emerald-800 font-bold">INR 1.5–3.0 Cr</td>
                    <td className="py-2 px-3 text-right text-slate-900">INR 4.0 Cr</td>
                    <td className="py-2 px-3 text-slate-500 font-sans">Mohit Sharma / Tushar Deshpande</td>
                  </tr>
                  <tr className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-bold text-slate-900">Ashutosh Sharma</td>
                    <td className="py-2 px-3 text-slate-600 font-sans">Impact Weapon Finisher</td>
                    <td className="py-2 px-3 text-right text-emerald-800 font-bold">INR 2.5–4.5 Cr</td>
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
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-emerald-900">
            <Target className="w-4 h-4 text-emerald-700" />
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
                className="p-2.5 bg-slate-50/70 border border-slate-200/60 hover:bg-emerald-50/50 hover:border-emerald-300 rounded-lg transition-all cursor-pointer group"
              >
                <div className="flex justify-between items-center">
                  <div className="space-y-0.5">
                    <span className="font-bold text-slate-900 text-xs group-hover:text-emerald-800 transition-colors">
                      #{b.rank} {b.player_name}
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      {b.archetype || b.primary_role}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-mono font-bold text-emerald-800 block">
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
        <div className="bg-white border border-slate-200/90 rounded-xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-emerald-900">
            <Shield className="w-4 h-4 text-emerald-700" />
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
                className="p-2.5 bg-slate-50/70 border border-slate-200/60 hover:bg-emerald-50/50 hover:border-emerald-300 rounded-lg transition-all cursor-pointer group"
              >
                <div className="flex justify-between items-center">
                  <div className="space-y-0.5">
                    <span className="font-bold text-slate-900 text-xs group-hover:text-emerald-800 transition-colors">
                      #{bw.rank} {bw.player_name}
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      {bw.archetype || bw.primary_role}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-mono font-bold text-emerald-800 block">
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
        <div className="bg-white border border-emerald-200 rounded-xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-emerald-800">
            <Sparkles className="w-4 h-4 text-emerald-700" />
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
              <span className="text-emerald-800 font-mono font-bold">INR 5.5–8.0 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Ashutosh Sharma:</strong> Crisis 360-Hitter (+79.1 SR)</span>
              <span className="text-emerald-800 font-mono font-bold">INR 2.5–4.5 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Rasikh Salam:</strong> Death Seamer (10.6 BpW)</span>
              <span className="text-emerald-800 font-mono font-bold">INR 1.5–3.0 Cr</span>
            </li>
            <li className="flex justify-between pb-0.5 font-sans">
              <span><strong>Sufiyan Muqeem:</strong> Mystery Wrist Spin (56.2% dots)</span>
              <span className="text-emerald-800 font-mono font-bold">INR 1.0–2.5 Cr</span>
            </li>
          </ul>
          <div className="bg-emerald-50/60 p-2.5 rounded border border-emerald-200 text-[11px] text-emerald-900 font-medium font-sans">
            <strong>War Room Impact:</strong> Secures 4 elite clutch match-winners for ~INR 14 Cr total, leaving 85% of RR's auction purse for marquee bidding.
          </div>
        </div>

        <div className="bg-white border border-slate-200/90 rounded-xl p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-slate-900">
            <Briefcase className="w-4 h-4 text-emerald-700" />
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
              <span className="text-emerald-800 font-mono font-bold">INR 10.0–13.0 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Rohit Sharma:</strong> Powerplay Crisis Aggressor</span>
              <span className="text-emerald-800 font-mono font-bold">INR 12.0–16.0 Cr</span>
            </li>
            <li className="flex justify-between border-b border-slate-100 pb-1 font-sans">
              <span><strong>Jasprit Bumrah:</strong> Pace Benchmark</span>
              <span className="text-emerald-800 font-mono font-bold">INR 18.0–22.0 Cr</span>
            </li>
            <li className="flex justify-between pb-0.5 font-sans">
              <span><strong>Rinku Singh:</strong> Ultimate Chase Finisher</span>
              <span className="text-emerald-800 font-mono font-bold">INR 9.0–13.0 Cr</span>
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
