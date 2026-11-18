import {
  MetaPackage,
  BatterRecord,
  BowlerRecord,
  PlayerIndexItem,
  PressureSummary,
  MethodologyPackage,
  ExcludedPlayer,
} from '../types';

let cachedMeta: MetaPackage | null = null;
let cachedBatters: BatterRecord[] | null = null;
let cachedBowlers: BowlerRecord[] | null = null;
let cachedGlobalBatters: BatterRecord[] | null = null;
let cachedGlobalBowlers: BowlerRecord[] | null = null;
let cachedExcluded: ExcludedPlayer[] | null = null;
let cachedIndex: PlayerIndexItem[] | null = null;
let cachedDetails: Record<string, any> | null = null;
let cachedPressure: PressureSummary | null = null;
let cachedMethodology: MethodologyPackage | null = null;

export async function fetchMeta(): Promise<MetaPackage> {
  if (cachedMeta) return cachedMeta;
  const res = await fetch('/data/meta.json');
  cachedMeta = await res.json();
  return cachedMeta!;
}

export async function fetchTop10Batters(): Promise<BatterRecord[]> {
  if (cachedBatters) return cachedBatters;
  const res = await fetch('/data/top10_batters.json');
  cachedBatters = await res.json();
  return cachedBatters!;
}

export async function fetchTop10Bowlers(): Promise<BowlerRecord[]> {
  if (cachedBowlers) return cachedBowlers;
  const res = await fetch('/data/top10_bowlers.json');
  cachedBowlers = await res.json();
  return cachedBowlers!;
}

export async function fetchGlobalBatters(): Promise<BatterRecord[]> {
  if (cachedGlobalBatters) return cachedGlobalBatters;
  const res = await fetch('/data/top10_batters_global.json');
  cachedGlobalBatters = await res.json();
  return cachedGlobalBatters!;
}

export async function fetchGlobalBowlers(): Promise<BowlerRecord[]> {
  if (cachedGlobalBowlers) return cachedGlobalBowlers;
  const res = await fetch('/data/top10_bowlers_global.json');
  cachedGlobalBowlers = await res.json();
  return cachedGlobalBowlers!;
}

export async function fetchExcludedLowIpl(): Promise<ExcludedPlayer[]> {
  if (cachedExcluded) return cachedExcluded;
  const res = await fetch('/data/excluded_low_ipl_sample.json');
  cachedExcluded = await res.json();
  return cachedExcluded!;
}

export async function fetchPlayersIndex(): Promise<PlayerIndexItem[]> {
  if (cachedIndex) return cachedIndex;
  const res = await fetch('/data/players_index.json');
  cachedIndex = await res.json();
  return cachedIndex!;
}

export async function fetchPlayersDetail(): Promise<Record<string, any>> {
  if (cachedDetails) return cachedDetails;
  const res = await fetch('/data/players_detail.json');
  cachedDetails = await res.json();
  return cachedDetails!;
}

export async function fetchPressureSummary(): Promise<PressureSummary> {
  if (cachedPressure) return cachedPressure;
  const res = await fetch('/data/pressure_summary.json');
  cachedPressure = await res.json();
  return cachedPressure!;
}

export async function fetchMethodology(): Promise<MethodologyPackage> {
  if (cachedMethodology) return cachedMethodology;
  const res = await fetch('/data/methodology.json');
  cachedMethodology = await res.json();
  return cachedMethodology!;
}

export function formatScore(score: number): string {
  return score.toFixed(1);
}

export function formatRate(val: number): string {
  return val.toFixed(1);
}

export function formatUplift(val: number): string {
  return val > 0 ? `+${val.toFixed(1)}` : val.toFixed(1);
}
