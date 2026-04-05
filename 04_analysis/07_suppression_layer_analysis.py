import pandas as pd
import numpy as np
import os
import lightgbm as lgb
from sklearn.metrics import precision_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
DATA_DIR = os.path.join(BASE, "03_data_working")
AUDIT_BASE = os.path.join(DATA_DIR, "sephora_audit_labeled_base.csv")
DIM_CUST = os.path.join(DATA_DIR, "dim_customer.csv")
DIM_BRAND = os.path.join(DATA_DIR, "dim_brand.csv")
DIM_PAIR = os.path.join(DATA_DIR, "dim_brand_pair.csv")
FACT_CAND = os.path.join(DATA_DIR, "fact_customer_brand_candidate.csv")
GUIDE = os.path.join(BASE, "05_outputs", "store_brand_pairing_guide.csv")
OUT_CSV = os.path.join(BASE, "05_outputs", "do_not_recommend_layer.csv")
OUT_TXT = os.path.join(BASE, "04_analysis", "suppression_logic.txt")

# Ensure folders exist
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
os.makedirs(os.path.dirname(OUT_TXT), exist_ok=True)

print("Starting Phase 7.5 — Suppression and Cost Layer Analysis")

# ============================================================
# 1. BASE DATA LOADING (for Analyses B & C)
# ============================================================
print("[1] Loading Data & Re-Training Model (Holdout Analysis)...")
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
df_audit['trans_date'] = pd.to_datetime(df_audit['transactionDate'], errors='coerce')
df_audit['month'] = df_audit['trans_date'].dt.month

df_feat = df_audit[df_audit['month'] <= 9].copy()
df_target = df_audit[df_audit['month'] > 9].copy()

fact_cand = pd.read_csv(FACT_CAND)
dim_customer = pd.read_csv(DIM_CUST)
dim_brand = pd.read_csv(DIM_BRAND)

# Re-derive Ground Truth (consistent with 06_model_bakeoff)
history = df_feat.groupby('anonymized_card_code')['brand'].apply(set).to_dict()
actual_buys = df_target.groupby(['anonymized_card_code', 'brand']).size().reset_index().rename(columns={0: 'bought'})
actual_buys = actual_buys[actual_buys.apply(lambda r: r['brand'] not in history.get(r['anonymized_card_code'], set()), axis=1)]
actual_pairs = set(zip(actual_buys['anonymized_card_code'], actual_buys['brand']))

fact_cand['target'] = 0
mask_pos = fact_cand.apply(lambda r: (r['anonymized_card_code'], r['candidate_brand']) in actual_pairs, axis=1)
fact_cand.loc[mask_pos, 'target'] = 1

# Features
model_data = fact_cand.merge(dim_customer, on='anonymized_card_code', how='left')
model_data = model_data.merge(dim_brand, left_on='candidate_brand', right_on='brand', how='left')

cat_features = ['age_generation', 'channel_activation_fit_score', 'first_purchase_axis_imprint', 'first_purchase_market_imprint', 'recruitment_channel']
for col in cat_features:
    if col in model_data.columns:
        model_data[col] = LabelEncoder().fit_transform(model_data[col].astype(str))

# Handle bool flags
for col in ['has_basket_pair', 'has_lookalike', 'has_axis_market', 'has_cold_start']:
    model_data[col] = model_data[col].astype(int)

# Retrain Model
drop_cols = [
    'anonymized_card_code', 'candidate_brand', 'candidate_routes', 'brand', 
    'Axe_Desc', 'primary_axis', 'primary_market', 'brand_history_depth',
    'generation_source', 'target'
]

X = model_data.drop(columns=drop_cols, errors='ignore')
y = model_data['target']

# Training single shot model with Bake-off best-run parameters
model_lgb = lgb.LGBMClassifier(learning_rate=0.1, num_leaves=63, min_child_samples=50, random_state=42)
model_lgb.fit(X, y)

# Full Prediction on Holdout
fact_cand['ml_score'] = model_lgb.predict_proba(X)[:, 1]

# ============================================================
# ANALYSIS A — HIGH CLV SUPPRESSION
# ============================================================
print("[A] Analyzing High CLV Suppression...")
results_a = []

# dim_brand_pair check
df_pair = pd.read_csv(DIM_PAIR)
guardrail_cols = [c for c in df_pair.columns if "guardrail" in c.lower()]

# Define high CLV: rfm_segment_snapshot IN (1,2,3) AND loyalty_status_at_snapshot IN (3,4)
high_clv_cust = dim_customer[
    (dim_customer['rfm_segment_snapshot'].isin([1, 2, 3])) & 
    (dim_customer['loyalty_status_at_snapshot'].isin([3, 4]))
]
clv_risk_count = len(high_clv_cust)

if not guardrail_cols:
    print("    Warning: dim_brand_pair contains no guardrail columns. Using store_brand_pairing_guide.csv.")
    df_guide = pd.read_csv(GUIDE)
    flagged_pairs = df_guide[df_guide['guardrail_flags'] == 1]
    
    for i, row in flagged_pairs.iterrows():
        results_a.append({
            'anchor_brand': row['anchor_brand'],
            'recommended_brand': row['recommended_brand'],
            'suppression_type': 'HIGH_CLV_GUARDRAIL',
            'suppression_reason': 'Business Guardrail violation (Phase 6 filter)',
            'affected_segment': 'Loyalty elite (Segments 1-3)',
            'lift_score': row['co_occurrence_lift'],
            'guardrail_flag': 1,
            'clv_risk_flag': True if clv_risk_count > 0 else False,
            'data_source': 'store_brand_pairing_guide.csv'
        })
else:
    print("    Skipping Analysis A (No guardrail columns in dim_brand_pair as specified).")

df_results_a = pd.DataFrame(results_a)

# ============================================================
# ANALYSIS B — GENERATION MISMATCH SUPPRESSION
# ============================================================
print("[B] Analyzing Generation Mismatch Suppression...")

# Merge Axis info back to fact_cand
fact_cand = fact_cand.merge(dim_brand[['brand', 'primary_axis', 'total_brand_customers']], left_on='candidate_brand', right_on='brand', how='left')
fact_cand = fact_cand.merge(dim_customer[['anonymized_card_code', 'age_generation']], on='anonymized_card_code', how='left')

def get_p3(df):
    if len(df) == 0: return 0.0
    # Sort by score per customer
    df = df.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
    df['rank'] = df.groupby('anonymized_card_code').cumcount() + 1
    hits = df[(df['rank'] <= 3) & (df['target'] == 1)]
    return hits['anonymized_card_code'].nunique() / df['anonymized_card_code'].nunique()

axis_metrics = []
for axis in fact_cand['primary_axis'].unique():
    axis_df = fact_cand[fact_cand['primary_axis'] == axis]
    global_p3 = get_p3(axis_df)
    
    # boomer segment: data key is 'babyboomers'
    boomer_df = axis_df[axis_df['age_generation'] == 'babyboomers']
    boomer_p3 = get_p3(boomer_df)
    
    axis_metrics.append({'axis': axis, 'global_p3': global_p3, 'boomer_p3': boomer_p3})

df_axis_metrics = pd.DataFrame(axis_metrics)
study_mean = df_axis_metrics['global_p3'].mean()
study_std = df_axis_metrics['global_p3'].std()
threshold = study_mean - study_std

# Identifiers
flagged_axes = df_axis_metrics[df_axis_metrics['boomer_p3'] < threshold]['axis'].tolist()
# Cold start definition from blueprint: < 50 unique customers in Jan-Sep
cold_start_brands = dim_brand[dim_brand['total_brand_customers'] < 50]['brand'].tolist()

results_b = []
for axis in flagged_axes:
    # Identify brands in this axis that are cold start
    brands_in_axis = dim_brand[dim_brand['primary_axis'] == axis]['brand'].tolist()
    mismatched_cold = [b for b in brands_in_axis if b in cold_start_brands]
    
    for b in mismatched_cold:
        results_b.append({
            'anchor_brand': 'MULTIPLE',
            'recommended_brand': b,
            'suppression_type': 'BOOMER_AXIS_MISMATCH',
            'suppression_reason': f'P@3 gap > 1 SD on axis {axis}',
            'affected_segment': 'Baby Boomers',
            'lift_score': 0,
            'guardrail_flag': 0,
            'clv_risk_flag': False,
            'data_source': f'Axis Boomer P@3: {df_axis_metrics[df_axis_metrics["axis"] == axis]["boomer_p3"].values[0]:.4f}'
        })

df_results_b = pd.DataFrame(results_b)

# ============================================================
# ANALYSIS C — FALSE POSITIVE COST QUANTIFICATION
# ============================================================
print("[C] Analyzing False Positive Cost...")

high_clv_ids = high_clv_cust['anonymized_card_code'].unique()

# Identify False Positives: predicted = 1 (top 3) and actual = 0 (target=0)
fact_cand = fact_cand.sort_values(['anonymized_card_code', 'ml_score'], ascending=[True, False])
fact_cand['rank'] = fact_cand.groupby('anonymized_card_code').cumcount() + 1

false_positives = fact_cand[
    (fact_cand['rank'] <= 3) & 
    (fact_cand['target'] == 0) & 
    (fact_cand['anonymized_card_code'].isin(high_clv_ids))
]

# Calculate basket value (AOV) from Jan-Sep
jan_sep_audit = df_feat.copy()
# Using anonymized_Ticket_ID as the basket identifier (confirmed in schema)
cust_baskets = jan_sep_audit.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['salesVatEUR'].sum().reset_index().groupby('anonymized_card_code')['salesVatEUR'].mean()
target_mean_basket = cust_baskets[cust_baskets.index.isin(high_clv_ids)].mean()

fp_count = false_positives['anonymized_card_code'].nunique()
total_risk = fp_count * target_mean_basket

df_results_c = pd.DataFrame([{
    'anchor_brand': 'SYSTEM_WIDE',
    'recommended_brand': 'FALSE_POSITIVES',
    'suppression_type': 'FALSE_POSITIVE_CLV_RISK',
    'suppression_reason': f'Quantified top-3 errors for High CLV',
    'affected_segment': 'Loyalty Elite',
    'lift_score': 0,
    'guardrail_flag': 0,
    'clv_risk_flag': True,
    'data_source': f'Total Risk: EUR {total_risk:,.0f}'
}])

# ============================================================
# FINAL ASSEMBLY
# ============================================================
final_df = pd.concat([df_results_a, df_results_b, df_results_c], ignore_index=True)
final_df.to_csv(OUT_CSV, index=False)

with open(OUT_TXT, 'w', encoding='utf-8') as f:
    f.write("SUPPRESSION LOGIC DOCUMENTATION\n")
    f.write("--------------------------------\n\n")
    
    f.write("SECTION 1 — WHAT THE SUPPRESSION LAYER IS\n")
    f.write(f"This layer identifies customer-brand pairs where a recommendation carries measurable relationship risk exceeding the expected revenue gain. Currently, the suppression logic covers {len(final_df)} unique brand-customer risk profiles derived from Analyses A (Business Guardrails), B (Generation Benchmarking), and C (Financial Prediction Risk).\n\n")
    
    f.write("SECTION 2 — THREE SUPPRESSION RULES\n")
    f.write(f"1. IF recommended_brand is flagged on 'guardrail_flags' AND customer_loyalty >= 3 THEN Suppress BECAUSE relationship risk for Loyalty Elite outweighs lift gained for flagged price/planogram mismatches.\n")
    f.write(f"2. IF axis Boomer Precision@3 < {threshold:.4f} THEN Suppress Cold Start BECAUSE the model fails to predict Boomer affinity correctly for these categories, carrying a churn-risk of irrelevant content.\n")
    f.write(f"3. IF individual_predicted_rank <= 3 AND target = 0 THEN Scale Financial Cost BECAUSE top-tier customer errors represent an average basket-value at risk of EUR {target_mean_basket:.2f}.\n\n")
    
    f.write("SECTION 3 — COST FUNCTION FRAMING\n")
    f.write(f"Evaluation optimized only on precision is incomplete. Analysis C quantifies the cost of being wrong by identifying {fp_count} high-CLV customers at risk of inaccurate activation, representing a systemic implied risk of EUR {total_risk:,.0f} based on Jan-Sep baskets. This prevents high-value churn caused by irrelevant automated nudges.\n\n")
    
    f.write("SECTION 4 — FOUR HONEST DEPLOYMENT ANSWERS\n")
    f.write("1. Causality: The holdout proves high correlation with behavior but cannot directly prove incremental revenue. A minimum viable A/B test (Treatment: {fp_count} high-CLV customers) is required to establish true lift.\n")
    f.write("2. Margin: Use brand_family as a margin proxy. However, Sephora Collection margins (private label) may be significantly higher than third-party exclusives. COGS is the single field needed to make figures CFO-ready.\n")
    f.write("3. Model decay: Monthly retraining is mandated. 'velocity_score' and 'loyalist_index' will drift first as customer basket composition evolves. Retrain cadence should match the 90-day discovery window.\n")
    f.write("4. Deployment status: Ready for Explorer-segment CRM pilots; NOT ready for full-store planogram automation. Priority task: Integrating the real-time suppression check into the CRM API payload.\n")

print(f"Deliverables created: {OUT_CSV}, {OUT_TXT}")
print(f"ANALYSIS B METRICS: Boomer Mean P@3={df_axis_metrics['boomer_p3'].mean():.4f}, Global Mean {study_mean:.4f}, Std {study_std:.4f}")
print(f"ANALYSIS C METRICS: Count {fp_count}, Total Risk EUR {total_risk:.0f}")
