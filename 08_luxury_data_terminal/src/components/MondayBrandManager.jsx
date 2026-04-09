import { motion } from 'framer-motion';
import { Target, Users, ArrowUpRight, Zap } from 'lucide-react';

const STRATEGIES = [
  {
    title: 'Deploy the 217 Validated Pairs In-Store',
    metric: '44.4× Peak Lift',
    detail: 'Push the Store Pairing Guide to regional directors. Mandate cross-merchandising for the top 10 highest-lift pairs (e.g., HOURGLASS and WESTMAN ATELIER) on premium endcaps to trigger impulse discovery.',
    icon: Target,
    color: 'accentGold'
  },
  {
    title: 'Target the "Explorer" Untapped Segments',
    metric: '32.4% Untapped',
    detail: 'For brands like DRUNK ELEPHANT, focus acquisition specifically on Gen Z customers who have a high Explorer Index (> 0.70) but have never purchased the brand. These are mathematically the cheapest conversions.',
    icon: Users,
    color: 'accentRose'
  },
  {
    title: 'Automate the "Rebound" Journeys',
    metric: '100% Coverage',
    detail: 'Because SEPHORA Collection acts as a universal bridge between premium items, trigger automated cross-sell emails featuring premium makeup 48 hours after a SEPHORA Collection purchase.',
    icon: Zap,
    color: 'accentLavender'
  }
];

export default function MondayBrandManager() {
  return (
    <div className="glass-panel slide-bg slide-bg-storefront w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-80 h-80 bg-gradient-to-bl from-accentRose/8 to-transparent rounded-full blur-3xl pointer-events-none z-0" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Strategic Wrap-Up I
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          Strategy I: The Acquisition Engine.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          How we deploy the mathematical insights to capture new basket volume immediately.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          {STRATEGIES.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.15 }}
              className={`bg-bgCard p-6 rounded-2xl border-t-4 border-${step.color} shadow-lift hover:border-accentGold transition-all`}
            >
              <div className={`w-12 h-12 rounded-full bg-${step.color}/10 flex items-center justify-center mb-4`}>
                <step.icon className={`w-6 h-6 text-${step.color}`} strokeWidth={1.5} />
              </div>
              
              <div className="flex justify-between items-start gap-2 mb-3">
                <h4 className="font-hero text-xl italic font-bold text-primaryText leading-snug">{step.title}</h4>
              </div>
              
              <div className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-${step.color}/5 border border-${step.color}/20 mb-4`}>
                <ArrowUpRight className={`w-3 h-3 text-${step.color}`} />
                <span className={`font-data text-[0.5rem] text-${step.color} uppercase tracking-widest font-bold`}>{step.metric}</span>
              </div>
              
              <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest leading-relaxed">
                {step.detail}
              </p>
            </motion.div>
          ))}
        </div>

        <div className="bg-bgSoft/40 p-6 rounded-2xl border border-accentPetal/15 max-w-4xl mx-auto">
          <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed text-center">
            "We are moving from brand-centric marketing to <span className="text-accentGold font-bold">relationship-centric geometry</span>. 
            We know exactly which brand sequences naturally occur in the checkout line. Now, we force them to happen."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: store_brand_pairing_guide.csv | activation_protocol.md</p>
    </div>
  );
}
