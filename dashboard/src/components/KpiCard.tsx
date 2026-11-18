import React from 'react';

interface KpiCardProps {
  label: string;
  value: React.ReactNode;
  hint?: string;
  icon?: React.ReactNode;
  accent?: boolean;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  label,
  value,
  hint,
  icon,
  accent = false,
}) => (
  <div
    className={`glass-kpi p-3.5 ${accent ? 'border-rr-pink/30 ring-1 ring-rr-pink/10' : ''}`}
  >
    <div className="flex items-start justify-between gap-2">
      <span
        className={`text-[10px] uppercase font-bold tracking-wider block ${
          accent ? 'text-rr-pink' : 'text-ink-500'
        }`}
      >
        {label}
      </span>
      {icon && (
        <span className={accent ? 'text-rr-pink' : 'text-rr-navy/50'}>{icon}</span>
      )}
    </div>
    <span className="text-lg font-black text-rr-navy font-mono mt-1 block">{value}</span>
    {hint && (
      <span
        className={`text-[10px] block mt-0.5 ${
          accent ? 'text-rr-pink-deep font-medium' : 'text-ink-500'
        }`}
      >
        {hint}
      </span>
    )}
  </div>
);
