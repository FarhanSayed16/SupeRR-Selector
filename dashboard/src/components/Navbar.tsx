import React from 'react';
import { PageId } from '../types';
import { 
  BarChart3, 
  Target, 
  Shield, 
  Activity, 
  Users, 
  BookOpen, 
  CheckSquare,
  Info,
  Menu,
  X
} from 'lucide-react';

interface NavbarProps {
  currentPage: PageId;
  onNavigate: (page: PageId, playerId?: number) => void;
  freezeSha?: string;
}

export const Navbar: React.FC<NavbarProps> = ({ currentPage, onNavigate, freezeSha }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const navItems: { id: PageId; label: string; icon: React.ReactNode }[] = [
    { id: 'command_centre', label: 'Overview', icon: <BarChart3 className="w-3.5 h-3.5" /> },
    { id: 'batters', label: 'Batters', icon: <Target className="w-3.5 h-3.5" /> },
    { id: 'bowlers', label: 'Bowlers', icon: <Shield className="w-3.5 h-3.5" /> },
    { id: 'auction_room', label: 'RR 2027 Squad & XI', icon: <Users className="w-3.5 h-3.5" /> },
    { id: 'pressure_lab', label: 'Pressure Engine', icon: <Activity className="w-3.5 h-3.5" /> },
    { id: 'methodology', label: 'Methodology', icon: <BookOpen className="w-3.5 h-3.5" /> },
    { id: 'about', label: 'Audit & Compliance', icon: <Info className="w-3.5 h-3.5" /> },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 text-slate-800 shadow-[0_1px_2px_rgba(0,0,0,0.03)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          {/* Brand Wordmark */}
          <div 
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => onNavigate('command_centre')}
          >
            <div className="w-8 h-8 rounded bg-[#064E3B] flex items-center justify-center shadow-xs border border-emerald-900">
              <span className="font-extrabold text-xs tracking-wider text-white">RR</span>
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="font-extrabold text-sm tracking-tight text-slate-900">
                  Pressure<span className="text-emerald-700">Pulse</span>
                </span>
                <span className="text-[9px] uppercase font-bold tracking-wider bg-emerald-50 text-emerald-800 px-1.5 py-0.2 rounded border border-emerald-200">
                  v1.2 Audited
                </span>
              </div>
              <p className="text-[10px] text-slate-500 font-medium tracking-tight">
                Rajasthan Royals • IPL 2027 War Room
              </p>
            </div>
          </div>

          {/* Desktop Nav Items */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-100/80 p-0.5 rounded-lg border border-slate-200/80">
            {navItems.map((item) => {
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-semibold tracking-tight transition-all cursor-pointer ${
                    active
                      ? 'bg-white text-emerald-900 shadow-xs border border-slate-200 font-bold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/50 border border-transparent'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Status / Freeze Chip */}
          <div className="hidden lg:flex items-center space-x-2.5">
            <div className="flex items-center space-x-1.5 text-xs text-slate-500 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[11px] font-mono text-slate-700 font-semibold">
                SHA: {freezeSha ? freezeSha.slice(0, 8) : '5cdd7b74'}
              </span>
            </div>
            <span className="text-slate-300">|</span>
            <span className="text-[11px] text-slate-500 font-medium">
              200,999 Balls
            </span>
          </div>

          {/* Mobile hamburger */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-1.5 rounded-md text-slate-600 hover:text-slate-900 hover:bg-slate-100 cursor-pointer"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-3 space-y-1 shadow-lg">
          {navItems.map((item) => {
            const active = currentPage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-semibold cursor-pointer ${
                  active
                    ? 'bg-emerald-50 text-emerald-900 font-bold border border-emerald-200'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      )}
    </header>
  );
};
