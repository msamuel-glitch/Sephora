import { motion } from 'framer-motion';

const FUNNEL = [
  { label: 'Raw Transactions', value: '399,997', detail: 'Full FY2025 loyalty dataset', color: 'bg-accentPetal/30' },
  { label: 'Duplicates Removed', value: '-892', detail: 'Exact row duplicates permanently purged', color: 'bg-accentPetal/20' },
  { label: 'Anomalies Flagged', value: '14,571', detail: 'Discount > sale price rows flagged (not deleted)', color: 'bg-accentRose/10' },
  { label: 'Eligible Rows', value: '385,879', detail: 'Clean signal for affinity modeling', color: 'bg-accentGold/10' },
];

const FEATURES = [
  'Explorer Index (median: 0.41)',
  'Basket Axis Density',
  'Brand Loyalty Concentration',
  'Cross-Axis Discovery Propensity',
  'Velocity Score (purchase interval)',
  'Market Migration Score',
];

export default function SuccessHexagon() {
  return (
    <div className="glass-panel w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-72 h-72 bg-gradient-to-br from-accentLavender/8 to-transparent rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Data Mastery — Rubric Criterion 3
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          Command of the dataset.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          50,805 customers × 239 brands × 19 engineered features per customer
        </p>

        <div className="grid grid-cols-12 gap-8 mb-10">
          {/* Left: Data Funnel */}
          <div className="col-span-12 lg:col-span-7">
            <p className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold mb-4">Data Cleaning Funnel</p>
            <div className="flex flex-col gap-3">
              {FUNNEL.map((step, i) => (
                <motion.div
                  key={step.label}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className={`${step.color} p-5 rounded-2xl border border-borderSubtle flex justify-between items-center`}
                >
                  <div>
                    <p className="font-hero text-lg italic font-bold text-primaryText">{step.label}</p>
                    <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest mt-1">{step.detail}</p>
                  </div>
                  <p className="font-hero text-3xl text-primaryText italic font-bold">{step.value}</p>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Right: Key Design Decisions */}
          <div className="col-span-12 lg:col-span-5 flex flex-col gap-6">
            <div className="stat-card border-top-gold">
              <p className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold mb-3">Time Split (Zero Leakage)</p>
              <div className="flex gap-4">
                <div className="flex-1 bg-bgSoft p-4 rounded-xl text-center">
                  <p className="font-hero text-xl text-primaryText italic font-bold">Jan → Sep</p>
                  <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest mt-1">Feature Window</p>
                  <p className="font-data text-[0.5rem] text-primaryText font-bold mt-1">259,023 rows</p>
                </div>
                <div className="flex-1 bg-accentGold/10 p-4 rounded-xl text-center border border-borderGold">
                  <p className="font-hero text-xl text-accentGold italic font-bold">Oct → Dec</p>
                  <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest mt-1">Holdout Test</p>
                  <p className="font-data text-[0.5rem] text-accentGold font-bold mt-1">126,856 rows</p>
                </div>
              </div>
            </div>

            <div className="stat-card">
              <p className="font-data text-[0.55rem] text-accentRose uppercase tracking-widest font-bold mb-3">19 Engineered Features</p>
              <div className="flex flex-wrap gap-2">
                {FEATURES.map(f => (
                  <span key={f} className="font-data text-[0.45rem] text-primaryText bg-bgSoft px-3 py-1.5 rounded-full border border-borderSubtle">
                    {f}
                  </span>
                ))}
              </div>
            </div>

            <div className="nocibe-jolt">
              <p className="font-data text-[0.5rem] text-accentRed uppercase tracking-widest font-bold mb-2">Acknowledged Limitation</p>
              <p className="font-hero text-sm text-primaryText italic leading-relaxed">
                "First-purchase history available for only 26% of customers. We used it for enrichment, never as mandatory input."
              </p>
            </div>
          </div>
        </div>

        <div className="bg-bgSoft/40 p-6 rounded-[2rem] border border-accentPetal/15">
          <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed text-center">
            "45,446 multi-brand baskets → 8,357 unique co-occurrence pairs → <span className="text-accentGold font-bold">3,998 statistically reliable pairs</span> (minimum 3 co-purchases). Every feature computed exclusively from the Jan-Sep window."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: cleaning_report.txt, feature_engineering_log.txt, leakage_audit.txt</p>
    </div>
  );
}
