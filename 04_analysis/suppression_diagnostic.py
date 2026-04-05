import pandas as pd
import numpy as np
import os
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
DATA_DIR = os.path.join(BASE, "03_data_working")
AUDIT_BASE = os.path.join(DATA_DIR, "sephora_audit_labeled_base.csv")
DIM_CUST = os.path.join(DATA_DIR, "dim_customer.csv")
DIM_BRAND = os.path.join(DATA_DIR, "dim_brand.csv")
FACT_CAND = os.path.join(DATA_DIR, "fact_customer_brand_candidate.csv")
GUIDE = os.path.join(BASE, "05_outputs", "store_brand_pairing_guide.csv")
DO_NOT_OUT = os.path.join(BASE, "05_outputs", "do_not_recommend_layer.csv")

# 1. LOAD DATA
df_cust = pd.read_csv(DIM_CUST)
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
df_audit['trans_date'] = pd.to_datetime(df_audit['transactionDate'], errors='coerce')
df_audit['month'] = df_audit['trans_date'].dt.month
df_feat = df_audit[df_audit['month'] <= 9].copy()
df_target_window = df_audit[df_audit['month'] > 9].copy()

fact_cand = pd.read_csv(FACT_CAND)
dim_brand = pd.read_csv(DIM_BRAND)

# Model Training (to get scores)
history = df_feat.groupby('anonymized_card_code')['brand'].apply(set).to_dict()
actual_buys = df_target_window.groupby(['anonymized_card_code', 'brand']).size().reset_index().rename(columns={0: 'bought'})
actual_buys = actual_buys[actual_buys.apply(lambda r: r['brand'] not in history.get(r['anonymized_card_code'], set()), axis=1)]
actual_pairs = set(zip(actual_buys['anonymized_card_code'], actual_buys['brand']))

fact_cand['target'] = 0
mask_pos = fact_cand.apply(lambda r: (r['anonymized_card_code'], r['candidate_brand']) in actual_pairs, axis=1)
fact_cand.loc[mask_pos, 'target'] = 1

model_data = fact_cand.merge(df_cust, on='anonymized_card_code', how='left')
model_data = model_data.merge(dim_brand, left_on='candidate_brand', right_on='brand', how='left')

cat_features = ['age_generation', 'channel_activation_fit_score', 'first_purchase_axis_imprint', 'first_purchase_market_imprint', 'recruitment_channel']
for col in cat_features:
    if col in model_data.columns:
        model_data[col] = LabelEncoder().fit_transform(model_data[col].astype(str))

for col in ['has_basket_pair', 'has_lookalike', 'has_axis_market', 'has_cold_start']:
    model_data[col] = model_data[col].astype(int)

drop_cols = [
    'anonymized_card_code', 'candidate_brand', 'candidate_routes', 'brand', 
    'Axe_Desc', 'primary_axis', 'primary_market', 'brand_history_depth',
    'generation_source', 'target'
]
X = model_data.drop(columns=drop_cols, errors='ignore')
y = model_data['target']

model_lgb = lgb.LGBMClassifier(learning_rate=0.1, num_leaves=63, min_child_samples=50, random_state=42)
model_lgb.fit(X, y)

ml_scores = model_lgb.predict_proba(X)[:, 1]
fact_cand['ml_score'] = ml_scores

# DIAGNOSTIC 1: REDEFINE HIGH-CLV
def get_pop_and_rate(def_name, segment_ids, loyalty_ids):
    pop = df_cust[
        (df_cust['rfm_segment_snapshot'].isin(segment_ids)) & 
        (df_cust['loyalty_status_at_snapshot'].isin(loyalty_ids))
    ]
    pop_ids = pop['anonymized_card_code'].unique()
    
    # Coverage for Analysis C (False Positive Top 3)
    # Re-calc rank for this pop
    temp_cand = fact_cand[fact_cand['anonymized_card_code'].isin(pop_ids)].copy()
    temp_cand = temp_cand.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
    temp_cand['rank'] = temp_cand.groupby('anonymized_card_code').cumcount() + 1
    
    fp_custs = temp_cand[(temp_cand['rank'] <= 3) & (temp_cand['target'] == 0)]['anonymized_card_code'].nunique()
    rate = (fp_custs / len(pop_ids)) * 100 if len(pop_ids) > 0 else 0
    return len(pop_ids), rate

print("DIAGNOSTIC 1 — HIGH-CLV REDEFINITION")
a_pop, a_rate = get_pop_and_rate("Definition A", [1,2,3], [3,4])
b_pop, b_rate = get_pop_and_rate("Definition B", [1,2], [4])
c_pop, c_rate = get_pop_and_rate("Definition C", [1,2,3,4], [3,4])

print(f"Definition A (Current): Pop={a_pop}, Coverage={a_rate:.2f}%")
print(f"Definition B (Tightened): Pop={b_pop}, Coverage={b_rate:.2f}%")
print(f"Definition C (Broadened): Pop={c_pop}, Coverage={c_rate:.2f}%")

# DIAGNOSTIC 2: CLARIFIED PROBABILITY SCORE
print("\nDIAGNOSTIC 2 — LIGHTGBM SCORE DISTRIBUTION")
print(f"Output scores are calibrated probabilities (0 to 1): {'predict_proba' in str(type(model_lgb.predict_proba(X)))}")
dist = {
    'Min': np.min(ml_scores),
    '25%': np.percentile(ml_scores, 25),
    '50%': np.percentile(ml_scores, 50),
    '75%': np.percentile(ml_scores, 75),
    '90% (Top 10%)': np.percentile(ml_scores, 90),
    'Max': np.max(ml_scores)
}
for k, v in dist.items():
    print(f"{k}: {v:.6f}")

# DIAGNOSTIC 3: SEPARATE SUPPRESSION TYPES
print("\nDIAGNOSTIC 3 — SEPARATE SUPPRESSION TYPES (of 12,363)")
# Note: 12,363 is specific to Definition A
pop_ids_a = df_cust[
    (df_cust['rfm_segment_snapshot'].isin([1,2,3])) & 
    (df_cust['loyalty_status_at_snapshot'].isin([3,4]))
]['anonymized_card_code'].unique()

temp_cand = fact_cand[fact_cand['anonymized_card_code'].isin(pop_ids_a)].copy()
temp_cand = temp_cand.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
temp_cand['rank'] = temp_cand.groupby('anonymized_card_code').cumcount() + 1

# IDENTIFY REASONS PER CUSTOMER
# Analysis C: False Positive Rank <= 3
fp_ids = set(temp_cand[(temp_cand['rank'] <= 3) & (temp_cand['target'] == 0)]['anonymized_card_code'])

# Analysis A: Guardrail from guide. We need to check if any of their top 3 recs were guardrailed.
df_guide = pd.read_csv(GUIDE)
flagged_brands = set(df_guide[df_guide['guardrail_flags'] == 1]['recommended_brand'])
gr_ids = set(temp_cand[(temp_cand['rank'] <= 3) & (temp_cand['candidate_brand'].isin(flagged_brands))]['anonymized_card_code'])

# Analysis B: Boomer Mismatch.
# Link generation and axis
temp_cand = temp_cand.merge(df_cust[['anonymized_card_code', 'age_generation']], on='anonymized_card_code', how='left')
temp_cand = temp_cand.merge(dim_brand[['brand', 'primary_axis']], left_on='candidate_brand', right_on='brand', how='left')

axis_p3_boomer = {}
boomer_pop = temp_cand[temp_cand['age_generation'] == 'babyboomers']
for axis in temp_cand['primary_axis'].unique():
    axis_df = boomer_pop[boomer_pop['primary_axis'] == axis]
    if len(axis_df) == 0: continue
    # sort by score
    axis_df = axis_df.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
    axis_df['rank_ax'] = axis_df.groupby('anonymized_card_code').cumcount() + 1
    p3 = axis_df[(axis_df['rank_ax'] <= 3) & (axis_df['target'] == 1)]['anonymized_card_code'].nunique() / axis_df['anonymized_card_code'].nunique()
    axis_p3_boomer[axis] = p3

# Study wide boomer P@3 mean/std (mimicking 07_suppression_layer_analysis logic)
p3_vals = list(axis_p3_boomer.values())
mean_p3 = np.mean(p3_vals)
std_p3 = np.std(p3_vals)
thresh = mean_p3 - std_p3
flagged_axes = [k for k, v in axis_p3_boomer.items() if v < thresh]

# Customers suppressed by B: Boomer AND receiving a top-3 rec on a flagged axis
bm_ids = set(temp_cand[
    (temp_cand['age_generation'] == 'babyboomers') & 
    (temp_cand['rank'] <= 3) & 
    (temp_cand['primary_axis'].isin(flagged_axes))
]['anonymized_card_code'])

# Breakdown of the 12,363 (FP IDs)
overlap = {
    'Analysis C Only': len(fp_ids - gr_ids - bm_ids),
    'Analysis A Only': len(gr_ids - fp_ids - bm_ids),
    'Analysis B Only': len(bm_ids - fp_ids - gr_ids),
    'A & C Overlap': len(gr_ids & fp_ids),
    'B & C Overlap': len(bm_ids & fp_ids),
    'A & B Overlap': len(gr_ids & bm_ids),
    'All Three': len(gr_ids & fp_ids & bm_ids)
}

for k, v in overlap.items():
    print(f"{k}: {v}")

print(f"\nTotal Unique Suppressed (Any reason): {len(fp_ids | gr_ids | bm_ids)}")
