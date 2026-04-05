import{useState,useEffect}from'react';
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
