import{motion}from'framer-motion';
import{BarChart,Bar,XAxis,YAxis,ResponsiveContainer,Cell}from'recharts';
import{useInView}from'../hooks/useInView';
import{useCountUp}from'../hooks/useCountUp';

export default function ProtectionLayerSection(){
  const{ref,inView}=useInView(0.1);
  const protectedCount=useCountUp(6995,1500,inView);
  const boomData=[{name:'Boomer Haircare',v:0.81},{name:'Study Average',v:5.26}];

  return(
  <section id="s7" className="bg-sephora-black py-24 px-6 md:px-12" ref={ref}>
    <div className="max-w-5xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">THE SAFEGUARD / 06</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-white leading-none mb-4">Knowing when not to recommend</h2>
      <p className="text-white/50 max-w-[45ch] mb-12">Every recommendation system maximizes reward. Ours also formalizes the cost of being wrong.</p>

      <div className="space-y-4">
        <motion.div initial={{opacity:0,y:30}} animate={inView?{opacity:1,y:0}:{}} transition={{delay:0,duration:0.5}} className="dark-card rounded-lg p-6">
          <p className="font-data text-4xl text-white mb-2">15</p>
          <p className="font-data text-sm text-white/40 mb-3">Brand pairs permanently blocked</p>
          <p className="text-sm text-white/50">Margin-dilutive pairings and luxury-mid-range conflicts. Blocked regardless of lift score.</p>
        </motion.div>

        <motion.div initial={{opacity:0,y:30}} animate={inView?{opacity:1,y:0}:{}} transition={{delay:0.15,duration:0.5}} className="dark-card rounded-lg p-6">
          <p className="font-data text-4xl text-white mb-2">14</p>
          <p className="font-data text-sm text-white/40 mb-3">Haircare brands suppressed for Baby Boomers</p>
          <p className="text-sm text-white/50 mb-4">Model accuracy for Baby Boomers in Haircare: 0.81%. Study-wide: 5.26%. The gap disqualifies.</p>
          <div className="max-w-[250px]">
            <ResponsiveContainer width="100%" height={80}>
              <BarChart data={boomData} layout="vertical" margin={{top:0,right:30,bottom:0,left:80}}>
                <XAxis type="number" domain={[0,6]} hide/>
                <YAxis type="category" dataKey="name" tick={{fontSize:10,fontFamily:'DM Mono',fill:'#888'}} width={80}/>
                <Bar dataKey="v" radius={[0,3,3,0]} animationDuration={800}>
                  <Cell fill="#E2001A"/><Cell fill="#555"/>
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div initial={{opacity:0,y:30}} animate={inView?{opacity:1,y:0}:{}} transition={{delay:0.3,duration:0.5}}
          className="rounded-lg p-6 bg-[#0F0F0F] border-2 border-sephora-red">
          <p className="font-data text-[clamp(2.5rem,5vw,4rem)] text-sephora-red mb-2">{protectedCount.toLocaleString()}</p>
          <p className="font-data text-sm text-white/40 mb-4">High-value customers protected</p>
          <div className="font-data text-sm text-white/80 bg-sephora-black rounded p-4 leading-loose mb-4">
            6,995 customers<br/>× €70.26 average basket value<br/>
            <span className="text-white/30">─────────────────────────────</span><br/>
            <span className="text-sephora-red font-medium text-lg">€491,476</span> in relationship equity protected
          </div>
          <p className="text-sm text-white/50">These customers received no guardrail-violating recommendation. <span className="font-display italic text-white text-lg">Zero.</span></p>
        </motion.div>
      </div>

      <p className="font-display italic text-xl md:text-2xl text-center text-white/80 mt-16 max-w-[55ch] mx-auto">The difference between a model and a deployable system is knowing the cost of being wrong.</p>
    </div>
  </section>)}
