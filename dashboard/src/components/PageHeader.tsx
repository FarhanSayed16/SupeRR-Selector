import React from 'react';

interface PageHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: React.ReactNode;
  badge?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  eyebrow,
  title,
  description,
  actions,
  badge,
}) => (
  <div className="glass-panel p-5 sm:p-6 space-y-3">
    <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
      <div className="space-y-1.5 min-w-0">
        {eyebrow && (
          <div className="flex flex-wrap items-center gap-2 text-[11px] font-bold text-ink-500 uppercase tracking-wider">
            <span>{eyebrow}</span>
            {badge}
          </div>
        )}
        <h1 className="text-xl sm:text-2xl font-black text-rr-navy tracking-tight">
          {title}
        </h1>
        {description && (
          <p className="text-xs sm:text-sm text-ink-500 leading-relaxed max-w-3xl">
            {description}
          </p>
        )}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2 shrink-0">{actions}</div>}
    </div>
  </div>
);
