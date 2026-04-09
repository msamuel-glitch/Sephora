import { motion } from 'framer-motion';

const BRANDS = [
  { name: 'BOBBI BROWN', market: 'Selective', untapped: '18,180', pct: 35.8, color: 'bg-accentRose' },
  { name: 'SUMMER FRIDAYS', market: 'Exclusive', untapped: '16,814', pct: 33.1, color: 'bg-accentGold' },
  { name: 'DRUNK ELEPHANT', market: 'Exclusive', untapped: '16,482', pct: 32.4, color: 'bg-accentLavender' },
  { name: 'TOM FORD', market: 'Selective', untapped: '15,662', pct: 30.8, color: 'bg-primaryText' },
  { name: 'KENZO', market: 'Selective', untapped: '15,662', pct: 30.8, color: 'bg-accentPetal' },
];

export default function BrandMarket() {
  return (
    <div className="glass-panel slide-bg slide-bg-giftbox w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-72 h-72 bg-gradient-to-bl from-accentGold/10 to-transparent rounded-full blur-3xl pointer-events-none z-0" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Brand Addressable Market — 239 Brands Ranked
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          The biggest opportunity is hiding in plain sight.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          Not unknown brands — well-known brands customers haven't tried yet
        </p>

        <div className="space-y-5 mb-10">
          {BRANDS.map((brand, i) => (
            <motion.div
              key={brand.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.12 }}
              className="bg-bgCard p-6 rounded-2xl border border-borderSubtle hover:border-accentPetal/30 transition-all cursor-help"
            >
              <div className="flex justify-between items-center mb-3">
                <div className="flex items-center gap-4">
                  <span className="font-hero text-2xl text-primaryText italic font-bold">#{i + 1}</span>
                  <div>
                    <h4 className="font-hero text-xl italic font-bold text-primaryText">{brand.name}</h4>
                    <span className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">{brand.market}</span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-hero text-3xl text-accentGold italic font-bold">{brand.untapped}</p>
                  <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">Untapped VIPs</p>
                </div>
              </div>

              {/* Progress Ring as Bar */}
              <div className="h-3 bg-bgSoft rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${brand.pct}%` }}
                  transition={{ duration: 1.5, delay: 0.3 + i * 0.1, ease: [0.16, 1, 0.3, 1] }}
                  className={`h-full rounded-full ${brand.color}`}
                />
              </div>
              <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest mt-1 text-right">{brand.pct}% of total customer base untapped</p>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-bgSoft/40 p-6 rounded-2xl border border-accentPetal/15">
            <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed">
              "All 5 are <span className="text-accentGold font-bold">Established brands</span>, not cold-start emerging labels. The biggest commercial opportunity lies in converting existing high-affinity customers to well-known brands they haven't yet tried."
            </p>
          </div>

          <div className="bg-bgCard p-6 rounded-2xl border border-borderGold">
            <p className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold mb-3">Business Implication</p>
            <p className="font-hero text-sm text-primaryText italic leading-relaxed">
              "BOBBI BROWN has 18,180 high-affinity customers who have never purchased. At the sample's average basket of €84.02, that's <span className="text-accentGold font-bold">€1.53M in addressable revenue</span> from a single brand conversion campaign."
            </p>
            <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest mt-2">
              Note: Sample-level estimate, not guaranteed P&L
            </p>
          </div>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: brand_addressable_market.csv | project_master_audit.txt Section 7</p>
    </div>
  );
}
