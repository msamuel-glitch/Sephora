import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import './App.css';

// Module components — 15 slides
import Provocation from './components/Provocation';
import SuccessDefinition from './components/SuccessDefinition';
import SuccessHexagon from './components/SuccessHexagon';
import RevenueArbitrage from './components/RevenueArbitrage';
import BrandDNA from './components/BrandDNA';
import MetricsPanel from './components/MetricsPanel';
import GoldenBridge from './components/GoldenBridge';
import MLEngine from './components/MLEngine';
import GrowthEngines from './components/GrowthEngines';
import BrandMarket from './components/BrandMarket';
import IntegrityShield from './components/IntegrityShield';
import TacticalCommand from './components/TacticalCommand';
import MondayBrandManager from './components/MondayBrandManager';
import MondayCRM from './components/MondayCRM';
import ROIReveal from './components/ROIReveal';

const MODULES = [
  { id: 0, num: '01', label: 'Question', pillar: 'THE HOOK', title: 'Which Brand Will They Buy Next?' },
  { id: 1, num: '02', label: 'Success', pillar: 'OUR DEFINITION', title: 'The Winning Formula' },
  { id: 2, num: '03', label: 'Data', pillar: 'DATA MASTERY', title: 'Command of the Dataset' },
  { id: 3, num: '04', label: 'Explorer', pillar: 'KEY FINDING', title: 'The Explorer Effect' },
  { id: 4, num: '05', label: 'Pairs', pillar: 'DELIVERABLE', title: 'The Top 11 Pairs' },
  { id: 5, num: '06', label: 'Playbook', pillar: 'ACTIONABILITY', title: 'The Action Playbook' },
  { id: 6, num: '07', label: 'Proof', pillar: 'TRUST', title: 'The Proof Engine' },
  { id: 7, num: '08', label: 'Rules', pillar: 'TRANSITIONS', title: '894 Behavioral Rules' },
  { id: 8, num: '09', label: 'Gen Z', pillar: 'PERSONA', title: 'Gen Z: Discovery Engine' },
  { id: 9, num: '10', label: 'Boomers', pillar: 'PERSONA', title: 'Boomers: Loyalty Fortress' },
  { id: 10, num: '11', label: 'Protect LTV', pillar: 'PROTECTION', title: 'The Cost of Being Wrong' },
  { id: 11, num: '12', label: 'Strategy I', pillar: 'ACQUISITION', title: 'Deploying the Engines' },
  { id: 12, num: '13', label: 'Strategy II', pillar: 'PRESERVATION', title: 'Deploying the Shield' },
  { id: 13, num: '14', label: 'Verdict', pillar: 'BOARDROOM', title: 'The Final Verdict' },
];

const pageVariants = {
  initial: { opacity: 0, y: 20, filter: 'blur(8px)' },
  animate: { opacity: 1, y: 0, filter: 'blur(0px)' },
  exit: { opacity: 0, y: -20, filter: 'blur(8px)' },
};

export default function App() {
  const [activeModule, setActiveModule] = useState(0);

  const renderModule = () => {
    switch (activeModule) {
      case 0: return <Provocation />;
      case 1: return <SuccessDefinition />;
      case 2: return <SuccessHexagon />;
      case 3: return <RevenueArbitrage />;
      case 4: return <BrandDNA />;
      case 5: return <MetricsPanel />;
      case 6: return <GoldenBridge />;
      case 7: return <MLEngine />;
      case 8: return <GrowthEngines initialSegment="viral-acquisitors" />;
      case 9: return <GrowthEngines initialSegment="future-loyalists" />;
      case 10: return <IntegrityShield />;
      case 11: return <MondayBrandManager />;
      case 12: return <MondayCRM />;
      case 13: return <ROIReveal />;
      default: return <Provocation />;
    }
  };

  return (
    <div className="h-screen w-full flex flex-col p-6 max-w-[1700px] mx-auto overflow-hidden">
      {/* ─── Header: Beauty Editorial ─── */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }} 
        animate={{ opacity: 1, y: 0 }} 
        className="flex justify-between items-end mb-6 px-4"
      >
        <div className="flex flex-col gap-1">
          <p className="font-data text-[0.6rem] text-accentRose uppercase tracking-[0.3em] font-bold">
            {MODULES[activeModule]?.pillar || 'BRAND AFFINITY'}
          </p>
          <div className="flex items-center gap-4">
            <h1 className="font-hero text-3xl lg:text-4xl text-primaryText font-semibold italic">
              {MODULES[activeModule]?.title || 'Sephora Brand Affinity'}
            </h1>
            <div className="shimmer-line w-24 hidden lg:block" />
          </div>
        </div>
        <div className="text-right flex flex-col items-end">
          <div className="flex items-center gap-2 mb-1">
             <div className="w-1.5 h-1.5 rounded-full bg-accentRose animate-pulse" />
             <span className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-[0.2em] font-medium">Case 3: Brand Affinity Detection</span>
          </div>
          <p className="font-hero text-xs text-primaryText italic font-semibold">Sephora France • Albert School</p>
        </div>
      </motion.div>

      {/* ─── Main Display Area ─── */}
      <div className="flex-1 overflow-y-auto custom-scrollbar px-4 pb-28">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeModule}
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.4, ease: "easeInOut" }}
            className="w-full min-h-full"
          >
            {renderModule()}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* ─── Navigation: Rose-Gold Pill ─── */}
      <motion.nav 
        initial={{ opacity: 0, y: 20 }} 
        animate={{ opacity: 1, y: 0 }} 
        className="fixed bottom-8 left-0 right-0 z-50 flex justify-center pointer-events-none"
      >
        <div className="glass-panel px-4 py-3 flex items-center gap-1 shadow-lift rounded-full bg-white/90 backdrop-blur-3xl border border-accentPetal/20 pointer-events-auto">
          {MODULES.map((mod, idx) => (
            <button
              key={mod.id}
              onClick={() => setActiveModule(idx)}
              className={`
                relative px-2.5 py-1.5 rounded-full transition-all duration-300 cursor-pointer
                ${activeModule === idx ? 'text-primaryText font-bold' : 'text-tertiaryText hover:text-primaryText'}
              `}
            >
              {activeModule === idx && (
                <motion.div
                  layoutId="active-pill-glow"
                  className="absolute inset-0 bg-accentRose/15 rounded-full"
                  initial={false}
                />
              )}
              <span className="relative z-10 font-data text-[0.55rem] uppercase tracking-widest">
                {mod.num}
              </span>
            </button>
          ))}
        </div>
      </motion.nav>
    </div>
  );
}
