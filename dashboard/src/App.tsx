import React, { useState, useEffect } from 'react';
import {
  PageId,
  MetaPackage,
  BatterRecord,
  BowlerRecord,
  PressureSummary,
  ExcludedPlayer,
  PlayerIndexItem,
  PlayerDetailMap,
  ScoutBoard,
} from './types';
import {
  fetchMeta,
  fetchTop10Batters,
  fetchTop10Bowlers,
  fetchFullBatters,
  fetchFullBowlers,
  fetchFullGlobalBatters,
  fetchFullGlobalBowlers,
  fetchExcludedLowIpl,
  fetchPressureSummary,
  fetchPlayersIndex,
  fetchPlayersDetail,
  fetchScoutBoard,
} from './lib/data';
import { Navbar } from './components/Navbar';
import { CommandCentre } from './pages/CommandCentre';
import { BatterIntelligence } from './pages/BatterIntelligence';
import { BowlerIntelligence } from './pages/BowlerIntelligence';
import { PressureLab } from './pages/PressureLab';
import { PlayerProfile } from './pages/PlayerProfile';
import { AuctionRoom } from './pages/AuctionRoom';
import { Methodology } from './pages/Methodology';
import { About } from './pages/About';
import { Loader2, AlertCircle } from 'lucide-react';

export function App() {
  const [currentPage, setCurrentPage] = useState<PageId>('command_centre');
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);

  const [meta, setMeta] = useState<MetaPackage | null>(null);
  const [batters, setBatters] = useState<BatterRecord[]>([]);
  const [bowlers, setBowlers] = useState<BowlerRecord[]>([]);
  const [fullBatters, setFullBatters] = useState<BatterRecord[]>([]);
  const [fullBowlers, setFullBowlers] = useState<BowlerRecord[]>([]);
  const [globalBatters, setGlobalBatters] = useState<BatterRecord[]>([]);
  const [globalBowlers, setGlobalBowlers] = useState<BowlerRecord[]>([]);
  const [excluded, setExcluded] = useState<ExcludedPlayer[]>([]);
  const [pressureSummary, setPressureSummary] = useState<PressureSummary | null>(null);
  const [playerIndex, setPlayerIndex] = useState<PlayerIndexItem[]>([]);
  const [playerDetails, setPlayerDetails] = useState<PlayerDetailMap>({});
  const [scoutBoard, setScoutBoard] = useState<ScoutBoard | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [
          metaData,
          battersData,
          bowlersData,
          fullBat,
          fullBowl,
          globalBat,
          globalBowl,
          excludedData,
          summaryData,
          indexData,
          detailData,
          scoutData,
        ] = await Promise.all([
          fetchMeta(),
          fetchTop10Batters(),
          fetchTop10Bowlers(),
          fetchFullBatters(),
          fetchFullBowlers(),
          fetchFullGlobalBatters(),
          fetchFullGlobalBowlers(),
          fetchExcludedLowIpl(),
          fetchPressureSummary(),
          fetchPlayersIndex(),
          fetchPlayersDetail(),
          fetchScoutBoard(),
        ]);
        setMeta(metaData);
        setBatters(battersData);
        setBowlers(bowlersData);
        setFullBatters(fullBat);
        setFullBowlers(fullBowl);
        setGlobalBatters(globalBat);
        setGlobalBowlers(globalBowl);
        setExcluded(excludedData);
        setPressureSummary(summaryData);
        setPlayerIndex(indexData);
        setPlayerDetails(detailData);
        setScoutBoard(scoutData);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
        setError(
          'Failed to load analytics data packages. Ensure run_pipeline.py has generated public/data JSON files.'
        );
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleNavigate = (page: PageId, playerId?: number) => {
    if (playerId !== undefined) {
      setSelectedPlayerId(playerId);
    }
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen text-rr-navy flex flex-col font-sans">
      <Navbar
        currentPage={currentPage}
        onNavigate={handleNavigate}
        freezeSha={meta?.freeze_sha256}
        playerIndex={playerIndex}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 pt-4 pb-4">
        {loading ? (
          <div className="glass-panel flex flex-col items-center justify-center py-32 space-y-4 page-enter">
            <Loader2 className="w-10 h-10 text-rr-pink animate-spin" />
            <p className="text-sm font-semibold text-ink-500">
              Initializing Royals Pressure Intelligence…
            </p>
          </div>
        ) : error ? (
          <div className="glass-panel p-6 flex items-center space-x-3 text-rose-800 my-8 page-enter">
            <AlertCircle className="w-6 h-6 flex-shrink-0 text-rose-600" />
            <p className="text-sm">{error}</p>
          </div>
        ) : (
          <div key={currentPage} className="page-enter">
            {currentPage === 'command_centre' && (
              <CommandCentre
                meta={meta}
                batters={batters}
                bowlers={bowlers}
                scoutBoard={scoutBoard}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'batters' && (
              <BatterIntelligence
                batters={fullBatters}
                globalBatters={globalBatters}
                excluded={excluded}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'bowlers' && (
              <BowlerIntelligence
                bowlers={fullBowlers}
                globalBowlers={globalBowlers}
                excluded={excluded}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'pressure_lab' && (
              <PressureLab summary={pressureSummary} meta={meta} />
            )}
            {currentPage === 'player_profile' && (
              <PlayerProfile
                playerId={selectedPlayerId}
                batters={fullBatters}
                bowlers={fullBowlers}
                details={playerDetails}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'auction_room' && (
              <AuctionRoom batters={batters} bowlers={bowlers} onNavigate={handleNavigate} />
            )}
            {currentPage === 'methodology' && <Methodology meta={meta} />}
            {currentPage === 'about' && <About meta={meta} />}
          </div>
        )}
      </main>

      <footer className="px-3 sm:px-4 pb-6">
        <div className="glass-nav max-w-7xl mx-auto rounded-2xl py-5 px-4 sm:px-6 text-xs text-ink-500">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center space-x-2.5">
              <img
                src="/assets/brand/rr-mark-pink.svg"
                alt="Rajasthan Royals"
                className="h-8 w-8 object-contain"
              />
              <span className="font-bold text-rr-navy tracking-wide uppercase">
                PressurePulse · SupeRR Selector Season 2
              </span>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1">
              <span className="font-medium">Rajasthan Royals × Unstop</span>
              <span className="text-ink-400">·</span>
              <span className="font-mono text-[11px] text-ink-500 bg-white/60 px-2 py-0.5 rounded-full border border-white/80">
                SHA256: {meta?.freeze_sha256 ? meta.freeze_sha256.slice(0, 12) : 'a819c0e65bf4'}…
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
