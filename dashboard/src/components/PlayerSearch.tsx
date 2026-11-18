import React, { useMemo, useRef, useState } from 'react';
import { Search, X } from 'lucide-react';
import { PageId, PlayerIndexItem } from '../types';
import { PlayerAvatar } from './PlayerAvatar';

interface PlayerSearchProps {
  index: PlayerIndexItem[];
  onNavigate: (page: PageId, playerId?: number) => void;
}

function roleLine(p: PlayerIndexItem): string {
  if (p.is_batter && p.is_bowler) {
    return `All-rounder · Bat #${p.rank} · Bowl #${p.bowler_rank ?? '—'}`;
  }
  if (p.is_batter) return `Batter · Board #${p.rank}`;
  return `Bowler · Board #${p.rank}`;
}

export const PlayerSearch: React.FC<PlayerSearchProps> = ({ index, onNavigate }) => {
  const [q, setQ] = useState('');
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const wrapRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const hits = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (needle.length < 2) return [];
    const scored = index
      .map((p) => {
        const name = p.player_name.toLowerCase();
        const starts = name.startsWith(needle) ? 0 : name.includes(needle) ? 1 : 2;
        return { p, starts };
      })
      .filter((x) => x.starts < 2)
      .sort((a, b) => a.starts - b.starts || (a.p.rank ?? 999) - (b.p.rank ?? 999));
    return scored.slice(0, 10).map((x) => x.p);
  }, [index, q]);

  React.useEffect(() => {
    setActive(0);
  }, [q]);

  React.useEffect(() => {
    const onDoc = (e: MouseEvent) => {
      if (!wrapRef.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', onDoc);
    return () => document.removeEventListener('mousedown', onDoc);
  }, []);

  const pick = (p: PlayerIndexItem) => {
    setQ('');
    setOpen(false);
    onNavigate('player_profile', p.player_id);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!open || hits.length === 0) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActive((i) => Math.min(i + 1, hits.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      pick(hits[active] ?? hits[0]);
    } else if (e.key === 'Escape') {
      setOpen(false);
      inputRef.current?.blur();
    }
  };

  return (
    <div ref={wrapRef} className="relative w-full max-w-[240px]">
      <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5 pointer-events-none" />
      <input
        ref={inputRef}
        type="search"
        value={q}
        placeholder="Search Kohli, Dhoni…"
        onChange={(e) => {
          setQ(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKeyDown}
        className="w-full pl-8 pr-7 py-1.5 text-xs rounded-full bg-white/70 border border-white/90 text-rr-navy placeholder:text-ink-400 focus:outline-none focus:border-rr-pink focus:bg-white"
        aria-label="Search players"
        aria-autocomplete="list"
        aria-expanded={open && q.trim().length >= 2}
      />
      {q && (
        <button
          type="button"
          className="absolute right-2 top-2 text-slate-400 hover:text-rr-navy cursor-pointer"
          onClick={() => {
            setQ('');
            setOpen(false);
            inputRef.current?.focus();
          }}
          aria-label="Clear search"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}
      {open && q.trim().length >= 2 && (
        <div className="search-panel absolute right-0 left-0 sm:left-auto sm:w-[22rem] mt-2 max-h-80 overflow-y-auto z-50">
          <div className="px-3 pt-2.5 pb-1.5 border-b border-slate-100">
            <p className="type-kicker">
              {hits.length ? `${hits.length} match${hits.length === 1 ? '' : 'es'}` : 'No matches'}
            </p>
          </div>
          {hits.length === 0 ? (
            <p className="px-3 py-3 text-xs text-slate-500">
              Try a full name — only ranked board players are searchable.
            </p>
          ) : (
            hits.map((p, i) => (
              <button
                key={p.player_id}
                type="button"
                className="search-hit w-full text-left px-3 py-2.5 border-b border-slate-50 last:border-0 cursor-pointer flex items-center gap-2.5"
                aria-selected={i === active}
                onMouseEnter={() => setActive(i)}
                onClick={() => pick(p)}
              >
                <PlayerAvatar playerId={p.player_id} name={p.player_name} size="sm" ring={false} />
                <div className="min-w-0 flex-1">
                  <div className="text-[13px] font-extrabold text-slate-900 truncate tracking-tight leading-tight">
                    {p.player_name}
                  </div>
                  <div className="text-[10px] text-slate-500 font-medium mt-0.5 truncate">
                    {roleLine(p)}
                    {p.board === 'global' ? ' · Global only' : ''}
                  </div>
                </div>
                {p.pressure_score != null && (
                  <div className="text-right shrink-0">
                    <div className="font-mono text-sm font-bold text-rr-pink-deep">
                      {Number(p.pressure_score).toFixed(1)}
                    </div>
                    <div className="text-[9px] uppercase tracking-wider text-slate-400 font-semibold">
                      Score
                    </div>
                  </div>
                )}
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
};
