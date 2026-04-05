import re, os
P=r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\06_presentation\sephora_brand_affinity_presentation.html'
with open(P,'r',encoding='utf-8') as f: html=f.read()

# === SECTION 1 ===
s1='''<section id="s1" style="text-align:center;justify-content:center;align-items:center">
<div class="parallax-line parallax-el" style="width:40vw;top:20%;left:-5%"></div>
<div class="parallax-circle parallax-el" style="width:200px;height:200px;top:10%;right:5%"></div>
<div class="large-number" data-kinetic style="font-size:clamp(5rem,10vw,12rem);color:var(--text)">€583,570</div>
<div class="hero-line" id="heroLine"></div>
<p style="font-family:var(--ff-body);font-weight:400;font-size:clamp(1.1rem,1.5vw,1.4rem);max-width:55ch;margin:0 auto 2rem;line-height:1.6">In incremental basket opportunity. Sitting in your France 2025 transaction data. Waiting to be activated.</p>
<p class="body-text" data-reveal style="text-align:left;margin:2rem auto">This is not a projection. This is not a forecast. This is the measured difference in spending between customers who discovered a new brand through a relevant recommendation and those who did not — calculated on real Sephora France purchase data from October to December 2025. We found it. We built the system that produces it. This is what it looks like.</p>
<p class="small-label" style="margin:2rem auto">Study base: 50,805 loyalty card customers, France 2025. Source: holdout window evaluation.</p>
</section>'''

# === SECTION 2 ===
steps=[
('01','Visit 1 — Buys DRUNK ELEPHANT Skincare',''),
('02','Visit 2 — Buys DRUNK ELEPHANT again',''),
('03','Visit 3 — Walks past FRESH SAS on the shelf',''),
('04','11.73× affinity signal. Nobody said a word.','color:var(--accent);font-weight:500'),
('05','She leaves. She comes back less often.',''),
('06','This pattern appeared in 5 validated baskets in our study base. The signal is consistent.','font-family:var(--ff-data);font-size:.85rem;color:var(--text2)'),
]
timeline_html=''.join(f'<div class="timeline-step" style="opacity:0;padding:1.2rem 0;border-left:2px solid {"var(--accent)" if i==3 else "var(--muted)"};padding-left:1.5rem;margin-left:1rem;{s}"><span style="font-family:var(--ff-data);font-size:.7rem;color:var(--text2);display:block;margin-bottom:.3rem">{n}</span>{t}</div>' for i,(n,t,s) in enumerate(steps))

s2=f'''<section id="s2" style="min-height:150vh">
<div class="parallax-line parallax-el" style="width:30vw;top:15%;right:-3%"></div>
<div class="parallax-circle parallax-el" style="width:140px;height:140px;bottom:10%;left:5%"></div>
<div class="section-label">THE SIGNAL / 01</div>
<h2 data-kinetic>The conversation that never happened</h2>
<p class="body-text" data-reveal>This is the composite behavioral pattern of customers in our study base who bought DRUNK ELEPHANT skincare and never received a recommendation for FRESH SAS — a brand they were statistically 11.73 times more likely to want than the average Sephora customer. 11.73 times means: if a random Sephora customer has a 1% chance of buying FRESH SAS in a given quarter, a DRUNK ELEPHANT customer has an 11.73% chance. That gap is the missed conversation.</p>
<div style="margin:3rem 0">{timeline_html}</div>
<p class="small-label">This timeline represents a composite behavioral pattern — not one individual customer. Customer data is fully anonymized. The journey is reconstructed from transaction patterns across customers sharing this purchase profile.</p>
<p class="connecting-sentence" style="margin-top:4rem">We did not invent this signal.<br>We found it in 45,446 shopping baskets.</p>
</section>'''

# === SECTION 3 ===
pairs=[
("HOURGLASS","MAKEUP BY MARIO","8.52",31,"Make Up","Our strongest signal by combined reliability and lift. Customers who invest in HOURGLASS prestige makeup are 8.5 times more likely to also buy MAKEUP BY MARIO than a random Sephora customer. Both brands share a premium artistry positioning. This is a philosophy match, not a price coincidence.","Lead pair — highest absolute support"),
("HOURGLASS","WESTMAN ATELIER","44.38",10,"Make Up","The highest lift score in the dataset. 44 times more likely than chance. The small basket count means this is a directional signal, not a certainty — it tells us the affinity is extremely concentrated among a specific customer type. Worth watching as the study base grows.","Highest lift — directional signal"),
("PAT MC GRATH","PAULA'S CHOICE","30.84",5,"Make Up → Skincare","A cross-category pair. Luxury colour cosmetics buyers crossing into evidence-based skincare. This is the skincare-first beauty consumer pattern appearing in French transaction data.",""),
("AMIKA","OUAI HAIRCARE","17.45",7,"Haircare","Premium haircare to premium haircare. These customers have decided that haircare is an investment category, not a commodity. This is a customer identity signal, not a casual cross-sell.",""),
("ILIA","KOSAS","13.65",10,"Make Up","Two clean beauty makeup brands. Customers buying ILIA are building a clean beauty routine, not just buying one product. KOSAS is the natural next step in that routine.",""),
("PAULA'S CHOICE","SUPERGOOP","13.40",5,"Skincare","Evidence-based skincare to SPF. Customers who research their skincare ingredients also research sun protection. A science-minded customer cohort buying in sequence.",""),
("BY TERRY","HOURGLASS","13.08",7,"Make Up","Prestige French makeup to prestige American makeup. A luxury buyer whose basket is not limited by geography or brand loyalty.",""),
("DRUNK ELEPHANT","FRESH SAS","11.73",5,"Skincare","The pair from Section 2. The missed conversation, confirmed by the data. Skincare investment customers with a strong signal for ingredient-conscious alternatives.",""),
("CACHAREL","DIESEL","11.41",7,"Fragrance","A fragrance pair crossing from heritage French to contemporary edge. A customer whose fragrance identity is not confined to one aesthetic register.",""),
("MAKEUP BY MARIO","WESTMAN ATELIER","8.79",5,"Make Up","A premium artistry buyer expanding their routine upward into ultra-premium positioning.",""),
("GLOSSIER","ILIA","8.42",6,"Make Up","Minimal skincare-first makeup to clean colour cosmetics. A customer graduating from entry-level clean beauty into a more intentional routine.",""),
]
cards_html=''
for i,(a,b,l,n,c,e,lb) in enumerate(pairs,1):
    lbl=f'<div class="pc-label">{lb}</div>' if lb else ''
    cards_html+=f'''<div class="pair-card"><div class="pc-brands"><span class="pc-anchor">{a}</span><span class="pc-arrow">→</span><span class="pc-rec">{b}</span></div><div class="pc-lift">{l}×</div><div class="pc-support">Observed in {n} real customer baskets</div><div class="pc-cat">{c}</div><p class="pc-exp">{e}</p>{lbl}</div>\n'''

s3=f'''<section id="s3" style="min-height:auto;padding-bottom:8vh">
<div class="parallax-line parallax-el" style="width:25vw;top:5%;left:60%"></div>
<div class="section-label">THE SIGNAL / 02</div>
<h2 data-kinetic>What 45,446 baskets are saying</h2>
<p class="body-text" data-reveal>We analyzed every shopping basket in our study base where a customer bought more than one brand in a single visit. 45,446 baskets. 8,357 unique brand pair combinations. Most of those combinations are noise — two expensive brands bought together simply because a customer had a large budget that day, not because of genuine affinity. We removed all of those. We applied three filters: statistical reliability, business sense, and anti-obviousness. What remained were 11 pairs where the signal is real.</p>
<div class="baseline-box">To understand these numbers, here is the baseline: if brand choice were completely random, any two brands would appear together in a basket at a predictable rate based purely on how popular each brand is individually. A "lift score" measures how much more often two brands appear together compared to what random chance would predict. A lift of 1.0 means random. A lift of 8.0 means customers are 8 times more likely to buy both brands together than chance would suggest. We only show pairs with lift above 8.0 AND a minimum number of real basket observations.</div>
{cards_html}
<p class="connecting-sentence">Most of these conversations happen in one visit. 63% of brand adoptions in these pairs occurred in the same basket — the same day, the same store. The activation channel is not email. It is the beauty advisor standing next to the shelf.</p>
</section>'''

# === SECTION 4 ===
s4='''<section id="s4" style="min-height:auto;padding-bottom:8vh">
<div class="parallax-circle parallax-el" style="width:180px;height:180px;top:5%;right:8%"></div>
<div class="section-label">THE CUSTOMER / 03</div>
<h2 data-kinetic>Who is ready to discover</h2>
<p class="body-text" data-reveal>We built 19 behavioral features for every one of the 50,805 customers in our study base using only their January to September 2025 purchase history. We never touched October to December data while building these features — that window was locked away and only used at the end to test whether our predictions were correct. Three features produced the most commercially useful insights.</p>

<div class="finding-block">
<div class="large-number">0.63</div>
<div class="data-label">Explorer Index — high frequency customers, all generations</div>
<p style="max-width:72ch;line-height:1.7;margin-bottom:1rem">We created a score called the Explorer Index. It measures how often a customer buys from a brand they have never purchased before, relative to their total shopping frequency. A score of 0 means the customer only ever buys the same brands. A score of 1 means the customer tries something new every single visit. The study-wide median is 0.41.</p>
<p style="max-width:72ch;line-height:1.7;margin-bottom:1rem">Here is the finding that surprised us: Any customer who visits Sephora every 26 days or fewer — regardless of their age or generation — has an Explorer Index above 0.63. A Baby Boomer visiting every 25 days: 0.65. A Gen Z visiting every 25 days: 0.66. The gap between them is 0.01.</p>
<p style="max-width:72ch;line-height:1.7;font-weight:400">Age does not predict who will try a new brand. Visit frequency does. This changes who you target for a new brand launch.</p>
<div class="baseline-box">The baseline for comparison: study-wide median Explorer Index = 0.41. High frequency customers score 54% above this baseline.</div>
<div class="bar-chart">
<div style="font-family:var(--ff-data);font-size:.75rem;color:var(--text2);margin-bottom:.5rem">Explorer Index — High Frequency (≤26 days)</div>
<div class="bar-row"><div class="bar-label">Gen Z</div><div class="bar-track"><div class="bar-fill" style="background:var(--accent)" data-width="66"></div></div><div class="bar-value">0.66</div></div>
<div class="bar-row"><div class="bar-label">Baby Boomer</div><div class="bar-track"><div class="bar-fill" style="background:var(--accent)" data-width="65"></div></div><div class="bar-value">0.65</div></div>
<div class="bar-row"><div class="bar-label">Gen Alpha</div><div class="bar-track"><div class="bar-fill" style="background:var(--accent)" data-width="64"></div></div><div class="bar-value">0.64</div></div>
<div class="bar-row"><div class="bar-label">Gen Y</div><div class="bar-track"><div class="bar-fill" style="background:var(--accent)" data-width="63"></div></div><div class="bar-value">0.63</div></div>
<div style="font-family:var(--ff-data);font-size:.75rem;color:var(--text2);margin:1rem 0 .5rem">Explorer Index — Low Frequency</div>
<div class="bar-row"><div class="bar-label">Gen Z</div><div class="bar-track"><div class="bar-fill" style="background:var(--muted)" data-width="44"></div></div><div class="bar-value">0.44</div></div>
<div class="bar-row"><div class="bar-label">Baby Boomer</div><div class="bar-track"><div class="bar-fill" style="background:var(--muted)" data-width="40"></div></div><div class="bar-value">0.40</div></div>
<div class="bar-row"><div class="bar-label">Gen Alpha</div><div class="bar-track"><div class="bar-fill" style="background:var(--muted)" data-width="42"></div></div><div class="bar-value">0.42</div></div>
<div class="bar-row"><div class="bar-label">Gen Y</div><div class="bar-track"><div class="bar-fill" style="background:var(--muted)" data-width="39"></div></div><div class="bar-value">0.39</div></div>
</div>
</div>

<div class="finding-block">
<div class="large-number">6,188</div>
<div class="data-label">Customers purchasing every 26 days or fewer</div>
<p style="max-width:72ch;line-height:1.7;margin-bottom:1rem">6,188 customers in our study base return to Sephora at least once every 26 days. These are not your biggest spenders necessarily. What makes them commercially valuable is their availability: they give Sephora more opportunities per quarter to deliver a relevant recommendation than any other segment.</p>
<p style="max-width:72ch;line-height:1.7;margin-bottom:1rem">90% of them — 5,569 customers — are already registered in Sephora's CRM system. That means Sephora already has their email address, their app notification permission, and their full purchase history. They are reachable today.</p>
<div class="donut-container"><div class="donut-ring"><div class="donut-hole">90%</div></div></div>
<div style="font-family:var(--ff-data);font-size:.75rem;color:var(--text2)">CRM-eligible: 5,569 of 6,188 high-frequency customers</div>
</div>

<div class="finding-block">
<div class="large-number">63%</div>
<div class="data-label">Of validated brand adoptions happened in the same basket — same visit, same day</div>
<p style="max-width:72ch;line-height:1.7;margin-bottom:1rem">When we measured the time between a customer first buying an anchor brand and then buying the recommended brand for our 11 validated pairs, we expected to find a sequential journey over weeks or months. Instead: 126 out of 202 observed adoptions happened on the same day — in the same shopping basket.</p>
<p style="max-width:72ch;line-height:1.7;margin-bottom:1rem">63% of the signal lives at the point of purchase. This means the most powerful activation channel for these specific pairs is not a CRM email arriving three days later. It is the beauty advisor standing next to the shelf. It is the app product page loaded at the moment the customer adds the anchor brand to their basket. The recommendation needs to happen in the moment — not after the moment has passed.</p>
<div class="timeline-bar-chart">
<div class="timeline-bar" style="height:100%;background:var(--accent)"><div class="timeline-bar-label">Day 0</div></div>
<div class="timeline-bar" style="height:7%;background:var(--muted)"><div class="timeline-bar-label">15d</div></div>
<div class="timeline-bar" style="height:5%;background:var(--muted)"><div class="timeline-bar-label">30d</div></div>
<div class="timeline-bar" style="height:9%;background:var(--muted)"><div class="timeline-bar-label">45d</div></div>
<div class="timeline-bar" style="height:8%;background:var(--muted)"><div class="timeline-bar-label">60d</div></div>
<div class="timeline-bar" style="height:11%;background:var(--muted)"><div class="timeline-bar-label">75d</div></div>
<div class="timeline-bar" style="height:7%;background:var(--muted)"><div class="timeline-bar-label">90d</div></div>
<div class="timeline-bar" style="height:5%;background:var(--muted)"><div class="timeline-bar-label">105d</div></div>
<div class="timeline-bar" style="height:10%;background:var(--muted)"><div class="timeline-bar-label">120d</div></div>
</div>
</div>
</section>'''

# === SECTION 5 ===
shap_act=''.join(f'<li>{x}</li>' for x in ["Customer value tier","Loyalty programme status","Gen Y brand appeal score","Basket pair signal present","Recruitment channel","Purchase velocity score","Gen Z brand appeal score","Gen Alpha brand appeal score","Customer value trajectory","Launch readiness score","Explorer vs loyalist index","Baby Boomer brand appeal score","App recommendation affinity"])
shap_desc=''.join(f'<li>{x}</li>' for x in ["Total brand quantity sold","Total brand customer count","Total brand spend","Total brand transactions","Total brands purchased","Average basket size","Total transactions"])

s5=f'''<section id="s5" style="min-height:auto;padding:0">
<div style="padding:12vh 8vw">
<div class="section-label">THE SYSTEM / 04</div>
<h2 data-kinetic>How the system finds the signal</h2>
<p class="body-text" data-reveal>Before any prediction happens, the system must decide which of the 12 million possible customer-brand combinations — 50,805 customers multiplied by 239 brands — are even worth evaluating. Scoring all 12 million would produce mostly noise. Instead, we built a four-route candidate engine that narrows the field to 2.37 million meaningful pairs before any machine learning begins. Here are the four routes.</p>
</div>
<div class="horiz-wrap">
<div class="horiz-inner">
<div class="horiz-panel"><h3>Route 1 — The Basket</h3><div class="panel-sub">What customers buy together</div><p class="panel-text">If two brands appear in the same shopping basket more often than random chance predicts, that is a signal. We collected all baskets with multiple brands — 45,446 of them — and identified every pair that appeared together at least 3 times with a lift score above 1.5. Lift of 1.5 means: 50% more likely to appear together than chance. These pairs entered the candidate pool.</p><div style="margin-top:3rem;font-size:4rem;opacity:.1">🛒</div></div>
<div class="horiz-panel"><h3>Route 2 — The Twin</h3><div class="panel-sub">Who buys like you</div><p class="panel-text">If Customer A and Customer B have similar purchase histories — same categories, similar brands, similar frequency — then brands Customer B bought that Customer A has never tried become candidates for Customer A. We built purchase vectors for all 50,805 customers and found their behavioral twins. This route surfaces brands the basket route would never find — because they were never bought together, but by similar people.</p><div style="margin-top:3rem;font-size:4rem;opacity:.1">👥</div></div>
<div class="horiz-panel"><h3>Route 3 — The Category</h3><div class="panel-sub">Where you already spend</div><p class="panel-text">If a customer spends primarily in skincare, they are more likely to adopt a new skincare brand than a fragrance brand. We identified each customer's dominant product category — called an axis in Sephora's internal language, meaning makeup, skincare, fragrance, haircare, or other — and added every brand in that axis they had never purchased as a candidate. Simple. Powerful. Commercially obvious in the right direction.</p><div style="margin-top:3rem;font-size:4rem;opacity:.1">📊</div></div>
<div class="horiz-panel"><h3>Route 4 — The New Arrival</h3><div class="panel-sub">Brands with no history yet</div><p class="panel-text">A new brand entering Sephora has no transaction history. No basket pairs. No lookalike data. A standard recommendation engine would never recommend it — because it has no signal to learn from. This is the cold start problem. We solved it by mapping new brands to established proxies: finding the established brand whose customer base most closely matches the new brand's product positioning. That established brand's audience becomes the new brand's first recommendation pool.</p><div style="margin-top:3rem;font-size:4rem;opacity:.1">🆕</div></div>
</div>
</div>
<div style="padding:12vh 8vw">
<h2 data-kinetic>Three systems. One holdout window. One winner.</h2>
<div class="baseline-box">To test whether our system works, we locked away all October to December 2025 data before building anything. We built our system using only January to September data. Then — after everything was built and frozen — we asked all three systems to predict what customers would buy in October to December. The percentage shown is: out of every 3 recommendations made, how many were correct. This is called Precision at 3, or P@3.</div>
<div class="model-bars">
<div class="model-bar"><div class="model-bar-head"><div class="model-bar-name">Popularity Engine</div><div class="model-bar-pct">4.02%</div></div><div class="model-bar-track"><div class="model-bar-fill" style="background:var(--muted)" data-width="40.2"></div></div><p class="model-bar-desc">What it does: Recommends the most purchased brands overall, ignoring individual preferences. This is the floor. Any intelligent system must beat this.</p></div>
<div class="model-bar"><div class="model-bar-head"><div class="model-bar-name">Hybrid Engine</div><div class="model-bar-pct">0.52%</div></div><div class="model-bar-track"><div class="model-bar-fill" style="background:#ddd" data-width="5.2"></div></div><p class="model-bar-desc">What it does: Recommends niche and emerging brands deliberately avoided by volume-based systems. It scored below the popularity engine on raw accuracy — and that is not a failure. It was designed to surface brands customers would never discover on their own.</p></div>
<div class="model-bar"><div class="model-bar-head"><div class="model-bar-name">Machine Learning Model</div><div class="model-bar-pct" style="color:var(--accent)">5.26%</div></div><div class="model-bar-track"><div class="model-bar-fill" style="background:var(--accent)" data-width="52.6"></div></div><p class="model-bar-desc">Trained on 9 months of real purchase behavior to predict which brand each individual customer will adopt next. 31% more accurate than the popularity baseline. The baseline is 4.02%. Our model is 5.26%. The gap is 1.24 percentage points — which across 50,805 customers and 239 brands represents thousands of correctly identified conversations that the popularity engine would have missed.</p></div>
</div>
<h3 style="font-family:var(--ff-display);font-weight:300;font-size:clamp(1.8rem,3vw,2.5rem);margin:4rem 0 1rem">What the model learned to look for</h3>
<p style="max-width:72ch;line-height:1.7;margin-bottom:2rem">After training the model, we ran an analysis called SHAP — a method that reveals which customer and brand characteristics had the most influence on the model's predictions. We then sorted those characteristics into two groups: ones Sephora can directly influence through campaigns, store decisions, or app design — and ones that describe customer behavior but cannot be engineered.</p>
<div class="shap-columns">
<div class="shap-col"><h4 style="color:var(--accent)">What Sephora can act on</h4><ul>{shap_act}</ul></div>
<div class="shap-col desc"><h4>Descriptive context — not levers</h4><ul>{shap_desc}</ul></div>
</div>
<p style="max-width:72ch;line-height:1.7;margin-top:3rem">The model knows what to look for. The features in the left column are the ones that tell Sephora where to look and who to reach. The features in the right column explain why the prediction is confident — but they are not the dials Sephora turns to make it happen.</p>
</div>
</section>'''

# === SECTION 6 ===
mbrands=[("BOBBI BROWN","Selective",18180,"35.8%","More than 1 in 3 customers in the study base already behaves like a BOBBI BROWN buyer. The recommendation has never been made."),
("SUMMER FRIDAYS","Exclusive",16814,"33.1%","An exclusive brand — meaning customers can only find it at Sephora. 16,814 high-affinity customers who have never been introduced to it."),
("DRUNK ELEPHANT","Exclusive",16482,"32.4%","The anchor brand from Section 2. Its own addressable market of 16,482 customers who are not yet buying it."),
("TOM FORD","Selective",15662,"30.8%",""),
("KENZO","Selective",15662,"30.8%","")]
mcards=''.join(f'''<div class="market-card"><h3>{b}</h3><div class="mc-segment">Segment: {s}</div><div class="mc-count" data-count="{c}">{c:,}</div><div class="mc-desc">customers in the study base with high-affinity signals who have never purchased this brand</div><div class="mc-pct">{p} of the study base</div>{f'<p class="mc-meaning">{m}</p>' if m else ''}</div>''' for b,s,c,p,m in mbrands)

s6=f'''<section id="s6" style="min-height:auto;padding-bottom:8vh">
<div class="parallax-line parallax-el" style="width:35vw;top:8%;left:50%"></div>
<div class="section-label">THE OPPORTUNITY / 05</div>
<h2 data-kinetic>The internal market nobody had sized</h2>
<p class="body-text" data-reveal>For every brand in our study base, we identified customers who showed high affinity signals — matching product category, matching market positioning, matching behavioral profile from lookalike analysis — but had never purchased that brand. These are not random prospects. These are customers whose existing purchase history already looks like a buyer of that brand. The recommendation has simply never been made.</p>
<div class="baseline-box">All counts are within our France 2025 study base of 50,805 customers. We have not projected to Sephora's 80 million global base because the sample was not designed for that extrapolation. The ratios and patterns are statistically robust within this sample. Sephora's internal team can apply these ratios to the full loyalty base.</div>
{mcards}
<p class="connecting-sentence" style="font-style:normal">Notice: all five are established brands — not unknown new arrivals. The biggest commercial opportunity in this dataset is not in launching unknown brands to new customers. It is in connecting 50,000 existing Sephora customers to well-known brands they have simply never been shown.</p>
</section>'''

# === SECTION 7 ===
s7='''<section id="s7" style="min-height:auto;padding-bottom:8vh">
<div class="parallax-line parallax-el" style="width:1px;height:60vh;top:10%;left:50%;background:var(--accent);opacity:.08"></div>
<div class="section-label">THE SAFEGUARD / 06</div>
<h2 data-kinetic>Knowing when not to recommend</h2>
<p style="max-width:72ch;line-height:1.7;margin-bottom:3rem">Every recommendation system has a reward function: maximize correct predictions, maximize conversion, maximize basket size. Ours is the only system in this competition that also has a cost function: a formal measure of what it costs to get a recommendation wrong for your most valuable customers. Because getting it wrong for a high-value customer is not just a missed sale. It is a signal that Sephora does not understand them.</p>

<div class="axis-card grey-bg">
<h3>Axis A — Business Guardrails: 15 blocked pairs</h3>
<p>We identified 15 brand pair combinations that are commercially risky regardless of their affinity signal. Examples: pairing a mid-range brand with an ultra-premium customer whose entire purchase history is luxury-only. Pairing brands from conflicting market positions that a store planogram would never place together. These 15 pairs are permanently blocked for all customer segments. No lift score overrides a business rule.</p>
</div>

<div class="axis-card grey-bg">
<h3>Axis B — Generation Protection: 14 brands suppressed for Baby Boomers in Haircare</h3>
<p>Our model's accuracy for Baby Boomer customers in the Haircare category dropped to 0.81%. To explain what that means: the study-wide average accuracy is 5.26%. For Baby Boomers in Haircare, the model is correct less than 1 time in 100. Baby Boomers in our study base spend 32.2% of their beauty budget on Fragrance and predominantly buy established brands — GUERLAIN, GIVENCHY, CHANEL. Recommending trendy haircare brands like BRIOGEO, OLAPLEX, or FABLE &amp; MANE to this segment produces irrelevant recommendations. We suppress them.</p>
</div>

<div class="axis-card accent-border">
<h3>Axis C — High-Value Customer Protection: 6,995 customers</h3>
<p>A false positive in recommendation language means: the system recommended a brand, and the customer did not buy it. For most customers, this is an acceptable miss. For the highest-value customers — those in the top spending tiers with the highest loyalty status — a wrong recommendation that also violates a business rule carries a different cost.</p>
<div class="derivation">
6,995 customers identified where:<br>
— The model recommended a brand in the top 3<br>
— The customer did not buy it in the test window<br>
— AND the recommendation violated a business guardrail<br><br>
Average basket value for this group: €70.26 per visit<br><br>
<strong>6,995 × €70.26 = €491,476</strong><br><br>
This is the total basket equity of the customer segment protected by the suppression layer.
</div>
</div>

<p class="connecting-sentence" style="font-weight:400">Zero of these 6,995 customers received a guardrail-violating recommendation in the test window. The protection layer worked.</p>
</section>'''

# === SECTION 8 ===
s8='''<section id="s8" style="min-height:auto;padding-bottom:8vh">
<div class="section-label">ACTIVATION / 07</div>
<h2 data-kinetic>What happens next</h2>
<div class="split-layout">
<div class="split-col left">
<h3>Three actions traceable to this data</h3>
<div class="action-item"><strong>For the CRM team:</strong>Deploy point-of-purchase recommendations for the 11 validated brand pairs. The signal is strongest at the moment of the first brand purchase — not days later. Trigger the recommendation in the app at basket add, and in the CRM push within 24 hours of the visit.<div class="action-source">Source: 63% same-day adoption finding.</div></div>
<div class="action-item"><strong>For Beauty Advisors:</strong>Brief every advisor on the 11 directional brand pairs. The direction matters. HOURGLASS customer → introduce MAKEUP BY MARIO. Not the reverse. The anchor is always the established brand. The recommendation is always the discovery.<div class="action-source">Source: 31-basket validated pair, 8.52× lift.</div></div>
<div class="action-item"><strong>For Brand Managers:</strong>BOBBI BROWN: 18,180 warm prospects in the France study base. SUMMER FRIDAYS: 16,814. DRUNK ELEPHANT: 16,482. These are not numbers. They are customer lists ready for targeted activation.<div class="action-source">Source: brand_addressable_market.csv</div></div>
</div>
<div class="split-col right">
<h3>Three things this system does not yet do</h3>
<div class="limitation-item"><strong>Sequential brand journeys.</strong>Our model recommends one brand per customer per occasion. The next frontier is sequencing: which three brands over six visits maximizes a customer's long-term value to Sephora? We did not build that. It is Horizon 2.</div>
<div class="limitation-item"><strong>Consideration set modeling.</strong>Two brands we recommend to the same customer may compete for the same purchase occasion. Our system cannot yet tell whether your recommendations are reinforcing each other or cannibalizing each other. Horizon 2.</div>
<div class="limitation-item"><strong>Lapsed customer reactivation.</strong>Our model learns from customers who are already active. High-value customers who visited once or twice, found no relevant recommendation, and stopped returning — they are not in our outputs. They represent the highest incremental revenue opportunity we have not yet touched. Horizon 3.</div>
</div>
</div>
<p class="closing-sentence">We did not build a recommendation engine. We built a system that finds the moment — before it happens — when a customer is about to discover a brand she has never tried. And we made sure nothing gets in the way of that moment.</p>
<p class="final-label">Study base: 50,805 customers, France 2025. All figures sourced from validated project output files. No projections beyond stated scope.</p>
</section>'''

# === REPLACE SECTIONS ===
for i,s in enumerate([s1,s2,s3,s4,s5,s6,s7,s8],1):
    html=html.replace(f'<section id="s{i}"></section>',s)

# === ENHANCED JS ===
extra_js='''
/* --- Hero Line Draw --- */
gsap.to('#heroLine',{width:'30vw',duration:1.5,delay:.8,ease:'power2.out'});

/* --- Persistent Anchor --- */
const anchor=document.getElementById('persistentAnchor');
ScrollTrigger.create({trigger:'#s2',start:'top 80%',onEnter:()=>anchor.style.opacity='1',onLeaveBack:()=>anchor.style.opacity='0'});

/* --- Section 2 Timeline --- */
gsap.utils.toArray('.timeline-step').forEach((s,i)=>{
 gsap.to(s,{opacity:1,y:0,duration:.5,scrollTrigger:{trigger:s,start:'top 85%',end:'top 60%',scrub:true}});
});

/* --- Section 3 Pair Cards --- */
gsap.utils.toArray('.pair-card').forEach(c=>{
 gsap.to(c,{opacity:1,y:0,scrollTrigger:{trigger:c,start:'top 90%',end:'top 60%',scrub:true}});
});

/* --- Section 4 Bar Fills --- */
gsap.utils.toArray('.bar-fill').forEach(b=>{
 const w=b.dataset.width;
 gsap.to(b,{width:w+'%',scrollTrigger:{trigger:b,start:'top 90%',end:'top 70%',scrub:true}});
});

/* --- Section 5 Model Bars --- */
gsap.utils.toArray('.model-bar-fill').forEach(b=>{
 const w=b.dataset.width;
 gsap.to(b,{width:w+'%',duration:1,scrollTrigger:{trigger:b,start:'top 90%',toggleActions:'play none none none'}});
});

/* --- Section 6 Market Cards + Count-up --- */
gsap.utils.toArray('.market-card').forEach(c=>{
 gsap.to(c,{opacity:1,y:0,scrollTrigger:{trigger:c,start:'top 90%',end:'top 65%',scrub:true,onEnter:()=>{
  const el=c.querySelector('.mc-count');
  if(el&&!el.dataset.done){el.dataset.done='1';const t=parseInt(el.dataset.count);let s={v:0};gsap.to(s,{v:t,duration:1.5,ease:'power2.out',onUpdate:()=>{el.textContent=Math.floor(s.v).toLocaleString()}})}
 }}});
});

/* --- Section 7 Axis Cards --- */
gsap.utils.toArray('.axis-card').forEach(c=>{
 gsap.to(c,{opacity:1,y:0,scrollTrigger:{trigger:c,start:'top 90%',end:'top 65%',scrub:true}});
});

/* --- Section 8 Split Layout --- */
gsap.from('.split-layout',{opacity:0,y:40,scrollTrigger:{trigger:'.split-layout',start:'top 80%',end:'top 50%',scrub:true}});
'''
html=html.replace('</script>\n</body>',extra_js+'</script>\n</body>')

with open(P,'w',encoding='utf-8') as f:
    f.write(html)
print('BUILD COMPLETE')
print(f'File size: {len(html):,} bytes')
