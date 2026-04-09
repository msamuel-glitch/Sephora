import { motion } from 'framer-motion';

const GENZ = {
  title: 'Gen Z: The Discovery Engine',
  subtitle: '1,425 high-frequency customers • Explorer Index: 0.73',
  image: '/persona_genz_viral.png',
  color: 'accentRose',
  stats: [
    { label: 'Top Axis', value: 'Make Up (43.6%)', sub: 'Digital-native brand mix' },
    { label: 'Brand Preference', value: '47.7% Exclusive', sub: 'Already premium — not entry-level' },
    { label: 'CRM Channel', value: '91.6% CRM Push', sub: 'App + email responsive' },
    { label: 'Explorer Index', value: '0.73 median', sub: 'Highest willingness to discover' },
  ],
  topBrand: 'HUDA BEAUTY → 71.4% repeat in Make Up, €30.49/basket',
  mondayAction: 'Push ILIA → KOSAS (13.7× lift) in-app at checkout for Gen Z make up buyers',
  retention: '57.9% retention rate | 3.44 brands explored | €208 total spend/client',
};

const BOOMER = {
  title: 'Baby Boomers: The Loyalty Fortress',
  subtitle: '465 high-frequency customers • Explorer Index: 0.64',
  image: '/persona_boomer_luxury.png',
  color: 'accentGold',
  stats: [
    { label: 'Top Axis', value: 'Fragrance (32.2%)', sub: 'Heritage fragrance loyalty' },
    { label: 'Brand Preference', value: '65.2% Selective', sub: 'DIOR, GUERLAIN, CHANEL dominate' },
    { label: 'CRM Channel', value: '84.9% CRM Push', sub: '+14.4% Store guidance needed' },
    { label: 'Avg Basket', value: '€46.11', sub: 'Highest per-visit value' },
  ],
  topBrand: 'CHANEL Fragrance → 74.5% repeat, €82.11/basket',
  mondayAction: 'Fragrance-first CRM sequence. Suppress all 14 haircare brands. Protect the relationship.',
  retention: '50.2% retention BUT €203 total spend/client | 3,176 single-visit = reactivation goldmine',
};

export default function GrowthEngines({ initialSegment = 'viral-acquisitors' }) {
  const persona = initialSegment === 'viral-acquisitors' ? GENZ : BOOMER;
  const accentColor = persona.color;

  return (
    <div className="glass-panel w-full flex flex-col p-10 lg:p-14 relative overflow-hidden">
      <div className="relative z-10">
        <p className={`font-data text-[0.65rem] text-${accentColor} uppercase tracking-[0.4em] font-bold mb-4`}>
          Persona Activation — Rubric: Actionability
        </p>
        <h2 className="font-hero text-4xl lg:text-5xl text-primaryText font-bold italic mb-2 leading-tight">
          {persona.title}
        </h2>
        <p className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest mb-10">{persona.subtitle}</p>

        <div className="grid grid-cols-12 gap-8 mb-8">
          {/* Left: Persona Image */}
          <div className="col-span-12 lg:col-span-5">
            <div className="rounded-[2rem] overflow-hidden border border-borderSubtle shadow-lift aspect-[3/4] bg-bgSoft flex items-center justify-center">
              <img
                src={persona.image}
                alt={persona.title}
                className="w-full h-full object-cover"
                onError={(e) => { e.target.style.display = 'none'; }}
              />
            </div>
          </div>

          {/* Right: Stats */}
          <div className="col-span-12 lg:col-span-7 flex flex-col gap-4">
            {persona.stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="stat-card flex justify-between items-center"
              >
                <div>
                  <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest font-bold">{stat.label}</p>
                  <p className="font-hero text-xl italic font-bold text-primaryText mt-1">{stat.value}</p>
                </div>
                <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest max-w-[200px] text-right">{stat.sub}</p>
              </motion.div>
            ))}

            {/* Purchase Pattern */}
            <div className="bg-bgSoft/60 p-5 rounded-2xl border border-borderSubtle">
              <p className="font-data text-[0.5rem] text-accentGold uppercase tracking-widest font-bold mb-2">Top Behavioral Rule</p>
              <p className="font-hero text-sm italic text-primaryText leading-relaxed">{persona.topBrand}</p>
            </div>

            <div className="bg-bgSoft/40 p-4 rounded-xl">
              <p className="font-data text-[0.45rem] text-tertiaryText uppercase tracking-widest">{persona.retention}</p>
            </div>
          </div>
        </div>

        {/* Monday Morning Action */}
        <div className={`bg-bgCard p-6 rounded-2xl border-l-4 border-${accentColor} shadow-lift`}>
          <div className="flex items-center gap-3 mb-3">
            <div className={`w-3 h-3 rounded-full bg-${accentColor} animate-pulse`} />
            <p className="font-data text-[0.55rem] text-primaryText uppercase tracking-widest font-bold">Monday Morning Action</p>
          </div>
          <p className="font-hero text-xl italic font-bold text-primaryText leading-relaxed">
            {persona.mondayAction}
          </p>
        </div>
      </div>

      <p className="source-tag text-right mt-6">Source: step3_4_report.txt | sephora_analysis_summary.pdf</p>
    </div>
  );
}
