import { motion } from 'framer-motion';
import { TOP_TRANSITION_RULES, SEPHORA_COLLECTION_BRIDGE, FRAGRANCE_MULTIPLIER, DATA_SCOPE } from '../data/validatedData';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.2, delayChildren: 0.15 } },
};

const stepVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0, transition: { type: 'spring', stiffness: 100, damping: 16 } },
};

// Representative journey: Gen Z → CHANEL Fragrance → store → repeat at €90.12
const JOURNEY_STEPS = [
  {
    phase: 'Recruitment',
    title: 'Store Visit',
    detail: '70.2% of customers are recruited in-store',
    metric: '35,650 customers',
    color: '#8BB6A0',
    source: 'project_master_audit.txt Section 2',
  },
  {
    phase: 'First Axis',
    title: 'Makeup Entry',
    detail: 'Sephora Collection acts as entry bridge — 434 profiles, 133,536 transitions converge here',
    metric: `Avg basket €${SEPHORA_COLLECTION_BRIDGE.avgBasket}`,
    color: '#C9847C',
    source: 'sephora_correspondance_profils.pdf.txt',
  },
  {
    phase: 'Axis Transition',
    title: 'Fragrance Discovery',
    detail: 'Customer converts to Fragrance axis. This is the highest-value transition in the dataset.',
    metric: FRAGRANCE_MULTIPLIER.multiplier + ' basket multiplier',
    color: '#B8A89A',
    source: 'top_rules.json — all top 25 rules are Fragrance',
  },
  {
    phase: 'Brand Lock-In',
    title: 'CHANEL Fragrance',
    detail: 'Gen Z customer purchases CHANEL in-store. 81.4% probability of repeat. Expected basket €90.12.',
    metric: '€90.12 per basket',
    color: '#E2001A',
    source: 'top_rules.json — rule 1',
  },
  {
    phase: 'Next Recommendation',
    title: 'Cross-Brand Affinity',
    detail: 'Engine identifies DIOR as next-best via basket pair route. Boomer CHANEL→DIOR transition: 74.5% probability, €82.11 basket.',
    metric: '74.5% probability',
    color: '#E2001A',
    source: 'top_rules.json — rule 10',
  },
];

export default function PurchaseJourney() {
  return (
    <div className="max-w-[1600px] mx-auto w-full pt-4">
      <div className="mb-10">
        <h1 className="text-4xl lg:text-5xl font-hero font-semibold tracking-wide text-primaryText leading-tight">
          05 The Purchase Journey
        </h1>
        <p className="font-data text-xs text-secondaryText tracking-[0.1em] mt-3 max-w-3xl border-l-[3px] border-accentGold pl-4 uppercase leading-relaxed">
          One customer. Five stages. From store visit to automated brand recommendation. Grounded in {DATA_SCOPE.uniqueCustomers.toLocaleString()} customers and 894 transition rules.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* ─── Left: Journey Flow ─── */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="lg:col-span-7 flex flex-col gap-0"
        >
          {JOURNEY_STEPS.map((step, i) => (
            <motion.div key={step.phase} variants={stepVariants} className="flex items-stretch">
              {/* Timeline line */}
              <div className="flex flex-col items-center mr-5 flex-shrink-0">
                <div
                  className="w-3 h-3 rounded-full border-2 flex-shrink-0"
                  style={{ borderColor: step.color, backgroundColor: i === 3 ? step.color : 'transparent' }}
                />
                {i < JOURNEY_STEPS.length - 1 && (
                  <div className="w-px flex-1 bg-gradient-to-b from-black/[0.08] to-transparent min-h-[20px]" />
                )}
              </div>

              {/* Content card */}
              <div className="glass-panel p-5 mb-4 flex-1 hover:shadow-sm border border-black/[0.06] transition-all duration-200 bg-white">
                <div className="flex items-center gap-3 mb-2">
                  <span
                    className="font-data text-[0.5rem] uppercase tracking-[0.2em] font-bold px-2 py-0.5 rounded"
                    style={{ color: step.color, backgroundColor: `${step.color}15` }}
                  >
                    {step.phase}
                  </span>
                  <h3 className="font-hero text-xl text-primaryText font-semibold">{step.title}</h3>
                </div>

                <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-wider leading-relaxed mb-3">
                  {step.detail}
                </p>

                <div className="flex items-center justify-between">
                  <span className="font-hero text-lg italic font-medium" style={{ color: step.color }}>
                    {step.metric}
                  </span>
                  <span className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest italic">
                    {step.source}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* ─── Right: Key Findings ─── */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          {/* Fragrance Multiplier */}
          <div className="glass-panel p-6 border-t-4 border-t-accentGold">
            <p className="font-data text-[0.6rem] text-accentGold uppercase tracking-[0.2em] font-bold mb-4">
              The Fragrance Multiplier
            </p>

            <div className="flex items-end gap-4 mb-5">
              <div className="flex-1">
                <p className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest mb-1">Fragrance Avg Basket</p>
                <p className="font-hero text-4xl text-primaryText italic font-semibold">€{FRAGRANCE_MULTIPLIER.fragranceAvgBasket}</p>
              </div>
              <div className="text-center px-3">
                <p className="font-hero text-2xl text-accentGold italic font-semibold">vs</p>
              </div>
              <div className="flex-1 text-right">
                <p className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest mb-1">Skincare Avg</p>
                <p className="font-hero text-3xl text-tertiaryText italic">€{FRAGRANCE_MULTIPLIER.skincareAvgBasket}</p>
              </div>
            </div>

            <div className="bg-[#FAFAFA] border border-black/5 rounded-lg p-4 shadow-sm">
              <p className="font-hero text-2xl text-primaryText italic text-center mb-2 font-semibold">
                {FRAGRANCE_MULTIPLIER.multiplier}
              </p>
              <p className="font-data text-[0.55rem] text-secondaryText uppercase tracking-widest text-center leading-relaxed">
                {FRAGRANCE_MULTIPLIER.insight}
              </p>
            </div>
          </div>

          {/* Sephora Collection Bridge */}
          <div className="glass-panel p-6 border-t-4 border-t-primaryText">
            <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-[0.2em] font-bold mb-4">
              Sephora Collection — The Rebound Bridge
            </p>

            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Profiles</span>
                <span className="font-hero text-2xl text-primaryText italic font-semibold">{SEPHORA_COLLECTION_BRIDGE.profiles}</span>
              </div>
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Transitions</span>
                <span className="font-hero text-xl text-primaryText italic font-semibold">{SEPHORA_COLLECTION_BRIDGE.transitions.toLocaleString()}</span>
              </div>
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Avg Basket</span>
                <span className="font-hero text-xl text-primaryText italic font-semibold">€{SEPHORA_COLLECTION_BRIDGE.avgBasket}</span>
              </div>
            </div>

            <p className="font-data text-[0.55rem] text-secondaryText uppercase tracking-wider leading-relaxed">
              {SEPHORA_COLLECTION_BRIDGE.insight}
            </p>
          </div>

          {/* Engine summary stats */}
          <div className="glass-panel p-6">
            <p className="font-data text-[0.55rem] text-secondaryText uppercase tracking-[0.15em] mb-4">
              Sequential Transition Engine
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Rules</span>
                <span className="font-hero text-3xl text-primaryText italic font-semibold">894</span>
              </div>
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Targets</span>
                <span className="font-hero text-3xl text-primaryText italic font-semibold">95</span>
              </div>
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Holdout</span>
                <span className="font-hero text-xl text-primaryText italic font-semibold">Oct–Dec 2025</span>
              </div>
              <div className="flex flex-col">
                <span className="font-data text-[0.5rem] text-secondaryText uppercase tracking-widest">Leakage Audit</span>
                <span className="font-hero text-xl text-accentGold italic font-semibold">Clean</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
