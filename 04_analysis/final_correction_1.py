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
# CORRECTION 1: UPDATE GUIDE
# ============================================================
df_guide = pd.read_csv(GUIDE)
# Remove CHAMPO -> DIOR from suppression
mask_champo = (df_guide['anchor_brand'] == "CHAMPO") & (df_guide['recommended_brand'] == "DIOR")
df_guide.loc[mask_champo, 'guardrail_flags'] = 0

# Add strategic_note
df_guide['strategic_note'] = "Standard recommendation, no strategic override."
df_guide.loc[mask_champo, 'strategic_note'] = "High-lift haircare identity signal at 4.96x lift. Store execution guidance recommended. Not a suppression candidate."

df_guide.to_csv(GUIDE, index=False)
print("Step 1: store_brand_pairing_guide.csv updated with strategic_note and CHAMPO override.")

# ============================================================
# RECOMPUTE ANALYSIS C
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
guide_flags = df_guide.groupby('recommended_brand')['guardrail_flags'].max().reset_index()
fact_cand = fact_cand.merge(guide_flags, left_on='candidate_brand', right_on='recommended_brand', how='left')
fact_cand['guardrail_flags'] = fact_cand['guardrail_flags'].fillna(0).astype(int)

# Join High-CLV Info
fact_cand = fact_cand.merge(df_cust[['anonymized_card_code', 'rfm_segment_snapshot', 'loyalty_status_at_snapshot']], on='anonymized_card_code', how='left')

high_clv_pop = df_cust[(df_cust['rfm_segment_snapshot'].isin([1, 2, 3])) & (df_cust['loyalty_status_at_snapshot'].isin([3, 4]))]
total_high_clv = len(high_clv_pop)

# Recompute C Metrics
base_fp = fact_cand[(fact_cand['predicted_rank'] <= 3) & (fact_cand['target'] == 0)]
gr_fp = base_fp[base_fp['guardrail_flags'] == 1]
revised_c = gr_fp[(gr_fp['rfm_segment_snapshot'].isin([1,2,3])) & (gr_fp['loyalty_status_at_snapshot'].isin([3,4]))]

c_cust_count = len(revised_c['anonymized_card_code'].unique())
coverage_rate = (c_cust_count / total_high_clv) * 100

cust_baskets = df_feat.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['salesVatEUR'].sum().reset_index().groupby('anonymized_card_code')['salesVatEUR'].mean()
mean_basket = cust_baskets[cust_baskets.index.isin(set(high_clv_pop['anonymized_card_code']))].mean()
equity = c_cust_count * mean_basket

print(f"UPDATED_C_COUNT: {c_cust_count}")
print(f"UPDATED_EQUITY: {equity:.0f}")
print(f"UPDATED_COVERAGE: {coverage_rate:.2f}%")
print(f"THRESHOLD_60: {'Above' if coverage_rate > 60 else 'Below'}")
