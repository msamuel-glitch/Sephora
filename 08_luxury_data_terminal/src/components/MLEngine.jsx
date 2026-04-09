import { motion } from 'framer-motion';

const RULES = [
  { gen: 'Gen Z', axis: 'MAKE UP', brand: 'HUDA BEAUTY', channel: 'Store', nextAxis: 'MAKE UP', prob: '71.4%', basket: '€30.49', transitions: '650', insight: 'Strongest same-axis brand loop outside Fragrance' },
  { gen: 'Boomers', axis: 'FRAGRANCE', brand: 'CHANEL', channel: 'Store', nextAxis: 'FRAGRANCE', prob: '74.5%', basket: '€82.11', transitions: '51', insight: 'Heritage loyalty — never leaves the axis' },
  { gen: 'Gen Y', axis: 'FRAGRANCE', brand: 'LANCÔME', channel: 'Store', nextAxis: 'FRAGRANCE', prob: '59.4%', basket: '€87.83', transitions: '32', insight: 'The HIGHEST-value cross-brand rule: Lancôme → DIOR' },
  { gen: 'Gen A', axis: 'MAKE UP', brand: 'CHARLOTTE TILBURY', channel: 'Store', nextAxis: 'MAKE UP', prob: '66.6%', basket: '€29.55', transitions: '220', insight: 'Social-media-native brand with strong repeat' },
];

export default function MLEngine() {
  return (
    <div className="glass-panel slide-bg slide-bg-entrance w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-accentLavender/5 to-transparent rounded-full blur-3xl pointer-events-none z-0" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Behavioral Transition Analysis — 224,212 Observed Transitions
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          894 rules. One row per profile.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          For each gender × generation × axis × brand × channel: the most likely next purchase, brand, and expected basket value
        </p>

        {/* Sample Rules */}
        <div className="space-y-4 mb-10">
          {RULES.map((rule, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -15 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-bgCard p-6 rounded-2xl border border-borderSubtle hover:border-accentPetal/30 transition-all cursor-help"
            >
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-2 mb-2">
                    <span className="font-data text-[0.5rem] bg-accentRose/10 text-accentRose px-2 py-0.5 rounded-full uppercase tracking-widest font-bold">{rule.gen}</span>
                    <span className="font-data text-[0.5rem] bg-accentGold/10 text-accentGold px-2 py-0.5 rounded-full uppercase tracking-widest font-bold">{rule.axis}</span>
                    <span className="font-data text-[0.5rem] bg-bgSoft text-primaryText px-2 py-0.5 rounded-full uppercase tracking-widest font-bold">{rule.brand}</span>
                    <span className="font-data text-[0.4rem] text-tertiaryText">→</span>
                    <span className="font-data text-[0.5rem] bg-accentLavender/10 text-accentLavender px-2 py-0.5 rounded-full uppercase tracking-widest font-bold">{rule.nextAxis}</span>
                  </div>
                  <p className="font-hero text-sm italic text-secondaryText">{rule.insight}</p>
                </div>
                <div className="flex gap-6 text-right">
                  <div>
                    <p className="font-hero text-2xl text-accentGold italic font-bold">{rule.prob}</p>
                    <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest">Probability</p>
                  </div>
                  <div>
                    <p className="font-hero text-2xl text-primaryText italic font-bold">{rule.basket}</p>
                    <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest">Exp. Basket</p>
                  </div>
                  <div>
                    <p className="font-hero text-2xl text-accentRose italic font-bold">{rule.transitions}</p>
                    <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest">Transitions</p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-bgSoft/50 p-6 rounded-2xl border border-accentPetal/15">
            <p className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold mb-3">Universal Finding</p>
            <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed">
              "SEPHORA Collection is the universal rebound brand — present in <span className="text-accentGold font-bold">100% of transition rules</span> as a bridge between two premium purchases. It's not brand loyalty; it's gap-filling behavior."
            </p>
          </div>

          <div className="nocibe-jolt">
            <p className="font-data text-[0.5rem] text-accentRed uppercase tracking-widest font-bold mb-2">Nocibé Cannot Do This</p>
            <p className="font-hero text-sm text-primaryText italic leading-relaxed">
              "Building 894 rules requires chronological transaction sorting and conditional probability tables per profile. Nocibé's single-model approach collapses all profiles into one prediction."
            </p>
          </div>
        </div>

        {/* Narrative Hook to Personas */}
        <div className="bg-bgCard p-5 rounded-2xl border-l-[6px] border-accentGold shadow-lift relative z-10">
            <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest font-bold mb-1">The Strategic Funnel</p>
            <p className="font-hero text-xl text-primaryText italic font-bold leading-relaxed">
              "When we sorted these 894 rules by ROI, two distinct growth engines emerged. The next step was mapping these statistical rules to the humans driving them."
            </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: sephora_analysis_summary.pdf | 894 validated behavioral rules</p>
    </div>
  );
}
