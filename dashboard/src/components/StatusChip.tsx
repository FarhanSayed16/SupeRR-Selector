import React from 'react';

interface StatusChipProps {
  label: string;
  pulse?: boolean;
  className?: string;
}

export const StatusChip: React.FC<StatusChipProps> = ({
  label,
  pulse = true,
  className = '',
}) => (
  <span className={`status-chip ${className}`}>
    {pulse && <span className="status-chip-dot" aria-hidden />}
    {label}
  </span>
);
