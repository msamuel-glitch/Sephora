import{motion}from'framer-motion';
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
