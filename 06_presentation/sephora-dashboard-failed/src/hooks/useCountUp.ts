import{useState,useEffect,useRef}from'react';
export function useCountUp(target:number,duration=1500,trigger=true){
  const[val,setVal]=useState(0);const started=useRef(false);
  useEffect(()=>{if(!trigger||started.current)return;started.current=true;
    const start=performance.now();
    function tick(now:number){const p=Math.min((now-start)/duration,1);
      setVal(Math.floor(p*target));if(p<1)requestAnimationFrame(tick)}
    requestAnimationFrame(tick)},[target,duration,trigger]);
  return val}
