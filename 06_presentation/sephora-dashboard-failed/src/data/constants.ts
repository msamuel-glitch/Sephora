export const BRAND_PAIRS = [
  { anchor: 'HOURGLASS', rec: 'MAKEUP BY MARIO', lift: 8.52, baskets: 31, cat: 'Make Up', exp: 'Premium artistry philosophy match — not a price coincidence.', label: 'Highest absolute support', p: 0.0012 },
  { anchor: 'HOURGLASS', rec: 'WESTMAN ATELIER', lift: 44.38, baskets: 10, cat: 'Make Up', exp: 'Highest lift in the dataset. Directional signal concentrated in a specific customer type.', label: 'Highest lift — directional signal', p: 0.0001 },
  { anchor: 'PAT MC GRATH', rec: "PAULA'S CHOICE", lift: 30.84, baskets: 5, cat: 'Make Up → Skincare', exp: 'Cross-category: luxury colour cosmetics into evidence-based skincare.', p: 0.0003 },
  { anchor: 'AMIKA', rec: 'OUAI HAIRCARE', lift: 17.45, baskets: 7, cat: 'Haircare', exp: 'Premium haircare as investment — a customer identity signal.', p: 0.0008 },
  { anchor: 'ILIA', rec: 'KOSAS', lift: 13.65, baskets: 10, cat: 'Make Up', exp: 'Clean beauty routine builders. KOSAS is the natural next step.', p: 0.0015 },
  { anchor: "PAULA'S CHOICE", rec: 'SUPERGOOP', lift: 13.40, baskets: 5, cat: 'Skincare', exp: 'Evidence-based skincare to SPF. Science-minded customer cohort.', p: 0.0021 },
  { anchor: 'BY TERRY', rec: 'HOURGLASS', lift: 13.08, baskets: 7, cat: 'Make Up', exp: 'Prestige French to prestige American. Luxury without geographic loyalty.', p: 0.0019 },
  { anchor: 'DRUNK ELEPHANT', rec: 'FRESH SAS', lift: 11.73, baskets: 5, cat: 'Skincare', exp: 'The missed conversation — confirmed by the data.', p: 0.0028 },
  { anchor: 'CACHAREL', rec: 'DIESEL', lift: 11.41, baskets: 7, cat: 'Fragrance', exp: 'Heritage French fragrance to contemporary edge.', p: 0.0031 },
  { anchor: 'MAKEUP BY MARIO', rec: 'WESTMAN ATELIER', lift: 8.79, baskets: 5, cat: 'Make Up', exp: 'Artistry expanding upward into ultra-premium.', p: 0.0044 },
  { anchor: 'GLOSSIER', rec: 'ILIA', lift: 8.42, baskets: 6, cat: 'Make Up', exp: 'Entry-level clean beauty graduating into intentional routine.', p: 0.0048 },
];

export const ADDRESSABLE_MARKET = [
  { brand: 'BOBBI BROWN', segment: 'Selective', count: 18180, pct: '35.8%', note: 'More than 1 in 3 study-base customers already behaves like a BOBBI BROWN buyer.' },
  { brand: 'SUMMER FRIDAYS', segment: 'Exclusive', count: 16814, pct: '33.1%', note: 'An exclusive brand — customers can only find it at Sephora.' },
  { brand: 'DRUNK ELEPHANT', segment: 'Exclusive', count: 16482, pct: '32.4%', note: 'The anchor brand from Section 2. Unactivated affinity.' },
  { brand: 'TOM FORD', segment: 'Selective', count: 15662, pct: '30.8%', note: '' },
  { brand: 'KENZO', segment: 'Selective', count: 15662, pct: '30.8%', note: '' },
];

export const SHAP_ACTIONABLE = [
  { tech: 'rfm_segment_snapshot', label: 'Customer value tier' },
  { tech: 'loyalty_status_at_snapshot', label: 'Loyalty programme status' },
  { tech: 'gen_brand_appeal_geny', label: 'Gen Y brand appeal' },
  { tech: 'has_basket_pair', label: 'Basket pair signal present' },
  { tech: 'recruitment_channel', label: 'Recruitment channel' },
  { tech: 'velocity_score', label: 'Purchase velocity' },
  { tech: 'gen_brand_appeal_genz', label: 'Gen Z brand appeal' },
  { tech: 'gen_brand_appeal_gena', label: 'Gen Alpha brand appeal' },
  { tech: 'rfm_trajectory', label: 'Customer value trajectory' },
  { tech: 'launch_readiness_score', label: 'Launch readiness' },
  { tech: 'loyalist_vs_explorer_index', label: 'Explorer vs loyalist index' },
  { tech: 'gen_brand_appeal_babyboomers', label: 'Boomer brand appeal' },
  { tech: 'app_recommendation_affinity_proxy', label: 'App recommendation affinity' },
];

export const SHAP_DESCRIPTIVE = [
  { tech: 'total_brand_qty', label: 'Brand quantity sold' },
  { tech: 'total_brand_customers', label: 'Brand customer count' },
  { tech: 'total_brand_spend', label: 'Brand spend' },
  { tech: 'total_brand_transactions', label: 'Brand transactions' },
  { tech: 'total_brands', label: 'Brands purchased' },
  { tech: 'avg_basket', label: 'Average basket size' },
  { tech: 'total_transactions', label: 'Total transactions' },
];

export const EXPLORER_DATA = [
  { gen: 'Gen Z', high: 0.66, low: 0.44 },
  { gen: 'Gen Alpha', high: 0.64, low: 0.42 },
  { gen: 'Gen Y', high: 0.63, low: 0.39 },
  { gen: 'Boomers', high: 0.65, low: 0.40 },
];

export const ADOPTION_TIMING = [
  { day: 'Day 0', count: 126, pct: 63 },
  { day: '15d', count: 5, pct: 2.5 },
  { day: '30d', count: 4, pct: 2 },
  { day: '45d', count: 8, pct: 4 },
  { day: '60d', count: 7, pct: 3.5 },
  { day: '75d', count: 10, pct: 5 },
  { day: '90d', count: 6, pct: 3 },
  { day: '105d', count: 5, pct: 2.5 },
  { day: '120d', count: 9, pct: 4.5 },
];

export const MODEL_COMPARISON = [
  { name: 'Popularity Engine', pct: 4.02, color: '#333333', desc: 'Recommends the most-purchased brands for everyone. This is the floor.' },
  { name: 'Hybrid Engine', pct: 0.52, color: '#555555', desc: 'Surfaces niche & emerging brands by design — built for discovery, not prediction.' },
  { name: 'ML Model', pct: 5.26, color: '#E2001A', desc: '31% more accurate than baseline. 1.24pp above the floor.' },
];

export const CATEGORIES = ['All', 'Make Up', 'Skincare', 'Haircare', 'Fragrance'] as const;

export const CAT_COLORS: Record<string, string> = {
  'Make Up': '#E2001A',
  'Skincare': '#2D6A4F',
  'Haircare': '#8B5E3C',
  'Fragrance': '#6B4C9A',
  'Make Up → Skincare': '#C4153A',
};

export const SECTION_NAMES = [
  'Brand Affinity Intelligence',
  'The Missed Moment',
  'The 11 Brand Pairs',
  'The Customer Profile',
  'The Engine',
  'Addressable Market',
  'The Protection Layer',
  'Monday Morning',
];
