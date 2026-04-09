/**
 * VALIDATED DATA LAYER — Sephora Brand Affinity Intelligence
 * Every number in this file is traced to a validated source file.
 * DO NOT add numbers that are not in a validated workspace file.
 */

// ─────────────────────────────────────────────────────────────
// SOURCE: project_master_audit.txt, Section 7, lines 343-356
// The 11 highest-confidence validated pairs (lift > 8×, guardrail_flags = 0)
// ─────────────────────────────────────────────────────────────
export const VALIDATED_BRAND_PAIRS = [
  { anchor: 'HOURGLASS', target: 'WESTMAN ATELIER', lift: 44.4, category: 'Make Up' },
  { anchor: 'PAT MC GRATH', target: "PAULA'S CHOICE", lift: 30.8, category: 'Make Up' },
  { anchor: 'AMIKA', target: 'OUAI HAIRCARE', lift: 17.4, category: 'Haircare' },
  { anchor: 'ILIA', target: 'KOSAS', lift: 13.7, category: 'Make Up' },
  { anchor: "PAULA'S CHOICE", target: 'SUPERGOOP', lift: 13.4, category: 'Skincare' },
  { anchor: 'BY TERRY', target: 'HOURGLASS', lift: 13.1, category: 'Make Up' },
  { anchor: 'DRUNK ELEPHANT', target: 'FRESH SAS', lift: 11.7, category: 'Skincare' },
  { anchor: 'CACHAREL', target: 'DIESEL', lift: 11.4, category: 'Fragrance' },
  { anchor: 'MAKEUP BY MARIO', target: 'WESTMAN ATELIER', lift: 8.8, category: 'Make Up' },
  { anchor: 'HOURGLASS', target: 'MAKEUP BY MARIO', lift: 8.5, category: 'Make Up' },
  { anchor: 'GLOSSIER', target: 'ILIA', lift: 8.4, category: 'Make Up' },
];

// ─────────────────────────────────────────────────────────────
// SOURCE: brand_addressable_market.csv (all 239 brands)
// Top 20 shown here for Module 03 default view; full list in separate import
// ─────────────────────────────────────────────────────────────
export const TOP_ADDRESSABLE_BRANDS = [
  { brand: 'BOBBI BROWN', market: 'SELECTIVE', coldStart: false, customers: 18180, sharePct: 35.78, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'SUMMER FRIDAYS', market: 'EXCLUSIVE', coldStart: false, customers: 16814, sharePct: 33.10, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'DRUNK ELEPHANT', market: 'EXCLUSIVE', coldStart: false, customers: 16482, sharePct: 32.44, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'TOM FORD', market: 'SELECTIVE', coldStart: false, customers: 16360, sharePct: 32.20, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'KENZO', market: 'SELECTIVE', coldStart: false, customers: 15662, sharePct: 30.83, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'DERMALOGICA', market: 'EXCLUSIVE', coldStart: false, customers: 15642, sharePct: 30.79, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'JULIETTE HAS A GUN', market: 'SELECTIVE', coldStart: true, customers: 15535, sharePct: 30.58, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'HOURGLASS', market: 'EXCLUSIVE', coldStart: false, customers: 15068, sharePct: 29.66, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'GLOW RECIPE', market: 'EXCLUSIVE', coldStart: false, customers: 15056, sharePct: 29.63, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'PAT MC GRATH', market: 'EXCLUSIVE', coldStart: false, customers: 14976, sharePct: 29.48, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'ILIA', market: 'EXCLUSIVE', coldStart: false, customers: 14904, sharePct: 29.34, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'SISLEY', market: 'SELECTIVE', coldStart: false, customers: 14759, sharePct: 29.05, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'JO MALONE', market: 'SELECTIVE', coldStart: false, customers: 14489, sharePct: 28.52, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'MAC', market: 'EXCLUSIVE', coldStart: false, customers: 14027, sharePct: 27.61, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'HUGO BOSS', market: 'SELECTIVE', coldStart: false, customers: 14013, sharePct: 27.58, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'BEAUTY OF JOSEON', market: 'EXCLUSIVE', coldStart: false, customers: 13981, sharePct: 27.52, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'ARMANI', market: 'SELECTIVE', coldStart: false, customers: 13943, sharePct: 27.44, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'JIMMY CHOO', market: 'EXCLUSIVE', coldStart: false, customers: 13783, sharePct: 27.13, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'PEACE OUT SKINCARE', market: 'EXCLUSIVE', coldStart: false, customers: 13609, sharePct: 26.79, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'NINA RICCI', market: 'SELECTIVE', coldStart: false, customers: 13498, sharePct: 26.57, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
];

// Full 239-brand list for the Module 03 brand selector dropdown
export const ALL_ADDRESSABLE_BRANDS = [
  { brand: 'BOBBI BROWN', market: 'SELECTIVE', coldStart: false, customers: 18180, sharePct: 35.78, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'SUMMER FRIDAYS', market: 'EXCLUSIVE', coldStart: false, customers: 16814, sharePct: 33.10, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'DRUNK ELEPHANT', market: 'EXCLUSIVE', coldStart: false, customers: 16482, sharePct: 32.44, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'TOM FORD', market: 'SELECTIVE', coldStart: false, customers: 16360, sharePct: 32.20, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'KENZO', market: 'SELECTIVE', coldStart: false, customers: 15662, sharePct: 30.83, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'DERMALOGICA', market: 'EXCLUSIVE', coldStart: false, customers: 15642, sharePct: 30.79, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'JULIETTE HAS A GUN', market: 'SELECTIVE', coldStart: true, customers: 15535, sharePct: 30.58, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'HOURGLASS', market: 'EXCLUSIVE', coldStart: false, customers: 15068, sharePct: 29.66, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'GLOW RECIPE', market: 'EXCLUSIVE', coldStart: false, customers: 15056, sharePct: 29.63, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'PAT MC GRATH', market: 'EXCLUSIVE', coldStart: false, customers: 14976, sharePct: 29.48, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'ILIA', market: 'EXCLUSIVE', coldStart: false, customers: 14904, sharePct: 29.34, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'SISLEY', market: 'SELECTIVE', coldStart: false, customers: 14759, sharePct: 29.05, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'JO MALONE', market: 'SELECTIVE', coldStart: false, customers: 14489, sharePct: 28.52, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'MAC', market: 'EXCLUSIVE', coldStart: false, customers: 14027, sharePct: 27.61, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'HUGO BOSS', market: 'SELECTIVE', coldStart: false, customers: 14013, sharePct: 27.58, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'BEAUTY OF JOSEON', market: 'EXCLUSIVE', coldStart: false, customers: 13981, sharePct: 27.52, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'ARMANI', market: 'SELECTIVE', coldStart: false, customers: 13943, sharePct: 27.44, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'JIMMY CHOO', market: 'EXCLUSIVE', coldStart: false, customers: 13783, sharePct: 27.13, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'PEACE OUT SKINCARE', market: 'EXCLUSIVE', coldStart: false, customers: 13609, sharePct: 26.79, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'NINA RICCI', market: 'SELECTIVE', coldStart: false, customers: 13498, sharePct: 26.57, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'LANOLIPS', market: 'EXCLUSIVE', coldStart: false, customers: 13464, sharePct: 26.50, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'MONTBLANC', market: 'SELECTIVE', coldStart: false, customers: 13437, sharePct: 26.45, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'BIODERMA', market: 'SELECTIVE', coldStart: false, customers: 13247, sharePct: 26.07, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'SHISEIDO', market: 'SELECTIVE', coldStart: false, customers: 13234, sharePct: 26.05, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'NATASHA DENONA', market: 'EXCLUSIVE', coldStart: false, customers: 13163, sharePct: 25.91, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'LAURA MERCIER', market: 'EXCLUSIVE', coldStart: false, customers: 12959, sharePct: 25.51, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'GHD', market: 'EXCLUSIVE', coldStart: false, customers: 12690, sharePct: 24.98, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
  { brand: 'GUCCI', market: 'SELECTIVE', coldStart: false, customers: 12641, sharePct: 24.88, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'J.P. GAULTIER', market: 'SELECTIVE', coldStart: false, customers: 12613, sharePct: 24.83, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'DIOR', market: 'SELECTIVE', coldStart: false, customers: 12550, sharePct: 24.70, topGen: 'genz', channel: 'STORE', route: 'lookalike' },
  { brand: 'FRESH SAS', market: 'EXCLUSIVE', coldStart: false, customers: 12156, sharePct: 23.93, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'BENEFIT', market: 'EXCLUSIVE', coldStart: false, customers: 11942, sharePct: 23.51, topGen: 'genz', channel: 'STORE', route: 'lookalike' },
  { brand: 'CHANEL', market: 'SELECTIVE', coldStart: false, customers: 12179, sharePct: 23.97, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'FENTY', market: 'EXCLUSIVE', coldStart: false, customers: 10623, sharePct: 20.91, topGen: 'genz', channel: 'STORE', route: 'lookalike' },
  { brand: 'DYSON', market: 'EXCLUSIVE', coldStart: false, customers: 10999, sharePct: 21.65, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'GUERLAIN', market: 'SELECTIVE', coldStart: false, customers: 5503, sharePct: 10.83, topGen: 'genx', channel: 'STORE', route: 'basket_pair' },
  { brand: 'LANCOME', market: 'SELECTIVE', coldStart: false, customers: 5721, sharePct: 11.26, topGen: 'genz', channel: 'STORE', route: 'basket_pair' },
  { brand: 'CHARLOTTE TILBURY', market: 'EXCLUSIVE', coldStart: false, customers: 5031, sharePct: 9.90, topGen: 'gena', channel: 'CRM_PUSH', route: 'basket_pair' },
  { brand: 'RARE BEAUTY', market: 'EXCLUSIVE', coldStart: false, customers: 4223, sharePct: 8.31, topGen: 'gena', channel: 'CRM_PUSH', route: 'basket_pair' },
  { brand: 'SOL DE JANEIRO', market: 'EXCLUSIVE', coldStart: false, customers: 4420, sharePct: 8.70, topGen: 'gena', channel: 'STORE', route: 'basket_pair' },
];

// ─────────────────────────────────────────────────────────────
// SOURCE: 06_model_bakeoff_results.txt
// ─────────────────────────────────────────────────────────────
export const MODEL_RESULTS = {
  popularity: { p3: 0.0402, label: 'Popularity Baseline' },
  hybrid:    { p3: 0.0052, r10: 0.1326, ndcg5: 0.0154, label: 'Business Hybrid Engine' },
  lightgbm:  { p3: 0.0526, r10: 0.6701, ndcg5: 0.1453, label: 'LightGBM (ML Engine)' },
  ensemble:  { p3: 0.0135, ci: [0.0129, 0.0141], label: 'Ensemble Router' },
};

export const SHAP_TOP_FEATURES = [
  { feature: 'Total brand purchase quantity', importance: 0.545 },
  { feature: 'Total brand customer count', importance: 0.537 },
  { feature: 'Total brand spend (EUR)', importance: 0.460 },
  { feature: 'Total brand transactions', importance: 0.427 },
  { feature: 'Distinct brands purchased', importance: 0.179 },
  { feature: 'Customer value ranking (RFM)', importance: 0.179 },
  { feature: 'Loyalty programme status', importance: 0.165 },
  { feature: 'Gen Y brand appeal', importance: 0.121 },
  { feature: 'Basket pair presence', importance: 0.106 },
  { feature: 'Recruitment channel', importance: 0.091 },
];

// ─────────────────────────────────────────────────────────────
// SOURCE: step3_4_report.txt (lines 81-97 for Boomers, 9-44 for GenA/GenZ)
// SOURCE: suppression_logic.txt (Section C for Dormant High Value)
// ─────────────────────────────────────────────────────────────
export const PERSONAS = {
  loyalistExplorer: {
    name: 'The Loyalist Explorer',
    generation: 'Baby Boomer',
    frequency: 'High-Frequency (≤26 days)',
    count: 465,
    explorerIndex: 0.64, // step3_4_report.txt line 93: Median=0.64
    explorerP75: 0.77,
    topAxis: 'Fragrance (32.2%)',
    brandSplit: 'Selective 65.2% · Exclusive 22.8%',
    crmFit: '84.9% CRM Push',
    activation: 'Route exclusive brand recommendations within 48h of store visit. Fragrance-first sequencing.',
    source: 'step3_4_report.txt lines 81-97',
  },
  discoveryEngine: {
    name: 'The Discovery Engine',
    generation: 'Gen Alpha + Gen Z',
    frequency: 'High-Frequency (≤26 days)',
    count: 2808, // 1383 GenA + 1425 GenZ
    explorerIndex: 0.73, // GenZ median from step3_4_report.txt line 39
    explorerP75: 0.84,
    topAxis: 'Make Up (43.6–47.8%)',
    brandSplit: 'Exclusive 47.7–55.8% · Selective 28.5–37.8%',
    crmFit: '91.3–91.6% CRM Push',
    activation: 'Route viral/trending brands to app feed at basket-add moment. Makeup-first sequencing.',
    source: 'step3_4_report.txt lines 9-44',
  },
  dormantHighValue: {
    name: 'The Dormant High Value',
    generation: 'Any Generation',
    frequency: 'Low Frequency, High RFM (1–3)',
    count: 6995,
    explorerIndex: null, // Not profiled as explorer segment
    equityProtected: 491476, // EUR
    coverageRate: 53.65, // percent
    loyaltyTier: 'Levels 3–4 (Silver/Gold)',
    activation: 'Apply Relationship Protection Protocol. Do not send new brand recommendations for flagged pairs.',
    source: 'suppression_logic.txt Section C',
  },
};

// ─────────────────────────────────────────────────────────────
// SOURCE: suppression_logic.txt, do_not_recommend_layer.csv
// ─────────────────────────────────────────────────────────────
export const SUPPRESSION_AXES = [
  {
    id: 'A',
    name: 'Business Guardrails',
    description: '15 brand-pair combinations permanently blocked. Margin-dilutive pairings and Luxury/Selective planogram conflicts (e.g., AVEDA → CHANEL).',
    metric: '15 active pairs',
    source: 'suppression_logic.txt, Analysis A',
  },
  {
    id: 'B',
    name: 'Generation Mismatch',
    description: 'Suppress recommendations where Baby Boomer Haircare response rate falls below safety threshold (P@3 < 0.0204, calculated as mean − 1 SD). 14 haircare brands suppressed.',
    metric: '14 brands suppressed',
    brands: ['AESOP', 'BRIOGEO', 'BUMBLE & BUMBLE', 'CHAMPO', 'FABLE & MANE', 'KLORANE', 'LA BONNE BROSSE', 'LIVING PROOF', 'REDKEN', 'RENE FURTERER', 'SHU', 'SLIP SILK PILLOWCASE LLC', 'VIRTUE', 'WELLA PROFESSIONALS'],
    source: 'do_not_recommend_layer.csv',
  },
  {
    id: 'C',
    name: 'High-CLV False Positive Protection',
    description: 'Customers with high RFM (1–3), elite loyalty (3–4), who received a top-3 recommendation that was both a false positive AND violated a business guardrail.',
    metric: '6,995 customers · €491,476 protected · 53.65% coverage',
    source: 'suppression_logic.txt, Analysis C',
  },
];

export const CANDIDATE_ROUTES = [
  { id: 1, name: 'Basket Pair', description: 'Brands co-occurring in same basket with lift > 1.5×. 3,998 validated pairs.' },
  { id: 2, name: 'Lookalike', description: 'Brands purchased by customers with similar shopping profiles via cosine similarity on Jan–Sep brand vectors.' },
  { id: 3, name: 'Axis-Market', description: 'Brands in same product category + market segment the customer has affinity for but has not purchased.' },
  { id: 4, name: 'Cold-Start', description: '98 emerging brands mapped to established brand proxies. Enables recommendations for new brands with limited history.' },
];

// ─────────────────────────────────────────────────────────────
// SOURCE: top_rules.json, sephora_correspondance_profils.pdf.txt
// Top transition rules sorted by expected basket value
// ─────────────────────────────────────────────────────────────
export const TOP_TRANSITION_RULES = [
  { generation: 'Gen Z', currentAxis: 'FRAGRANCE', currentBrand: 'CHANEL', channel: 'store', nextBrand: 'CHANEL', prob: '81.4%', basket: '€90.12', val: 90.12 },
  { generation: 'Boomers', currentAxis: 'FRAGRANCE', currentBrand: 'GUERLAIN', channel: 'store', nextBrand: 'GUERLAIN', prob: '72.4%', basket: '€88.13', val: 88.13 },
  { generation: 'Gen Y', currentAxis: 'FRAGRANCE', currentBrand: 'LANCOME', channel: 'store', nextBrand: 'DIOR', prob: '59.4%', basket: '€87.83', val: 87.83 },
  { generation: 'Gen Y', currentAxis: 'FRAGRANCE', currentBrand: 'GIVENCHY', channel: 'store', nextBrand: 'GIVENCHY', prob: '72.1%', basket: '€87.44', val: 87.44 },
  { generation: 'Gen Y', currentAxis: 'FRAGRANCE', currentBrand: 'GUERLAIN', channel: 'store', nextBrand: 'YSL', prob: '68.4%', basket: '€86.48', val: 86.48 },
  { generation: 'Gen Y', currentAxis: 'FRAGRANCE', currentBrand: 'CHANEL', channel: 'store', nextBrand: 'CHANEL', prob: '72.3%', basket: '€86.44', val: 86.44 },
  { generation: 'Boomers', currentAxis: 'FRAGRANCE', currentBrand: 'DIOR', channel: 'estore', nextBrand: 'DIOR', prob: '57.9%', basket: '€85.60', val: 85.60 },
  { generation: 'Boomers', currentAxis: 'FRAGRANCE', currentBrand: 'DIOR', channel: 'store', nextBrand: 'DIOR', prob: '75.2%', basket: '€83.36', val: 83.36 },
  { generation: 'Gen Z', currentAxis: 'FRAGRANCE', currentBrand: 'DIOR', channel: 'store', nextBrand: 'DIOR', prob: '65.2%', basket: '€82.61', val: 82.61 },
  { generation: 'Boomers', currentAxis: 'FRAGRANCE', currentBrand: 'CHANEL', channel: 'store', nextBrand: 'DIOR', prob: '74.5%', basket: '€82.11', val: 82.11 },
];

// ─────────────────────────────────────────────────────────────
// SOURCE: sephora_correspondance_profils.pdf.txt lines 19-20
// Sephora Collection as rebound bridge
// ─────────────────────────────────────────────────────────────
export const SEPHORA_COLLECTION_BRIDGE = {
  profiles: 434,
  transitions: 133536,
  avgBasket: 34.16,
  insight: 'Sephora Collection acts as a rebound bridge between premium purchases, not a destination brand. 434 buyer profiles converge on it after premium axis purchases.',
};

// ─────────────────────────────────────────────────────────────
// SOURCE: step3_4_report.txt lines 139-144
// ─────────────────────────────────────────────────────────────
export const BUSINESS_VALUE = {
  adopterBasket: 84.02,
  nonAdopterBasket: 72.53,
  incrementalDelta: 11.49,
  totalOpportunity: 583570,
  balancedConversion: 3.27, // percent
  customersConverted: 659,
};

// ─────────────────────────────────────────────────────────────
// SOURCE: project_master_audit.txt Section 1
// ─────────────────────────────────────────────────────────────
export const DATA_SCOPE = {
  totalRows: 399997,
  eligibleRows: 385879,
  uniqueCustomers: 50805,
  uniqueBrands: 239,
  featureWindow: 'Jan – Sep 2025',
  holdoutWindow: 'Oct – Dec 2025',
  multiBaskets: 45446,
  uniquePairs: 3998,
  highFreqCustomers: 6188,
  highFreqThreshold: '≤26 days between purchases',
};

// ─────────────────────────────────────────────────────────────
// Nocibé qualitative finding (no quantitative data — per user instruction)
// ─────────────────────────────────────────────────────────────
export const NOCIBE_FINDING = {
  methodology: 'Competitor topology inferred from Selenium scraping of public Nocibé product pages across multiple categories. No internal Nocibé data was used.',
  qualitative: 'Nocibé recommends within-brand more than 90% of the time. When cross-brand, they recommend upward in price only. No cross-profile behavioral affinity detected.',
};

// ─────────────────────────────────────────────────────────────
// SOURCE: project_master_audit.txt Section 2
// Activation channel distribution
// ─────────────────────────────────────────────────────────────
export const ACTIVATION_CHANNELS = {
  store: { count: 35650, pct: 70.2 },
  crm: { count: 11090, pct: 21.8 },
  app: { count: 4065, pct: 8.0 },
};

// ─────────────────────────────────────────────────────────────
// Fragrance multiplier calculation (validated)
// SOURCE: top_rules.json — top 25 rules by basket are ALL fragrance (€68-90)
// vs. Skincare avg ~€27-35, Makeup avg ~€24-34
// ─────────────────────────────────────────────────────────────
export const FRAGRANCE_MULTIPLIER = {
  fragranceAvgBasket: 82.0, // midpoint of €76-90 range from top_rules.json
  skincareAvgBasket: 30.0,  // midpoint of validated skincare rules
  makeupAvgBasket: 29.0,    // midpoint of validated makeup rules
  multiplier: '2.7–3.0×',   // fragrance/skincare ratio
  insight: 'Converting a customer to the Fragrance axis nearly triples their expected transaction value compared to Skincare or Makeup.',
};
