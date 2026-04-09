import { motion } from 'framer-motion';

const SCENARIOS = [
  { name: 'Margin-First', rate: '3.10%', customers: 626, bar: 62, winner: false },
  { name: 'Balanced', rate: '3.27%', customers: 659, bar: 66, winner: true },
  { name: 'Discovery-First', rate: '2.89%', customers: 583, bar: 58, winner: false },
];

export default function SuccessDefinition() {
  return (
    <div className="glass-panel w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-gradient-to-tr from-accentGold/10 to-transparent rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Our Definition of Success
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          We defined it. We tested it. We proved it.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          Teams must propose their own definition of success — Rubric Criterion 2
        </p>

        {/* Success Formula */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { weight: '40%', metric: 'Basket Size Lift', value: '+€11.49', sub: 'Adopters vs non-adopters' },
            { weight: '30%', metric: 'Brand Diversity', value: '+1.2 brands', sub: 'Multi-brand exploration drives retention' },
            { weight: '30%', metric: 'Purchase Frequency', value: '26-day cycle', sub: '6,188 high-frequency VIPs identified' },
          ].map((m, i) => (
            <motion.div
              key={m.metric}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.15 }}
              className="stat-card text-center border-top-gold hover-iridescent cursor-help"
            >
              <p className="font-data text-[0.5rem] text-accentGold uppercase tracking-widest font-bold mb-2">Weight: {m.weight}</p>
              <p className="font-hero text-lg text-primaryText italic font-bold mb-2">{m.metric}</p>
              <p className="font-hero text-3xl text-accentGold italic font-bold mb-2">{m.value}</p>
              <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest">{m.sub}</p>
            </motion.div>
          ))}
        </div>

        {/* Scenario Bakeoff */}
        <div className="bg-bgCard p-8 rounded-[2rem] border border-borderSubtle mb-8">
          <p className="font-data text-[0.6rem] text-primaryText uppercase tracking-widest font-bold mb-6">
            Three Scenarios Tested on 20,181 Active Customers
          </p>
          <div className="flex flex-col gap-6">
            {SCENARIOS.map((s, i) => (
              <div key={s.name}>
                <div className="flex justify-between items-end mb-2">
                  <div className="flex items-center gap-3">
                    <h4 className="font-hero text-xl italic font-bold text-primaryText">{s.name}</h4>
                    {s.winner && (
                      <span className="font-data text-[0.5rem] bg-accentGold/15 text-accentGold px-3 py-1 rounded-full uppercase tracking-widest font-bold">
                        Winner
                      </span>
                    )}
                  </div>
                  <div className="text-right">
                    <span className={`font-hero text-2xl italic font-bold ${s.winner ? 'text-accentGold' : 'text-primaryText'}`}>
                      {s.rate}
                    </span>
                    <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">
                      {s.customers} customers converted
                    </p>
                  </div>
                </div>
                <div className="h-3 bg-bgSoft rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${s.bar}%` }}
                    transition={{ duration: 1.2, delay: i * 0.2, ease: [0.16, 1, 0.3, 1] }}
                    className={`h-full rounded-full ${s.winner ? 'bg-accentGold shadow-glow-gold' : 'bg-accentPetal'}`}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-bgSoft/50 p-6 rounded-[2rem] border border-accentPetal/20 text-center">
          <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed">
            "Neither pure profit-chasing nor pure novelty-seeking maximizes adoption.
            The <span className="text-accentGold font-bold">Balanced scenario</span> won — confirming that discovery and margin must be weighted equally."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: step3_4_report.txt L120-135 | 60,463 recommendations scored</p>
    </div>
  );
}
