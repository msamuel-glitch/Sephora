import { motion } from 'framer-motion';
import { Database, Brain, Shield, ChevronRight, CheckCircle } from 'lucide-react';

const FUNNEL_STEPS = [
  {
    Icon: Database,
    step: '01',
    title: 'Raw Basket Mining',
    subtitle: '45,446 baskets analyzed',
    detail: 'We scanned every real transaction to find which brands naturally appear in the same shopping bag.',
    input: '8,357 brand pairs detected',
    output: '3,998 statistically reliable (min 3 co-purchases)',
    color: 'accentRose',
  },
  {
    Icon: Brain,
    step: '02',
    title: 'ML Validation',
    subtitle: '4 independent candidate routes',
    detail: 'Each pair was validated through Basket Pair Analysis, Lookalike Segments, Axis-Market Logic, and Cold-Start Proxy — not just one method.',
    input: '3,998 reliable pairs',
    output: '217 high-confidence pairs (lift > 5×)',
    color: 'accentGold',
  },
  {
    Icon: Shield,
    step: '03',
    title: 'Business Guardrails',
    subtitle: 'Human commercial logic applied',
    detail: 'We removed same-parent-company artifacts (e.g. LVMH internal cannibalizations), margin-dilutive conflicts, and generation mismatches.',
    input: '217 high-confidence pairs',
    output: '203 deployment-ready pairs',
    color: 'accentLavender',
  },
];

const TRUST_POINTS = [
  { label: 'Zero Data Leakage', detail: 'Training: Jan-Sep | Testing: Oct-Dec holdout', icon: CheckCircle },
  { label: 'Correlation ≠ Causation', detail: '179 trivial associations filtered (same parent company)', icon: CheckCircle },
  { label: '4-Route Ensemble', detail: 'No single-method bias. Each pair confirmed by independent logic', icon: CheckCircle },
  { label: '€491K Equity Protected', detail: '6,995 high-value customers shielded from bad recommendations', icon: CheckCircle },
];

export default function GoldenBridge() {
  return (
    <div className="glass-panel slide-bg slide-bg-leather w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-3">
          The Proof Engine — Why You Can Trust These Numbers
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-2 leading-tight">
          How we went from raw data to boardroom-ready.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-8">
          3 rigorous filtration stages. Each pair earned its place.
        </p>

        {/* 3-Step Funnel */}
        <div className="flex flex-col gap-4 mb-8">
          {FUNNEL_STEPS.map((step, i) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, x: -25 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.2, duration: 0.5 }}
            >
              <div className={`bg-bgCard rounded-2xl border border-borderSubtle p-6 relative`}>
                {/* Step Badge */}
                <div className={`absolute -left-3 top-6 w-10 h-10 rounded-full bg-${step.color}/15 flex items-center justify-center`}>
                  <step.Icon className={`w-5 h-5 text-${step.color}`} strokeWidth={1.5} />
                </div>

                <div className="ml-8">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`font-data text-[0.55rem] text-${step.color} uppercase tracking-widest font-bold bg-${step.color}/10 px-2 py-0.5 rounded-full`}>
                      Step {step.step}
                    </span>
                    <h3 className="font-hero text-xl italic font-bold text-primaryText">{step.title}</h3>
                    <span className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">{step.subtitle}</span>
                  </div>

                  <p className="font-data text-[0.55rem] text-tertiaryText leading-relaxed mb-3">{step.detail}</p>

                  <div className="flex items-center gap-3 text-[0.5rem]">
                    <span className="font-data text-tertiaryText uppercase tracking-widest bg-bgSoft px-3 py-1 rounded-full">{step.input}</span>
                    <ChevronRight className="w-4 h-4 text-accentGold" />
                    <span className={`font-data text-${step.color} uppercase tracking-widest font-bold bg-${step.color}/10 px-3 py-1 rounded-full`}>{step.output}</span>
                  </div>
                </div>
              </div>

              {/* Connector Arrow */}
              {i < FUNNEL_STEPS.length - 1 && (
                <div className="flex justify-center py-1">
                  <div className="w-px h-4 bg-gradient-to-b from-borderSubtle to-transparent" />
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* Trust Badges Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {TRUST_POINTS.map((tp, i) => (
            <motion.div
              key={tp.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + i * 0.1 }}
              className="stat-card text-center py-4 px-3"
            >
              <tp.icon className="w-5 h-5 text-green-500 mx-auto mb-2" strokeWidth={1.5} />
              <p className="font-hero text-sm italic font-bold text-primaryText mb-1">{tp.label}</p>
              <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest leading-relaxed">{tp.detail}</p>
            </motion.div>
          ))}
        </div>
      </div>

      <p className="source-tag text-right mt-4 relative z-10">Source: validation_report.txt | suppression_logic.txt | 06_model_bakeoff_results.txt</p>
    </div>
  );
}
