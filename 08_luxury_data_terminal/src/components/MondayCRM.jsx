import { motion } from 'framer-motion';
import { ShieldCheck, MailX, FlaskConical, Lock } from 'lucide-react';

const STRATEGIES = [
  {
    title: 'Deploy the "Do-Not-Recommend" Layer',
    metric: '14 Toxic Brands Blocked',
    detail: 'Immediately upload the suppression list to the CRM. Block high-churn trend haircare brands (e.g., OLAPLEX, VIRTUE) from ever appearing in emails sent to our Boomer Loyalists. Prevent trust erosion.',
    icon: MailX,
    color: 'accentLavender'
  },
  {
    title: 'Lock Down the VIP Segment',
    metric: '6,995 VIPs Protected',
    detail: 'Isolate the customers with the highest lifetime value (LTV). By shielding these 6,995 VIPs from the raw Machine Learning model output, we actively defend €491,476 in baseline revenue from accidental churn.',
    icon: Lock,
    color: 'accentGold'
  },
  {
    title: 'Launch the A/B Test Framework',
    metric: 'Success: > €11.49',
    detail: 'A/B test the recommendation system with strict business guardrails active. Treatment arm: Top 10% ML probability scores. Control: Masked standard merchandising. Stop the test if churn increases by 0.5% in the treatment group.',
    icon: FlaskConical,
    color: 'accentRose'
  }
];

export default function MondayCRM() {
  return (
    <div className="glass-panel slide-bg slide-bg-leather w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-gradient-to-tr from-accentGold/8 to-transparent rounded-full blur-3xl pointer-events-none z-0" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Strategic Wrap-Up II
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          Strategy II: The Protection Engine.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          How we deploy the business guardrails to protect our most valuable asset: Customer Trust.
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
                <ShieldCheck className={`w-3 h-3 text-${step.color}`} />
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
            "We do not let the algorithm dictate our brand equity. 
            By deploying this protection layer, we <span className="text-accentGold font-bold">de-risk the machine learning deployment</span> and ensure Sephora remains a luxury advisor, not just a vending machine."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: suppression_logic.txt | project_master_audit.txt Section 8</p>
    </div>
  );
}
