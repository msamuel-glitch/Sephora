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

# Rank candidates
fact_cand = fact_cand.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
fact_cand['predicted_rank'] = fact_cand.groupby('anonymized_card_code').cumcount() + 1

# ============================================================
# CHECK 0 — PREDICTION TABLE STRUCTURE
# ============================================================
print("CHECK 0 — PREDICTION TABLE STRUCTURE")
print("-" * 40)
print(f"Total row count: {len(fact_cand)}")
print(f"Columns: {list(fact_cand.columns)}")
rank_counts = fact_cand['predicted_rank'].value_counts()
print(f"Rank 1 count: {rank_counts.get(1, 0)}")
print(f"Rank 2 count: {rank_counts.get(2, 0)}")
print(f"Rank 3 count: {rank_counts.get(3, 0)}")
print(f"target = 1 count: {len(fact_cand[fact_cand['target'] == 1])}")
print(f"target = 0 count: {len(fact_cand[fact_cand['target'] == 0])}")
print(f"target = 0 AND predicted_rank <= 3 count: {len(fact_cand[(fact_cand['target'] == 0) & (fact_cand['predicted_rank'] <= 3)])}")
print("\n")

# ============================================================
# CHECK 1 — JOIN LOGIC
# ============================================================
print("CHECK 1 — JOIN LOGIC")
print("-" * 40)
print(f"Exact column name used for guardrail match: 'guardrail_flags'")
print(f"Source table: {os.path.basename(GUIDE)}")
print(f"Join key: candidate_brand (predictions) -> recommended_brand (guide)")

# Joined table before filtering
df_guide = pd.read_csv(GUIDE)
# Dedup guide to avoid fan-out if multiple anchors per recommended
guide_status = df_guide.groupby('recommended_brand')['guardrail_flags'].max().reset_index()

joined_table = fact_cand.merge(guide_status, left_on='candidate_brand', right_on='recommended_brand', how='left')
joined_table['guardrail_flags'] = joined_table['guardrail_flags'].fillna(0).astype(int)

# Merging metadata for high-CLV check in step 3
joined_table = joined_table.merge(df_cust[['anonymized_card_code', 'rfm_segment_snapshot', 'loyalty_status_at_snapshot']], on='anonymized_card_code', how='left')

print("First 5 rows of joined table:")
print(joined_table[['anonymized_card_code', 'candidate_brand', 'predicted_rank', 'target', 'guardrail_flags', 'rfm_segment_snapshot', 'loyalty_status_at_snapshot']].head(5).to_string(index=False))
print("\n")

# ============================================================
# CHECK 2 — GUARDRAIL FLAGS IN SCORING OUTPUT
# ============================================================
print("CHECK 2 — GUARDRAIL FLAGS IN SCORING OUTPUT")
print("-" * 40)
guide_raw = pd.read_csv(GUIDE)
active_cols = [c for c in guide_raw.columns if guide_raw[c].dtype in [np.int64, np.float64, bool] and (guide_raw[c] == 1).any()]
print(f"Active guardrail columns in {os.path.basename(GUIDE)}: {active_cols}")
print(f"Total rows with guardrail column = 1 in GUIDE: {len(guide_raw[guide_raw['guardrail_flags'] == 1])}")

schema_match = 'guardrail_flags' in joined_table.columns
print(f"guardrail_flags appear in joined scoring table? {schema_match}")

count_gr_in_scoring = len(joined_table[joined_table['guardrail_flags'] == 1])
print(f"Count of rows with guardrail_flags = 1 in joined scoring table: {count_gr_in_scoring}")
print("\n")

# ============================================================
# CHECK 3 — ISOLATE WHERE THE COUNT DROPS TO ZERO
# ============================================================
print("CHECK 3 — ISOLATE WHERE THE COUNT DROPS TO ZERO")
print("-" * 40)

base_fp = joined_table[(joined_table['predicted_rank'] <= 3) & (joined_table['target'] == 0)]
base_fp_count = len(base_fp)

guardrail_fp = base_fp[base_fp['guardrail_flags'] == 1]
guardrail_fp_count = len(guardrail_fp)

revised_analysis_c = guardrail_fp[
    (guardrail_fp['rfm_segment_snapshot'].isin([1, 2, 3])) & 
    (guardrail_fp['loyalty_status_at_snapshot'].isin([3, 4]))
]
revised_analysis_c_count = len(revised_analysis_c)

filter_4 = joined_table[joined_table['guardrail_flags'] == 1]
f4_count = len(filter_4)

print(f"Filter 1 — Base FP (Rank <=3, target=0): {base_fp_count}")
print(f"Filter 2 — Guardrail (Rank <=3, target=0, GR=1): {guardrail_fp_count}")
print(f"Filter 3 — High-CLV (Rank <=3, target=0, GR=1, Seg 1-3, Loy 3-4): {revised_analysis_c_count}")
print(f"Filter 4 — Sense check (GR=1 alone): {f4_count}")

# Explicit zero step
steps = [
    ("Filter 1", base_fp_count),
    ("Filter 2", guardrail_fp_count),
    ("Filter 3", revised_analysis_c_count)
]
zero_step = "None"
for name, val in steps:
    if val == 0:
        zero_step = name
        break
print(f"First zero encountered at: {zero_step}")
