import { motion } from 'framer-motion';

const FINDINGS = [
  { key: 'fragrance', title: 'FRAGRANCE is the universal value lever', metric: '€90.12', sub: 'Expected AOV for Fragrance axis', detail: 'Every customer converted to FRAGRANCE triples their transaction value. The top 10 most valuable transition rules are ALL Fragrance → Fragrance. Male FRAGRANCE buyers (6% of base) generate €95.98 avg basket — the highest per-transaction segment.' },
  { key: 'store', title: 'Store is the dominant channel (86-94%)', metric: '70.2%', sub: 'Customers best served in-store', detail: '35,650 customers assigned to in-store guidance. Digital advertising must drive store footfall, not online conversion. In-store activation (samples, pop-ups, events) is the highest-ROI touchpoint.' },
  { key: 'diversity', title: 'Brand diversity drives loyalty', metric: '3.60', sub: 'Gen A brands explored (highest)', detail: 'Customers who explore more brands return more often. Gen A explores 3.60 brands and has 60.7% retention vs Boomers at 2.50 brands and 50.2% retention. Discovery mechanics are retention tools, not acquisition tools.' },
];

export default function TacticalCommand() {
  return (
    <div className="glass-panel w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-72 h-72 bg-gradient-to-bl from-accentPetal/10 to-transparent rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Three Universal Rules from 894 Behavioral Transitions
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          What every Sephora team must know.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          Validated across 224,212 purchase transitions • All generations • All channels
        </p>

        <div className="space-y-6 mb-10">
          {FINDINGS.map((finding, i) => (
            <motion.div
              key={finding.key}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.15 }}
              className="bg-bgCard p-8 rounded-2xl border border-borderSubtle hover:border-accentPetal/30 transition-all"
            >
              <div className="flex flex-wrap justify-between items-start gap-6 mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-data text-[0.5rem] bg-accentGold/10 text-accentGold w-8 h-8 rounded-full flex items-center justify-center font-bold">
                      #{i + 1}
                    </span>
                    <h4 className="font-hero text-2xl italic font-bold text-primaryText">{finding.title}</h4>
                  </div>
                  <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest leading-relaxed">{finding.detail}</p>
                </div>
                <div className="text-right flex-shrink-0">
                  <p className="font-hero text-4xl text-accentGold italic font-bold">{finding.metric}</p>
                  <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">{finding.sub}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="nocibe-jolt">
          <p className="font-data text-[0.5rem] text-accentRed uppercase tracking-widest font-bold mb-2">Why Sephora Wins Over Nocibé</p>
          <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed">
            "Nocibé is trapped in single-brand loops — their rules recommend within-brand 90% of the time.
            Sephora's 894-rule system identifies <span className="text-accentGold font-bold">cross-axis transitions</span> that triple transaction value:
            moving a customer from a €30 Make Up entry point to the €90 Fragrance zenith."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: sephora_analysis_summary.pdf — Three Universal Rules | sephora_correspondance_profils.pdf</p>
    </div>
  );
}
