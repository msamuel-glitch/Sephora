import { motion } from 'framer-motion';

export default function RevenueArbitrage() {
  return (
    <div className="glass-panel w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-80 h-80 bg-gradient-to-bl from-accentRose/8 to-transparent rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Key Finding 1 — The Explorer Effect
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          The less loyal, the more valuable.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          Counterintuitive: Our ML adds the MOST value where customers are already open to discovery
        </p>

        <div className="grid grid-cols-12 gap-8 mb-10">
          {/* Left: Explorer Distribution */}
          <div className="col-span-12 lg:col-span-7">
            <div className="stat-card border-left-rose mb-6">
              <p className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold mb-4">Explorer Index Distribution — 50,805 Customers</p>
              <div className="flex items-end gap-1 h-32">
                {[8, 12, 15, 22, 28, 35, 42, 38, 30, 18, 12, 8].map((h, i) => (
                  <motion.div
                    key={i}
                    initial={{ height: 0 }}
                    animate={{ height: `${h * 3}px` }}
                    transition={{ delay: i * 0.05, duration: 0.8 }}
                    className={`flex-1 rounded-t-lg ${i >= 5 ? 'bg-accentGold' : 'bg-accentPetal/40'}`}
                  />
                ))}
              </div>
              <div className="flex justify-between mt-3">
                <span className="font-data text-[0.45rem] text-tertiaryText uppercase">Loyal (0.0)</span>
                <span className="font-data text-[0.45rem] text-accentGold uppercase font-bold">← Median: 0.41 →</span>
                <span className="font-data text-[0.45rem] text-tertiaryText uppercase">Explorer (1.0)</span>
              </div>
            </div>

            {/* The AOV Comparison */}
            <div className="grid grid-cols-2 gap-4">
              <div className="stat-card text-center">
                <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold mb-2">Non-Discoverers</p>
                <p className="font-hero text-4xl text-primaryText italic font-bold">€72.53</p>
                <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest mt-2">Avg Basket (Holdout)</p>
              </div>
              <div className="stat-card text-center border-top-gold shadow-glow-gold">
                <p className="font-data text-[0.5rem] text-accentGold uppercase tracking-widest font-bold mb-2">Brand Discoverers</p>
                <p className="font-hero text-4xl text-accentGold italic font-bold">€84.02</p>
                <p className="font-data text-[0.45rem] text-accentGold uppercase tracking-widest mt-2">+15.8% Lift</p>
              </div>
            </div>
          </div>

          {/* Right: ML Winner Profile */}
          <div className="col-span-12 lg:col-span-5 flex flex-col gap-6">
            <div className="stat-card">
              <p className="font-data text-[0.55rem] text-accentRose uppercase tracking-widest font-bold mb-4">Who Does Our ML Help Most?</p>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="font-hero text-lg italic text-primaryText">ML-only winners</span>
                  <span className="font-hero text-2xl italic font-bold text-accentGold">0.582</span>
                </div>
                <div className="h-px bg-borderSubtle" />
                <div className="flex justify-between items-center">
                  <span className="font-hero text-lg italic text-primaryText">Hybrid-only winners</span>
                  <span className="font-hero text-2xl italic font-bold text-accentLavender">0.605</span>
                </div>
              </div>
              <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest mt-4">Mean Explorer Index of correctly predicted customers</p>
            </div>

            <div className="nocibe-jolt">
              <p className="font-data text-[0.5rem] text-accentRed uppercase tracking-widest font-bold mb-2">Nocibé Limitation</p>
              <p className="font-hero text-sm text-primaryText italic leading-relaxed">
                "Nocibé recommends same-brand 90% of the time. They cannot identify explorers because they never measure explorer willingness. Our Explorer Index is proprietary to this analysis."
              </p>
            </div>

            <div className="bg-bgSoft p-5 rounded-2xl border border-borderSubtle">
              <p className="font-hero text-sm text-primaryText italic leading-relaxed">
                <span className="font-bold text-accentGold">Business decision:</span> "Don't waste ML on loyal customers who already know what they want. Deploy ML on explorers — each recommendation is a potential +€11.49."
              </p>
            </div>
          </div>
        </div>
      </div>

      <p className="source-tag text-right">Source: 06_model_bakeoff_results.txt L35-37 | step3_4_report.txt L139-144</p>
    </div>
  );
}
