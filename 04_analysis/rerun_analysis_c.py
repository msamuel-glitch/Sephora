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
LOGIC_OUT = os.path.join(BASE, "04_analysis", "suppression_logic.txt")

# 1. LOAD DATA
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

# Preprocessing
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

# Join Guardrail Flags
df_guide = pd.read_csv(GUIDE)
# Join on recommended_brand
guide_flags = df_guide.groupby('recommended_brand')['guardrail_flags'].max().reset_index()
fact_cand = fact_cand.merge(guide_flags, left_on='candidate_brand', right_on='recommended_brand', how='left')
fact_cand['guardrail_flags'] = fact_cand['guardrail_flags'].fillna(0).astype(int)

# Join High-CLV Info
fact_cand = fact_cand.merge(df_cust[['anonymized_card_code', 'rfm_segment_snapshot', 'loyalty_status_at_snapshot']], on='anonymized_card_code', how='left')

# Rerun Metrics
base_fp = fact_cand[(fact_cand['predicted_rank'] <= 3) & (fact_cand['target'] == 0)]
gr_fp = base_fp[base_fp['guardrail_flags'] == 1]
revised_c = gr_fp[(gr_fp['rfm_segment_snapshot'].isin([1,2,3])) & (gr_fp['loyalty_status_at_snapshot'].isin([3,4]))]
gr_alone = fact_cand[fact_cand['guardrail_flags'] == 1]

print("### STEP 4: RERUN ANALYSIS C")
print(f"Filter 1 (Base FP): {len(base_fp)}")
print(f"Filter 2 (GR FP): {len(gr_fp)}")
print(f"Filter 3 (Revised C): {len(revised_c)}")
print(f"Filter 4 (GR Sense Check): {len(gr_alone)}")

# Business Equity
cust_baskets = df_feat.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['salesVatEUR'].sum().reset_index().groupby('anonymized_card_code')['salesVatEUR'].mean()
mean_basket = cust_baskets[cust_baskets.index.isin(set(df_cust[(df_cust['rfm_segment_snapshot'].isin([1,2,3])) & (df_cust['loyalty_status_at_snapshot'].isin([3,4]))]['anonymized_card_code']))].mean()

c_count = len(revised_c['anonymized_card_code'].unique())
equity = c_count * mean_basket

print(f"\nFinal C Count (Unique Customers): {c_count}")
print(f"Relationship Equity Protected: EUR {equity:,.0f}")
