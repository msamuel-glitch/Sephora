"""
Step 3: High-frequency customer profiling
Step 4: Composite scoring engine evaluation
"""
import pandas as pd
import numpy as np
import os, time
import warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
AUDIT_BASE = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")
DIM_CUST = os.path.join(BASE, "03_data_working", "dim_customer.csv")
DIM_BRAND = os.path.join(BASE, "03_data_working", "dim_brand.csv")
FACT_CAND = os.path.join(BASE, "03_data_working", "fact_customer_brand_candidate.csv")

OUT_REPORT = os.path.join(BASE, "04_analysis", "step3_4_report.txt")

lines = []
def log(msg):
    print(msg)
    lines.append(str(msg))

t0 = time.time()
log("=" * 60)
log("Step 3: High-frequency Setup & Step 4: Scoring Engine")
log("=" * 60)

# ============================================================
# 0. LOAD TABLES
# ============================================================
log("\n[0] Loading data...")
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
df_elig = df_audit[df_audit['eligible_for_affinity_v1'] == True].copy()
df_elig['trans_date'] = pd.to_datetime(df_elig['transactionDate'], errors='coerce')
df_elig['month'] = df_elig['trans_date'].dt.month

df_feat = df_elig[df_elig['month'] <= 9].copy()
df_target = df_elig[df_elig['month'] > 9].copy()

dim_customer = pd.read_csv(DIM_CUST)
dim_brand = pd.read_csv(DIM_BRAND)
if not os.path.exists(FACT_CAND):
    log("fact_customer_brand_candidate.csv not found. Did Step 1 finish?")
else:
    fact_cand = pd.read_csv(FACT_CAND)

# Target purchases map
cust_target_history = df_target.groupby('anonymized_card_code')['brand'].apply(set).to_dict()

# ============================================================
# 3. HIGH FREQUENCY PROFILING
# ============================================================
log("\n[3] High-Frequency Customer Profiling")
hf_cust = dim_customer[dim_customer['high_frequency_flag'] == 1].copy()
hf_codes = set(hf_cust['anonymized_card_code'])

df_hf = df_feat[df_feat['anonymized_card_code'].isin(hf_codes)].copy()

generations = ['gena', 'genz', 'geny', 'genx', 'babyboomers', 'UNKNOWN']
for gen in generations:
    subset = hf_cust[hf_cust['age_generation'] == gen]
    n_cust = len(subset)
    if n_cust == 0:
        continue
    
    log(f"\n--- HIGH FREQUENCY PROFILE: {gen.upper()} ---")
    log(f"Count: {n_cust} customers")
    
    # Get transaction level features for these exact customers
    subset_df = df_hf[df_hf['anonymized_card_code'].isin(subset['anonymized_card_code'])]
    
    # Dominant axes by spend
    axes = subset_df.groupby('Axe_Desc')['salesVatEUR'].sum().sort_values(ascending=False)
    axes_pct = (axes / axes.sum() * 100).round(1).head(3)
    log(f"Top Axes by Spend:")
    for a, p in axes_pct.items():
        log(f"  {a}: {p}%")
        
    # Brand-family splits (Market_Desc)
    mkt = subset_df.groupby('Market_Desc')['salesVatEUR'].sum().sort_values(ascending=False)
    mkt_pct = (mkt / mkt.sum() * 100).round(1)
    log(f"Brand-Family Split:")
    for m, p in mkt_pct.items():
        log(f"  {m}: {p}%")
        
    # Explorer index distribution
    exp_med = subset['loyalist_vs_explorer_index'].median()
    exp_p75 = subset['loyalist_vs_explorer_index'].quantile(0.75)
    log(f"Explorer Index: Median={exp_med:.2f}, 75th pctl={exp_p75:.2f}")
    
    # Activation fit
    act = subset['channel_activation_fit_score'].value_counts(normalize=True).round(3) * 100
    log(f"Activation Fit:")
    for a, p in act.items():
        log(f"  {a}: {p:.1f}%")

# ============================================================
# 4. SCORING ENGINE EVALUATION
# ============================================================
log("\n[4] Composite Scoring Engine (Scenario Test)")
if 'fact_cand' in locals():
    # We apply a basic heuristic weighting based on blueprint components
    # We join brand features once
    cand_scores = fact_cand.merge(
        dim_brand[['brand', 'brand_volatility_index', 'not_just_popularity_penalty', 
                   'market_priority_margin_first', 'market_priority_balanced_growth', 'market_priority_discovery_first']],
        left_on='candidate_brand', right_on='brand', how='left'
    )
    
    # Base heuristic:
    # 2 pts for basket_pair, 1 pt for lookalike, 0.5 for axis_market, 0.5 for cold_start
    cand_scores['route_score'] = (cand_scores['has_basket_pair'] * 2.0 + 
                                  cand_scores['has_lookalike'] * 1.0 + 
                                  cand_scores['has_axis_market'] * 0.5 + 
                                  cand_scores['has_cold_start'] * 0.5)
    
    # Add discovery penalty/bonus and repeat potential (1 - volatility)
    cand_scores['base_score'] = cand_scores['route_score'] + cand_scores['not_just_popularity_penalty'] * 2.0 + (1 - cand_scores['brand_volatility_index'].fillna(1)) * 1.5
    
    # Scenarios = Base + 3 * overlay weight
    cand_scores['score_margin'] = cand_scores['base_score'] + cand_scores['market_priority_margin_first'] * 3.0
    cand_scores['score_balanced'] = cand_scores['base_score'] + cand_scores['market_priority_balanced_growth'] * 3.0
    cand_scores['score_discovery'] = cand_scores['base_score'] + cand_scores['market_priority_discovery_first'] * 3.0
    
    scenarios = ['score_margin', 'score_balanced', 'score_discovery']
    results = []
    
    # For evaluation, we only assess customers who HAD purchases in the target window
    eval_customers = set(cust_target_history.keys())
    eval_cands = cand_scores[cand_scores['anonymized_card_code'].isin(eval_customers)].copy()
    
    # We will compute Hit Rate @ Top 3 recommendations
    log(f"Evaluating scenarios against {len(eval_customers)} active target-window customers...")
    for scn in scenarios:
        # Sort and take top 3 per customer
        eval_cands = eval_cands.sort_values(['anonymized_card_code', scn], ascending=[True, False])
        top3 = eval_cands.groupby('anonymized_card_code').head(3)
        
        hits = 0
        cust_hits = 0
        total_recs = len(top3)
        unique_rec_customers = top3['anonymized_card_code'].nunique()
        
        # Check hits
        for cust, df_cust in top3.groupby('anonymized_card_code'):
            target_set = cust_target_history.get(cust, set())
            cust_hit = False
            for b in df_cust['candidate_brand']:
                if b in target_set:
                    hits += 1
                    cust_hit = True
            if cust_hit:
                cust_hits += 1
                
        rec_hit_rate = (hits / total_recs) * 100 if total_recs > 0 else 0
        cust_hit_rate = (cust_hits / unique_rec_customers) * 100 if unique_rec_customers > 0 else 0
        
        log(f"\nScenario: {scn.replace('score_', '').upper()}")
        log(f"  Recs Made (Top 3): {total_recs} across {unique_rec_customers} customers")
        log(f"  Brand-Level Hit Rate (Precision@3): {rec_hit_rate:.2f}% ({hits} correct recommendations)")
        log(f"  Customer-Level Hit Rate (Adopted $\ge$ 1): {cust_hit_rate:.2f}% ({cust_hits} customers)")
        results.append((scn, cust_hit_rate))

    best_scn = max(results, key=lambda x: x[1])[0]
    log(f"\nEmpirical Winner: {best_scn.replace('score_', '').upper()} (highest customer conversion rate)")

# ============================================================
# DONE
# ============================================================
elapsed = time.time() - t0
log(f"\n[DONE] Execution elapsed: {elapsed:.1f}s")
with open(OUT_REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
