import { motion } from 'framer-motion';
import { SUPPRESSION_AXES, CANDIDATE_ROUTES } from '../data/validatedData';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.15, delayChildren: 0.1 } },
};

const cardVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 120, damping: 18 } },
};

export default function FormalCostFunction() {
  return (
    <div className="max-w-[1600px] mx-auto w-full pt-4">
      <div className="mb-10">
        <h1 className="text-4xl lg:text-5xl font-hero font-semibold tracking-wide text-primaryText leading-tight">
          04 Recommendation Risk Framework
        </h1>
        <p className="font-data text-xs text-primaryText tracking-[0.1em] mt-3 max-w-3xl border-l-[3px] border-primaryText pl-4 uppercase font-bold leading-relaxed">
          Every recommendation system has a reward function. We are the only team that built a cost function.
        </p>
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 lg:grid-cols-12 gap-6"
      >
        {/* ─── Left: Three Suppression Axes ─── */}
        <motion.div variants={cardVariants} className="lg:col-span-5 glass-panel p-6 flex flex-col border-t-4 border-t-accentGold">
          <p className="font-data text-[0.6rem] text-accentGold uppercase tracking-[0.2em] font-bold mb-6">
            Relationship Protection Protocol
          </p>

          <div className="flex flex-col gap-4 flex-1">
            {SUPPRESSION_AXES.map((axis) => (
              <div
                key={axis.id}
                className="bg-white p-4 rounded-lg border border-black/[0.06] hover:border-accentGold/40 hover:shadow-sm transition-all duration-200"
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold">
                    Axis {axis.id}
                  </span>
                  <span className="font-hero text-lg text-primaryText font-semibold">{axis.name}</span>
                </div>
                <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-wider leading-relaxed">
                  {axis.description}
                </p>
                <p className="font-data text-[0.55rem] text-primaryText uppercase tracking-widest mt-2 font-bold">
                  {axis.metric}
                </p>

                {/* Show suppressed brands for Axis B */}
                {axis.brands && (
                  <div className="mt-3 pt-2 border-t border-black/5">
                    <p className="font-data text-[0.45rem] text-secondaryText uppercase tracking-widest mb-1.5">Suppressed brands:</p>
                    <div className="flex flex-wrap gap-1">
                      {axis.brands.slice(0, 8).map(b => (
                        <span key={b} className="font-data text-[0.45rem] text-primaryText bg-black/[0.03] border border-black/[0.05] px-1.5 py-0.5 rounded uppercase tracking-wider">
                          {b}
                        </span>
                      ))}
                      {axis.brands.length > 8 && (
                        <span className="font-data text-[0.45rem] text-secondaryText px-1.5 py-0.5 uppercase">
                          +{axis.brands.length - 8} more
                        </span>
                      )}
                    </div>
                  </div>
                )}

                <p className="font-data text-[0.4rem] text-tertiaryText uppercase tracking-widest mt-2 italic">
                  {axis.source}
                </p>
              </div>
            ))}
          </div>

          {/* Bottom metrics */}
          <div className="mt-6 pt-5 border-t border-black/5">
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-end">
                <span className="font-data text-[0.6rem] text-secondaryText uppercase tracking-widest">Equity Protected</span>
                <span className="font-hero text-3xl text-primaryText italic font-semibold">€491,476</span>
              </div>
              <div className="flex justify-between items-end">
                <span className="font-data text-[0.6rem] text-accentGold uppercase tracking-widest font-bold">Customers Shielded</span>
                <span className="font-hero text-3xl text-accentGold italic font-semibold">6,995</span>
              </div>
              <div className="flex justify-between items-end">
                <span className="font-data text-[0.6rem] text-secondaryText uppercase tracking-widest">Coverage Rate</span>
                <span className="font-hero text-2xl text-primaryText italic">53.65%</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* ─── Right: Four-Route Candidate Engine ─── */}
        <motion.div variants={cardVariants} className="lg:col-span-7 glass-panel p-6 flex flex-col border-t-4 border-t-primaryText">
          <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-[0.2em] mb-8">
            Four-Route Candidate Engine
          </p>

          <div className="flex-1 flex flex-col justify-center">
            {/* Central hub */}
            <div className="flex justify-center mb-8">
              <div className="w-28 h-28 rounded-full border border-black/10 flex items-center justify-center bg-white shadow-lift">
                <div className="text-center">
                  <span className="font-data text-[0.5rem] text-primaryText font-bold uppercase tracking-widest block">Ensemble</span>
                  <span className="font-data text-[0.5rem] text-primaryText font-bold uppercase tracking-widest block">Router</span>
                </div>
              </div>
            </div>

            {/* Route cards */}
            <div className="grid grid-cols-2 gap-4">
              {CANDIDATE_ROUTES.map((route) => (
                <div
                  key={route.id}
                  className={`p-4 rounded-lg border transition-all duration-200 hover:shadow-sm cursor-default bg-white ${
                    route.id === 4
                      ? 'border-accentGold/40 bg-[#FAFAFA]'
                      : 'border-black/[0.06]'
                  }`}
                >
                  <p className={`font-data text-[0.5rem] uppercase tracking-widest mb-1.5 font-bold ${
                    route.id === 4 ? 'text-accentGold' : 'text-secondaryText'
                  }`}>
                    Route {String(route.id).padStart(2, '0')} {route.id === 4 ? '— Exclusive' : ''}
                  </p>
                  <p className="font-hero text-lg text-primaryText font-semibold mb-1.5">{route.name}</p>
                  <p className="font-data text-[0.5rem] text-secondaryText uppercase tracking-wider leading-relaxed">
                    {route.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Cost-Weighted Decision Matrix */}
          <div className="mt-8 pt-5 border-t border-black/5">
            <p className="font-data text-[0.55rem] text-secondaryText uppercase tracking-[0.15em] mb-4">
              Cost-Weighted Decision Matrix
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white p-3 rounded-lg border border-black/[0.06] shadow-sm">
                <p className="font-data text-[0.5rem] text-primaryText uppercase tracking-widest mb-1 font-bold">High-Confidence Activation</p>
                <p className="font-data text-[0.5rem] text-secondaryText uppercase tracking-wider leading-relaxed">
                  Top 10% ML probability (≥0.0219). Direct recommendation. Revenue capture.
                </p>
              </div>
              <div className="bg-[#FAFAFA] p-3 rounded-lg border border-accentGold/20 shadow-sm">
                <p className="font-data text-[0.5rem] text-accentGold uppercase tracking-widest mb-1 font-bold">Systemic Suppression</p>
                <p className="font-data text-[0.5rem] text-secondaryText uppercase tracking-wider leading-relaxed">
                  6,995 High-CLV customers. Active guardrail violation + false positive. Equity protection.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
