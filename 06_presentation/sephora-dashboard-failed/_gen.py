import os
B=r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\06_presentation\sephora-dashboard\src'

def w(path,content):
    fp=os.path.join(B,path)
    os.makedirs(os.path.dirname(fp),exist_ok=True)
    with open(fp,'w',encoding='utf-8') as f: f.write(content)
    print(f'  wrote {path}')

# === HOOKS ===
w('hooks/useCountUp.ts','''import{useState,useEffect,useRef}from'react';
export function useCountUp(target:number,duration=1500,trigger=true){
  const[val,setVal]=useState(0);const started=useRef(false);
  useEffect(()=>{if(!trigger||started.current)return;started.current=true;
    const start=performance.now();
    function tick(now:number){const p=Math.min((now-start)/duration,1);
      setVal(Math.floor(p*target));if(p<1)requestAnimationFrame(tick)}
    requestAnimationFrame(tick)},[target,duration,trigger]);
  return val}
''')

w('hooks/useInView.ts','''import{useState,useEffect,useRef}from'react';
export function useInView(threshold=0.2){
  const ref=useRef<HTMLDivElement>(null);const[inView,setInView]=useState(false);
  useEffect(()=>{if(!ref.current)return;
    const obs=new IntersectionObserver(([e])=>{if(e.isIntersecting)setInView(true)},{threshold});
    obs.observe(ref.current);return()=>obs.disconnect()},[threshold]);
  return{ref,inView}}
''')

# === SEPHORA LOGO ===
w('components/SephoraLogo.tsx','''export default function SephoraLogo(){return(
<svg viewBox="0 0 200 40" className="h-8" aria-label="Sephora">
<rect width="200" height="40" fill="#0A0A0A"/>
<g fill="#FAFAFA">
<rect x="8" y="10" width="16" height="2"/>
<rect x="8" y="15" width="16" height="2"/>
<rect x="8" y="20" width="16" height="2"/>
<rect x="8" y="25" width="16" height="2"/>
</g>
<text x="32" y="26" fill="#FAFAFA" fontFamily="\'DM Sans\',sans-serif" fontWeight="700" fontSize="16" letterSpacing="3">SEPHORA</text>
</svg>)}
''')

# === NAVIGATION ===
w('components/Navigation.tsx','''import{useState,useEffect}from'react';
import SephoraLogo from'./SephoraLogo';
import{SECTION_NAMES}from'../data/constants';
export default function Navigation(){
  const[progress,setProgress]=useState(0);
  const[section,setSection]=useState(0);
  useEffect(()=>{
    const onScroll=()=>{const h=document.documentElement.scrollHeight-window.innerHeight;
      setProgress(window.scrollY/h*100);
      const sections=document.querySelectorAll('section[id]');
      sections.forEach((s,i)=>{const r=s.getBoundingClientRect();
        if(r.top<window.innerHeight/2&&r.bottom>0)setSection(i)})};
    window.addEventListener('scroll',onScroll);return()=>window.removeEventListener('scroll',onScroll)},[]);
  return(<>
    <nav className="fixed top-0 left-0 right-0 z-50 bg-sephora-black/90 backdrop-blur-md">
      <div className="flex items-center justify-between px-6 py-3">
        <SephoraLogo/>
        <span className="font-data text-xs tracking-widest text-sephora-white/60 hidden md:block">{SECTION_NAMES[section]}</span>
        <span className="font-data text-xs text-sephora-red">{section+1} / 8</span>
      </div>
      <div className="h-[2px] bg-sephora-red transition-all duration-100" style={{width:`${progress}%`}}/>
    </nav>
  </>)}
''')

# === SECTION 1 HERO ===
w('components/HeroSection.tsx','''import{motion}from'framer-motion';
export default function HeroSection(){
  const chars='€583,570'.split('');
  return(
  <section id="s1" className="min-h-screen bg-sephora-black relative flex items-center overflow-hidden pt-16">
    <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none">
      <span className="font-display text-[20vw] text-white/[0.03] whitespace-nowrap">SEPHORA FRANCE 2025</span>
    </div>
    <div className="relative z-10 w-full max-w-7xl mx-auto px-6 md:px-12 grid md:grid-cols-[40%_60%] gap-8 items-center">
      <div>
        <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">BRAND AFFINITY INTELLIGENCE — FRANCE 2025</p>
        <p className="font-display italic text-2xl md:text-3xl text-sephora-white/90 leading-snug mb-8">Your customers are already telling you which brand they will buy next. The signal is in your data. We built the system that reads it.</p>
        <p className="font-data text-xs text-white/40 leading-relaxed">Study base: 50,805 loyalty card customers<br/>Source: holdout window evaluation Oct–Dec 2025</p>
      </div>
      <div className="text-right">
        <div className="font-display text-[clamp(4rem,12vw,14rem)] leading-none text-sephora-white tracking-tight">
          {chars.map((c,i)=>(
            <motion.span key={i} initial={{y:'110%',opacity:0}} animate={{y:0,opacity:1}}
              transition={{delay:0.3+i*0.06,duration:0.7,ease:[0.22,1,0.36,1]}}
              className="inline-block">{c}</motion.span>
          ))}
        </div>
        <motion.div className="h-[1px] bg-sephora-red mt-2" initial={{width:0}} animate={{width:'100%'}} transition={{delay:1.2,duration:1.5}}/>
        <p className="font-data text-xs text-white/40 mt-4">in incremental basket opportunity</p>
      </div>
    </div>
    <motion.div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/30 text-2xl"
      animate={{y:[0,8,0],opacity:[0.3,1,0.3]}} transition={{duration:2,repeat:Infinity}}
      initial={{opacity:0.3}}>↓</motion.div>
  </section>)}
''')

# === SECTION 2 MISSED MOMENT ===
w('components/MissedMomentSection.tsx','''import{useInView}from'../hooks/useInView';
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
''')

# === SECTION 3 BRAND PAIRS DASHBOARD ===
w('components/BrandPairsSection.tsx','''import{useState}from'react';
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
''')

# === SECTION 4 CUSTOMER PROFILE ===
w('components/CustomerProfileSection.tsx','''import{BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer,ReferenceLine,PieChart,Pie,Cell}from'recharts';
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
''')

# === SECTION 5 ENGINE ===
w('components/EngineSection.tsx','''import{motion}from'framer-motion';
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
''')

# === SECTION 6 ADDRESSABLE MARKET ===
w('components/AddressableMarketSection.tsx','''import{BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer}from'recharts';
import{motion}from'framer-motion';
import{useInView}from'../hooks/useInView';
import{useCountUp}from'../hooks/useCountUp';
import{ADDRESSABLE_MARKET}from'../data/constants';

function BrandRow({b,i}:{b:typeof ADDRESSABLE_MARKET[0],i:number}){
  const{ref,inView}=useInView(0.3);
  const count=useCountUp(b.count,1500,inView);
  return(
    <motion.div ref={ref} initial={{opacity:0,y:30}} animate={inView?{opacity:1,y:0}:{}} transition={{delay:i*0.1,duration:0.5}}
      className="py-6 border-b border-gray-100">
      <div className="flex justify-between items-baseline mb-1">
        <span className="font-display text-2xl md:text-3xl text-sephora-black">{b.brand}</span>
        <span className="font-data text-[0.65rem] text-gray-400 border border-gray-200 px-2 py-0.5 rounded">{b.segment}</span>
      </div>
      <p className="font-data text-[clamp(2.5rem,6vw,5rem)] text-sephora-red leading-none my-2">{count.toLocaleString()}</p>
      <p className="text-sm text-gray-500 mb-1">customers with high-affinity signals who have never purchased this brand</p>
      <p className="font-data text-sm text-gray-400">{b.pct} of the study base</p>
      {b.note&&<p className="text-sm text-gray-400 italic mt-1">{b.note}</p>}
    </motion.div>
  )}

export default function AddressableMarketSection(){
  return(
  <section id="s6" className="bg-sephora-white sephora-stripe py-24 px-6 md:px-12">
    <div className="max-w-5xl mx-auto">
      <p className="font-data text-[0.7rem] tracking-[0.2em] text-sephora-red mb-6">THE OPPORTUNITY / 05</p>
      <h2 className="font-display text-[clamp(2.5rem,6vw,5rem)] text-sephora-black leading-none mb-4">The internal market nobody had sized</h2>
      <div className="bg-gray-50 rounded p-4 mb-2 max-w-[55ch]">
        <p className="text-sm text-gray-500 leading-relaxed">All counts within our France 2025 study base of 50,805 customers. These are customers whose purchase behavior already matches the brand's buyer profile.</p>
      </div>
      <p className="font-data text-[0.65rem] text-gray-400 mb-8">Not projected to Sephora's 80M global base. Ratios are statistically robust within this sample.</p>

      {ADDRESSABLE_MARKET.map((b,i)=>(<BrandRow key={b.brand} b={b} i={i}/>))}

      <div className="bg-white rounded-lg border border-gray-100 p-4 mt-8">
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={ADDRESSABLE_MARKET} margin={{top:10,right:20,bottom:5,left:0}}>
            <XAxis dataKey="brand" tick={{fontSize:9,fontFamily:'DM Mono'}} interval={0} angle={-15} textAnchor="end"/>
            <YAxis tick={{fontSize:10,fontFamily:'DM Mono'}}/>
            <Tooltip contentStyle={{fontFamily:'DM Mono',fontSize:'0.75rem'}} formatter={(v:number)=>v.toLocaleString()}/>
            <Bar dataKey="count" fill="#E2001A" radius={[3,3,0,0]} name="Addressable Pool" animationDuration={1200}/>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p className="font-display italic text-xl md:text-2xl text-center text-sephora-black mt-12 max-w-[55ch] mx-auto">All five are established brands. The opportunity is not launching the unknown. It is activating the already-affine.</p>
    </div>
  </section>)}
''')

# === SECTION 7 PROTECTION LAYER ===
w('components/ProtectionLayerSection.tsx','''import{motion}from'framer-motion';
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
''')

# === SECTION 8 MONDAY MORNING ===
w('components/MondayMorningSection.tsx','''import{motion}from'framer-motion';
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
''')

# === APP.TSX ===
w('App.tsx','''import{useEffect}from'react';
import Lenis from'lenis';
import{gsap}from'gsap';
import{ScrollTrigger}from'gsap/ScrollTrigger';
import Navigation from'./components/Navigation';
import HeroSection from'./components/HeroSection';
import MissedMomentSection from'./components/MissedMomentSection';
import BrandPairsSection from'./components/BrandPairsSection';
import CustomerProfileSection from'./components/CustomerProfileSection';
import EngineSection from'./components/EngineSection';
import AddressableMarketSection from'./components/AddressableMarketSection';
import ProtectionLayerSection from'./components/ProtectionLayerSection';
import MondayMorningSection from'./components/MondayMorningSection';

gsap.registerPlugin(ScrollTrigger);

export default function App(){
  useEffect(()=>{
    const lenis=new Lenis({duration:1.2,easing:(t:number)=>Math.min(1,1.001-Math.pow(2,-10*t)),smoothWheel:true});
    lenis.on('scroll',ScrollTrigger.update);
    gsap.ticker.add((t)=>{lenis.raf(t*1000)});
    gsap.ticker.lagSmoothing(0);
    function raf(time:number){lenis.raf(time);requestAnimationFrame(raf)}
    requestAnimationFrame(raf);
    return()=>{lenis.destroy()}},[]);
  return(
    <div className="min-h-screen">
      <Navigation/>
      <HeroSection/>
      <MissedMomentSection/>
      <BrandPairsSection/>
      <CustomerProfileSection/>
      <EngineSection/>
      <AddressableMarketSection/>
      <ProtectionLayerSection/>
      <MondayMorningSection/>
    </div>
  )}
''')

# === MAIN.TSX ===
w('main.tsx','''import{StrictMode}from'react'
import{createRoot}from'react-dom/client'
import'./index.css'
import App from'./App'
createRoot(document.getElementById('root')!).render(<StrictMode><App/></StrictMode>)
''')

print('ALL COMPONENTS WRITTEN')
