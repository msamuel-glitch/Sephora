"""
Phase 4 Patch — Two blocking fixes:
1. Fix MAEK UP → MAKE UP across all tables and re-derive axis-dependent features
2. Infer age_generation from age where missing, using Sephora's own boundaries
"""
import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict
import os, time

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
AUDIT_BASE = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")
DIM_CUST = os.path.join(BASE, "03_data_working", "dim_customer.csv")
DIM_BRAND = os.path.join(BASE, "03_data_working", "dim_brand.csv")
DIM_PAIR = os.path.join(BASE, "03_data_working", "dim_brand_pair.csv")
LOG_PATH = os.path.join(BASE, "04_analysis", "patch_log.txt")

lines = []
def log(msg):
    print(msg)
    lines.append(str(msg))

t0 = time.time()
log("=" * 60)
log("PHASE 4 PATCH — Blocking Fixes")
log("=" * 60)

# ============================================================
# LOAD
# ============================================================
log("\n[LOAD] Loading all tables...")
df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
dim_customer = pd.read_csv(DIM_CUST)
dim_brand = pd.read_csv(DIM_BRAND)
dim_brand_pair = pd.read_csv(DIM_PAIR)

# ============================================================
# FIX 1: MAEK UP → MAKE UP
# ============================================================
log("\n[FIX 1] Patching MAEK UP → MAKE UP")

# Fix in audit base
maek_count_audit = (df_audit['Axe_Desc'] == 'MAEK UP').sum()
df_audit['Axe_Desc'] = df_audit['Axe_Desc'].replace('MAEK UP', 'MAKE UP')
log(f"  Audit base: {maek_count_audit} rows patched")

# Fix first-purchase axis imprint too
if 'Axe_Desc_first_purchase' in df_audit.columns:
    df_audit['Axe_Desc_first_purchase'] = df_audit['Axe_Desc_first_purchase'].str.replace('MAEK UP', 'MAKE UP', regex=False)

# Fix in dim_brand
maek_brand = (dim_brand['primary_axis'] == 'MAEK UP').sum()
dim_brand['primary_axis'] = dim_brand['primary_axis'].replace('MAEK UP', 'MAKE UP')
log(f"  dim_brand: {maek_brand} brands patched")

# Fix in dim_customer (first_purchase_axis_imprint)
if 'first_purchase_axis_imprint' in dim_customer.columns:
    maek_cust = (dim_customer['first_purchase_axis_imprint'] == 'MAEK UP').sum()
    dim_customer['first_purchase_axis_imprint'] = dim_customer['first_purchase_axis_imprint'].replace('MAEK UP', 'MAKE UP')
    log(f"  dim_customer first_purchase_axis_imprint: {maek_cust} patched")

# Re-derive axis-dependent features from corrected audit base
log("  Re-deriving axis-dependent features...")
df_elig = df_audit[df_audit['eligible_for_affinity_v1'] == True].copy()
df_elig['trans_date'] = pd.to_datetime(df_elig['transactionDate'], errors='coerce')
df_elig['month'] = df_elig['trans_date'].dt.month
df_feat = df_elig[df_elig['month'] <= 9].copy()

# Re-compute: cross_axis_discovery_propensity, axis_concentration, basket_axis_density
cust_axes = df_feat.groupby('anonymized_card_code')['Axe_Desc'].nunique().reset_index()
cust_axes.columns = ['anonymized_card_code', 'total_axes_corrected']
dim_customer = dim_customer.merge(cust_axes, on='anonymized_card_code', how='left')
dim_customer['cross_axis_discovery_propensity'] = dim_customer['total_axes_corrected'].fillna(dim_customer['total_axes']) / 5.0
dim_customer.drop(columns=['total_axes_corrected'], inplace=True, errors='ignore')

# Re-compute axis_concentration
axis_spend = df_feat.groupby(['anonymized_card_code', 'Axe_Desc'])['salesVatEUR'].sum().reset_index()
axis_spend_total = axis_spend.groupby('anonymized_card_code')['salesVatEUR'].transform('sum')
axis_spend['share'] = axis_spend['salesVatEUR'] / axis_spend_total.replace(0, 1)
axis_conc = axis_spend.groupby('anonymized_card_code')['share'].max().reset_index()
axis_conc.columns = ['anonymized_card_code', 'axis_concentration_corrected']
dim_customer = dim_customer.merge(axis_conc, on='anonymized_card_code', how='left')
dim_customer['axis_concentration'] = dim_customer['axis_concentration_corrected'].fillna(dim_customer['axis_concentration'])
dim_customer.drop(columns=['axis_concentration_corrected'], inplace=True, errors='ignore')

# Re-compute basket_axis_density
basket_axis = df_feat.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['Axe_Desc'].nunique().reset_index()
basket_axis_avg = basket_axis.groupby('anonymized_card_code')['Axe_Desc'].mean().reset_index()
basket_axis_avg.columns = ['anonymized_card_code', 'basket_axis_density_corrected']
dim_customer = dim_customer.merge(basket_axis_avg, on='anonymized_card_code', how='left')
dim_customer['basket_axis_density'] = dim_customer['basket_axis_density_corrected'].fillna(dim_customer['basket_axis_density'])
dim_customer.drop(columns=['basket_axis_density_corrected'], inplace=True, errors='ignore')

# Re-compute basket_complementarity_score in dim_brand_pair
log("  Re-computing basket_complementarity_score...")
brand_axes = df_feat.groupby('brand')['Axe_Desc'].apply(lambda x: set(x)).to_dict()
def recompute_complementarity(row):
    axes_a = brand_axes.get(row['brand_a'], set())
    axes_b = brand_axes.get(row['brand_b'], set())
    return len(axes_a | axes_b) / 5.0
dim_brand_pair['basket_complementarity_score'] = dim_brand_pair.apply(recompute_complementarity, axis=1)

log("  FIX 1 COMPLETE.")

# ============================================================
# FIX 2: Infer age_generation from age
# ============================================================
log("\n[FIX 2] Inferring age_generation from age")

# Sephora's own boundaries (extracted from data):
# gena: 15-25, genz: 26-35, geny: 36-45, (gap: 46-60), babyboomers: 61+
# The 46-60 gap = Gen X equivalent, not labeled by Sephora originally

def infer_generation(age):
    if age <= 0:
        return np.nan  # truly unknown
    elif 15 <= age <= 25:
        return 'gena'
    elif 26 <= age <= 35:
        return 'genz'
    elif 36 <= age <= 45:
        return 'geny'
    elif 46 <= age <= 60:
        return 'genx'  # unlabeled gap in original data
    elif age >= 61:
        return 'babyboomers'
    else:  # age 1-14
        return np.nan  # too young, likely data error

# First get age per customer from feature-window data
cust_age = df_feat.groupby('anonymized_card_code')['age'].last().reset_index()
cust_age.columns = ['anonymized_card_code', 'age_val']

# Merge age into dim_customer
dim_customer = dim_customer.merge(cust_age, on='anonymized_card_code', how='left')

# Track original vs inferred
before_null = dim_customer['age_generation'].isnull().sum()
log(f"  Before inference: {before_null} customers with null age_generation")

# Add generation_source column
dim_customer['generation_source'] = 'original'
dim_customer.loc[dim_customer['age_generation'].isnull(), 'generation_source'] = np.nan

# Infer where missing
mask_missing = dim_customer['age_generation'].isnull()
dim_customer.loc[mask_missing, 'age_generation'] = dim_customer.loc[mask_missing, 'age_val'].apply(infer_generation)
dim_customer.loc[mask_missing & dim_customer['age_generation'].notna(), 'generation_source'] = 'inferred_from_age'

# Remaining nulls → UNKNOWN
still_null = dim_customer['age_generation'].isnull().sum()
dim_customer.loc[dim_customer['age_generation'].isnull(), 'age_generation'] = 'UNKNOWN'
dim_customer.loc[dim_customer['generation_source'].isnull(), 'generation_source'] = 'unknown_age'

after_null = (dim_customer['age_generation'] == 'UNKNOWN').sum()
inferred_count = (dim_customer['generation_source'] == 'inferred_from_age').sum()
log(f"  Inferred from age: {inferred_count} customers")
log(f"  Remaining UNKNOWN (age=0): {after_null} customers")
log(f"  Generation distribution after patch:")
log(dim_customer['age_generation'].value_counts().to_string())
log(f"\n  Generation source distribution:")
log(dim_customer['generation_source'].value_counts().to_string())

# Re-compute gen_basket_index and generation_discovery_gap
log("  Re-computing generation-conditioned features...")

# gen_basket_index
dim_customer['avg_basket'] = dim_customer['total_spend'] / dim_customer['total_transactions'].replace(0, 1)
gen_avg = dim_customer[dim_customer['age_generation'] != 'UNKNOWN'].groupby('age_generation')['avg_basket'].mean().to_dict()
dim_customer['gen_avg_basket'] = dim_customer['age_generation'].map(gen_avg)
dim_customer['gen_basket_index'] = dim_customer['avg_basket'] / dim_customer['gen_avg_basket'].replace(0, 1)
# UNKNOWN gets null for gen_basket_index
dim_customer.loc[dim_customer['age_generation'] == 'UNKNOWN', 'gen_basket_index'] = np.nan

# generation_discovery_gap
# Need brands_first_3m (already in dim_customer from Phase 4)
gen_disc_avg = dim_customer[dim_customer['age_generation'] != 'UNKNOWN'].groupby('age_generation')['brands_first_3m'].mean().to_dict()
dim_customer['gen_disc_avg_new'] = dim_customer['age_generation'].map(gen_disc_avg)
dim_customer['generation_discovery_gap'] = dim_customer['brands_first_3m'] - dim_customer['gen_disc_avg_new'].fillna(0)
dim_customer.loc[dim_customer['age_generation'] == 'UNKNOWN', 'generation_discovery_gap'] = np.nan

# Re-compute launch_readiness_score with updated generation weights
gen_weight_map = {
    'gena': 1.0,     # youngest, highest discovery
    'genz': 0.8,     # young adults
    'geny': 0.6,     # millennials
    'genx': 0.4,     # gen X (newly inferred)
    'babyboomers': 0.3,
    'UNKNOWN': 0.3
}
dim_customer['gen_weight'] = dim_customer['age_generation'].map(gen_weight_map).fillna(0.3)
max_explorer = dim_customer['loyalist_vs_explorer_index'].max()
dim_customer['launch_readiness_score'] = (
    0.4 * dim_customer['novelty_receptiveness_score'].fillna(0) +
    0.3 * (dim_customer['loyalist_vs_explorer_index'] / max_explorer if max_explorer > 0 else 0) +
    0.3 * dim_customer['gen_weight']
)

# Clean up temp columns
dim_customer.drop(columns=['age_val', 'gen_avg_basket', 'gen_disc_avg_new', 'gen_weight'], inplace=True, errors='ignore')

log("  FIX 2 COMPLETE.")

# ============================================================
# SAVE
# ============================================================
log("\n[SAVE] Writing corrected tables...")

df_audit.to_csv(AUDIT_BASE, index=False)
log(f"  sephora_audit_labeled_base.csv updated (MAEK UP fix)")

dim_customer.to_csv(DIM_CUST, index=False)
log(f"  dim_customer.csv updated ({len(dim_customer)} rows, {len(dim_customer.columns)} cols)")

dim_brand.to_csv(os.path.join(BASE, "03_data_working", "dim_brand.csv"), index=False)
log(f"  dim_brand.csv updated")

dim_brand_pair.to_csv(os.path.join(BASE, "03_data_working", "dim_brand_pair.csv"), index=False)
log(f"  dim_brand_pair.csv updated")

elapsed = time.time() - t0
log(f"\n[DONE] Patch elapsed: {elapsed:.1f}s")

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
