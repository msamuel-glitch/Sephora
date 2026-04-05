import{useState}from'react';
import{motion,AnimatePresence}from'framer-motion';
import{ScatterChart,Scatter,XAxis,YAxis,Tooltip,ReferenceLine,ResponsiveContainer,Cell}from'recharts';
import{BRAND_PAIRS,CATEGORIES,CAT_COLORS}from'../data/constants';
import{useInView}from'../hooks/useInView';
import{CheckCircle}from'lucide-react';

export default function BrandPairsSection(){
  const[filter,setFilter]=useState<string>('All');
  const[hoveredIdx,setHoveredIdx]=useState<number|null>(null);
  const{ref,inView}=useInView(0.05);
  const filtered=filter==='All'?BRAND_PAIRS:BRAND_PAIRS.filter(p=>p.cat.includes(filter));
  const scatterData=BRAND_PAIRS.map((p,i)=>({x:p.lift,y:p.baskets,name:`${p.anchor} → ${p.rec}`,cat:p.cat,idx:i}));

  return(
  <section id="s3" className="bg-sephora-white sephora-stripe py-24 px-6 md:px-12" ref={ref}>
    <div className="max-w-6xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">THE SIGNAL / 02</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-black leading-none mb-4">What 45,446 baskets are saying</h2>

      <div className="bg-gray-50 rounded p-4 mb-8 max-w-[55ch]">
        <p className="text-sm text-gray-500 leading-relaxed">Lift measures how much more often two brands appear together vs. chance. Lift 1.0 = random. We show pairs above 8.0× with verified basket observations.</p>
      </div>

      <div className="bg-white rounded-lg border border-gray-100 p-6 mb-8">
        <p className="font-data text-xs text-gray-400 mb-3">LIFT × BASKET SUPPORT SCATTER</p>
        <ResponsiveContainer width="100%" height={280}>
          <ScatterChart margin={{top:10,right:20,bottom:10,left:10}}>
            <XAxis dataKey="x" type="number" name="Lift" tick={{fontSize:11,fontFamily:'DM Mono'}} label={{value:'Lift Score ×',position:'bottom',fontSize:11,fontFamily:'DM Mono'}}/>
            <YAxis dataKey="y" type="number" name="Baskets" tick={{fontSize:11,fontFamily:'DM Mono'}} label={{value:'Basket Count',angle:-90,position:'insideLeft',fontSize:11,fontFamily:'DM Mono'}}/>
            <Tooltip content={({payload})=>{if(!payload?.length)return null;const d=payload[0].payload;return(
              <div className="bg-sephora-black text-white p-3 rounded text-xs font-data"><p className="text-sephora-red mb-1">{d.name}</p><p>Lift: {d.x}×</p><p>Baskets: {d.y}</p></div>)}}/>
            <ReferenceLine x={1} stroke="#ccc" strokeDasharray="4 4" label={{value:'Random chance',fill:'#999',fontSize:10}}/>
            <Scatter data={scatterData} onMouseEnter={(_,i)=>setHoveredIdx(i)} onMouseLeave={()=>setHoveredIdx(null)}>
              {scatterData.map((d,i)=>(<Cell key={i} fill={CAT_COLORS[d.cat]||'#E2001A'} r={hoveredIdx===i?8:5} opacity={hoveredIdx!==null&&hoveredIdx!==i?0.3:1}/>))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      <div className="flex gap-2 mb-8 flex-wrap">
        {CATEGORIES.map(c=>(
          <button key={c} onClick={()=>setFilter(c)}
            className={`font-data text-xs px-4 py-2 rounded-full border transition-all ${filter===c?'bg-sephora-red text-white border-sephora-red':'bg-white text-gray-500 border-gray-200 hover:border-sephora-red'}`}>{c}</button>
        ))}
      </div>

      <AnimatePresence mode="popLayout">
        {filtered.map((p,i)=>(
          <motion.div key={p.anchor+p.rec} layout initial={{opacity:0,y:40}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-20}}
            transition={{duration:0.4,delay:i*0.05}}
            className={`py-6 border-b border-gray-100 ${hoveredIdx!==null&&BRAND_PAIRS[hoveredIdx]===p?'bg-red-50/50 -mx-4 px-4 rounded':''}`}>
            <div className="flex flex-wrap items-baseline gap-3 mb-2">
              <span className="font-body font-medium text-lg text-sephora-black">{p.anchor}</span>
              <span className="text-sephora-red text-2xl">→</span>
              <span className="font-body font-medium text-lg text-sephora-red">{p.rec}</span>
              {p.label&&<span className="font-data text-[0.6rem] text-sephora-red border border-sephora-red px-2 py-0.5 rounded">{p.label}</span>}
            </div>
            <div className="flex flex-wrap items-baseline gap-6 mb-2">
              <span className="font-data text-3xl text-sephora-black">{p.lift}<span className="text-sephora-red">×</span></span>
              <span className="font-data text-xs text-gray-400">Observed in {p.baskets} real baskets</span>
              <span className="font-data text-[0.65rem] text-gray-400 uppercase tracking-wider">{p.cat}</span>
              <span className="font-data text-[0.6rem] text-green-600 flex items-center gap-1"><CheckCircle size={12}/>p &lt; {p.p?.toFixed(4)}</span>
            </div>
            <p className="text-sm text-gray-500 max-w-[55ch]">{p.exp}</p>
          </motion.div>
        ))}
      </AnimatePresence>

      <p className="font-display text-xl md:text-2xl text-center text-sephora-black mt-12 max-w-[55ch] mx-auto">
        <span className="text-sephora-red">63%</span> of these conversations happen in one visit. The channel is not email. It is the beauty advisor next to the shelf.
      </p>
    </div>
  </section>)}
