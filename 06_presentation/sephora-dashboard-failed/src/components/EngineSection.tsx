import{motion}from'framer-motion';
import{BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer,Cell,LabelList}from'recharts';
import{useInView}from'../hooks/useInView';
import{MODEL_COMPARISON,SHAP_ACTIONABLE,SHAP_DESCRIPTIVE}from'../data/constants';

const routes=[
  {n:'01',title:'The Basket',sub:'What customers buy together',desc:'45,446 baskets analyzed. Pairs appearing together 50% more than chance entered the candidate pool.'},
  {n:'02',title:'The Twin',sub:'Who buys like you',desc:'50,805 customer profiles compared. Brands bought by your behavioral twin become your candidates.'},
  {n:'03',title:'The Category',sub:'Where you already spend',desc:'Every customer has a dominant axis: makeup, skincare, fragrance, haircare. Unpurchased brands in that axis enter the pool.'},
  {n:'04',title:'The New Arrival',sub:'Brands with no history yet',desc:'New brands have no basket data. We map them to their closest established proxy and inherit that audience.'},
];

export default function EngineSection(){
  const{ref,inView}=useInView(0.1);
  return(
  <section id="s5" className="bg-sephora-black py-24 px-6 md:px-12" ref={ref}>
    <div className="max-w-6xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">THE SYSTEM / 04</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-white leading-none mb-4">How the system finds the signal</h2>
      <p className="text-white/50 max-w-[45ch] mb-12">12 million possible combinations. 50,805 × 239 brands. We scored 2.37 million meaningful ones.</p>

      <div className="grid md:grid-cols-2 gap-4 mb-20">
        {routes.map((r,i)=>(
          <motion.div key={i} initial={{opacity:0,y:30}} animate={inView?{opacity:1,y:0}:{}} transition={{delay:i*0.1,duration:0.5}}
            whileHover={{y:-4,boxShadow:'0 8px 30px rgba(226,0,26,0.15)'}}
            className="glass-card rounded-lg p-6 transition-all cursor-default">
            <p className="font-data text-sephora-red text-sm mb-2">ROUTE {r.n}</p>
            <h3 className="font-display text-2xl text-white mb-1">{r.title}</h3>
            <p className="font-data text-xs text-white/40 mb-3">{r.sub}</p>
            <p className="text-sm text-white/60 leading-relaxed">{r.desc}</p>
          </motion.div>
        ))}
      </div>

      <h3 className="font-display text-[clamp(2rem,4vw,3.5rem)] text-sephora-white mb-6">Three systems. One test.</h3>
      <div className="bg-white/[0.03] rounded-lg p-4 mb-6 max-w-[55ch]">
        <p className="text-sm text-white/40 leading-relaxed">We locked away Oct–Dec data completely. Built on Jan–Sep only. P@3 = of every 3 recommendations, how many correct.</p>
      </div>

      <div className="bg-white/[0.02] rounded-lg p-6 mb-12">
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={MODEL_COMPARISON} layout="vertical" margin={{top:5,right:60,bottom:5,left:100}}>
            <XAxis type="number" domain={[0,6]} tick={{fontSize:10,fontFamily:'DM Mono',fill:'#888'}}/>
            <YAxis type="category" dataKey="name" tick={{fontSize:11,fontFamily:'DM Mono',fill:'#aaa'}} width={100}/>
            <Tooltip contentStyle={{background:'#0A0A0A',border:'1px solid #E2001A',fontFamily:'DM Mono',fontSize:'0.75rem',color:'#fff'}}/>
            <Bar dataKey="pct" radius={[0,4,4,0]} animationDuration={1200}>
              {MODEL_COMPARISON.map((d,i)=>(<Cell key={i} fill={d.color}/>))}
              <LabelList dataKey="pct" position="right" formatter={(v:number)=>v+'%'} style={{fontSize:12,fontFamily:'DM Mono',fill:'#fff'}}/>
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="font-data text-xs text-sephora-red mt-2">31% improvement over baseline · 1.24pp gap</p>
      </div>

      <h3 className="font-display text-2xl text-sephora-white mb-6">What the model learned to look for</h3>
      <p className="text-sm text-white/40 mb-6">13 of the top 20 predictive features are ones Sephora can directly influence.</p>
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h4 className="font-data text-xs text-sephora-red tracking-wider mb-4 pb-2 border-b border-sephora-red/30">SEPHORA CAN ACT ON</h4>
          <ul className="space-y-2">{SHAP_ACTIONABLE.map(f=>(
            <li key={f.tech} className="text-sm text-white/70"><span className="text-white/90">{f.label}</span><br/><span className="font-data text-[0.65rem] text-white/30">{f.tech}</span></li>
          ))}</ul>
        </div>
        <div>
          <h4 className="font-data text-xs text-white/40 tracking-wider mb-4 pb-2 border-b border-white/10">DESCRIPTIVE ONLY</h4>
          <ul className="space-y-2">{SHAP_DESCRIPTIVE.map(f=>(
            <li key={f.tech} className="text-sm text-white/50"><span className="text-white/60">{f.label}</span><br/><span className="font-data text-[0.65rem] text-white/20">{f.tech}</span></li>
          ))}</ul>
        </div>
      </div>
      <p className="text-sm text-white/30 mt-6">Left column: the levers. Right column: the context. The system acts on levers.</p>
    </div>
  </section>)}
