import React from 'react';
import { PageId, PlayerIndexItem } from '../types';
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
import { PlayerSearch } from './PlayerSearch';
import { getBrandLogoSrc } from '../lib/images';

interface NavbarProps {
  currentPage: PageId;
  onNavigate: (page: PageId, playerId?: number) => void;
  freezeSha?: string;
  playerIndex?: PlayerIndexItem[];
}

const iconProps = { className: 'w-4 h-4', strokeWidth: 2.25 as const };

export const Navbar: React.FC<NavbarProps> = ({
  currentPage,
  onNavigate,
  freezeSha,
  playerIndex = [],
}) => {
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
      <div className="glass-nav max-w-7xl mx-auto rounded-2xl px-3 sm:px-4">
        <div className="flex items-center gap-2 sm:gap-3 min-h-14 py-2">
          <div
            className="flex items-center gap-2.5 cursor-pointer group shrink-0"
            onClick={() => onNavigate('command_centre')}
          >
            <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center shadow-sm border border-slate-200/80 overflow-hidden p-1.5">
              <img
                src={getBrandLogoSrc()}
                alt="Rajasthan Royals"
                className="block w-full h-full object-contain"
              />
            </div>
            <div className="hidden sm:block leading-tight">
              <div className="flex items-center gap-1.5">
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

          <nav className="hidden xl:flex items-center gap-0.5 bg-white/45 p-1 rounded-full border border-white/70 mx-auto">
            {navItems.map((item) => {
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-full text-xs tracking-tight transition-all cursor-pointer whitespace-nowrap ${
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

          <div className="ml-auto flex items-center gap-2 shrink-0">
            <div className="hidden md:block">
              <PlayerSearch index={playerIndex} onNavigate={onNavigate} />
            </div>
            <div className="hidden sm:flex items-center h-8">
              <StatusChip label="Ranks Frozen" />
            </div>
            <span className="text-[10px] font-mono text-ink-500 hidden 2xl:inline">
              SHA {freezeSha ? freezeSha.slice(0, 8) : 'a819c0e6'}
            </span>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="xl:hidden p-2 rounded-xl text-rr-navy hover:bg-white/50 cursor-pointer"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" strokeWidth={2.25} /> : <Menu className="w-5 h-5" strokeWidth={2.25} />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="xl:hidden border-t border-white/50 pt-2 pb-3 space-y-1">
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
            <div className="pt-2 px-1 space-y-2">
              <PlayerSearch
                index={playerIndex}
                onNavigate={(page, id) => {
                  onNavigate(page, id);
                  setMobileMenuOpen(false);
                }}
              />
              <StatusChip label="Ranks Frozen" />
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
