"""
Sephora Case 3 — Feature Engineering Script
Phase 4 Implementation (Blueprint Rev 2)

Produces four output tables:
  03_data_working/dim_customer.csv
  03_data_working/dim_brand.csv
  03_data_working/dim_brand_pair.csv
  03_data_working/fact_customer_brand_candidate.csv

Does NOT overwrite sephora_audit_labeled_base.csv.
"""

import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict
import os, time, warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
IN_PATH  = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")
OUT_DIR  = os.path.join(BASE, "03_data_working")
LOG_PATH = os.path.join(BASE, "04_analysis", "feature_engineering_log.txt")

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(msg)

def save_log():
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))

# ============================================================
# 0. LOAD & TIME SPLIT
# ============================================================
log("=" * 60)
log("PHASE 4 — FEATURE ENGINEERING")
log("=" * 60)
t0 = time.time()

log("\n[0] Loading audit-labeled base...")
df = pd.read_csv(IN_PATH, low_memory=False)
log(f"    Loaded {len(df)} rows, {len(df.columns)} columns")

# Filter to eligible rows
df = df[df['eligible_for_affinity_v1'] == True].copy()
log(f"    After eligibility filter: {len(df)} rows")

# Parse dates
df['trans_date'] = pd.to_datetime(df['transactionDate'], errors='coerce')
df['month'] = df['trans_date'].dt.month

# Time split
FEATURE_END_MONTH = 9  # Jan-Sep
df_feat = df[df['month'] <= FEATURE_END_MONTH].copy()
df_target = df[df['month'] > FEATURE_END_MONTH].copy()
log(f"    Feature window (Jan-Sep): {len(df_feat)} rows")
log(f"    Target window  (Oct-Dec): {len(df_target)} rows")

# Unique counts
customers_feat = df_feat['anonymized_card_code'].nunique()
brands_feat = df_feat['brand'].nunique()
log(f"    Feature-window customers: {customers_feat}")
log(f"    Feature-window brands:    {brands_feat}")

# ============================================================
# LAYER 1 — CORE AFFINITY SIGNAL
# ============================================================
log("\n[1] LAYER 1 — Core Affinity Signal")

# --- A. Basket Co-occurrence ---
log("  [1A] Basket co-occurrence...")

# Build basket-brand sets (feature window only)
basket_brands = df_feat.groupby('anonymized_Ticket_ID')['brand'].apply(set).reset_index()
basket_brands.columns = ['ticket', 'brands']
# Filter to baskets with 2+ brands
basket_brands = basket_brands[basket_brands['brands'].apply(len) >= 2]
log(f"       Multi-brand baskets: {len(basket_brands)}")

# Brand pair counts
pair_counts = defaultdict(int)
brand_basket_counts = defaultdict(int)
total_baskets = len(basket_brands)

for _, row in basket_brands.iterrows():
    brands = sorted(row['brands'])
    for b in brands:
        brand_basket_counts[b] += 1
    for i in range(len(brands)):
        for j in range(i + 1, len(brands)):
            pair_counts[(brands[i], brands[j])] += 1

log(f"       Unique brand pairs found: {len(pair_counts)}")

# Compute lift, complementarity, promo pairing
# Get axis lookup for complementarity
brand_axes = df_feat.groupby('brand')['Axe_Desc'].apply(lambda x: set(x)).to_dict()

# Discount info per basket for promo pairing
basket_discount = df_feat.groupby('anonymized_Ticket_ID').apply(
    lambda g: (g['discountEUR'].sum() / g['salesVatEUR'].sum()) if g['salesVatEUR'].sum() > 0 else 0
).to_dict()

# Build brand-pair dataframe
bp_records = []
for (a, b), count in pair_counts.items():
    if count < 3:  # minimum support
        continue
    pa = brand_basket_counts.get(a, 1) / total_baskets
    pb = brand_basket_counts.get(b, 1) / total_baskets
    pab = count / total_baskets
    lift = pab / (pa * pb) if (pa * pb) > 0 else 0

    # Complementarity: distinct axes covered by the pair
    axes_a = brand_axes.get(a, set())
    axes_b = brand_axes.get(b, set())
    complementarity = len(axes_a | axes_b) / 5.0  # max 5 axes

    bp_records.append({
        'brand_a': a,
        'brand_b': b,
        'cooccurrence_count': count,
        'brand_cooccurrence_lift': round(lift, 4),
        'basket_complementarity_score': round(complementarity, 4),
    })

dim_brand_pair = pd.DataFrame(bp_records)
log(f"       Brand pairs with support >= 3: {len(dim_brand_pair)}")

# --- B. Customer Similarity prep ---
log("  [1B] Customer-brand purchase matrix...")

# Customer-brand purchase vectors (binary for cosine later)
cust_brand_matrix = df_feat.groupby(['anonymized_card_code', 'brand'])['quantity'].sum().reset_index()
cust_brand_matrix.columns = ['customer', 'brand', 'qty']
cust_brand_pivot = cust_brand_matrix.pivot_table(index='customer', columns='brand', values='qty', fill_value=0)
# Binarize for cosine
cust_brand_binary = (cust_brand_pivot > 0).astype(int)
log(f"       Matrix shape: {cust_brand_binary.shape}")

# --- C. Customer-level features (Layer 1) ---
log("  [1C] Customer-level Layer 1 features...")

cust_agg = df_feat.groupby('anonymized_card_code').agg(
    total_spend=('salesVatEUR', 'sum'),
    total_qty=('quantity', 'sum'),
    total_transactions=('anonymized_Ticket_ID', 'nunique'),
    total_brands=('brand', 'nunique'),
    total_axes=('Axe_Desc', 'nunique'),
    total_markets=('Market_Desc', 'nunique'),
    total_discount=('discountEUR', 'sum'),
    first_trans=('trans_date', 'min'),
    last_trans=('trans_date', 'max'),
).reset_index()

# Loyalist vs Explorer index (1 - HHI of brand spend share)
brand_spend = df_feat.groupby(['anonymized_card_code', 'brand'])['salesVatEUR'].sum().reset_index()
brand_spend_total = brand_spend.groupby('anonymized_card_code')['salesVatEUR'].transform('sum')
brand_spend['share'] = brand_spend['salesVatEUR'] / brand_spend_total.replace(0, 1)
brand_spend['share_sq'] = brand_spend['share'] ** 2
hhi = brand_spend.groupby('anonymized_card_code')['share_sq'].sum().reset_index()
hhi.columns = ['anonymized_card_code', 'hhi']
cust_agg = cust_agg.merge(hhi, on='anonymized_card_code', how='left')
cust_agg['loyalist_vs_explorer_index'] = 1 - cust_agg['hhi']

# Cross-axis discovery propensity
cust_agg['cross_axis_discovery_propensity'] = cust_agg['total_axes'] / 5.0

# Axis concentration (max axis share of spend)
axis_spend = df_feat.groupby(['anonymized_card_code', 'Axe_Desc'])['salesVatEUR'].sum().reset_index()
axis_spend_total = axis_spend.groupby('anonymized_card_code')['salesVatEUR'].transform('sum')
axis_spend['share'] = axis_spend['salesVatEUR'] / axis_spend_total.replace(0, 1)
axis_conc = axis_spend.groupby('anonymized_card_code')['share'].max().reset_index()
axis_conc.columns = ['anonymized_card_code', 'axis_concentration']
cust_agg = cust_agg.merge(axis_conc, on='anonymized_card_code', how='left')

# Basket axis density (avg distinct axes per basket)
basket_axis = df_feat.groupby(['anonymized_card_code', 'anonymized_Ticket_ID'])['Axe_Desc'].nunique().reset_index()
basket_axis_avg = basket_axis.groupby('anonymized_card_code')['Axe_Desc'].mean().reset_index()
basket_axis_avg.columns = ['anonymized_card_code', 'basket_axis_density']
cust_agg = cust_agg.merge(basket_axis_avg, on='anonymized_card_code', how='left')

# Velocity score (median inter-purchase gap in days)
trans_dates = df_feat.groupby('anonymized_card_code')['trans_date'].apply(lambda x: sorted(x.unique())).reset_index()
def median_gap(dates):
    if len(dates) < 2:
        return np.nan
    gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    return np.median(gaps)
trans_dates['velocity_score'] = trans_dates['trans_date'].apply(median_gap)
cust_agg = cust_agg.merge(trans_dates[['anonymized_card_code', 'velocity_score']], on='anonymized_card_code', how='left')

# Loyalty concentration (top brand spend share)
top_brand_share = brand_spend.loc[brand_spend.groupby('anonymized_card_code')['share'].idxmax()]
top_brand_share = top_brand_share[['anonymized_card_code', 'share']].rename(columns={'share': 'loyalty_concentration'})
cust_agg = cust_agg.merge(top_brand_share, on='anonymized_card_code', how='left')

# Market_Desc loyalty (dominant market share)
mkt_spend = df_feat.groupby(['anonymized_card_code', 'Market_Desc'])['salesVatEUR'].sum().reset_index()
mkt_spend_total = mkt_spend.groupby('anonymized_card_code')['salesVatEUR'].transform('sum')
mkt_spend['share'] = mkt_spend['salesVatEUR'] / mkt_spend_total.replace(0, 1)
mkt_conc = mkt_spend.groupby('anonymized_card_code')['share'].max().reset_index()
mkt_conc.columns = ['anonymized_card_code', 'market_desc_loyalty']
cust_agg = cust_agg.merge(mkt_conc, on='anonymized_card_code', how='left')

# Brand-family switch tolerance (entropy of Market_Desc)
def entropy(shares):
    shares = shares[shares > 0]
    return -np.sum(shares * np.log2(shares))
mkt_entropy = mkt_spend.groupby('anonymized_card_code')['share'].apply(entropy).reset_index()
mkt_entropy.columns = ['anonymized_card_code', 'brand_family_switch_tolerance']
cust_agg = cust_agg.merge(mkt_entropy, on='anonymized_card_code', how='left')

log(f"       Customer features computed: {len(cust_agg)} customers, {len(cust_agg.columns)} columns")

# ============================================================
# LAYER 2 — BUSINESS VALUE OVERLAY
# ============================================================
log("\n[2] LAYER 2 — Business Value Overlay")

# --- E. Generation-Aware ---
log("  [2E] Generation-aware features...")

# Get generation per customer (last known)
gen_lookup = df_feat.dropna(subset=['age_generation']).groupby('anonymized_card_code')['age_generation'].last().reset_index()
cust_agg = cust_agg.merge(gen_lookup, on='anonymized_card_code', how='left')

# gen_basket_index: customer avg basket / generation avg basket
cust_agg['avg_basket'] = cust_agg['total_spend'] / cust_agg['total_transactions'].replace(0, 1)
gen_avg = cust_agg.groupby('age_generation')['avg_basket'].mean().to_dict()
cust_agg['gen_avg_basket'] = cust_agg['age_generation'].map(gen_avg)
cust_agg['gen_basket_index'] = cust_agg['avg_basket'] / cust_agg['gen_avg_basket'].replace(0, 1)

# generation_discovery_gap: distinct brands in first 3 months, conditioned by generation
first_3m = df_feat[df_feat['month'] <= 3]
discovery_3m = first_3m.groupby('anonymized_card_code')['brand'].nunique().reset_index()
discovery_3m.columns = ['anonymized_card_code', 'brands_first_3m']
cust_agg = cust_agg.merge(discovery_3m, on='anonymized_card_code', how='left')
cust_agg['brands_first_3m'] = cust_agg['brands_first_3m'].fillna(0)
gen_disc_avg = cust_agg.groupby('age_generation')['brands_first_3m'].mean().to_dict()
cust_agg['gen_disc_avg'] = cust_agg['age_generation'].map(gen_disc_avg)
cust_agg['generation_discovery_gap'] = cust_agg['brands_first_3m'] - cust_agg['gen_disc_avg'].fillna(0)

# generation_brand_loyalty_index: repeat rate of top brand by generation
# First get per-customer top brand repeat count
brand_repeat = df_feat.groupby(['anonymized_card_code', 'brand'])['anonymized_Ticket_ID'].nunique().reset_index()
brand_repeat.columns = ['anonymized_card_code', 'brand', 'ticket_count']
top_brand_repeat = brand_repeat.loc[brand_repeat.groupby('anonymized_card_code')['ticket_count'].idxmax()]
top_brand_repeat = top_brand_repeat[['anonymized_card_code', 'ticket_count']].rename(columns={'ticket_count': 'top_brand_tickets'})
cust_agg = cust_agg.merge(top_brand_repeat, on='anonymized_card_code', how='left')
cust_agg['generation_brand_loyalty_index'] = cust_agg['top_brand_tickets'] / cust_agg['total_transactions'].replace(0, 1)

# --- Market migration scores ---
log("  [2D] Market migration scores...")

# Split feature window into early (months 1-3) and late (months 7-9)
early = df_feat[df_feat['month'] <= 3]
late = df_feat[(df_feat['month'] >= 7) & (df_feat['month'] <= 9)]

def market_share(sub, mkt_name):
    spend = sub.groupby('anonymized_card_code').apply(
        lambda g: g[g['Market_Desc'] == mkt_name]['salesVatEUR'].sum() / g['salesVatEUR'].sum()
        if g['salesVatEUR'].sum() > 0 else 0
    ).reset_index()
    spend.columns = ['anonymized_card_code', f'{mkt_name}_share']
    return spend

early_excl = market_share(early, 'EXCLUSIVE')
late_excl = market_share(late, 'EXCLUSIVE')
early_seph = market_share(early, 'SEPHORA')
late_seph = market_share(late, 'SEPHORA')

migration = cust_agg[['anonymized_card_code']].copy()
migration = migration.merge(early_excl, on='anonymized_card_code', how='left')
migration = migration.merge(late_excl.rename(columns={'EXCLUSIVE_share': 'EXCLUSIVE_share_late'}), on='anonymized_card_code', how='left')
migration['selective_to_exclusive_tradeup_score'] = migration['EXCLUSIVE_share_late'].fillna(0) - migration['EXCLUSIVE_share'].fillna(0)

migration = migration.merge(early_seph, on='anonymized_card_code', how='left')
migration = migration.merge(late_seph.rename(columns={'SEPHORA_share': 'SEPHORA_share_late'}), on='anonymized_card_code', how='left')
migration['exclusive_to_sephora_migration_score'] = migration['SEPHORA_share_late'].fillna(0) - migration['SEPHORA_share'].fillna(0)

cust_agg = cust_agg.merge(migration[['anonymized_card_code', 'selective_to_exclusive_tradeup_score', 'exclusive_to_sephora_migration_score']], on='anonymized_card_code', how='left')

# --- F. Cold-start ---
log("  [2F] Cold-start features...")

# Brand history depth
brand_purchasers = df_feat.groupby('brand')['anonymized_card_code'].nunique().reset_index()
brand_purchasers.columns = ['brand', 'unique_purchasers']

def classify_brand(n):
    if n >= 50:
        return 'Established'
    elif n >= 1:
        return 'Emerging'
    else:
        return 'Unseen'

brand_purchasers['brand_history_depth'] = brand_purchasers['unique_purchasers'].apply(classify_brand)
log(f"       Established: {(brand_purchasers['brand_history_depth']=='Established').sum()}, Emerging: {(brand_purchasers['brand_history_depth']=='Emerging').sum()}")

# Novelty receptiveness (share of purchases going to brands with <50 purchasers)
emerging_brands = set(brand_purchasers[brand_purchasers['unique_purchasers'] < 50]['brand'])
cust_brand_emerging = df_feat.copy()
cust_brand_emerging['is_emerging'] = cust_brand_emerging['brand'].isin(emerging_brands)
novelty = cust_brand_emerging.groupby('anonymized_card_code').agg(
    emerging_purchases=('is_emerging', 'sum'),
    total_purchases=('is_emerging', 'count')
).reset_index()
novelty['novelty_receptiveness_score'] = novelty['emerging_purchases'] / novelty['total_purchases'].replace(0, 1)
cust_agg = cust_agg.merge(novelty[['anonymized_card_code', 'novelty_receptiveness_score']], on='anonymized_card_code', how='left')

# Launch readiness score (composite)
# Normalize components to 0-1 before combining
cust_agg['norm_novelty'] = cust_agg['novelty_receptiveness_score'].fillna(0)
max_explorer = cust_agg['loyalist_vs_explorer_index'].max()
cust_agg['norm_explorer'] = cust_agg['loyalist_vs_explorer_index'] / max_explorer if max_explorer > 0 else 0
# Generation weight: Gen Z = 1.0, Millennial = 0.7, Gen X = 0.4, others = 0.3
gen_weight_map = {}
for g in cust_agg['age_generation'].dropna().unique():
    gl = str(g).lower()
    if 'z' in gl:
        gen_weight_map[g] = 1.0
    elif 'millennial' in gl or 'y' in gl:
        gen_weight_map[g] = 0.7
    elif 'x' in gl:
        gen_weight_map[g] = 0.4
    else:
        gen_weight_map[g] = 0.3
cust_agg['gen_weight'] = cust_agg['age_generation'].map(gen_weight_map).fillna(0.3)
cust_agg['launch_readiness_score'] = (
    0.4 * cust_agg['norm_novelty'] +
    0.3 * cust_agg['norm_explorer'] +
    0.3 * cust_agg['gen_weight']
)

# --- G. High-frequency flag ---
log("  [2G] High-frequency flag...")
velocity_25 = cust_agg['velocity_score'].quantile(0.25)
cust_agg['high_frequency_flag'] = (cust_agg['velocity_score'] <= velocity_25).astype(int)
log(f"       Velocity 25th pctl: {velocity_25:.1f} days")
log(f"       High-frequency customers: {cust_agg['high_frequency_flag'].sum()}")

# --- H. Sephora-native features ---
log("  [2H] Sephora-native features...")

# Loyalty status at snapshot (last status <= Sep 30)
status_snap = df_feat.groupby('anonymized_card_code')['status'].last().reset_index()
status_snap.columns = ['anonymized_card_code', 'loyalty_status_at_snapshot']
cust_agg = cust_agg.merge(status_snap, on='anonymized_card_code', how='left')

# Loyalty trajectory
early_status = df_feat[df_feat['month'] <= 3].groupby('anonymized_card_code')['status'].max().reset_index()
early_status.columns = ['anonymized_card_code', 'early_status']
late_status = df_feat[(df_feat['month'] >= 7) & (df_feat['month'] <= 9)].groupby('anonymized_card_code')['status'].max().reset_index()
late_status.columns = ['anonymized_card_code', 'late_status']
traj = early_status.merge(late_status, on='anonymized_card_code', how='outer')
traj['loyalty_trajectory'] = traj['late_status'].fillna(0) - traj['early_status'].fillna(0)
cust_agg = cust_agg.merge(traj[['anonymized_card_code', 'loyalty_trajectory']], on='anonymized_card_code', how='left')

# RFM snapshot and trajectory
rfm_snap = df_feat.groupby('anonymized_card_code')['RFM_Segment_ID'].last().reset_index()
rfm_snap.columns = ['anonymized_card_code', 'rfm_segment_snapshot']
cust_agg = cust_agg.merge(rfm_snap, on='anonymized_card_code', how='left')

early_rfm = df_feat[df_feat['month'] <= 3].groupby('anonymized_card_code')['RFM_Segment_ID'].first().reset_index()
early_rfm.columns = ['anonymized_card_code', 'early_rfm']
late_rfm = df_feat[(df_feat['month'] >= 7) & (df_feat['month'] <= 9)].groupby('anonymized_card_code')['RFM_Segment_ID'].last().reset_index()
late_rfm.columns = ['anonymized_card_code', 'late_rfm']
rfm_traj = early_rfm.merge(late_rfm, on='anonymized_card_code', how='outer')
rfm_traj['rfm_trajectory'] = rfm_traj['late_rfm'].fillna(0) - rfm_traj['early_rfm'].fillna(0)
cust_agg = cust_agg.merge(rfm_traj[['anonymized_card_code', 'rfm_trajectory']], on='anonymized_card_code', how='left')

# Omnichannel behavior
omni = df_feat.groupby('anonymized_card_code')['store_type_app'].nunique().reset_index()
omni.columns = ['anonymized_card_code', 'omnichannel_behavior_score']
cust_agg = cust_agg.merge(omni, on='anonymized_card_code', how='left')

# Click-and-collect propensity
# Rule: channel='estore' but store_code_name does not contain 'ESTORE'
df_feat_cc = df_feat.copy()
df_feat_cc['is_cnc'] = (df_feat_cc['channel'].str.lower() == 'estore') & (~df_feat_cc['store_code_name'].str.upper().str.contains('ESTORE', na=False))
cnc = df_feat_cc.groupby('anonymized_card_code').agg(
    cnc_count=('is_cnc', 'sum'),
    total_count=('is_cnc', 'count')
).reset_index()
cnc['click_and_collect_propensity'] = cnc['cnc_count'] / cnc['total_count'].replace(0, 1)
cust_agg = cust_agg.merge(cnc[['anonymized_card_code', 'click_and_collect_propensity']], on='anonymized_card_code', how='left')

# First-purchase imprints (where available)
fp_cols = ['anonymized_card_code', 'Axe_Desc_first_purchase', 'Market_Desc_first_purchase', 'channel_recruitment']
fp_data = df_feat.dropna(subset=['Axe_Desc_first_purchase']).groupby('anonymized_card_code').first()[
    ['Axe_Desc_first_purchase', 'Market_Desc_first_purchase', 'channel_recruitment']
].reset_index()
fp_data.columns = ['anonymized_card_code', 'first_purchase_axis_imprint', 'first_purchase_market_imprint', 'recruitment_channel']
cust_agg = cust_agg.merge(fp_data, on='anonymized_card_code', how='left')

# Spend decile
cust_agg['spend_decile'] = pd.qcut(cust_agg['total_spend'], 10, labels=False, duplicates='drop')

# ============================================================
# LAYER 3 — ACTIVATION & STORYTELLING
# ============================================================
log("\n[3] LAYER 3 — Activation & Storytelling")

# Channel activation proxies
chan_share = df_feat.copy()
chan_share['is_digital'] = chan_share['store_type_app'].isin(['APP', 'ESTORE', 'MOBILE', 'WEB'])
chan_share['is_store'] = chan_share['store_type_app'] == 'STORE'

chan_agg = chan_share.groupby('anonymized_card_code').agg(
    digital_count=('is_digital', 'sum'),
    store_count=('is_store', 'sum'),
    total_count=('is_digital', 'count')
).reset_index()
chan_agg['app_recommendation_affinity_proxy'] = chan_agg['digital_count'] / chan_agg['total_count'].replace(0, 1)
chan_agg['store_guidance_affinity_proxy'] = chan_agg['store_count'] / chan_agg['total_count'].replace(0, 1)
cust_agg = cust_agg.merge(chan_agg[['anonymized_card_code', 'app_recommendation_affinity_proxy', 'store_guidance_affinity_proxy']], on='anonymized_card_code', how='left')

# CRM push eligibility: high frequency AND explorer
vel_median = cust_agg['velocity_score'].median()
cust_agg['crm_push_eligibility_proxy'] = (
    (cust_agg['velocity_score'] <= vel_median) &
    (cust_agg['loyalist_vs_explorer_index'] > 0.3)
).astype(int)

# Channel activation fit
def best_channel(row):
    scores = {
        'CRM_PUSH': row.get('crm_push_eligibility_proxy', 0),
        'APP_SITE': row.get('app_recommendation_affinity_proxy', 0),
        'STORE': row.get('store_guidance_affinity_proxy', 0)
    }
    return max(scores, key=scores.get)
cust_agg['channel_activation_fit_score'] = cust_agg.apply(best_channel, axis=1)

log(f"       Channel fit distribution:\n{cust_agg['channel_activation_fit_score'].value_counts().to_string()}")

# ============================================================
# BUILD dim_brand TABLE
# ============================================================
log("\n[4] Building dim_brand...")

# Brand-level aggregations from feature window
brand_agg = df_feat.groupby('brand').agg(
    total_brand_transactions=('anonymized_Ticket_ID', 'nunique'),
    total_brand_spend=('salesVatEUR', 'sum'),
    total_brand_qty=('quantity', 'sum'),
    total_brand_customers=('anonymized_card_code', 'nunique'),
    median_price=('salesVatEUR', 'median'),
    primary_axis=('Axe_Desc', lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'UNKNOWN'),
    primary_market=('Market_Desc', lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'UNKNOWN'),
).reset_index()

# Not-just-popularity penalty
brand_agg['not_just_popularity_penalty'] = 1 / np.log(brand_agg['total_brand_transactions'] + 2)

# Brand volatility index
brand_repeat_rate = df_feat.groupby('brand')['anonymized_card_code'].apply(
    lambda x: 1 - (x.nunique() / len(x)) if len(x) > 0 else 0
).reset_index()
brand_repeat_rate.columns = ['brand', 'brand_volatility_index']
brand_agg = brand_agg.merge(brand_repeat_rate, on='brand', how='left')

# Brand history depth
brand_agg = brand_agg.merge(brand_purchasers[['brand', 'unique_purchasers', 'brand_history_depth']], on='brand', how='left')

# Gen brand appeal (brand purchase rate within generation vs global)
gen_brand_appeal_records = []
global_brand_rates = df_feat.groupby('brand')['anonymized_card_code'].nunique() / customers_feat
gen_cust_counts = df_feat.dropna(subset=['age_generation']).groupby('age_generation')['anonymized_card_code'].nunique()

for gen in gen_cust_counts.index:
    gen_data = df_feat[df_feat['age_generation'] == gen]
    gen_brand_rates = gen_data.groupby('brand')['anonymized_card_code'].nunique() / gen_cust_counts[gen]
    for brand in gen_brand_rates.index:
        global_rate = global_brand_rates.get(brand, 0.001)
        appeal = gen_brand_rates[brand] / global_rate if global_rate > 0 else 0
        gen_brand_appeal_records.append({'brand': brand, 'generation': gen, 'gen_brand_appeal': round(appeal, 4)})

gen_appeal_df = pd.DataFrame(gen_brand_appeal_records)
# Pivot to wide format for dim_brand
gen_appeal_wide = gen_appeal_df.pivot_table(index='brand', columns='generation', values='gen_brand_appeal', fill_value=1.0)
gen_appeal_wide.columns = [f'gen_brand_appeal_{c}' for c in gen_appeal_wide.columns]
gen_appeal_wide = gen_appeal_wide.reset_index()
brand_agg = brand_agg.merge(gen_appeal_wide, on='brand', how='left')

# Business priority scenarios
def scenario_weight(market, scenario):
    weights = {
        'Margin-First': {'SEPHORA': 1.0, 'EXCLUSIVE': 0.6, 'SELECTIVE': 0.3},
        'Balanced Growth': {'SEPHORA': 0.7, 'EXCLUSIVE': 0.8, 'SELECTIVE': 0.6},
        'Discovery-First': {'SEPHORA': 0.5, 'EXCLUSIVE': 1.0, 'SELECTIVE': 0.5},
    }
    return weights.get(scenario, {}).get(market, 0.3)

for scenario in ['Margin-First', 'Balanced Growth', 'Discovery-First']:
    col = f'market_priority_{scenario.lower().replace("-", "_").replace(" ", "_")}'
    brand_agg[col] = brand_agg['primary_market'].apply(lambda m: scenario_weight(m, scenario))

dim_brand = brand_agg.copy()
log(f"       dim_brand: {len(dim_brand)} brands, {len(dim_brand.columns)} columns")

# ============================================================
# FINALIZE dim_brand_pair (add guardrails)
# ============================================================
log("\n[5] Finalizing dim_brand_pair with guardrails...")

# High price artifact flag
brand_median_price = brand_agg.set_index('brand')['median_price'].to_dict()
p75 = brand_agg['median_price'].quantile(0.75)

def price_artifact(row):
    pa = brand_median_price.get(row['brand_a'], 0)
    pb = brand_median_price.get(row['brand_b'], 0)
    return 1 if (pa > p75 and pb > p75) else 0

dim_brand_pair['high_price_artifact_flag'] = dim_brand_pair.apply(price_artifact, axis=1)

# Trivial association flag (lift < 1.5 AND both in top 20 by volume)
top20_brands = set(brand_agg.nlargest(20, 'total_brand_transactions')['brand'])
dim_brand_pair['trivial_association_flag'] = (
    (dim_brand_pair['brand_cooccurrence_lift'] < 1.5) &
    (dim_brand_pair['brand_a'].isin(top20_brands)) &
    (dim_brand_pair['brand_b'].isin(top20_brands))
).astype(int)

# Quantity-revenue divergence
brand_rank_rev = brand_agg[['brand', 'total_brand_spend']].set_index('brand')['total_brand_spend'].rank(ascending=False).to_dict()
brand_rank_qty = brand_agg[['brand', 'total_brand_qty']].set_index('brand')['total_brand_qty'].rank(ascending=False).to_dict()

dim_brand_pair['quantity_revenue_divergence'] = dim_brand_pair.apply(
    lambda r: abs(brand_rank_rev.get(r['brand_a'], 0) - brand_rank_qty.get(r['brand_a'], 0)) +
              abs(brand_rank_rev.get(r['brand_b'], 0) - brand_rank_qty.get(r['brand_b'], 0)),
    axis=1
)

log(f"       dim_brand_pair final: {len(dim_brand_pair)} pairs, {len(dim_brand_pair.columns)} columns")
log(f"       High price artifact flagged: {dim_brand_pair['high_price_artifact_flag'].sum()}")
log(f"       Trivial association flagged: {dim_brand_pair['trivial_association_flag'].sum()}")

# ============================================================
# FINALIZE dim_customer
# ============================================================
log("\n[6] Finalizing dim_customer...")

# Drop intermediate columns
drop_cols = ['hhi', 'gen_avg_basket', 'gen_disc_avg', 'norm_novelty', 'norm_explorer', 'gen_weight',
             'first_trans', 'last_trans', 'total_discount']
dim_customer = cust_agg.drop(columns=[c for c in drop_cols if c in cust_agg.columns], errors='ignore')
log(f"       dim_customer final: {len(dim_customer)} customers, {len(dim_customer.columns)} columns")

# ============================================================
# SAVE ALL TABLES
# ============================================================
log("\n[7] Saving output tables...")

dim_customer.to_csv(os.path.join(OUT_DIR, 'dim_customer.csv'), index=False)
log(f"       Saved dim_customer.csv")

dim_brand.to_csv(os.path.join(OUT_DIR, 'dim_brand.csv'), index=False)
log(f"       Saved dim_brand.csv")

dim_brand_pair.to_csv(os.path.join(OUT_DIR, 'dim_brand_pair.csv'), index=False)
log(f"       Saved dim_brand_pair.csv")

# fact_customer_brand_candidate will be built in the scoring phase
# as it requires candidate generation to run first
log(f"       fact_customer_brand_candidate deferred to scoring phase (requires candidate generation)")

elapsed = time.time() - t0
log(f"\n[DONE] Total elapsed: {elapsed:.1f}s")

save_log()
log("Log saved.")
