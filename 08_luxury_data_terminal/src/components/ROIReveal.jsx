import { motion } from 'framer-motion';
import { Target, TrendingUp, ShieldAlert, BadgeCheck } from 'lucide-react';

export default function ROIReveal() {
  return (
    <div className="glass-panel slide-bg slide-bg-gold w-full flex flex-col p-10 lg:p-14 relative overflow-hidden border-top-gold">
      <div className="absolute inset-0 bg-gradient-to-br from-accentGold/3 via-transparent to-accentRose/3 pointer-events-none z-0" />

      <div className="relative z-10 flex-1 flex flex-col justify-center max-w-5xl mx-auto py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <p className="font-data text-[0.65rem] text-accentGold uppercase tracking-[0.4em] font-bold mb-4 text-center">
            Strategic Wrap-Up III — The Final Verdict
          </p>

          <h2 className="font-hero text-5xl lg:text-6xl text-primaryText font-bold italic mb-8 leading-tight text-center">
            We predicted. We protected.<br/>
            <span className="text-accentGold">We delivered.</span>
          </h2>

          <div className="shimmer-line w-48 mx-auto mb-10" />

          {/* Core Promise vs Reality */}
          <div className="bg-bgCard p-6 rounded-2xl border border-borderGold mb-10 shadow-glow-gold relative overflow-hidden">
            <div className="absolute right-0 top-0 w-32 h-32 bg-accentGold/5 rounded-bl-full pointer-events-none" />
            <div className="flex flex-col md:flex-row gap-6 items-center">
              <div className="flex-1">
                <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-widest font-bold mb-2">The Original Promise (Slide 02)</p>
                <p className="font-hero text-xl italic font-bold text-primaryText mb-1">Target: +€10.00</p>
                <p className="font-data text-[0.55rem] text-tertiaryText leading-relaxed">Incremental basket value per user per visit, achieved without margin-diluting promotions or eroding Boomer trust.</p>
              </div>
              <div className="hidden md:block w-px h-16 bg-borderSubtle" />
              <div className="flex-1 text-right">
                <p className="font-data text-[0.65rem] text-accentGold uppercase tracking-widest font-bold mb-2 flex justify-end items-center gap-1">The Actual Delivery <BadgeCheck className="w-4 h-4" /></p>
                <p className="font-hero text-4xl italic font-bold text-accentGold mb-1">+€11.49</p>
                <p className="font-data text-[0.55rem] text-tertiaryText">Actual incremental AOV for explorers vs non-adopters (€84.02 vs €72.53)</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
            {/* The Revenue Result */}
            <div className="stat-card border-left-rose">
              <div className="flex items-center gap-3 mb-3">
                <TrendingUp className="w-5 h-5 text-accentRose" strokeWidth={1.5} />
                <p className="font-data text-[0.6rem] text-tertiaryText uppercase tracking-widest font-bold">Acquisition Impact</p>
              </div>
              <p className="font-hero text-4xl text-primaryText italic font-bold mb-2">659 Sales</p>
              <p className="font-data text-[0.55rem] text-tertiaryText leading-relaxed">
                Successful cross-brand conversions detected automatically within the Q4 validation holdout.
              </p>
            </div>

            {/* The Equity Result */}
            <div className="stat-card border-l-4 border-accentLavender">
              <div className="flex items-center gap-3 mb-3">
                <ShieldAlert className="w-5 h-5 text-accentLavender" strokeWidth={1.5} />
                <p className="font-data text-[0.6rem] text-tertiaryText uppercase tracking-widest font-bold">Protection Impact</p>
              </div>
              <p className="font-hero text-4xl text-primaryText italic font-bold mb-2">€491,476</p>
              <p className="font-data text-[0.55rem] text-tertiaryText leading-relaxed">
                Baseline VIP revenue completely shielded from commercially toxic "mathematical" recommendations.
              </p>
            </div>
          </div>

          {/* Scale */}
          <div className="bg-bgSoft/40 p-6 rounded-2xl border border-borderSubtle">
            <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed text-center">
              "When you run this architecture across <span className="text-accentGold font-bold">80M+ Sephora loyalty members</span>, 
              +€11.49 multiplied by our new conversion volume is not just an optimization. 
              It is a <span className="text-accentGold font-bold">board-level margin driver</span>."
            </p>
          </div>
        </motion.div>
      </div>

      <p className="source-tag text-center z-10">Source: project_master_audit.txt — Figures validated against 45,446 basket dataset</p>
    </div>
  );
}
