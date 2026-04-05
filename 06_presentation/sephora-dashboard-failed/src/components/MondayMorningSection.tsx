import{motion}from'framer-motion';
import{useInView}from'../hooks/useInView';

export default function MondayMorningSection(){
  const{ref,inView}=useInView(0.1);
  return(
  <section id="s8" className="bg-sephora-warm py-24 px-6 md:px-12" ref={ref}>
    <div className="max-w-6xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">ACTIVATION / 07</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-black leading-none mb-10">What happens next</h2>

      <motion.div initial={{opacity:0,y:30}} animate={inView?{opacity:1,y:0}:{}} transition={{duration:0.6}}
        className="grid md:grid-cols-2 gap-12 md:gap-16">
        <div>
          <h3 className="font-body font-medium text-sephora-black mb-6">Three actions traceable to this data</h3>
          <div className="space-y-6">
            <div><p className="font-body font-medium text-sm text-sephora-black mb-1">For the CRM & App team:</p>
              <p className="text-sm text-sephora-black/70 leading-relaxed">Deploy point-of-purchase recommendations for the 11 validated pairs. 63% of adoptions happen same-day — trigger the recommendation at basket add, not days later.</p>
              <p className="font-data text-[0.65rem] text-sephora-black/40 mt-1">Source: 63% same-day adoption (126 of 202)</p></div>
            <div><p className="font-body font-medium text-sm text-sephora-black mb-1">For Beauty Advisors:</p>
              <p className="text-sm text-sephora-black/70 leading-relaxed">Brief every advisor on the 11 directional pairs. HOURGLASS customer: ask about MAKEUP BY MARIO. 8.52× lift. 31 validated baskets.</p>
              <p className="font-data text-[0.65rem] text-sephora-black/40 mt-1">Source: Lead pair, highest absolute support</p></div>
            <div><p className="font-body font-medium text-sm text-sephora-black mb-1">For Brand Managers:</p>
              <p className="text-sm text-sephora-black/70 leading-relaxed">BOBBI BROWN: 18,180 warm prospects. SUMMER FRIDAYS: 16,814. DRUNK ELEPHANT: 16,482. These are customer lists, not projections.</p>
              <p className="font-data text-[0.65rem] text-sephora-black/40 mt-1">Source: brand_addressable_market.csv</p></div>
          </div>
        </div>
        <div>
          <h3 className="font-body font-medium text-sephora-black/50 mb-6">Three things we do not yet do</h3>
          <div className="space-y-6 text-sm text-sephora-black/60 leading-relaxed">
            <div><p className="font-body font-medium text-sephora-black/70 mb-1">Sequential journeys — Horizon 2</p>We recommend one brand per occasion. Next: which sequence over three visits maximizes customer lifetime value.</div>
            <div><p className="font-body font-medium text-sephora-black/70 mb-1">Consideration set — Horizon 2</p>Two recommended brands may compete for the same occasion. Next: occasion-level routing.</div>
            <div><p className="font-body font-medium text-sephora-black/70 mb-1">Lapsed customers — Horizon 3</p>Our model learns from active customers. High-value lapsed customers are not yet in scope.</div>
            <div><p className="font-body font-medium text-sephora-black/70 mb-1">Seasonal regime — Horizon 2</p>The model was trained on Jan–Sep standard behavior. December gifting is a distinct pattern. A production system requires a seasonal variant.</div>
          </div>
        </div>
      </motion.div>

      <p className="font-display italic text-xl md:text-2xl text-center text-sephora-black mt-20 max-w-[55ch] mx-auto leading-snug">We did not build a recommendation engine. We built a system that finds the moment — before it happens — when a customer is about to discover a brand she has never tried. And we made sure nothing gets in the way of that moment.</p>
      <p className="font-data text-[0.6rem] text-sephora-black/30 text-center mt-8 max-w-[50ch] mx-auto">Study base: 50,805 customers, France 2025. All figures sourced from validated project outputs. No projections beyond stated scope.</p>
    </div>
  </section>)}
