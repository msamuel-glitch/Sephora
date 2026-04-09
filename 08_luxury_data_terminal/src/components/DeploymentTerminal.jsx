import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ALL_ADDRESSABLE_BRANDS, TOP_TRANSITION_RULES, BUSINESS_VALUE, DATA_SCOPE } from '../data/validatedData';

const PILLARS = [
  { id: 'growth', label: 'Get New Buyers' },
  { id: 'upsell', label: 'Sell More Perfume' },
  { id: 'save', label: 'Save Top Clients' },
  { id: 'channel', label: 'Right Channel' },
];

export default function DeploymentTerminal() {
  const [selectedBrand, setSelectedBrand] = useState(ALL_ADDRESSABLE_BRANDS[0]?.brand || '');
  const [activePillar, setActivePillar] = useState('growth');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredBrands = useMemo(() => {
    if (!searchQuery) return ALL_ADDRESSABLE_BRANDS.slice(0, 15);
    return ALL_ADDRESSABLE_BRANDS.filter(b =>
      b.brand.toLowerCase().includes(searchQuery.toLowerCase())
    ).slice(0, 15);
  }, [searchQuery]);

  const activeBrand = useMemo(() =>
    ALL_ADDRESSABLE_BRANDS.find(b => b.brand === selectedBrand) || ALL_ADDRESSABLE_BRANDS[0],
    [selectedBrand]
  );

  // Growth Lever Logic (Simplified Directives)
  const getDirective = (pillar, brand) => {
    switch (pillar) {
      case 'growth':
        return {
          title: 'New Shopper Focus',
          value: brand.customers.toLocaleString(),
          sub: 'Potential New Buyers',
          detail: `Focus on ${brand.brand} viral trends. These shoppers are ready to buy if they see it mentioned correctly in the app or store.`,
        };
      case 'upsell':
        return {
          title: 'Premium Upgrade',
          value: '2.8x',
          sub: 'Value Multiplier',
          detail: 'When clients move to the Perfume category, they spend nearly 3 times more per visit starting Monday.',
        };
      case 'save':
        return {
          title: 'Safety Check',
          value: 'Active',
          sub: 'Relationship Filter',
          detail: 'We are protecting our biggest spenders by only showing them brands that perfectly match their style.',
        };
      case 'channel':
        return {
          title: 'Best Place to Buy',
          value: brand.channel === 'STORE' ? 'Physical Stores' : 'Mobile App',
          sub: 'Main Selling Path',
          detail: `${brand.brand} sells best through ${brand.channel === 'STORE' ? 'our local stores' : 'personalized mobile notifications'}.`,
        };
      default: return {};
    }
  };

  const activeDirective = getDirective(activePillar, activeBrand);

  return (
    <div className="max-w-[1700px] mx-auto w-full pt-4">
      {/* Header */}
      <div className="mb-12">
        <h1 className="text-4xl lg:text-5xl font-hero font-semibold tracking-tight text-primaryText leading-none">
          03 Growth Plans
        </h1>
        <p className="font-data text-[0.65rem] text-secondaryText tracking-[0.2em] border-l-2 border-accentGold pl-5 uppercase mt-6 max-w-3xl leading-relaxed">
          Select a brand to see how we grow. No complex tables—just clear actions to increase our revenue.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        {/* Left: Brand Spotlight (Simplified) */}
        <div className="lg:col-span-4 space-y-6">
          <div className="glass-panel p-6">
            <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-[0.2em] mb-4 font-bold">
              Select Brand
            </p>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search brands..."
              className="w-full bg-white border border-black/[0.06] rounded-lg px-4 py-2 font-data text-[0.7rem] uppercase tracking-wider mb-4 h-10 outline-none focus:border-accentGold"
            />
            <div className="max-h-[350px] overflow-y-auto pr-2 space-y-1">
              {filteredBrands.map((b) => (
                <button
                  key={b.brand}
                  onClick={() => setSelectedBrand(b.brand)}
                  className={`
                    w-full text-left px-3 py-2.5 rounded-lg font-data text-[0.6rem] uppercase tracking-widest transition-all
                    ${selectedBrand === b.brand ? 'bg-primaryText text-white' : 'hover:bg-black/5 text-secondaryText'}
                  `}
                >
                  {b.brand}
                </button>
              ))}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="glass-panel p-6 space-y-4">
             <div className="flex justify-between items-end">
                <span className="font-data text-[0.55rem] text-secondaryText uppercase tracking-widest">Total Opportunity</span>
                <span className="font-hero text-2xl text-primaryText font-bold italic">€{BUSINESS_VALUE.totalOpportunity.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-end">
                <span className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold">Extra Spend Lift</span>
                <span className="font-hero text-2xl text-accentGold font-bold italic">+€{BUSINESS_VALUE.incrementalDelta}</span>
              </div>
          </div>
        </div>

        {/* Right: The Activation Dossier */}
        <div className="lg:col-span-8">
           <AnimatePresence mode="wait">
            <motion.div
              key={activeBrand.brand}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="glass-panel p-10 min-h-[600px] flex flex-col items-center justify-between border-t-2 border-t-accentGold"
            >
              <div className="text-center w-full">
                <p className="font-data text-[0.6rem] text-accentGold uppercase tracking-[0.3em] mb-2 font-bold">
                  Weekly Growth Action
                </p>
                <h2 className="font-hero text-4xl lg:text-5xl font-bold tracking-tight text-primaryText">
                  {activeBrand.brand}
                </h2>
                <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-[0.2em] mt-4">
                   {activeBrand.customers.toLocaleString()} Active Clients
                </p>
              </div>

              {/* Central Visualization */}
              <div className="flex-1 flex flex-col justify-center w-full max-w-lg">
                 <AnimatePresence mode="wait">
                  <motion.div
                    key={activePillar}
                    initial={{ opacity: 0, filter: 'blur(8px)' }}
                    animate={{ opacity: 1, filter: 'blur(0px)' }}
                    exit={{ opacity: 0, filter: 'blur(8px)' }}
                    className="text-center"
                  >
                    <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-[0.3em] mb-3">
                       {activeDirective.title}
                    </p>
                    <p className="font-hero text-7xl font-light italic tracking-tighter text-primaryText">
                       {activeDirective.value}
                    </p>
                    <p className="font-data text-[0.5rem] text-accentGold uppercase tracking-widest font-bold mt-2">
                       {activeDirective.sub}
                    </p>
                    <div className="mt-10 p-6 rounded-2xl bg-black/[0.02] border border-black/[0.05]">
                      <p className="font-data text-[0.7rem] text-secondaryText leading-relaxed uppercase tracking-widest">
                         {activeDirective.detail}
                      </p>
                    </div>
                  </motion.div>
                 </AnimatePresence>
              </div>

              {/* Pillar Selector at Bottom */}
              <div className="w-full pt-10 border-t border-black/5">
                 <div className="flex flex-wrap justify-center gap-3">
                  {PILLARS.map((p) => (
                    <button
                      key={p.id}
                      onClick={() => setActivePillar(p.id)}
                      className={`
                        px-5 py-2.5 rounded-full border font-data text-[0.5rem] uppercase tracking-widest font-bold transition-all cursor-pointer
                        ${activePillar === p.id 
                          ? 'bg-primaryText text-white border-primaryText shadow-lift' 
                          : 'bg-white text-secondaryText border-black/10 hover:border-accentGold/40'
                        }
                      `}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
           </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
