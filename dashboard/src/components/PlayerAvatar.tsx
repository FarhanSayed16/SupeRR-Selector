import React, { useState } from 'react';
import { getPlayerImageSrc } from '../lib/images';

interface PlayerAvatarProps {
  playerId: number;
  name: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  ring?: boolean;
}

const sizeMap = {
  xs: 'w-7 h-7 text-[10px]',
  sm: 'w-10 h-10 text-xs',
  md: 'w-12 h-12 text-sm',
  lg: 'w-16 h-16 text-lg',
  xl: 'w-24 h-24 text-2xl',
};

function initials(name: string): string {
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export const PlayerAvatar: React.FC<PlayerAvatarProps> = ({
  playerId,
  name,
  size = 'md',
  className = '',
  ring = true,
}) => {
  const [failed, setFailed] = useState(false);
  const src = getPlayerImageSrc(playerId);

  const shell = `${sizeMap[size]} rounded-full overflow-hidden bg-rr-navy/10 flex items-center justify-center shrink-0 ${
    ring ? 'ring-2 ring-white/90 shadow-md' : 'shadow-none'
  } ${className}`;

  if (!src || failed) {
    return (
      <div className={shell} title={name} aria-label={name}>
        <span className="font-black text-rr-pink-deep">{initials(name)}</span>
      </div>
    );
  }

  return (
    <div className={shell} title={name}>
      <img
        src={src}
        alt={name}
        className="w-full h-full object-cover object-top"
        loading="lazy"
        onError={() => setFailed(true)}
      />
    </div>
  );
};
