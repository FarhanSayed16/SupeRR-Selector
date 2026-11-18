/** Local asset helpers — images live under dashboard/public/assets */

export function getPlayerImageSrc(playerId: number | string | null | undefined): string | null {
  if (playerId === null || playerId === undefined) return null;
  return `/assets/players/${playerId}.jpg`;
}

/** Pink RR crest for light / glass surfaces (no gradient plate needed) */
export function getBrandLogoSrc(): string {
  return '/assets/brand/rr-mark-pink.svg';
}

/** White RR crest for dark / pink solid plates */
export function getBrandLogoOnDarkSrc(): string {
  return '/assets/brand/rr-logo-official.svg';
}

export function getBrandWordmarkSrc(): string {
  return '/assets/brand/rr-logo.png';
}

export function getBrandCrestSrc(): string {
  return '/assets/brand/rr-crest.png';
}

export function getBrandSocialSrc(): string {
  return '/assets/brand/rr-social-share.jpeg';
}
