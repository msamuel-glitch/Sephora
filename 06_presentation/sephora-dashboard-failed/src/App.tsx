import{useEffect}from'react';
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
