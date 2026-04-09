import { motion } from 'framer-motion';
import { Store, Sparkles, Scissors, Wind } from 'lucide-react';

const PAIRS = [
  { anchor: 'HOURGLASS', rec: 'WESTMAN ATELIER', lift: '44.4×', cat: 'Make Up' },
  { anchor: 'PAT MC GRATH', rec: "PAULA'S CHOICE", lift: '30.8×', cat: 'Make Up' },
  { anchor: 'AMIKA', rec: 'OUAI HAIRCARE', lift: '17.4×', cat: 'Haircare' },
  { anchor: 'ILIA', rec: 'KOSAS', lift: '13.7×', cat: 'Make Up' },
  { anchor: "PAULA'S CHOICE", rec: 'SUPERGOOP', lift: '13.4×', cat: 'Skincare' },
  { anchor: 'BY TERRY', rec: 'HOURGLASS', lift: '13.1×', cat: 'Make Up' },
  { anchor: 'DRUNK ELEPHANT', rec: 'FRESH SAS', lift: '11.7×', cat: 'Skincare' },
  { anchor: 'CACHAREL', rec: 'DIESEL', lift: '11.4×', cat: 'Fragrance' },
  { anchor: 'MAKEUP BY MARIO', rec: 'WESTMAN ATELIER', lift: '8.8×', cat: 'Make Up' },
  { anchor: 'HOURGLASS', rec: 'MAKEUP BY MARIO', lift: '8.5×', cat: 'Make Up' },
  { anchor: 'GLOSSIER', rec: 'ILIA', lift: '8.4×', cat: 'Make Up' },
];

const CAT_ICON = {
  'Make Up': Sparkles,
  'Haircare': Scissors,
  'Skincare': Wind,
  'Fragrance': Store,
};

const CAT_COLORS = {
  'Make Up': 'text-accentRose',
  'Haircare': 'text-accentLavender',
  'Skincare': 'text-accentGold',
  'Fragrance': 'text-primaryText',
};

export default function BrandDNA() {
  return (
    <div className="glass-panel slide-bg slide-bg-stripes w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="sephora-stripe-accent" />
      <div className="relative z-10">
        <div className="flex flex-wrap justify-between items-end gap-6 mb-6">
          <div>
            <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-3">
              The Core Deliverable — 11 Validated Cross-Sell Pairs
            </p>
            <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic leading-tight">
              These brands belong together.
            </h2>
            <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest mt-2">
              From 8,357 raw pairs → 3,998 statistically reliable → 217 guardrail-clean → Top 11 highest-lift
            </p>
          </div>
          <div className="text-right">
            <p className="font-hero text-4xl text-accentGold font-bold italic">203</p>
            <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest">guardrail-clean pairs<br/>ready to deploy</p>
          </div>
        </div>

        {/* Top 11 Pairs Table */}
        <div className="bg-bgCard rounded-2xl border border-borderSubtle overflow-hidden mb-6">
          {/* Table Header */}
          <div className="grid grid-cols-12 gap-2 px-6 py-3 bg-bgSoft/80 border-b border-borderSubtle">
            <p className="col-span-1 font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold text-center">#</p>
            <p className="col-span-3 font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold">If they buy...</p>
            <p className="col-span-3 font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold">Recommend...</p>
            <p className="col-span-2 font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold text-center">Lift vs Random</p>
            <p className="col-span-2 font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold text-center">Category</p>
            <p className="col-span-1 font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold text-center">Safe</p>
          </div>

          {/* Table Rows */}
          {PAIRS.map((pair, i) => {
            const Icon = CAT_ICON[pair.cat];
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="grid grid-cols-12 gap-2 px-6 py-2.5 border-b border-borderSubtle/50 hover:bg-accentPetal/5 transition-colors"
              >
                <p className="col-span-1 font-data text-sm text-tertiaryText text-center">{i + 1}</p>
                <p className="col-span-3 font-hero text-sm italic font-bold text-primaryText">{pair.anchor}</p>
                <div className="col-span-3 flex items-center gap-2">
                  <span className="font-data text-accentGold text-xs">→</span>
                  <p className="font-hero text-sm italic font-bold text-accentGold">{pair.rec}</p>
                </div>
                <p className="col-span-2 font-hero text-lg italic font-bold text-primaryText text-center">{pair.lift}</p>
                <div className={`col-span-2 flex items-center justify-center gap-1.5 ${CAT_COLORS[pair.cat]}`}>
                  <Icon className="w-3.5 h-3.5" strokeWidth={1.5} />
                  <span className="font-data text-[0.5rem] uppercase tracking-widest font-bold">{pair.cat}</span>
                </div>
                <div className="col-span-1 flex justify-center items-center">
                  <span className="w-2.5 h-2.5 rounded-full bg-green-400" title="No guardrail flags" />
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Bottom Insight */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div className="bg-bgSoft/40 p-5 rounded-2xl border border-accentPetal/15">
            <p className="font-hero text-base text-primaryText italic font-semibold leading-relaxed">
              "A customer who buys <span className="text-accentGold font-bold">HOURGLASS</span> is
              <span className="text-accentGold font-bold"> 44× more likely</span> to buy WESTMAN ATELIER than a random customer.
              This is not a guess — it is a validated statistical signal from 45,446 real baskets."
            </p>
          </div>

          <div className="nocibe-jolt">
            <p className="font-data text-[0.5rem] text-accentRed uppercase tracking-widest font-bold mb-2">vs Nocibé</p>
            <p className="font-hero text-sm text-primaryText italic leading-relaxed">
              "Nocibé recommends by within-brand popularity. They would never discover the
              <span className="font-bold"> AMIKA → OUAI</span> haircare bridge at 17.4× lift.
              Cross-brand affinity is our competitive moat."
            </p>
          </div>
        </div>
      </div>

      <p className="source-tag text-right mt-4 relative z-10">Source: store_brand_pairing_guide.csv | validation_report.txt L174-186</p>
    </div>
  );
}
