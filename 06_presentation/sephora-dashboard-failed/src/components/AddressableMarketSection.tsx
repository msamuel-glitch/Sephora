import{BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer}from'recharts';
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
