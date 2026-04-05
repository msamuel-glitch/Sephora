import{useInView}from'../hooks/useInView';
import{motion}from'framer-motion';
const steps=[
  {text:'Visit 1 — Buys DRUNK ELEPHANT Skincare'},
  {text:'Visit 2 — Buys DRUNK ELEPHANT again'},
  {text:'Visit 3 — Walks past FRESH SAS on the shelf'},
  {text:'11.73× signal. Nobody said a word.',accent:true},
  {text:'She leaves. She comes back less often.'},
  {text:'Pattern observed across customers sharing this exact profile. Data fully anonymized.',mono:true},
];
export default function MissedMomentSection(){
  const{ref,inView}=useInView(0.1);
  return(
  <section id="s2" className="min-h-screen bg-sephora-white sephora-stripe relative py-24 px-6 md:px-12" ref={ref}>
    <div className="max-w-4xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">THE MISSED MOMENT / 01</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-black leading-none mb-8">The conversation that never happened</h2>
      <p className="font-body text-sephora-black/70 max-w-[45ch] mb-4 leading-relaxed">DRUNK ELEPHANT customers are 11.73 times more likely to want FRESH SAS than the average Sephora customer. That conversation never happened.</p>
      <div className="mt-10 space-y-0">
        {steps.map((s,i)=>(
          <motion.div key={i} initial={{opacity:0,x:-20}} animate={inView?{opacity:1,x:0}:{}}
            transition={{delay:i*0.2,duration:0.5}}
            className={`py-4 pl-5 border-l-2 ${s.accent?'border-sephora-red text-sephora-red font-medium':'border-gray-200 text-sephora-black/80'} ${s.mono?'font-data text-sm text-gray-400':''}`}>
            <span className="font-data text-[0.65rem] text-gray-400 block mb-1">0{i+1}</span>
            {s.text}
          </motion.div>
        ))}
      </div>
      <p className="font-display text-2xl md:text-3xl text-center text-sephora-black mt-16">We found this signal in <span className="text-sephora-red">45,446</span> baskets.</p>
    </div>
  </section>)}
