import { motion } from 'framer-motion';
import { ShieldAlert, TrendingDown, Users, ShieldCheck } from 'lucide-react';

export default function IntegrityShield() {
  return (
    <div className="glass-panel slide-bg slide-bg-leather w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="absolute bottom-0 right-0 w-80 h-80 bg-gradient-to-tl from-accentGold/8 to-transparent rounded-full blur-3xl pointer-events-none z-0" />

      <div className="relative z-10">
        <p className="font-data text-[0.65rem] text-accentRose uppercase tracking-[0.4em] font-bold mb-4">
          Protection Pillar — The Integrity Shield
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-3 leading-tight">
          The Cost of Being Wrong.
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">
          A bad recommendation doesn't just miss a sale. It erodes brand trust and causes churn.
        </p>

        <div className="grid grid-cols-12 gap-8 mb-8">
          {/* Left: LTV Logic */}
          <div className="col-span-12 lg:col-span-6 space-y-5">
            <div className="bg-bgCard p-6 rounded-2xl border-l-4 border-accentRed shadow-lift hover:border-accentGold transition-colors">
              <div className="flex items-center gap-3 mb-3">
                <TrendingDown className="w-6 h-6 text-accentRed" strokeWidth={1.5} />
                <h4 className="font-hero text-xl italic font-bold text-primaryText">The Danger of Raw Machine Learning</h4>
              </div>
              <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest leading-relaxed">
                Raw models will recommend trendy teen haircare (e.g., OLAPLEX, BRIOGEO) to ultra-high-net-worth 
                Baby Boomers simply because the brands are mathematically popular. This generation mismatch destroys the luxury mirage.
              </p>
            </div>

            <div className="bg-bgCard p-6 rounded-2xl border-l-4 border-accentLavender shadow-lift hover:border-accentGold transition-colors">
              <div className="flex items-center gap-3 mb-3">
                <ShieldAlert className="w-6 h-6 text-accentLavender" strokeWidth={1.5} />
                <h4 className="font-hero text-xl italic font-bold text-primaryText">The Do-Not-Recommend Layer</h4>
              </div>
              <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest leading-relaxed">
                We programmed a commercial shield overriding the ML. It permanently blocks 14 trend brands from Boomer profiles 
                and restricts margin-dilutive pairs. If a recommendation violates the Sephora DNA, it is killed before reaching the customer.
              </p>
            </div>
          </div>

          {/* Right: Key Metrics / LTV Protected */}
          <div className="col-span-12 lg:col-span-6 flex flex-col gap-5">
            <div className="stat-card border-top-gold text-center shadow-glow-gold py-10">
              <p className="font-data text-[0.55rem] text-accentGold uppercase tracking-widest font-bold mb-3 flex items-center justify-center gap-2">
                <ShieldCheck className="w-4 h-4" /> Lifetime Value (LTV) Protected
              </p>
              <p className="font-hero text-6xl text-accentGold italic font-bold mb-2">€491,476</p>
              <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest px-8">
                The total historical basket value of the VIPs we shielded from mathematically "correct" but commercially toxic recommendations.
              </p>
            </div>

            <div className="flex gap-5">
              <div className="flex-1 stat-card text-center py-6">
                <p className="font-data text-[0.55rem] text-accentRose uppercase tracking-widest font-bold mb-2 flex items-center justify-center gap-1"><Users className="w-3 h-3"/> Shield Activations</p>
                <p className="font-hero text-3xl text-primaryText italic font-bold">6,995</p>
                <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest mt-1">High-CLV Customers blocked</p>
              </div>
              <div className="flex-1 stat-card text-center py-6 border-left-rose">
                <p className="font-data text-[0.55rem] text-accentRose uppercase tracking-widest font-bold mb-2">Protection Rate</p>
                <p className="font-hero text-3xl text-primaryText italic font-bold">53.6%</p>
                <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest mt-1">Of bad recommendations killed</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-bgSoft/40 p-6 rounded-2xl border border-accentPetal/15">
          <p className="font-hero text-lg text-primaryText italic font-semibold leading-relaxed text-center">
            "A recommender system that only tries to increase conversion is a liability. 
            We built a system that <span className="text-accentGold font-bold">prioritizes the protection of the client relationship</span> above the immediate sale."
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: suppression_logic.txt | do_not_recommend_layer.csv</p>
    </div>
  );
}
