import React from 'react';

export const Medal: React.FC<{ rank: number }> = ({ rank }) => {
  if (rank === 1) {
    return (
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-rr-gold-soft text-amber-900 font-black text-xs shadow-sm border border-rr-gold/40">
        1
      </span>
    );
  }
  if (rank === 2) {
    return (
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-white/90 text-rr-navy font-black text-xs shadow-sm border border-slate-200">
        2
      </span>
    );
  }
  if (rank === 3) {
    return (
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-orange-50 text-orange-900 font-black text-xs shadow-sm border border-orange-200">
        3
      </span>
    );
  }
  return (
    <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-white/70 text-ink-700 font-bold text-xs border border-white/90">
      {rank}
    </span>
  );
};
