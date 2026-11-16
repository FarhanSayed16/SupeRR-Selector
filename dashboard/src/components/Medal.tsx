import React from 'react';

export const Medal: React.FC<{ rank: number }> = ({ rank }) => {
  if (rank === 1) {
    return (
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-amber-100 text-amber-900 font-black text-xs shadow-xs border border-amber-300">
        1
      </span>
    );
  }
  if (rank === 2) {
    return (
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-slate-100 text-slate-800 font-black text-xs shadow-xs border border-slate-300">
        2
      </span>
    );
  }
  if (rank === 3) {
    return (
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-orange-100 text-orange-900 font-black text-xs shadow-xs border border-orange-300">
        3
      </span>
    );
  }
  return (
    <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-slate-50 text-slate-700 font-bold text-xs border border-slate-200">
      {rank}
    </span>
  );
};
