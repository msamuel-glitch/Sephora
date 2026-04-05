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

# 1. total_high_clv_population
df_cust = pd.read_csv(DIM_CUST)
high_clv = df_cust[
    (df_cust['rfm_segment_snapshot'].isin([1, 2, 3])) & 
    (df_cust['loyalty_status_at_snapshot'].isin([3, 4]))
]
total_high_clv_population = len(high_clv)

# 2. suppression_coverage_rate
suppression_coverage_rate = (12363 / total_high_clv_population) * 100

# 3. 75th percentile LightGBM probability score
# I need to rerun the model prediction logic to get the distribution of ml_score
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
p75_score = np.percentile(ml_scores, 75)

print(f"TOTAL_HIGH_CLV: {total_high_clv_population}")
print(f"COVERAGE_RATE: {suppression_coverage_rate:.2f}%")
print(f"P75_SCORE: {p75_score:.6f}")
