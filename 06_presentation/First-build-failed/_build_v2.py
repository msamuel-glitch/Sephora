import os
P=r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\06_presentation\sephora_v2.html'
with open(P,'r',encoding='utf-8') as f: html=f.read()

s1='''<section id="s1" class="world-1">
<div class="bg-texture"><div class="bg-texture-text">SEPHORA FRANCE 2025</div></div>
<div class="content-z" style="text-align:center;display:flex;flex-direction:column;align-items:center">
<div class="section-label">BRAND AFFINITY INTELLIGENCE — FRANCE 2025</div>
<div class="large-number" data-kinetic="load" style="color:var(--w1-data)">€583,570</div>
<div class="hero-line" id="heroLine"></div>
<p class="body-text" style="color:var(--w1-text);text-align:center;max-width:50ch">In incremental basket opportunity. France 2025. Real purchase data.</p>
<p class="body-text reveal-text" style="text-align:center;max-width:50ch">The signal was always in your data. We built the system that reads it.</p>
<p class="small-label" style="color:var(--w1-text2);text-align:center">Study base: 50,805 loyalty card customers. Source: holdout window evaluation Oct–Dec 2025.</p>
</div>
<div class="scroll-cue" id="scrollCue">↓</div>
</section>'''

steps=''.join(f'<div class="timeline-step{" accent-border" if i==3 else ""}" style="{("font-family:var(--ff-data);font-size:.8rem;color:var(--w2-text2)" if i==5 else "")}">{t}</div>' for i,t in enumerate([
"Visit 1 — Buys DRUNK ELEPHANT Skincare",
"Visit 2 — Buys DRUNK ELEPHANT again",
"Visit 3 — Walks past FRESH SAS on the shelf",
"11.73× signal. Nobody said a word.",
"She leaves. She comes back less often.",
"Pattern observed across customers sharing this exact profile. Data fully anonymized."]))

s2=f'''<section id="s2" class="world-2" style="min-height:150vh">
<div class="bg-texture"><div class="bg-stripe"></div></div>
<div class="content-z">
<div class="section-label">THE MISSED MOMENT / 01</div>
<h2 data-kinetic>The conversation that never happened</h2>
<p class="body-text" style="max-width:50ch">DRUNK ELEPHANT customers are 11.73 times more likely to want FRESH SAS than the average Sephora customer. That conversation never happened.</p>
<div class="baseline-box">11.73 times more likely means: if a random customer has a 1% chance of buying FRESH SAS, a DRUNK ELEPHANT customer has an 11.73% chance. We call this a lift score. This one was never used.</div>
<div style="margin:2.5rem 0">{steps}</div>
<p class="connecting-sentence" style="font-style:normal;color:var(--w2-text)">We found this signal in 45,446 baskets.</p>
</div></section>'''

pairs=[("HOURGLASS","MAKEUP BY MARIO","8.52",31,"Make Up","Premium artistry philosophy match — not a price coincidence.","Highest absolute support"),
("HOURGLASS","WESTMAN ATELIER","44.38",10,"Make Up","Highest lift in the dataset. Directional signal concentrated in a specific customer type.","Highest lift score — directional signal"),
("PAT MC GRATH","PAULA'S CHOICE","30.84",5,"Make Up → Skincare","Cross-category: luxury colour cosmetics buyers crossing into evidence-based skincare.",""),
("AMIKA","OUAI HAIRCARE","17.45",7,"Haircare","Premium haircare as an investment category — a customer identity signal.",""),
("ILIA","KOSAS","13.65",10,"Make Up","Clean beauty routine builders. KOSAS is the natural next step after ILIA.",""),
("PAULA'S CHOICE","SUPERGOOP","13.40",5,"Skincare","Evidence-based skincare to SPF. A science-minded customer cohort.",""),
("BY TERRY","HOURGLASS","13.08",7,"Make Up","Prestige French to prestige American makeup. Luxury without geographic loyalty.",""),
("DRUNK ELEPHANT","FRESH SAS","11.73",5,"Skincare","The missed conversation from Section 2, confirmed by the data.",""),
("CACHAREL","DIESEL","11.41",7,"Fragrance","Heritage French fragrance to contemporary edge. Identity not confined to one register.",""),
("MAKEUP BY MARIO","WESTMAN ATELIER","8.79",5,"Make Up","Premium artistry expanding upward into ultra-premium positioning.",""),
("GLOSSIER","ILIA","8.42",6,"Make Up","Entry-level clean beauty graduating into a more intentional routine.","")]
rows=''
for a,b,l,n,c,e,lb in pairs:
    pill=f'<div class="pair-pill">{lb}</div>' if lb else ''
    rows+=f'''<div class="pair-row"><div class="pair-anchor">{a}</div><div class="pair-arrow">→</div><div class="pair-rec">{b}</div>
<div class="pair-meta"><div class="pair-lift">{l}<span>×</span></div><div class="pair-baskets">Observed in {n} real baskets</div><div class="pair-cat">{c}</div></div>
<div class="pair-exp">{e}</div>{pill}</div>\n'''

s3=f'''<section id="s3" class="world-2" style="min-height:auto;padding-bottom:8vh">
<div class="bg-texture"><div class="bg-stripe"></div></div>
<div class="content-z">
<div class="section-label">THE SIGNAL / 02</div>
<h2 data-kinetic>What 45,446 baskets are saying</h2>
<div class="baseline-box reveal-text">Lift measures how much more often two brands appear together versus pure chance. Lift 1.0 = random. Lift 8.0 = customers are 8× more likely to buy both than chance predicts. We only show pairs above 8.0× with verified basket observations.</div>
{rows}
<p class="connecting-sentence" style="font-style:normal;color:var(--w2-text);font-size:clamp(1.3rem,2.5vw,2rem)">63% of these conversations happen in one visit. The channel is not email. It is the beauty advisor next to the shelf.</p>
</div></section>'''

s4='''<section id="s4" class="world-3" style="min-height:auto;padding-bottom:8vh">
<div class="content-z">
<div class="section-label">THE CUSTOMER / 03</div>
<h2 data-kinetic>Who is ready to discover</h2>
<p class="body-text reveal-text">We built 19 behavioral features per customer using only January–September data. Three produced commercially actionable insights.</p>
<div class="finding-block">
<div class="stat-number">0.63</div>
<div class="data-label">Explorer Index — high frequency customers, all generations</div>
<p class="body-text">Any customer visiting every 26 days or fewer has an Explorer Index above 0.63 — regardless of age or generation. A Baby Boomer at 0.65. A Gen Z at 0.66. The gap is 0.01.</p>
<div class="baseline-box">Study-wide median Explorer Index: 0.41. High-frequency customers score 54% above this.</div>
<div class="bar-chart">
<div style="font-family:var(--ff-data);font-size:.65rem;color:var(--w3-text2);margin-bottom:.3rem">HIGH FREQUENCY (≤26 DAYS)</div>
<div class="bar-row"><div class="bar-label">Gen Z</div><div class="bar-track"><div class="bar-fill" style="background:#E2001A" data-w="66"></div></div><div class="bar-value">0.66</div></div>
<div class="bar-row"><div class="bar-label">Boomer</div><div class="bar-track"><div class="bar-fill" style="background:#E2001A" data-w="65"></div></div><div class="bar-value">0.65</div></div>
<div class="bar-row"><div class="bar-label">Gen Alpha</div><div class="bar-track"><div class="bar-fill" style="background:#E2001A" data-w="64"></div></div><div class="bar-value">0.64</div></div>
<div class="bar-row"><div class="bar-label">Gen Y</div><div class="bar-track"><div class="bar-fill" style="background:#E2001A" data-w="63"></div></div><div class="bar-value">0.63</div></div>
<div style="font-family:var(--ff-data);font-size:.65rem;color:var(--w3-text2);margin:.8rem 0 .3rem">LOW FREQUENCY</div>
<div class="bar-row"><div class="bar-label">Gen Z</div><div class="bar-track"><div class="bar-fill" style="background:#CCCCCC" data-w="44"></div></div><div class="bar-value">0.44</div></div>
<div class="bar-row"><div class="bar-label">Boomer</div><div class="bar-track"><div class="bar-fill" style="background:#CCCCCC" data-w="40"></div></div><div class="bar-value">0.40</div></div>
<div class="bar-row"><div class="bar-label">Gen Alpha</div><div class="bar-track"><div class="bar-fill" style="background:#CCCCCC" data-w="42"></div></div><div class="bar-value">0.42</div></div>
<div class="bar-row"><div class="bar-label">Gen Y</div><div class="bar-track"><div class="bar-fill" style="background:#CCCCCC" data-w="39"></div></div><div class="bar-value">0.39</div></div>
</div></div>
<div class="finding-block">
<div class="stat-number">6,188</div>
<div class="data-label">Customers visiting every 26 days or fewer</div>
<p class="body-text">90% of these customers — 5,569 people — are already in Sephora's CRM system. They are reachable today.</p>
<div class="donut-wrap"><div class="donut-ring"><div class="donut-hole">5,569</div></div></div>
<div style="font-family:var(--ff-data);font-size:.7rem;color:var(--w3-text2)">90% CRM-eligible</div>
</div>
<div class="finding-block">
<div class="stat-number">63%</div>
<div class="data-label">Of brand adoptions happened in the same basket — same visit, same day</div>
<p class="body-text">126 of 202 observed adoptions occurred on the exact same day as the first brand purchase. The recommendation must happen in the moment.</p>
<div class="day-chart">
<div class="day-bar" style="height:100%;background:#E2001A"><div class="day-label">Day 0</div></div>
<div class="day-bar" style="height:7%;background:#CCCCCC"><div class="day-label">15d</div></div>
<div class="day-bar" style="height:5%;background:#CCCCCC"><div class="day-label">30d</div></div>
<div class="day-bar" style="height:9%;background:#CCCCCC"><div class="day-label">45d</div></div>
<div class="day-bar" style="height:8%;background:#CCCCCC"><div class="day-label">60d</div></div>
<div class="day-bar" style="height:11%;background:#CCCCCC"><div class="day-label">75d</div></div>
<div class="day-bar" style="height:7%;background:#CCCCCC"><div class="day-label">90d</div></div>
<div class="day-bar" style="height:5%;background:#CCCCCC"><div class="day-label">105d</div></div>
<div class="day-bar" style="height:10%;background:#CCCCCC"><div class="day-label">120d</div></div>
</div></div>
</div></section>'''

shap_a=''.join(f'<li>{p} <span class="tech">({t})</span></li>' for p,t in [
("Customer value tier","rfm_segment_snapshot"),("Loyalty programme status","loyalty_status_at_snapshot"),
("Gen Y brand appeal","gen_brand_appeal_geny"),("Basket pair signal","has_basket_pair"),
("Recruitment channel","recruitment_channel"),("Purchase velocity","velocity_score"),
("Gen Z brand appeal","gen_brand_appeal_genz"),("Gen Alpha brand appeal","gen_brand_appeal_gena"),
("Value trajectory","rfm_trajectory"),("Launch readiness","launch_readiness_score"),
("Explorer vs loyalist","loyalist_vs_explorer_index"),("Boomer brand appeal","gen_brand_appeal_babyboomers"),
("App recommendation affinity","app_recommendation_affinity_proxy")])
shap_d=''.join(f'<li>{p} <span class="tech">({t})</span></li>' for p,t in [
("Brand quantity sold","total_brand_qty"),("Brand customer count","total_brand_customers"),
("Brand spend","total_brand_spend"),("Brand transactions","total_brand_transactions"),
("Brands purchased","total_brands"),("Avg basket size","avg_basket"),("Total transactions","total_transactions")])

s5=f'''<section id="s5" class="world-1" style="min-height:auto;padding:0">
<div style="padding:12vh 8vw;position:relative">
<div class="bg-texture"><div class="bg-texture-text">CANDIDATE ENGINE</div></div>
<div class="content-z">
<div class="section-label">THE SYSTEM / 04</div>
<h2 data-kinetic>How the system finds the signal</h2>
<p class="body-text" style="color:var(--w1-text)">12 million possible customer-brand combinations. 50,805 customers × 239 brands. We scored 2.37 million meaningful ones. Here is how.</p>
</div></div>
<div class="horiz-wrap" style="background:var(--w1-bg)">
<div class="horiz-inner">
<div class="horiz-panel"><h3>Route 1 — The Basket</h3><div class="panel-sub">WHAT CUSTOMERS BUY TOGETHER</div><p class="panel-text">45,446 baskets analyzed. Pairs appearing together 50% more than chance entered the candidate pool.</p></div>
<div class="horiz-panel"><h3>Route 2 — The Twin</h3><div class="panel-sub">WHO BUYS LIKE YOU</div><p class="panel-text">50,805 customer profiles compared. Brands bought by your behavioral twin become your candidates.</p></div>
<div class="horiz-panel"><h3>Route 3 — The Category</h3><div class="panel-sub">WHERE YOU ALREADY SPEND</div><p class="panel-text">Every customer has a dominant axis: makeup, skincare, fragrance, haircare. Unpurchased brands in that axis enter the pool.</p></div>
<div class="horiz-panel"><h3>Route 4 — The New Arrival</h3><div class="panel-sub">BRANDS WITH NO HISTORY YET</div><p class="panel-text">New brands have no basket data. We map them to their closest established proxy and inherit that proxy's audience.</p></div>
</div></div>
<div style="padding:12vh 8vw;background:var(--w1-bg);position:relative">
<div class="content-z">
<h2 data-kinetic style="color:var(--w1-text)">Three systems. One test.</h2>
<div class="baseline-box reveal-text">We locked away October–December data completely. Built everything on January–September only. Then asked three systems to predict what customers would buy in the holdout window. P@3 = of every 3 recommendations, how many correct.</div>
<div class="model-bars">
<div><div class="model-bar-head"><div class="model-bar-name">POPULARITY ENGINE</div><div class="model-bar-pct">4.02%</div></div><div class="model-bar-track"><div class="model-bar-fill" style="background:#333" data-w="40.2"></div></div><p class="model-bar-desc">Recommends the most-purchased brands for everyone. This is the floor.</p></div>
<div><div class="model-bar-head"><div class="model-bar-name">HYBRID ENGINE</div><div class="model-bar-pct">0.52%</div></div><div class="model-bar-track"><div class="model-bar-fill" style="background:#555" data-w="5.2"></div></div><p class="model-bar-desc">Deliberately surfaces niche and emerging brands. Lower raw accuracy by design — built for discovery, not prediction.</p></div>
<div><div class="model-bar-head"><div class="model-bar-name" style="color:#E2001A">ML MODEL</div><div class="model-bar-pct" style="color:#E2001A">5.26%</div></div><div class="model-bar-track"><div class="model-bar-fill" style="background:#E2001A" data-w="52.6"></div></div><p class="model-bar-desc">31% more accurate than the popularity baseline. 1.24 percentage points above the floor.</p></div>
</div>
<h3 style="font-family:var(--ff-display);font-weight:300;font-size:clamp(1.8rem,3vw,2.5rem);margin:3rem 0 1rem;color:var(--w1-text)">What the model learned to look for</h3>
<p class="body-text" style="color:var(--w1-text2)">13 of the top 20 predictive features are ones Sephora can directly influence.</p>
<div class="shap-columns">
<div class="shap-col"><h4 style="color:#E2001A;border-color:#E2001A">SEPHORA CAN ACT ON</h4><ul>{shap_a}</ul></div>
<div class="shap-col"><h4 style="color:#555;border-color:#333">DESCRIPTIVE ONLY</h4><ul>{shap_d}</ul></div>
</div>
<p style="font-size:.85rem;color:var(--w1-text2);margin-top:2rem;max-width:50ch">Left column: the levers. Right column: the context. The system acts on levers.</p>
</div></div>
</section>'''

mbrands=[("BOBBI BROWN","Selective",18180,"35.8%","More than 1 in 3 study-base customers already behaves like a BOBBI BROWN buyer."),
("SUMMER FRIDAYS","Exclusive",16814,"33.1%","An exclusive brand — customers can only find it at Sephora. 16,814 have never been introduced."),
("DRUNK ELEPHANT","Exclusive",16482,"32.4%","The anchor brand from Section 2. Its own addressable market of unactivated affinity."),
("TOM FORD","Selective",15662,"30.8%",""),("KENZO","Selective",15662,"30.8%","")]
mcards=''.join(f'''<div class="market-brand"><div class="mb-top"><div class="mb-name">{b}</div><div class="mb-segment">{s}</div></div>
<div class="mb-count" data-count="{c}">{c:,}</div><div class="mb-desc">customers in study base with high-affinity signals who have never purchased this brand</div>
<div class="mb-pct">{p} of the study base</div>{f'<p class="mb-desc" style="margin-top:.5rem;font-style:italic">{m}</p>' if m else ''}</div>''' for b,s,c,p,m in mbrands)

s6=f'''<section id="s6" class="world-2" style="min-height:auto;padding-bottom:8vh">
<div class="bg-texture"><div class="bg-stripe"></div></div>
<div class="content-z">
<div class="section-label">THE OPPORTUNITY / 05</div>
<h2 data-kinetic>The internal market nobody had sized</h2>
<div class="baseline-box reveal-text">All counts are within our France 2025 study base of 50,805 customers. These are customers whose existing purchase behavior already matches the brand's buyer profile.</div>
<div class="rep-note">Not projected to Sephora's 80M global base. Ratios are statistically robust within this sample.</div>
{mcards}
<p class="connecting-sentence">All five are established brands. The opportunity is not launching the unknown. It is activating the already-affine.</p>
</div></section>'''

s7='''<section id="s7" class="world-1" style="min-height:auto;padding-bottom:8vh">
<div class="bg-texture"><div class="bg-texture-text">GUARDRAIL SYSTEM</div></div>
<div class="content-z">
<div class="section-label">THE SAFEGUARD / 06</div>
<h2 data-kinetic>Knowing when not to recommend</h2>
<p class="body-text" style="color:var(--w1-text)">Every recommendation system maximizes reward. Ours is the only one in this competition that also formalizes the cost of being wrong.</p>
<div class="axis-card dark-card"><div class="card-number" style="color:var(--w1-data)">15</div><div class="card-label">Brand pairs permanently blocked</div><p>Margin-dilutive pairings and luxury-mid-range conflicts. Blocked regardless of lift score.</p></div>
<div class="axis-card dark-card"><div class="card-number" style="color:var(--w1-data)">14</div><div class="card-label">Haircare brands suppressed for Baby Boomers</div><p>Model accuracy for Baby Boomers in Haircare: 0.81%. Study-wide average: 5.26%. The gap disqualifies the recommendation.</p></div>
<div class="axis-card accent-card"><div class="card-number" style="color:#E2001A">6,995</div><div class="card-label">High-value customers protected</div>
<div class="derivation">6,995 customers<br>× €70.26 average basket value<br>─────────────────────────────<br><strong style="color:#E2001A">€491,476 in relationship equity protected</strong></div>
<p>These customers received no guardrail-violating recommendation in the test window. Zero.</p></div>
<p class="connecting-sentence" style="color:var(--w1-text)">The difference between a model and a deployable system is knowing the cost of being wrong.</p>
</div></section>'''

s8='''<section id="s8" class="world-3" style="min-height:auto;padding-bottom:8vh">
<div class="content-z">
<div class="section-label">ACTIVATION / 07</div>
<h2 data-kinetic>What happens next</h2>
<div class="split-layout">
<div class="split-col"><h3 style="color:var(--w3-text)">Three actions traceable to this data</h3>
<div class="action-item"><strong>For the CRM &amp; App team:</strong>Deploy point-of-purchase recommendations for the 11 validated pairs. 63% of adoptions happen same-day — trigger the recommendation at basket add, not days later.<div class="action-source">Source: 63% same-day adoption (126 of 202)</div></div>
<div class="action-item"><strong>For Beauty Advisors:</strong>Brief every advisor on the 11 directional pairs. HOURGLASS customer: ask about MAKEUP BY MARIO. 8.52× lift. 31 validated baskets.<div class="action-source">Source: Lead pair, highest absolute support</div></div>
<div class="action-item"><strong>For Brand Managers:</strong>BOBBI BROWN: 18,180 warm prospects in study base. SUMMER FRIDAYS: 16,814. DRUNK ELEPHANT: 16,482. These are customer lists, not projections.<div class="action-source">Source: brand_addressable_market.csv</div></div>
</div>
<div class="split-col right-col"><h3>Three things we do not yet do</h3>
<div class="limitation-item"><strong>Sequential journeys — Horizon 2</strong>We recommend one brand per occasion. Next: which sequence over three visits maximizes customer lifetime value.</div>
<div class="limitation-item"><strong>Consideration set — Horizon 2</strong>Two recommended brands may compete for the same occasion. Next: occasion-level routing.</div>
<div class="limitation-item"><strong>Lapsed customers — Horizon 3</strong>Our model learns from active customers. High-value lapsed customers are not yet in scope.</div>
</div></div>
<p class="closing-sentence">We did not build a recommendation engine. We built a system that finds the moment — before it happens — when a customer is about to discover a brand she has never tried. And we made sure nothing gets in the way of that moment.</p>
<p class="final-label">Study base: 50,805 customers, France 2025. All figures sourced from validated project outputs. No projections beyond stated scope.</p>
</div></section>'''

for i,s in enumerate([s1,s2,s3,s4,s5,s6,s7,s8],1):
    html=html.replace(f'<section id="s{i}" class="world-{"1" if i in(1,5,7) else "2" if i in(2,3,6) else "3"}"></section>',s)

extra_js='''
/* Hero line draw */
gsap.to('#heroLine',{width:'30vw',duration:1.5,delay:.8,ease:'power2.out'});
/* Scroll cue fade */
gsap.to('#scrollCue',{opacity:0,delay:3,duration:1});
/* Timeline steps */
gsap.utils.toArray('.timeline-step').forEach(s=>{gsap.to(s,{opacity:1,scrollTrigger:{trigger:s,start:'top 85%',end:'top 60%',scrub:1}})});
/* Pair rows */
gsap.utils.toArray('.pair-row').forEach(r=>{gsap.to(r,{opacity:1,y:0,scrollTrigger:{trigger:r,start:'top 92%',end:'top 65%',scrub:1}})});
/* Bar fills */
gsap.utils.toArray('.bar-fill').forEach(b=>{gsap.to(b,{width:b.dataset.w+'%',scrollTrigger:{trigger:b,start:'top 90%',end:'top 70%',scrub:1}})});
/* Model bar fills */
gsap.utils.toArray('.model-bar-fill').forEach(b=>{gsap.to(b,{width:b.dataset.w+'%',scrollTrigger:{trigger:b,start:'top 92%',toggleActions:'play none none none',once:true}})});
/* Market brands + count-up */
gsap.utils.toArray('.market-brand').forEach(c=>{gsap.to(c,{opacity:1,y:0,scrollTrigger:{trigger:c,start:'top 90%',end:'top 65%',scrub:1,onEnter:()=>{const el=c.querySelector('.mb-count');if(el&&!el.dataset.done){el.dataset.done='1';const t=parseInt(el.dataset.count);let o={v:0};gsap.to(o,{v:t,duration:1.5,ease:'power2.out',onUpdate:()=>{el.textContent=Math.floor(o.v).toLocaleString()}})}}}})});
/* Axis cards */
gsap.utils.toArray('.axis-card').forEach(c=>{gsap.to(c,{opacity:1,y:0,scrollTrigger:{trigger:c,start:'top 90%',end:'top 65%',scrub:1}})});
/* Split layout */
gsap.from('.split-layout',{opacity:0,y:30,scrollTrigger:{trigger:'.split-layout',start:'top 80%',end:'top 55%',scrub:1}});
/* Finding blocks */
gsap.utils.toArray('.finding-block').forEach(f=>{gsap.from(f,{opacity:0,y:30,scrollTrigger:{trigger:f,start:'top 85%',end:'top 60%',scrub:1}})});
'''
html=html.replace('</script>\n</body>',extra_js+'</script>\n</body>')
with open(P,'w',encoding='utf-8') as f: f.write(html)
print(f'BUILD COMPLETE — {len(html):,} bytes')
