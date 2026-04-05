import{useState,useEffect,useRef}from'react';
export function useInView(threshold=0.2){
  const ref=useRef<HTMLDivElement>(null);const[inView,setInView]=useState(false);
  useEffect(()=>{if(!ref.current)return;
    const obs=new IntersectionObserver(([e])=>{if(e.isIntersecting)setInView(true)},{threshold});
    obs.observe(ref.current);return()=>obs.disconnect()},[threshold]);
  return{ref,inView}}
