import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  strong?: boolean;
  hover?: boolean;
  onClick?: () => void;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = '',
  strong = false,
  hover = false,
  onClick,
}) => {
  const base = strong ? 'glass-panel-strong' : 'glass-panel';
  const hoverCls = hover
    ? 'transition-all duration-200 hover:-translate-y-0.5 hover:border-rr-pink/30 cursor-pointer'
    : '';
  return (
    <div className={`${base} ${hoverCls} ${className}`} onClick={onClick}>
      {children}
    </div>
  );
};

interface GlassSubcardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export const GlassSubcard: React.FC<GlassSubcardProps> = ({
  children,
  className = '',
  onClick,
}) => (
  <div className={`glass-subcard ${className}`} onClick={onClick}>
    {children}
  </div>
);
