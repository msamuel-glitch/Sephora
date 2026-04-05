"""
Step 5: Generate Final Phase 6 Deliverables
Includes:
1. Statistical Significance Tests on Brand Pairs
2. APP/E-MERCH Feed Output
3. Store Beauty Advisor Brand-Pairing Guide
4. Brand Market Sizing Report
5. Top 10 Store Brand Pairs (Presentable)
6. Business Value Quantification
"""
import pandas as pd
import numpy as np
import os, time
from scipy.stats import chi2_contingency, fisher_exact
import warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
AUDIT_BASE = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")
DIM_CUST = os.path.join(BASE, "03_data_working", "dim_customer.csv")
DIM_BRAND = os.path.join(BASE, "03_data_working", "dim_brand.csv")
DIM_PAIR = os.path.join(BASE, "03_data_working", "dim_brand_pair.csv")
FACT_CAND = os.path.join(BASE, "03_data_working", "fact_customer_brand_candidate.csv")

OUT_DIR = os.path.join(BASE, "05_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

APP_FEED = os.path.join(OUT_DIR, "app_emerchandising_feed.csv")
STORE_GUIDE = os.path.join(OUT_DIR, "store_brand_pairing_guide.csv")
MARKET_SIZING = os.path.join(OUT_DIR, "brand_addressable_market.csv")
TOP10_PRESENTABLE = os.path.join(OUT_DIR, "top10_store_brand_pairs_presentable.csv")
REPORT_PATH = os.path.join(BASE, "04_analysis", "step3_4_report.txt")

def log(msg):
    print(msg, flush=True)

t0 = time.time()
log("=" * 60)
log("Phase 6 Deliverables Generation Script")
log("=" * 60)

# ============================================================
# 0. LOAD DATA
# ============================================================
log("\n[0] Loading data tables...")
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
df_elig = df_audit[df_audit['eligible_for_affinity_v1'] == True].copy()
df_elig['trans_date'] = pd.to_datetime(df_elig['transactionDate'], errors='coerce')
df_elig['month'] = df_elig['trans_date'].dt.month
# Feature window (Jan-Sep)
df_feat = df_elig[df_elig['month'] <= 9].copy()
# Target window (Oct-Dec)
df_target = df_elig[df_elig['month'] > 9].copy()

dim_customer = pd.read_csv(DIM_CUST)
dim_brand = pd.read_csv(DIM_BRAND)
dim_brand_pair = pd.read_csv(DIM_PAIR)
fact_cand = pd.read_csv(FACT_CAND)

# ============================================================
# 1. STATISTICAL SIGNIFICANCE TESTS
# ============================================================
log("\n[1] Running Statistical Significance Tests (Ticket Level)...")
total_tickets = df_feat['anonymized_Ticket_ID'].nunique()
brand_ticket_counts = df_feat.groupby('brand')['anonymized_Ticket_ID'].nunique().to_dict()

p_values = []
test_used = []
is_sig = []

for _, row in dim_brand_pair.iterrows():
    b_a = row['brand_a']
    b_b = row['brand_b']
    obs_both = row['cooccurrence_count']
    
    count_a = brand_ticket_counts.get(b_a, 0)
    count_b = brand_ticket_counts.get(b_b, 0)
    
    # Contingency Table:
    #             In B    Not in B
    #   In A      obs_both   count_a - obs_both
    #   Not in A  count_b-obs  total - count_a - count_b + obs
    
    a_and_b = obs_both
    a_not_b = count_a - obs_both
    not_a_b = count_b - obs_both
    not_a_not_b = total_tickets - count_a - count_b + obs_both
    
    table = [[a_and_b, a_not_b], [not_a_b, not_a_not_b]]
    expected = (np.array([a_and_b + a_not_b, not_a_b + not_a_not_b])[:,None] * 
               np.array([a_and_b + not_a_b, a_not_b + not_a_not_b])[None,:]) / total_tickets
    
    if np.any(expected < 5):
        # Fisher's Exact (using 2-sided)
        odds, p = fisher_exact(table)
        test = "Fisher"
    else:
        # Chi-Square
        chi2, p, dof, ex = chi2_contingency(table)
        test = "Chi-Square"
        
    p_values.append(p)
    test_used.append(test)
    is_sig.append(p < 0.05)

dim_brand_pair['p_value'] = p_values
dim_brand_pair['significance_test_used'] = test_used
dim_brand_pair['is_significant'] = is_sig
dim_brand_pair.to_csv(DIM_PAIR, index=False)
log(f"    Significance tests complete for {len(dim_brand_pair)} pairs.")

# ============================================================
# 2. APP/E-MERCH FEED OUTPUT
# ============================================================
log("\n[2] Generating APP/E-MERCH Feed...")
# Join priorities
cand_full = fact_cand.merge(
    dim_brand[['brand', 'brand_volatility_index', 'not_just_popularity_penalty', 'market_priority_balanced_growth', 'primary_market']],
    left_on='candidate_brand', right_on='brand', how='left'
)

# Balanced Scenario Score Logic (Matching Phase 5 blueprint)
cand_full['route_score'] = (cand_full['has_basket_pair'] * 2.0 + 
                            cand_full['has_lookalike'] * 1.0 + 
                            cand_full['has_axis_market'] * 0.5 + 
                            cand_full['has_cold_start'] * 0.5)

cand_full['composite_score'] = (cand_full['route_score'] + 
                                cand_full['not_just_popularity_penalty'] * 2.0 + 
                                (1 - cand_full['brand_volatility_index'].fillna(1)) * 1.5 +
                                cand_full['market_priority_balanced_growth'] * 3.0)

# Join user info
cand_full = cand_full.merge(
    dim_customer[['anonymized_card_code', 'age_generation']], on='anonymized_card_code', how='left'
)

# Rank top 10
cand_full = cand_full.sort_values(['anonymized_card_code', 'composite_score'], ascending=[True, False])
app_feed = cand_full.groupby('anonymized_card_code').head(10).copy()
app_feed['rank'] = app_feed.groupby('anonymized_card_code').cumcount() + 1

app_feed_final = app_feed[[
    'anonymized_card_code', 'rank', 'candidate_brand', 'composite_score', 
    'candidate_routes', 'age_generation', 'primary_market'
]].rename(columns={'anonymized_card_code': 'customer_id', 'candidate_brand': 'brand', 'age_generation': 'generation', 'primary_market': 'market_desc'})

app_feed_final.to_csv(APP_FEED, index=False)
log(f"    app_emerchandising_feed.csv saved ({len(app_feed_final)} rows).")

# ============================================================
# 3. STORE BEAUTY ADVISOR BRAND-PAIRING CARD
# ============================================================
log("\n[3] Generating Store Brand-Pairing Guide...")
# Need top generation affinity
log("    Calculating generation concentration for pairs...")

# Get customer generation map
cust_gen_map = dim_customer.set_index('anonymized_card_code')['age_generation'].to_dict()
gen_base_counts = dim_customer['age_generation'].value_counts().to_dict()

# Filter dim_brand_pair
guide = dim_brand_pair[
    (dim_brand_pair['brand_cooccurrence_lift'] > 1.5) & 
    (dim_brand_pair['cooccurrence_count'] >= 5) &
    (dim_brand_pair['high_price_artifact_flag'] == 0) &
    (dim_brand_pair['trivial_association_flag'] == 0) &
    (dim_brand_pair['quantity_revenue_divergence'].fillna(0) <= 20)
].copy()

# For these pairs, find the top generation
top_gens = []
for _, row in guide.iterrows():
    b_a, b_b = row['brand_a'], row['brand_b']
    # Customers buying both in feature window
    custs_a = set(df_feat[df_feat['brand'] == b_a]['anonymized_card_code'])
    custs_b = set(df_feat[df_feat['brand'] == b_b]['anonymized_card_code'])
    both_custs = custs_a.intersection(custs_b)
    
    if not both_custs:
        top_gens.append('UNKNOWN')
        continue
        
    gen_counts = pd.Series([cust_gen_map.get(c, 'UNKNOWN') for c in both_custs]).value_counts()
    # concentration
    gen_conc = {g: count/gen_base_counts.get(g, 1) for g, count in gen_counts.items()}
    best_gen = max(gen_conc, key=gen_conc.get)
    top_gens.append(best_gen)

guide['top_generation_affinity'] = top_gens

# Add metadata
brand_meta = dim_brand.set_index('brand')
guide['dominant_axis'] = guide['brand_a'].map(brand_meta['primary_axis'])
guide['market_desc_pair'] = guide['brand_a'].map(brand_meta['primary_market']) + " + " + guide['brand_b'].map(brand_meta['primary_market'])
guide['guardrail_flags'] = "None" 

guide_final = guide[[
    'brand_a', 'brand_b', 'brand_cooccurrence_lift', 'basket_complementarity_score',
    'dominant_axis', 'market_desc_pair', 'guardrail_flags', 'top_generation_affinity'
]].rename(columns={'brand_a': 'anchor_brand', 'brand_b': 'recommended_brand', 'brand_cooccurrence_lift': 'co_occurrence_lift'})

guide_final.to_csv(STORE_GUIDE, index=False)
log(f"    store_brand_pairing_guide.csv saved ({len(guide_final)} rows).")

# ============================================================
# 4. BRAND MARKET SIZING REPORT
# ============================================================
log("\n[4] Generating Brand Market Sizing Report...")

# Addressable pool = top 30% of that brand's score who never purchased it.
cust_never_purchased = df_feat.groupby('brand')['anonymized_card_code'].apply(set).to_dict()

market_sizing = []
for brand_name, df_b in cand_full.groupby('candidate_brand'):
    history_set = cust_never_purchased.get(brand_name, set())
    # Candidate pool for this brand who never bought it
    pool_never = df_b[~df_b['anonymized_card_code'].isin(history_set)].copy()
    if pool_never.empty:
        continue
        
    # Top 30% score threshold for THIS brand
    thresh = pool_never['composite_score'].quantile(0.7)
    high_affinity = pool_never[pool_never['composite_score'] >= thresh]
    
    pool_size = len(high_affinity)
    share_pct = (pool_size / 50805) * 100
    
    top_gen = high_affinity['age_generation'].mode()[0] if not high_affinity['age_generation'].mode().empty else "UNKNOWN"
    
    # activation channels
    cust_channels = dim_customer.set_index('anonymized_card_code')['channel_activation_fit_score'].to_dict()
    high_affinity['channel'] = high_affinity['anonymized_card_code'].map(cust_channels)
    top_chan = high_affinity['channel'].mode()[0] if not high_affinity['channel'].mode().empty else "UNKNOWN"
    
    # top route
    route_cols = ['has_basket_pair', 'has_lookalike', 'has_axis_market', 'has_cold_start']
    route_counts = high_affinity[route_cols].sum()
    top_route = route_counts.idxmax().replace('has_', '')
    
    market_sizing.append({
        'brand': brand_name,
        'market_desc': dim_brand[dim_brand['brand'] == brand_name]['primary_market'].values[0],
        'cold_start_flag': 1 if dim_brand[dim_brand['brand'] == brand_name]['brand_history_depth'].values[0] == 'Emerging' else 0,
        'total_customers_with_high_affinity_never_purchased': pool_size,
        'share_of_base_pct': round(share_pct, 2),
        'top_generation': top_gen,
        'top_activation_channel': top_chan,
        'top_candidate_route': top_route
    })

market_sizing_df = pd.DataFrame(market_sizing).sort_values('total_customers_with_high_affinity_never_purchased', ascending=False)
market_sizing_df.to_csv(MARKET_SIZING, index=False)
log(f"    brand_addressable_market.csv saved ({len(market_sizing_df)} rows).")

# ============================================================
# 5. TOP 10 PRESENTABLE STORE BRAND PAIRS
# ============================================================
log("\n[5] Generating Top 10 Presentable Pairs...")

top10 = guide[guide['is_significant'] == True].sort_values('basket_complementarity_score', ascending=False).head(10).copy()

def generate_story(row):
    b1, b2 = row['brand_a'], row['brand_b']
    axis = row['dominant_axis']
    mkt = row['market_desc_pair']
    lift = row['brand_cooccurrence_lift']
    return f"Customers buying {b1} show a {lift:.1f}x higher affinity for {b2} in {axis}, making them prime cross-sell candidates within the {mkt} segment."

top10['pairing_story'] = top10.apply(generate_story, axis=1)
top10_final = top10[[
    'brand_a', 'brand_b', 'brand_cooccurrence_lift', 'basket_complementarity_score',
    'dominant_axis', 'market_desc_pair', 'pairing_story'
]].rename(columns={'brand_a': 'anchor_brand', 'brand_b': 'recommended_brand', 'brand_cooccurrence_lift': 'co_occurrence_lift'})

top10_final.to_csv(TOP10_PRESENTABLE, index=False)
log(f"    top10_store_brand_pairs_presentable.csv saved.")

# ============================================================
# 6. BUSINESS VALUE QUANTIFICATION
# ============================================================
log("\n[6] Quantifying Business Value...")

# Get customers who bought a NEW brand in Oct-Dec (Target Window)
# that they had not bought in Jan-Sep (Feature Window)
cust_hist_brands = df_feat.groupby('anonymized_card_code')['brand'].apply(set).to_dict()
cust_target_brands = df_target.groupby('anonymized_card_code')['brand'].apply(set).to_dict()

adopters = []
non_adopters = []

# Iterate over brands to define the pools as requested
for brand_name in cand_full['candidate_brand'].unique():
    # Who was in the candidate pool for this brand?
    b_cands = set(cand_full[cand_full['candidate_brand'] == brand_name]['anonymized_card_code'])
    # Who actually bought this brand in Oct-Dec?
    b_purchasers = set(df_target[df_target['brand'] == brand_name]['anonymized_card_code'])
    # Who had NEVER bought it before Oct?
    b_history = cust_never_purchased.get(brand_name, set())
    
    # ADOPTERS for this brand: In candidate pool AND bought in Target AND Never bought before
    b_adopters = b_cands.intersection(b_purchasers).difference(b_history)
    # NON-ADOPTERS for this brand: In candidate pool AND Never bought before AND NOT bought in Target
    b_non_adopters = b_cands.difference(b_purchasers).difference(b_history)
    
    adopters.extend(list(b_adopters))
    non_adopters.extend(list(b_non_adopters))

# Dedup
adopters = list(set(adopters))
non_adopters = list(set(non_adopters))

# Get basket values in Target Window
basket_vals = df_target.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['salesVatEUR'].sum().reset_index()
avg_basket = basket_vals.groupby('anonymized_card_code')['salesVatEUR'].mean().to_dict()

adopter_baskets = [avg_basket[c] for c in adopters if c in avg_basket]
non_adopter_baskets = [avg_basket[c] for c in non_adopters if c in avg_basket]

mean_adopter = np.mean(adopter_baskets) if adopter_baskets else 0
mean_non_adopter = np.mean(non_adopter_baskets) if non_adopter_baskets else 0
delta = mean_adopter - mean_non_adopter
total_uplift = delta * 50805

log(f"    Adopters Mean Basket: EUR {mean_adopter:.2f}")
log(f"    Non-Adopters Mean Basket: EUR {mean_non_adopter:.2f}")
log(f"    Incremental Delta: EUR {delta:.2f} per customer")
log(f"    Total Addressable Uplift (scaled to 50k base): EUR {total_uplift:,.0f}")

with open(REPORT_PATH, 'a', encoding='utf-8') as f:
    f.write("\n\n--- Estimated Business Value ---\n")
    f.write(f"Adopters Mean Basket (Target Window): EUR {mean_adopter:.2f}\n")
    f.write(f"Non-Adopters Mean Basket (Target Window): EUR {mean_non_adopter:.2f}\n")
    f.write(f"Estimated Incremental Delta: EUR {delta:.2f} per positive conversion\n")
    f.write(f"Total Scaled Addressable Opportunity: EUR {total_uplift:,.0f}\n")
    f.write(f"Methodology: Comparison of Oct-Dec average basket value for customers in the candidate pool who converted vs those who did not.\n")

elapsed = time.time() - t0
log(f"\n[DONE] All Phase 6 deliverables generated in {elapsed:.1f}s")
