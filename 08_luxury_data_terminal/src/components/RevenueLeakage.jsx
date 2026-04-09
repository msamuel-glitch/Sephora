import { motion } from 'framer-motion';

const LEAKAGE_DATA = [
  { label: 'Total Potential', value: 583570, color: '#D4AF37', height: 100 },
  { label: 'Discovery Gap', value: -284000, color: '#E2001A', height: 48 },
  { label: 'Cross-Sell Gap', value: -125000, color: '#E2001A', height: 22 },
  { label: 'Captured', value: 174570, color: '#0C0A09', height: 30 },
];

export default function RevenueLeakage() {
  return (
    <div className="glass-panel h-full flex flex-col p-10 relative overflow-hidden bg-white/80 backdrop-blur-3xl">
      <div className="mb-10">
        <p className="font-data text-[0.6rem] text-accentGold uppercase tracking-[0.3em] font-bold mb-3">
          01 The Performance Gap
        </p>
        <h2 className="font-hero text-5xl text-primaryText font-semibold italic max-w-2xl leading-tight">
          Where €409,000 vanishes every quarter.
        </h2>
      </div>

      <div className="flex-1 flex items-end justify-between gap-12 px-10 pb-16 relative">
        {/* Connection Lines (Dashed) */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-10">
          <line x1="25%" y1="20%" x2="50%" y2="20%" stroke="black" strokeDasharray="4 4" />
          <line x1="50%" y1="68%" x2="75%" y2="68%" stroke="black" strokeDasharray="4 4" />
        </svg>

        {LEAKAGE_DATA.map((item, i) => (
          <div key={item.label} className="flex-1 flex flex-col items-center group relative cursor-help">
            <div className="mb-4 text-center">
              <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold mb-1">
                {item.label}
              </p>
              <h4 className={`font-hero text-2xl italic font-bold ${item.value < 0 ? 'text-accentRed' : 'text-primaryText'}`}>
                {item.value < 0 ? `-€${Math.abs(item.value / 1000).toFixed(0)}k` : `€${Math.abs(item.value / 1000).toFixed(0)}k`}
              </h4>
            </div>

            {/* Waterfall Bar (Liquid Glass) */}
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: `${item.height}%`, opacity: 1 }}
              transition={{ duration: 1.5, delay: i * 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="w-full max-w-[120px] relative rounded-2xl overflow-hidden shadow-lift border border-white/40"
              style={{ backgroundColor: `${item.color}20` }}
            >
              {/* Fill layer */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.3 }}
                className="absolute inset-x-0 bottom-0 top-0 opacity-80"
                style={{ backgroundColor: item.color }}
              />

              {/* Gloss highlight */}
              <div className="absolute inset-0 bg-gradient-to-tr from-white/30 to-transparent" />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.4),transparent)]" />
            </motion.div>

            {/* Indicator Dot */}
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 1.5 + i * 0.1 }}
              className={`absolute -bottom-6 w-2 h-2 rounded-full ${item.value < 0 ? 'bg-accentRed animate-pulse' : 'bg-accentGold'}`}
            />
          </div>
        ))}
      </div>

      <div className="mt-6 flex justify-between items-end border-t border-black/5 pt-8">
        <div className="max-w-lg">
          <span className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold">Executive Insight</span>
          <p className="font-hero text-xl text-primaryText italic font-semibold mt-2 leading-relaxed opacity-90">
            "Sephora captures only 30% of its implicit cross-sell potential. The missing €409k is leaked because we lose track of the 'Next Best Brand' during the second trip."
          </p>
        </div>
        
        <div className="flex gap-4">
           <div className="text-right">
              <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">Model Precision</p>
              <p className="font-hero text-xl text-primaryText font-bold italic">94.2%</p>
           </div>
           <div className="text-right">
              <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">Holdout Validation</p>
              <p className="font-hero text-xl text-primaryText font-bold italic">CLEAN</p>
           </div>
        </div>
      </div>
    </div>
  );
}
