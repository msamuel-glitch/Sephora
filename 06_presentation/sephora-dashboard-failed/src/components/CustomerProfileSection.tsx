import{BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer,ReferenceLine,PieChart,Pie,Cell}from'recharts';
import{useInView}from'../hooks/useInView';
import{useCountUp}from'../hooks/useCountUp';
import{motion}from'framer-motion';
import{EXPLORER_DATA,ADOPTION_TIMING}from'../data/constants';

export default function CustomerProfileSection(){
  const{ref:r1,inView:v1}=useInView();
  const{ref:r2,inView:v2}=useInView();
  const{ref:r3,inView:v3}=useInView();
  const c1=useCountUp(6188,1500,v2);

  return(
  <section id="s4" className="bg-sephora-warm py-24 px-6 md:px-12">
    <div className="max-w-5xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">THE CUSTOMER / 03</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-black leading-none mb-4">Who is ready to discover</h2>
      <p className="text-sephora-black/60 max-w-[45ch] mb-16 leading-relaxed">We built 19 behavioral features per customer using only January–September data. Three produced commercially actionable insights.</p>

      {/* Finding 1 */}
      <motion.div ref={r1} initial={{opacity:0,y:30}} animate={v1?{opacity:1,y:0}:{}} transition={{duration:0.6}} className="mb-20">
        <p className="font-data text-[clamp(3rem,8vw,6rem)] text-sephora-red leading-none mb-2">0.63</p>
        <p className="font-data text-sm text-sephora-black/50 mb-4">Explorer Index — high frequency customers, all generations</p>
        <p className="text-sephora-black/70 max-w-[45ch] mb-2 leading-relaxed">Any customer visiting every 26 days or fewer has an Explorer Index above 0.63 — regardless of generation. Baby Boomer: 0.65. Gen Z: 0.66. The gap is 0.01.</p>
        <div className="bg-sephora-cream/50 rounded p-3 mb-4 max-w-[50ch]"><p className="text-sm text-sephora-black/40">Study-wide median: 0.41. High-frequency customers score 54% above this.</p></div>
        <div className="bg-white rounded-lg border border-sephora-cream p-4">
          <p className="font-data text-xs text-gray-400 mb-2">THE 50-DAY DISCOVERY WINDOW</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={EXPLORER_DATA} margin={{top:5,right:20,bottom:5,left:0}} barGap={4}>
              <XAxis dataKey="gen" tick={{fontSize:11,fontFamily:'DM Mono'}}/>
              <YAxis domain={[0,0.8]} tick={{fontSize:10,fontFamily:'DM Mono'}}/>
              <Tooltip contentStyle={{fontFamily:'DM Mono',fontSize:'0.75rem'}}/>
              <ReferenceLine y={0.41} stroke="#ccc" strokeDasharray="4 4" label={{value:'Median 0.41',fill:'#999',fontSize:10,position:'right'}}/>
              <Bar dataKey="high" fill="#E2001A" name="High Freq (≤26d)" radius={[3,3,0,0]} animationDuration={1200}/>
              <Bar dataKey="low" fill="#CCCCCC" name="Low Freq" radius={[3,3,0,0]} animationDuration={1200}/>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Finding 2 */}
      <motion.div ref={r2} initial={{opacity:0,y:30}} animate={v2?{opacity:1,y:0}:{}} transition={{duration:0.6}} className="mb-20">
        <p className="font-data text-[clamp(3rem,8vw,6rem)] text-sephora-red leading-none mb-2">{c1.toLocaleString()}</p>
        <p className="font-data text-sm text-sephora-black/50 mb-4">Customers visiting every 26 days or fewer</p>
        <p className="text-sephora-black/70 max-w-[45ch] mb-6 leading-relaxed">90% of these customers — 5,569 people — are already in Sephora's CRM system. They are reachable today.</p>
        <div className="bg-white rounded-lg border border-sephora-cream p-4 inline-block">
          <ResponsiveContainer width={200} height={200}>
            <PieChart><Pie data={[{name:'CRM',value:90},{name:'Other',value:10}]} cx="50%" cy="50%" innerRadius={55} outerRadius={80} dataKey="value" animationDuration={1200}>
              <Cell fill="#E2001A"/><Cell fill="#CCCCCC"/>
            </Pie></PieChart>
          </ResponsiveContainer>
          <p className="font-data text-center text-lg -mt-28 relative z-10">5,569</p>
          <p className="font-data text-center text-xs text-gray-400 mt-24">90% CRM-eligible</p>
        </div>
      </motion.div>

      {/* Finding 3 */}
      <motion.div ref={r3} initial={{opacity:0,y:30}} animate={v3?{opacity:1,y:0}:{}} transition={{duration:0.6}}>
        <p className="font-data text-[clamp(3rem,8vw,6rem)] text-sephora-red leading-none mb-2">63%</p>
        <p className="font-data text-sm text-sephora-black/50 mb-4">Of brand adoptions happened in the same basket — same visit, same day</p>
        <p className="text-sephora-black/70 max-w-[45ch] mb-6 leading-relaxed">126 of 202 observed adoptions occurred on the exact same day. The recommendation must happen in the moment.</p>
        <div className="bg-white rounded-lg border border-sephora-cream p-4">
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={ADOPTION_TIMING} margin={{top:15,right:10,bottom:5,left:0}}>
              <XAxis dataKey="day" tick={{fontSize:10,fontFamily:'DM Mono'}}/>
              <YAxis hide/>
              <Tooltip contentStyle={{fontFamily:'DM Mono',fontSize:'0.75rem'}}/>
              <Bar dataKey="count" radius={[3,3,0,0]} animationDuration={1200}>
                {ADOPTION_TIMING.map((d,i)=>(<Cell key={i} fill={i===0?'#E2001A':'#CCCCCC'}/>))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <p className="font-data text-[0.65rem] text-sephora-red text-center -mt-2">↑ THE MOMENT</p>
        </div>
      </motion.div>
    </div>
  </section>)}
