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

# Model Training
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

# HIGH CLV POPULATION
high_clv_pop = df_cust[
    (df_cust['rfm_segment_snapshot'].isin([1, 2, 3])) & 
    (df_cust['loyalty_status_at_snapshot'].isin([3, 4]))
]
high_clv_count = len(high_clv_pop)
high_clv_ids = set(high_clv_pop['anonymized_card_code'])

# REVISED ANALYSIS C
df_guide = pd.read_csv(GUIDE)
flagged_brands = set(df_guide[df_guide['guardrail_flags'] == 1]['recommended_brand'])

temp_cand = fact_cand[fact_cand['anonymized_card_code'].isin(high_clv_ids)].copy()
temp_cand = temp_cand.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
temp_cand['rank'] = temp_cand.groupby('anonymized_card_code').cumcount() + 1

# Revised Filter: Rank <= 3 AND Target = 0 AND High CLV AND Guardrail=1
revised_c_custs = temp_cand[
    (temp_cand['rank'] <= 3) & 
    (temp_cand['target'] == 0) & 
    (temp_cand['candidate_brand'].isin(flagged_brands))
]['anonymized_card_code'].nunique()

# Mean Basket Value
cust_baskets = df_feat.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['salesVatEUR'].sum().reset_index().groupby('anonymized_card_code')['salesVatEUR'].mean()
revised_mean_basket = cust_baskets[cust_baskets.index.isin(high_clv_ids)].mean()

revised_equity = revised_c_custs * revised_mean_basket
revised_coverage = (revised_c_custs / high_clv_count) * 100

print(f"REVISED_C_COUNT: {revised_c_custs}")
print(f"REVISED_EQUITY: {revised_equity:.0f}")
print(f"REVISED_COVERAGE: {revised_coverage:.2f}%")
print(f"MEAN_BASKET: {revised_mean_basket:.2f}")
print(f"TOTAL_HIGH_CLV: {high_clv_count}")
