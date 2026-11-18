import React from 'react';

export const ConfidenceBadge: React.FC<{ level: 'High' | 'Medium' | 'Low' }> = ({ level }) => {
  if (level === 'High') {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50/90 text-emerald-800 border border-emerald-200/80">
        HIGH SAMPLE
      </span>
    );
  }
  if (level === 'Medium') {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50/90 text-amber-800 border border-amber-200/80">
        MED SAMPLE
      </span>
    );
  }
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50/90 text-rose-800 border border-rose-200/80">
      LOW SAMPLE
    </span>
  );
};
