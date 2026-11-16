import React from 'react';

export const ConfidenceBadge: React.FC<{ level: 'High' | 'Medium' | 'Low' }> = ({ level }) => {
  if (level === 'High') {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
        HIGH SAMPLE
      </span>
    );
  }
  if (level === 'Medium') {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
        MED SAMPLE
      </span>
    );
  }
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200">
      LOW SAMPLE
    </span>
  );
};
