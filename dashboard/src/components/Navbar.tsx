import React from 'react';
import { PageId } from '../types';
import {
  LayoutDashboard,
  Crosshair,
  Shield,
  Radar,
  Shirt,
  ScrollText,
  BadgeCheck,
  Menu,
  X,
} from 'lucide-react';
import { StatusChip } from './StatusChip';
import { getBrandLogoSrc } from '../lib/images';

interface NavbarProps {
  currentPage: PageId;
  onNavigate: (page: PageId, playerId?: number) => void;
  freezeSha?: string;
}

const iconProps = { className: 'w-4 h-4', strokeWidth: 2.25 as const };

export const Navbar: React.FC<NavbarProps> = ({ currentPage, onNavigate, freezeSha }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const navItems: { id: PageId; label: string; short?: string; icon: React.ReactNode }[] = [
    { id: 'command_centre', label: 'Overview', icon: <LayoutDashboard {...iconProps} /> },
    { id: 'batters', label: 'Batters', icon: <Crosshair {...iconProps} /> },
    { id: 'bowlers', label: 'Bowlers', icon: <Shield {...iconProps} /> },
    { id: 'auction_room', label: 'RR 2027 Squad', short: 'Squad', icon: <Shirt {...iconProps} /> },
    { id: 'pressure_lab', label: 'Pressure Lab', icon: <Radar {...iconProps} /> },
    { id: 'methodology', label: 'Methodology', icon: <ScrollText {...iconProps} /> },
    { id: 'about', label: 'Audit', icon: <BadgeCheck {...iconProps} /> },
  ];

  return (
    <header className="sticky top-0 z-50 px-3 sm:px-4 pt-3 pb-2">
      <div className="glass-nav max-w-7xl mx-auto rounded-2xl px-3 sm:px-5">
        <div className="flex items-center justify-between h-14 gap-3">
          <div
            className="flex items-center space-x-3 cursor-pointer group shrink-0"
            onClick={() => onNavigate('command_centre')}
          >
            <div className="w-11 h-11 rounded-xl bg-white flex items-center justify-center shadow-sm border border-slate-200/80 overflow-hidden p-1.5">
              <img
                src={getBrandLogoSrc()}
                alt="Rajasthan Royals"
                className="w-full h-full object-contain"
              />
            </div>
            <div className="hidden sm:block">
              <div className="flex items-center space-x-1.5">
                <span className="font-extrabold text-sm tracking-tight text-rr-navy">
                  Pressure<span className="text-rr-pink">Pulse</span>
                </span>
                <span className="text-[9px] uppercase font-bold tracking-wider bg-rr-pink-soft text-rr-pink-deep px-1.5 py-0.5 rounded-full border border-rr-pink-border">
                  v1.2
                </span>
              </div>
              <p className="text-[10px] text-ink-500 font-medium tracking-tight">
                Rajasthan Royals · IPL 2027
              </p>
            </div>
          </div>

          <nav className="hidden lg:flex items-center gap-0.5 bg-white/45 p-1 rounded-full border border-white/70">
            {navItems.map((item) => {
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs tracking-tight transition-all cursor-pointer ${
                    active
                      ? 'bg-rr-pink text-white shadow-md font-bold'
                      : 'text-ink-500 hover:text-rr-navy hover:bg-white/70 font-semibold'
                  }`}
                >
                  <span className={active ? 'opacity-100' : 'opacity-80'}>{item.icon}</span>
                  <span>{item.short || item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="hidden md:flex items-center gap-2 shrink-0">
            <StatusChip label="Ranks Frozen" />
            <span className="text-[10px] font-mono text-ink-500 hidden xl:inline">
              SHA {freezeSha ? freezeSha.slice(0, 8) : '5cdd7b74'}
            </span>
          </div>

          <div className="flex lg:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-rr-navy hover:bg-white/50 cursor-pointer"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" strokeWidth={2.25} /> : <Menu className="w-5 h-5" strokeWidth={2.25} />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="lg:hidden border-t border-white/50 pt-2 pb-3 space-y-1">
            {navItems.map((item) => {
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onNavigate(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-xs cursor-pointer ${
                    active
                      ? 'bg-rr-pink text-white font-bold shadow-sm'
                      : 'text-ink-500 hover:bg-white/40 font-semibold'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              );
            })}
            <div className="pt-2 px-1">
              <StatusChip label="Ranks Frozen" />
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
