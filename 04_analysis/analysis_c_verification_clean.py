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

# ============================================================
# DATA PREP (Internal Prediction Table Construction)
# ============================================================
df_cust = pd.read_csv(DIM_CUST)
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
df_audit['trans_date'] = pd.to_datetime(df_audit['transactionDate'], errors='coerce')
df_audit['month'] = df_audit['trans_date'].dt.month
df_feat = df_audit[df_audit['month'] <= 9].copy()
df_target_window = df_audit[df_audit['month'] > 9].copy()

fact_cand = pd.read_csv(FACT_CAND)
dim_brand = pd.read_csv(DIM_BRAND)

history = df_feat.groupby('anonymized_card_code')['brand'].apply(set).to_dict()
actual_buys = df_target_window.groupby(['anonymized_card_code', 'brand']).size().reset_index().rename(columns={0: 'bought'})
actual_buys = actual_buys[actual_buys.apply(lambda r: r['brand'] not in history.get(r['anonymized_card_code'], set()), axis=1)]
actual_pairs = set(zip(actual_buys['anonymized_card_code'], actual_buys['brand']))

fact_cand['target'] = 0
mask_pos = fact_cand.apply(lambda r: (r['anonymized_card_code'], r['candidate_brand']) in actual_pairs, axis=1)
fact_cand.loc[mask_pos, 'target'] = 1

model_data = fact_cand.merge(df_cust, on='anonymized_card_code', how='left')
model_data = model_data.merge(dim_brand, left_on='candidate_brand', right_on='brand', how='left')

# Ensure numeric types
numeric_cols = ['brand_history_depth', 'total_brand_customers', 'median_price', 'total_brand_qty', 'total_brand_spend']
for col in numeric_cols:
    if col in model_data.columns:
        model_data[col] = pd.to_numeric(model_data[col], errors='coerce').fillna(0)

cat_features = ['age_generation', 'channel_activation_fit_score', 'first_purchase_axis_imprint', 'first_purchase_market_imprint', 'recruitment_channel']
for col in cat_features:
    if col in model_data.columns:
        model_data[col] = LabelEncoder().fit_transform(model_data[col].astype(str))

for col in ['has_basket_pair', 'has_lookalike', 'has_axis_market', 'has_cold_start']:
    model_data[col] = model_data[col].astype(int)

X = model_data.drop(columns=['anonymized_card_code', 'candidate_brand', 'candidate_routes', 'brand', 'Axe_Desc', 'primary_axis', 'primary_market', 'generation_source', 'target'], errors='ignore')
y = model_data['target']

model_lgb = lgb.LGBMClassifier(learning_rate=0.1, num_leaves=63, min_child_samples=50, random_state=42)
model_lgb.fit(X, y)

fact_cand['ml_score'] = model_lgb.predict_proba(X)[:, 1]
fact_cand = fact_cand.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
fact_cand['predicted_rank'] = fact_cand.groupby('anonymized_card_code').cumcount() + 1

# ============================================================
# CHECK 0 — PREDICTION TABLE STRUCTURE
# ============================================================
print("### CHECK 0: PREDICTION TABLE STRUCTURE")
print("| Metric | Value |")
print("| :--- | :--- |")
print(f"| Total rows | {len(fact_cand)} |")
print(f"| Columns | {', '.join(fact_cand.columns)} |")
rank_counts = fact_cand['predicted_rank'].value_counts()
print(f"| Rank 1 count | {rank_counts.get(1, 0)} |")
print(f"| Rank 2 count | {rank_counts.get(2, 0)} |")
print(f"| Rank 3 count | {rank_counts.get(3, 0)} |")
print(f"| target = 1 count | {len(fact_cand[fact_cand['target'] == 1])} |")
print(f"| target = 0 count | {len(fact_cand[fact_cand['target'] == 0])} |")
print(f"| target = 0 AND rank <= 3 | {len(fact_cand[(fact_cand['target'] == 0) & (fact_cand['predicted_rank'] <= 3)])} |")

# ============================================================
# CHECK 1 & 2 — JOIN & GUARDRAIL
# ============================================================
df_guide = pd.read_csv(GUIDE)
guide_status = df_guide.groupby('recommended_brand')['guardrail_flags'].max().reset_index()
joined = fact_cand.merge(guide_status, left_on='candidate_brand', right_on='recommended_brand', how='left')
joined['guardrail_flags'] = joined['guardrail_flags'].fillna(0).astype(int)
joined = joined.merge(df_cust[['anonymized_card_code', 'rfm_segment_snapshot', 'loyalty_status_at_snapshot']], on='anonymized_card_code', how='left')

print("\n### CHECK 1: JOIN LOGIC")
print(f"**Column**: 'guardrail_flags' from '{os.path.basename(GUIDE)}'")
print(f"**Key**: candidate_brand -> recommended_brand")
print("\n| customer | brand | rank | target | guardrail_flag | segment | loyalty |")
print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
cols = ['anonymized_card_code', 'candidate_brand', 'predicted_rank', 'target', 'guardrail_flags', 'rfm_segment_snapshot', 'loyalty_status_at_snapshot']
for i, row in joined[cols].head(5).iterrows():
    print(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |")

print("\n### CHECK 2: GUARDRAIL FLAGS IN SCORING OUTPUT")
print("| Metric | Value |")
print("| :--- | :--- |")
print(f"| Rows in GUIDE with GR=1 | {len(df_guide[df_guide['guardrail_flags'] == 1])} |")
print(f"| guardrail_flags in schema? | {'guardrail_flags' in joined.columns} |")
print(f"| Rows in joined with GR=1 | {len(joined[joined['guardrail_flags'] == 1])} |")

# ============================================================
# CHECK 3 — ISOLATE ZERO
# ============================================================
base_fp_count = len(joined[(joined['predicted_rank'] <= 3) & (joined['target'] == 0)])
gr_fp_count = len(joined[(joined['predicted_rank'] <= 3) & (joined['target'] == 0) & (joined['guardrail_flags'] == 1)])
high_clv_c_count = len(joined[(joined['predicted_rank'] <= 3) & (joined['target'] == 0) & (joined['guardrail_flags'] == 1) & (joined['rfm_segment_snapshot'].isin([1,2,3])) & (joined['loyalty_status_at_snapshot'].isin([3,4]))])
gr_alone = len(joined[joined['guardrail_flags'] == 1])

print("\n### CHECK 3: ISOLATE WHERE THE COUNT DROPS TO ZERO")
print("| Filter | Row Count |")
print("| :--- | :--- |")
print(f"| Filter 1 — Base FP (Rank <=3, target=0) | {base_fp_count} |")
print(f"| Filter 2 — Guardrail (Rank <=3, target=0, GR=1) | {gr_fp_count} |")
print(f"| Filter 3 — High-CLV (Rank <=3, target=0, GR=1, Elite) | {high_clv_c_count} |")
print(f"| Filter 4 — Sense check (GR=1 alone) | {gr_alone} |")

zero_point = "None"
if base_fp_count == 0: zero_point = "Filter 1"
elif gr_fp_count == 0: zero_point = "Filter 2"
elif high_clv_c_count == 0: zero_point = "Filter 3"
print(f"\n**First zero encountered at**: {zero_point}")
