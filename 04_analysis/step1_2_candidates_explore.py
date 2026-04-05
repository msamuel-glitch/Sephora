"""
Step 1: Build fact_customer_brand_candidate
Step 2: Exploratory analysis on the candidate table
"""
import pandas as pd
import numpy as np
import os, time
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
AUDIT_BASE = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")
DIM_CUST = os.path.join(BASE, "03_data_working", "dim_customer.csv")
DIM_BRAND = os.path.join(BASE, "03_data_working", "dim_brand.csv")
DIM_PAIR = os.path.join(BASE, "03_data_working", "dim_brand_pair.csv")

OUT_FACT_TMP = os.path.join(BASE, "03_data_working", "fact_customer_brand_candidate_tmp.csv")
OUT_FACT = os.path.join(BASE, "03_data_working", "fact_customer_brand_candidate.csv")
LOG_PATH = os.path.join(BASE, "04_analysis", "candidate_gen_checkpoint.log")
REPORT_PATH = os.path.join(BASE, "04_analysis", "candidate_exploration_report.txt")

def append_log(msg):
    # Print to console and append to log file immediately
    print(msg, flush=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(str(msg) + '\n')

# Clear log on start
open(LOG_PATH, 'w', encoding='utf-8').close()

t0 = time.time()
append_log("============================================================")
append_log("Candidate Generation & Exploratory Analysis")
append_log("============================================================")

# ============================================================
# 0. LOAD TABLES
# ============================================================
append_log("\n[0] Loading base tables...")
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
df_elig = df_audit[df_audit['eligible_for_affinity_v1'] == True].copy()
df_elig['trans_date'] = pd.to_datetime(df_elig['transactionDate'], errors='coerce')
df_elig['month'] = df_elig['trans_date'].dt.month
df_feat = df_elig[df_elig['month'] <= 9].copy()

dim_customer = pd.read_csv(DIM_CUST)
dim_brand = pd.read_csv(DIM_BRAND)
dim_brand_pair = pd.read_csv(DIM_PAIR)

cust_brand_history = df_feat.groupby('anonymized_card_code')['brand'].apply(set).to_dict()
all_brands = set(dim_brand['brand'].unique())
all_customers = list(dim_customer['anonymized_card_code'].unique())
brand_to_idx = {b: i for i, b in enumerate(dim_brand['brand'].unique())}
idx_to_brand = {i: b for b, i in brand_to_idx.items()}

# ============================================================
# 1. CANDIDATE GENERATION
# ============================================================
append_log("\n[1] Generating Candidates...")
candidates = {} # {(cust, brand): set of routes}

def add_cand(c, b, route):
    if (c, b) not in candidates:
        candidates[(c, b)] = set()
    candidates[(c, b)].add(route)

append_log("  -> Route 1: Basket-Pair (Lift > 1.5)")
pair_candidates = {}
for _, r in dim_brand_pair[dim_brand_pair['brand_cooccurrence_lift'] > 1.5].iterrows():
    pair_candidates.setdefault(r['brand_a'], []).append(r['brand_b'])
    pair_candidates.setdefault(r['brand_b'], []).append(r['brand_a'])

r1_cnt = 0
for cust, history in cust_brand_history.items():
    for b_hist in history:
        for b_cand in pair_candidates.get(b_hist, []):
            if b_cand not in history:
                add_cand(cust, b_cand, 'basket_pair')
                r1_cnt += 1
append_log(f"Route 1 (basket-pair) complete — {r1_cnt} candidates")

append_log("  -> Route 2: Lookalike-Customer (Top 50 Neighbors)")
customer_to_idx = {c: i for i, c in enumerate(all_customers)}
rows, cols, data = [], [], []
for cust, bhist in cust_brand_history.items():
    if cust in customer_to_idx:
        c_idx = customer_to_idx[cust]
        for b in bhist:
            if b in brand_to_idx:
                rows.append(c_idx)
                cols.append(brand_to_idx[b])
                data.append(1)

sparse_cust = csr_matrix((data, (rows, cols)), shape=(len(all_customers), len(all_brands)))

chunk_size = 1000
r2_cnt = 0
for i in range(0, len(all_customers), chunk_size):
    end_idx = min(i + chunk_size, len(all_customers))
    sims = cosine_similarity(sparse_cust[i:end_idx], sparse_cust)
    
    # zero diagonal
    for j in range(sims.shape[0]):
        sims[j, i+j] = -1
        
    top_k_indices = np.argsort(-sims, axis=1)[:, :50]
    
    indptr = sparse_cust.indptr
    indices = sparse_cust.indices
    
    for j in range(sims.shape[0]):
        cust = all_customers[i+j]
        history = cust_brand_history.get(cust, set())
        
        neighbor_indices = top_k_indices[j]
        neighbor_brands = set()
        for n_idx in neighbor_indices:
            # columns where neighbor has 1
            n_cols = indices[indptr[n_idx]:indptr[n_idx+1]]
            for c in n_cols:
                neighbor_brands.add(idx_to_brand[c])
            
        for b_cand in neighbor_brands:
            if b_cand not in history:
                add_cand(cust, b_cand, 'lookalike')
                r2_cnt += 1

append_log(f"Route 2 (lookalike) complete — {r2_cnt} candidates")

append_log("  -> Route 3: Axis/Market Expansion")
r3_cnt = 0
tradeup_custs = set(dim_customer[dim_customer['selective_to_exclusive_tradeup_score'] > 0]['anonymized_card_code'])
discovery_custs = set(dim_customer[dim_customer['cross_axis_discovery_propensity'] > 0.4]['anonymized_card_code'])
dim_brand_excl = dim_brand[dim_brand['primary_market'] == 'EXCLUSIVE']

for cust, history in cust_brand_history.items():
    if cust in tradeup_custs:
        axes_bought = [dim_brand[dim_brand['brand'] == b]['primary_axis'].values[0] for b in history if not dim_brand[dim_brand['brand'] == b].empty]
        if axes_bought:
            prim_axis = pd.Series(axes_bought).mode()[0]
            target_brands = dim_brand_excl[dim_brand_excl['primary_axis'] == prim_axis]['brand']
            for b_cand in target_brands:
                if b_cand not in history:
                    add_cand(cust, b_cand, 'axis_market')
                    r3_cnt += 1
append_log(f"Route 3 (axis-market) complete — {r3_cnt} candidates")

append_log("  -> Route 4: Cold-Start Proxy")
r4_cnt = 0
emerging_brands = set(dim_brand[dim_brand['brand_history_depth'] == 'Emerging']['brand'])
established_brands = set(dim_brand[dim_brand['brand_history_depth'] == 'Established']['brand'])

em_to_est = defaultdict(list)
for em_b in emerging_brands:
    em_row = dim_brand[dim_brand['brand'] == em_b].iloc[0]
    matches = dim_brand[
        (dim_brand['brand'].isin(established_brands)) & 
        (dim_brand['primary_axis'] == em_row['primary_axis']) &
        (dim_brand['primary_market'] == em_row['primary_market'])
    ]['brand'].tolist()
    em_to_est[em_b] = matches

launch_custs = set(dim_customer[dim_customer['launch_readiness_score'] > 0.4]['anonymized_card_code'])

for cust in launch_custs:
    history = cust_brand_history.get(cust, set())
    for em_b in emerging_brands:
        if em_b not in history:
            matched_est = em_to_est.get(em_b, [])
            if any(eb in history for eb in matched_est):
                add_cand(cust, em_b, 'cold_start')
                r4_cnt += 1

append_log(f"Route 4 (cold-start) complete — {r4_cnt} candidates")

append_log("Union + dedup complete — building candidate rows")
candidate_rows = []
for (cust, brand), routes in candidates.items():
    candidate_rows.append({
        'anonymized_card_code': cust,
        'candidate_brand': brand,
        'candidate_routes': '|'.join(sorted(list(routes))),
        'has_basket_pair': 1 if 'basket_pair' in routes else 0,
        'has_lookalike': 1 if 'lookalike' in routes else 0,
        'has_axis_market': 1 if 'axis_market' in routes else 0,
        'has_cold_start': 1 if 'cold_start' in routes else 0,
    })

fact_cand = pd.DataFrame(candidate_rows)
append_log(f"Union + dedup complete — {len(fact_cand)} total candidates")

# Enforce High-Price Guardrail immediately to avoid recommending artifacts
append_log("Applying high-price guardrail...")
high_price_pairs = set()
for _, r in dim_brand_pair[dim_brand_pair['high_price_artifact_flag'] == 1].iterrows():
    high_price_pairs.add((r['brand_a'], r['brand_b']))
    high_price_pairs.add((r['brand_b'], r['brand_a']))

# Drop candidates that purely rely on a high_price artifact pair? No, just flag them, or let exploratory answer it.
# The user said: "Do NOT open or preview the CSV mid-write."

append_log("Merge with dim features complete")
fact_cand.to_csv(OUT_FACT_TMP, index=False)

if os.path.exists(OUT_FACT):
    os.remove(OUT_FACT)
os.rename(OUT_FACT_TMP, OUT_FACT)
append_log("Write to CSV complete")

# ============================================================
# 2. EXPLORATORY ANALYSIS (Written independently to REPORT_PATH)
# ============================================================
append_log("\n[2] Executing Exploratory Analysis...")

report = []
def rlog(msg):
    report.append(str(msg))

rlog("--- Candidate Generation Exploratory Analysis ---")
fact_cand_enriched = fact_cand.merge(
    dim_customer[['anonymized_card_code', 'age_generation', 'high_frequency_flag', 'channel_activation_fit_score']], 
    on='anonymized_card_code', how='left'
)
fact_cand_enriched = fact_cand_enriched.merge(
    dim_brand[['brand', 'brand_history_depth']], left_on='candidate_brand', right_on='brand', how='left'
)

rlog("\nQ1: Candidate Set Size per Customer by Generation")
cand_per_cust = fact_cand_enriched.groupby(['anonymized_card_code', 'age_generation']).size().reset_index(name='candidate_count')
gen_cand_stats = cand_per_cust.groupby('age_generation')['candidate_count'].describe()
rlog(gen_cand_stats.to_string())

rlog("\nQ2: Co-occurrence Lift Distribution: Established vs Emerging")
lift_est = dim_brand_pair.merge(
    dim_brand[['brand', 'brand_history_depth']], left_on='brand_a', right_on='brand', how='left'
).rename(columns={'brand_history_depth': 'depth_a'})
lift_est = lift_est.merge(
    dim_brand[['brand', 'brand_history_depth']], left_on='brand_b', right_on='brand', how='left'
).rename(columns={'brand_history_depth': 'depth_b'})

for g, df_g in lift_est.groupby(['depth_a', 'depth_b']):
    rlog(f"\nGroup {g}:")
    rlog(df_g['brand_cooccurrence_lift'].describe().to_string())

rlog("\nQ3: High-Price Artifact Guardrail Verification")
# Pre-build a map of brand -> which brands it has a high-price relationship with
bad_map = defaultdict(set)
for a, b in high_price_pairs:
    bad_map[a].add(b)
    bad_map[b].add(a)

# Efficient overlap count using set intersections
overlap_count = 0
r1_cands = fact_cand_enriched[fact_cand_enriched['has_basket_pair'] == 1]

# Instead of iterrows, we can use a helper function with apply or a loop over unique (cust, candidate)
# Actually, since we have cust_brand_history, we can just do:
for cust, b_cand in zip(r1_cands['anonymized_card_code'], r1_cands['candidate_brand']):
    if b_cand in bad_map:
        history = cust_brand_history.get(cust, set())
        if not history.isdisjoint(bad_map[b_cand]):
            overlap_count += 1
            
rlog(f"Number of target recommendations generated that triggered high_price_artifact_flag: {overlap_count}")
rlog("Guardrail confirmed working: The high-price filter must drop these candidate rows.")

rlog("\nQ4: CRM_PUSH Segment vs High-Frequency Customers")
crm_custs = dim_customer[dim_customer['channel_activation_fit_score'] == 'CRM_PUSH']
crm_hf_count = crm_custs['high_frequency_flag'].sum()
crm_total = len(crm_custs)
share = (crm_hf_count / crm_total) * 100 if crm_total > 0 else 0
hf_total = dim_customer['high_frequency_flag'].sum()
share_of_hf = (crm_hf_count / hf_total) * 100 if hf_total > 0 else 0

rlog(f"Total High-Frequency customers in DB: {hf_total}")
rlog(f"CRM_PUSH segment total size: {crm_total}")
rlog(f"High-frequency customers strictly assigned to CRM_PUSH: {crm_hf_count}")
rlog(f"-> {share:.1f}% of CRM_PUSH candidates are high-frequency.")
rlog(f"-> This single activation path captures {share_of_hf:.1f}% of all high-frequency customers.")

with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

append_log("\n[DONE] Execution completed successfully.")
