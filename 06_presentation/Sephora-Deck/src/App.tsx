import React from 'react'
import { CinematicHero } from './components/Hero'
import { NetworkGraph } from './components/NetworkGraph'
import { GenerationalProfile } from './components/GenerationalProfile'

function App() {
  return (
    <main className="min-h-screen bg-background text-foreground antialiased selection:bg-primary selection:text-white">
      <CinematicHero />
      
      {/* 3D Network Section */}
      <section className="min-h-screen flex flex-col justify-center border-t border-white/5 relative">
        <NetworkGraph />
      </section>

      {/* Engine & Generational Profiling Placeholder */}
      <section className="min-h-screen flex flex-col items-center justify-center p-8 border-t border-white/5 relative">
        <div className="w-full max-w-5xl mx-auto mb-16">
          <p className="t-label text-primary mb-2">The Machine / 03</p>
          <h2 className="t-display text-white text-5xl">Generational Arbitration</h2>
          <p className="text-neutral-400 font-light mt-4 max-w-2xl">
            Model scores must be subordinated to strategic value. The Explorer Index remains robust across generation, 
            but frequency dictates the activation pathway.
          </p>
        </div>
        
        <GenerationalProfile />
      </section>
      
      {/* Final Delivery Pipeline */}
      <section className="min-h-screen flex flex-col items-center justify-center p-16 border-t border-white/5 bg-neutral-950 text-center">
         <p className="t-label text-primary mb-2">Activation / 04</p>
         <h2 className="t-display text-white text-4xl mb-12">The Deployment Pipeline</h2>
         
         <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl">
            <div className="p-8 border border-white/10 bg-white/5 rounded text-left">
              <h3 className="font-mono text-sm text-primary tracking-widest uppercase mb-4">Phase 1: CRM & Email</h3>
              <p className="text-neutral-400 font-light text-sm mb-4">Primary channel for high-frequency segments mapping to exclusive markets.</p>
              <div className="text-2xl font-display text-white">Targeted Lookalikes</div>
            </div>
            <div className="p-8 border border-white/10 bg-white/5 rounded text-left">
              <h3 className="font-mono text-sm tracking-widest uppercase mb-4 text-neutral-500">Phase 2: App Feed</h3>
              <p className="text-neutral-400 font-light text-sm mb-4">Leverage behavioral twins to alter zero-party data algorithms.</p>
              <div className="text-2xl font-display text-white">Dynamic Routing</div>
            </div>
            <div className="p-8 border border-white/10 bg-white/5 rounded text-left">
              <h3 className="font-mono text-sm tracking-widest uppercase mb-4 text-neutral-500">Phase 3: Store Advisor</h3>
              <p className="text-neutral-400 font-light text-sm mb-4">Point of contact cross-sell guidelines based on the 5.0x verified pair logic.</p>
              <div className="text-2xl font-display text-white">Human Augmentation</div>
            </div>
         </div>
      </section>
    </main>
  )
}

export default App
