import { motion } from 'framer-motion';
import { Store, Mail, Smartphone, ShoppingBag, ArrowRight } from 'lucide-react';

const DIRECTIVES = [
  {
    channel: 'In-Store',
    Icon: Store,
    color: 'accentRose',
    actions: [
      { pair: 'HOURGLASS → WESTMAN ATELIER', action: 'Place side-by-side on premium counter. Staff brief: "Customers who love HOURGLASS also discover WESTMAN ATELIER."', lift: '44.4×' },
      { pair: 'AMIKA → OUAI HAIRCARE', action: 'Co-shelf in haircare aisle. Cross-sampling station with travel sizes.', lift: '17.4×' },
      { pair: 'GLOSSIER → ILIA', action: 'Build a "Clean Beauty Discovery" endcap with both brands.', lift: '8.4×' },
    ],
  },
  {
    channel: 'CRM / Email',
    Icon: Mail,
    color: 'accentGold',
    actions: [
      { pair: "PAULA'S CHOICE → SUPERGOOP", action: 'Post-purchase email Day 7: "Love your skincare routine? Complete it with SPF."', lift: '13.4×' },
      { pair: 'DRUNK ELEPHANT → FRESH', action: 'VIP segment: Skincare cross-sell campaign with sample offer.', lift: '11.7×' },
      { pair: 'BY TERRY → HOURGLASS', action: 'Loyalty program trigger: "Your next luxury makeup match."', lift: '13.1×' },
    ],
  },
  {
    channel: 'App / Digital',
    Icon: Smartphone,
    color: 'accentLavender',
    actions: [
      { pair: 'PAT MC GRATH → PAULA\'S CHOICE', action: 'Homepage carousel: "Editors who love PAT also swear by PAULA\'S CHOICE."', lift: '30.8×' },
      { pair: 'CACHAREL → DIESEL', action: 'Push notification after fragrance browse: "Your next signature scent?"', lift: '11.4×' },
      { pair: 'ILIA → KOSAS', action: 'Personalized "For You" widget: Clean beauty bundle suggestion.', lift: '13.7×' },
    ],
  },
];

export default function MetricsPanel() {
  return (
    <div className="glass-panel slide-bg slide-bg-entrance w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-3">
          The Action Playbook — What Happens Monday Morning
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-2 leading-tight">
          From data to the shop floor.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-8">
          Each directive maps directly to a validated pair from the previous slide
        </p>

        <div className="space-y-6 mb-8">
          {DIRECTIVES.map((d, di) => (
            <motion.div
              key={d.channel}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: di * 0.15 }}
              className="bg-bgCard rounded-2xl border border-borderSubtle overflow-hidden"
            >
              {/* Channel Header */}
              <div className={`flex items-center gap-3 px-6 py-3 bg-${d.color}/5 border-b border-borderSubtle`}>
                <d.Icon className={`w-5 h-5 text-${d.color}`} strokeWidth={1.5} />
                <h3 className={`font-hero text-xl italic font-bold text-${d.color}`}>{d.channel}</h3>
              </div>

              {/* Action Rows */}
              <div className="divide-y divide-borderSubtle/50">
                {d.actions.map((a, ai) => (
                  <motion.div
                    key={ai}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 + ai * 0.08 }}
                    className="px-6 py-4 hover:bg-accentPetal/3 transition-colors"
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        <div className={`flex items-center gap-1.5 bg-${d.color}/10 px-3 py-1 rounded-full`}>
                          <ShoppingBag className={`w-3 h-3 text-${d.color}`} strokeWidth={1.5} />
                          <span className={`font-data text-[0.5rem] text-${d.color} uppercase tracking-widest font-bold`}>{a.lift}</span>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <p className="font-hero text-sm italic font-bold text-primaryText">{a.pair.split(' → ')[0]}</p>
                          <ArrowRight className="w-3.5 h-3.5 text-accentGold flex-shrink-0" strokeWidth={2} />
                          <p className="font-hero text-sm italic font-bold text-accentGold">{a.pair.split(' → ')[1]}</p>
                        </div>
                        <p className="font-data text-[0.55rem] text-tertiaryText leading-relaxed">{a.action}</p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="bg-bgSoft/40 p-5 rounded-2xl border border-accentPetal/15">
          <p className="font-hero text-base text-primaryText italic font-semibold leading-relaxed text-center">
            "Every directive above is backed by a <span className="text-accentGold font-bold">statistically validated lift score</span>.
            This is not intuition — it is a <span className="text-accentGold font-bold">deployment-ready playbook</span> for
            store managers, CRM directors, and digital merchandisers."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-4 relative z-10">Source: store_brand_pairing_guide.csv | activation_protocol.md</p>
    </div>
  );
}
