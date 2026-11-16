import React, { useState, useEffect } from 'react';
import { PageId, MetaPackage, BatterRecord, BowlerRecord, PressureSummary } from './types';
import { 
  fetchMeta, 
  fetchTop10Batters, 
  fetchTop10Bowlers, 
  fetchPressureSummary 
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
  const [pressureSummary, setPressureSummary] = useState<PressureSummary | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [metaData, battersData, bowlersData, summaryData] = await Promise.all([
          fetchMeta(),
          fetchTop10Batters(),
          fetchTop10Bowlers(),
          fetchPressureSummary()
        ]);
        setMeta(metaData);
        setBatters(battersData);
        setBowlers(bowlersData);
        setPressureSummary(summaryData);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
        setError('Failed to load analytics data packages. Ensure run_pipeline.py has generated public/data JSON files.');
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
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-emerald-600 selection:text-white">
      {/* Navbar Header */}
      <Navbar
        currentPage={currentPage}
        onNavigate={handleNavigate}
        freezeSha={meta?.freeze_sha256}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-32 space-y-4">
            <Loader2 className="w-10 h-10 text-emerald-700 animate-spin" />
            <p className="text-sm font-semibold text-slate-600">Initializing Royals War Room Intelligence...</p>
          </div>
        ) : error ? (
          <div className="p-6 bg-rose-50 border border-rose-200 rounded-xl flex items-center space-x-3 text-rose-800 my-12">
            <AlertCircle className="w-6 h-6 flex-shrink-0 text-rose-600" />
            <p className="text-sm">{error}</p>
          </div>
        ) : (
          <>
            {currentPage === 'command_centre' && (
              <CommandCentre
                meta={meta}
                batters={batters}
                bowlers={bowlers}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'batters' && (
              <BatterIntelligence
                batters={batters}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'bowlers' && (
              <BowlerIntelligence
                bowlers={bowlers}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'pressure_lab' && (
              <PressureLab summary={pressureSummary} />
            )}
            {currentPage === 'player_profile' && (
              <PlayerProfile
                playerId={selectedPlayerId}
                batters={batters}
                bowlers={bowlers}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'auction_room' && (
              <AuctionRoom
                batters={batters}
                bowlers={bowlers}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'methodology' && <Methodology />}
            {currentPage === 'about' && <About meta={meta} />}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-8 text-xs text-slate-500 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 rounded bg-emerald-900 flex items-center justify-center font-black text-xs text-white">
              RR
            </div>
            <span className="font-bold text-slate-800 tracking-wide uppercase">
              PressurePulse • SupeRR Selector Season 2
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-slate-600 font-medium">Rajasthan Royals × Unstop Challenge</span>
            <span>•</span>
            <span className="font-mono text-[11px] text-slate-500 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
              SHA256: {meta?.freeze_sha256 ? meta.freeze_sha256.slice(0, 12) : '5cdd7b74'}...
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
