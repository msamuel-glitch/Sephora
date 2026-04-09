import { motion } from 'framer-motion';
import { ShoppingBag, Sparkles, Target } from 'lucide-react';

export default function Provocation() {
  return (
    <div className="glass-panel slide-bg slide-bg-storefront w-full flex flex-col p-10 lg:p-14 relative overflow-hidden border-top-gold">
      {/* Decorative perfume mist blob */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-accentPetal/20 via-accentRose/5 to-transparent rounded-full blur-3xl pointer-events-none z-0" />
      {/* Floating Petal Particles */}
      {[...Array(5)].map((_, i) => (
        <div key={i} className="petal-particle" style={{ left: `${15 + i * 18}%`, width: `${6 + i * 2}px`, height: `${6 + i * 2}px`, background: i % 2 === 0 ? 'rgba(236,72,153,0.3)' : 'rgba(202,138,4,0.25)', animationDuration: `${12 + i * 4}s`, animationDelay: `${i * 2}s` }} />
      ))}

      <div className="relative z-10 flex-1 flex flex-col justify-center max-w-5xl mx-auto py-8">
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-6">
            Case 3: Brand Affinity Detection
          </p>

          <h2 className="font-hero text-5xl lg:text-6xl text-primaryText font-bold italic mb-8 leading-tight">
            Which brand will your <br />
            customer buy next?
          </h2>

          <div className="shimmer-line w-32 mb-10" />

          <p className="font-hero text-2xl lg:text-3xl text-secondaryText italic leading-relaxed mb-14 max-w-4xl">
            "Predict which brands a customer is most likely to buy
            — even if never purchased before — to identify cross-sell
            opportunities and size the internal market for emerging brands."
          </p>

          {/* Three Business Objectives */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-14">
            {[
              { Icon: ShoppingBag, title: 'Increase Basket Size', sub: 'AOV from €72.53 → €84.02', highlight: '+15.8% lift' },
              { Icon: Sparkles, title: 'Accelerate Discovery', sub: '239 brands, 50,805 customers', highlight: '18,180 untapped' },
              { Icon: Target, title: 'Personalize Recommendations', sub: 'Affinity scores → CRM actions', highlight: '894 rules' },
            ].map((obj, i) => (
              <motion.div
                key={obj.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + i * 0.15 }}
                className="stat-card text-center hover-iridescent cursor-help"
              >
                <div className="flex justify-center mb-3">
                  <obj.Icon className="w-8 h-8 text-accentRose" strokeWidth={1.5} />
                </div>
                <p className="font-hero text-lg text-primaryText italic font-bold mb-1">{obj.title}</p>
                <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-3">{obj.sub}</p>
                <p className="font-hero text-2xl text-accentGold italic font-bold">{obj.highlight}</p>
              </motion.div>
            ))}
          </div>

          {/* Hook Stat */}
          <div className="bg-bgSoft/60 p-8 rounded-[2rem] border border-accentPetal/20 text-center">
             <p className="font-hero text-xl text-primaryText italic font-semibold leading-relaxed">
               "Customers who discover just one new brand spend <span className="text-accentGold font-bold">€84.02</span> vs <span className="text-tertiaryText">€72.53</span> for non-discoverers.
               That's <span className="text-accentRose font-bold">+€11.49 per customer</span> — and we have 50,805 of them."
             </p>
          </div>
        </motion.div>
      </div>

      <p className="source-tag text-right">Source: step3_4_report.txt lines 139-144 | Sephora France FY2025 sample</p>
    </div>
  );
}
