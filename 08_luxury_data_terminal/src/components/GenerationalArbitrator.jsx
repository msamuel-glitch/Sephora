import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PERSONAS } from '../data/validatedData';

// ─── Value Pillars ───
const PILLARS = [
  { id: 'basket', label: 'Bigger Baskets' },
  { id: 'discovery', label: 'New Brands' },
  { id: 'personalization', label: 'Matching Offers' },
  { id: 'loyalty', label: 'Loyal Clients' },
];

const personaConfigs = [
  {
    key: 'loyalistExplorer',
    data: PERSONAS.loyalistExplorer,
    accent: '#D4AF37',
    name: 'Mature Buyers',
    narrative: 'High-value clients who shop often. They are moving from basic skincare to expensive perfumes.',
    values: {
      basket: { title: 'Spending Power', value: '€82.00', sub: 'Perfume Category', detail: 'Clients spend €82 on perfume compared to only €30 on skincare.' },
      discovery: { title: 'New Category Speed', value: 'Fast', sub: '48h Window', detail: 'These clients usually buy a new brand within 48 hours of visiting the store.' },
      personalization: { title: 'Success Rate', value: '85%', sub: 'Direct Messaging', detail: '85% of these clients buy when we send them a personalized recommendation.' },
      loyalty: { title: 'Loyalty Level', value: 'High', sub: 'Elite Members', detail: 'These are your most stable clients. They mostly buy high-end selective brands.' },
    },
  },
  {
    key: 'discoveryEngine',
    data: PERSONAS.discoveryEngine,
    accent: '#171717',
    name: 'Young Gen Buyers',
    narrative: 'Young shoppers (Gen Alpha/Z) who love viral trends and trying new brands before anyone else.',
    values: {
      basket: { title: 'Basket Growth', value: '+€11.49', sub: 'Extra Spending', detail: 'We can grow their average spend from €72 to €84 by showing them new brands.' },
      discovery: { title: 'Trend Velocity', value: 'High', sub: 'Viral Makeup', detail: 'They are the first to buy trending makeup brands on social media.' },
      personalization: { title: 'App Success', value: '91%', sub: 'Mobile Users', detail: '91% of these shoppers use the app to find their next purchase.' },
      loyalty: { title: 'New Growth', value: '659', sub: 'New Fans', detail: 'We gained 659 new high-value young shoppers in the last 3 months.' },
    },
  },
  {
    key: 'dormantHighValue',
    data: PERSONAS.dormantHighValue,
    accent: '#737373',
    name: 'Valuable Sleepers',
    narrative: 'Top clients who stopped buying. We need to be careful not to annoy them with wrong offers.',
    values: {
      basket: { title: 'Money at Risk', value: '€491,476', sub: 'Total Segment', detail: 'These clients are worth nearly €500k. We must protect this relationship.' },
      discovery: { title: 'Smart Filters', value: 'Active', sub: 'Safety Rules', detail: 'We stopped showing them 14 brands that didn\'t match their style.' },
      personalization: { title: 'Reach', value: '54%', sub: 'Top Clients', detail: 'We are currently protecting over half of our most valuable sleepers.' },
      loyalty: { title: 'Status', value: 'Gold/Silver', sub: 'Top Tiers', detail: 'These are long-term Sephora fans. We prioritize quality over quantity for them.' },
    },
  },
];

export default function GenerationalArbitrator() {
  const [selectedPillars, setSelectedPillars] = useState({
    loyalistExplorer: 'basket',
    discoveryEngine: 'discovery',
    dormantHighValue: 'loyalty',
  });

  const selectPillar = (personaKey, pillarId) => {
    setSelectedPillars(prev => ({ ...prev, [personaKey]: pillarId }));
  };

  return (
    <div className="max-w-[1700px] mx-auto w-full pt-4">
      {/* Boardroom Header */}
      <div className="mb-14">
        <h1 className="text-4xl lg:text-5xl font-hero font-semibold tracking-tight text-primaryText leading-none">
          02 Customer Profiles
        </h1>
        <p className="font-data text-[0.65rem] text-secondaryText tracking-[0.2em] border-l-2 border-accentGold pl-5 uppercase mt-6 max-w-3xl leading-relaxed">
          Focus on how clients shop, not just their age. This is how we grow our revenue by matching the right client to the right brand.
        </p>
      </div>

      {/* Persona Dossier Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {personaConfigs.map(({ key, accent, narrative, values, name }) => {
          const activePillarId = selectedPillars[key];
          const activeData = values[activePillarId];
          const isHighlight = key === 'discoveryEngine';

          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className={`
                glass-panel p-8 flex flex-col relative overflow-hidden transition-all duration-500
                border-t-2 ${isHighlight ? 'shadow-glow-gold' : 'hover:shadow-lift'}
              `}
              style={{ borderTopColor: accent }}
            >
              {/* Narrative Quote */}
              <div className="mb-8">
                <p className="font-data text-[0.55rem] uppercase tracking-[0.25em] mb-4 font-bold" style={{ color: accent }}>
                  {name}
                </p>
                <div className="min-h-[80px]">
                   <p className="font-hero text-2xl font-bold leading-tight italic text-primaryText">
                    "{narrative}"
                  </p>
                </div>
              </div>

              {/* The "Sweetness" - Dynamic Value Illustration */}
              <div className="flex-1 flex flex-col justify-center min-h-[220px]">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activePillarId}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.05 }}
                    transition={{ duration: 0.3 }}
                    className="flex flex-col items-center text-center px-4"
                  >
                    <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-[0.3em] mb-3">
                      {activeData.title}
                    </p>
                    <p className="font-hero text-6xl italic font-light tracking-tighter" style={{ color: accent }}>
                      {activeData.value}
                    </p>
                    <p className="font-data text-[0.5rem] text-accentGold uppercase tracking-widest font-bold mt-1">
                      {activeData.sub}
                    </p>
                    <div className="mt-8 p-4 rounded-xl bg-black/[0.02] border border-black/[0.05] w-full">
                      <p className="font-data text-[0.6rem] text-secondaryText leading-relaxed uppercase tracking-wider">
                        {activeData.detail}
                      </p>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>

              {/* The Value Pill Selector */}
              <div className="mt-10 pt-8 border-t border-black/5">
                <p className="font-data text-[0.5rem] uppercase tracking-widest mb-4 text-center text-tertiaryText">
                  Show Business Aspect
                </p>
                <div className="flex flex-wrap justify-center gap-2">
                  {PILLARS.map((pill) => (
                    <button
                      key={pill.id}
                      onClick={() => selectPillar(key, pill.id)}
                      className={`
                        flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300 cursor-pointer
                        ${activePillarId === pill.id
                          ? 'bg-primaryText text-white border-primaryText shadow-lift'
                          : 'bg-white text-secondaryText border-black/10 hover:border-accentGold/40 hover:bg-black/[0.02]'
                        }
                      `}
                    >
                      <span className="font-data text-[0.45rem] uppercase tracking-widest font-bold">
                        {pill.label}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
