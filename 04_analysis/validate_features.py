"""Quick validation of Phase 4 output tables — writes to file."""
import pandas as pd
import os

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\03_data_working"
OUT = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\validation_report.txt"

lines = []
def log(msg):
    print(msg)
    lines.append(str(msg))

log("=" * 60)
log("VALIDATION REPORT — Phase 4 Feature Tables")
log("=" * 60)

log("\n--- dim_customer ---")
dc = pd.read_csv(os.path.join(BASE, 'dim_customer.csv'))
log(f"Shape: {dc.shape}")
log(f"Columns: {list(dc.columns)}")
log(f"\nNull counts (non-zero only):")
nulls = dc.isnull().sum()
nulls = nulls[nulls > 0].sort_values(ascending=False)
log(nulls.to_string())

log(f"\nloyalist_vs_explorer_index:\n{dc['loyalist_vs_explorer_index'].describe().to_string()}")
log(f"\ngeneration_discovery_gap:\n{dc['generation_discovery_gap'].describe().to_string()}")
log(f"\nlaunch_readiness_score:\n{dc['launch_readiness_score'].describe().to_string()}")
log(f"\nselective_to_exclusive_tradeup_score:\n{dc['selective_to_exclusive_tradeup_score'].describe().to_string()}")
log(f"\nloyalty_trajectory:\n{dc['loyalty_trajectory'].value_counts().head(10).to_string()}")
log(f"\nchannel_activation_fit_score:\n{dc['channel_activation_fit_score'].value_counts().to_string()}")
log(f"\nhigh_frequency_flag:\n{dc['high_frequency_flag'].value_counts().to_string()}")
log(f"\nage_generation:\n{dc['age_generation'].value_counts().to_string()}")
log(f"\nloyalty_status_at_snapshot:\n{dc['loyalty_status_at_snapshot'].value_counts().to_string()}")
log(f"\nrfm_segment_snapshot:\n{dc['rfm_segment_snapshot'].value_counts().to_string()}")

log("\n" + "=" * 60)
log("--- dim_brand ---")
db = pd.read_csv(os.path.join(BASE, 'dim_brand.csv'))
log(f"Shape: {db.shape}")
log(f"Columns: {list(db.columns)}")
log(f"\nbrand_history_depth:\n{db['brand_history_depth'].value_counts().to_string()}")
log(f"\nnot_just_popularity_penalty:\n{db['not_just_popularity_penalty'].describe().to_string()}")
log(f"\nprimary_axis:\n{db['primary_axis'].value_counts().to_string()}")
log(f"\nprimary_market:\n{db['primary_market'].value_counts().to_string()}")

log("\n" + "=" * 60)
log("--- dim_brand_pair ---")
dbp = pd.read_csv(os.path.join(BASE, 'dim_brand_pair.csv'))
log(f"Shape: {dbp.shape}")
log(f"Columns: {list(dbp.columns)}")
log(f"\nbrand_cooccurrence_lift:\n{dbp['brand_cooccurrence_lift'].describe().to_string()}")
log(f"\nbasket_complementarity_score:\n{dbp['basket_complementarity_score'].describe().to_string()}")
log(f"\nGuardrail flags:")
log(f"  high_price_artifact_flag=1: {dbp['high_price_artifact_flag'].sum()}")
log(f"  trivial_association_flag=1: {dbp['trivial_association_flag'].sum()}")
log(f"\nTop 10 pairs by lift (non-flagged):")
clean = dbp[(dbp['high_price_artifact_flag']==0) & (dbp['trivial_association_flag']==0)]
log(clean.nlargest(10, 'brand_cooccurrence_lift')[['brand_a','brand_b','brand_cooccurrence_lift','basket_complementarity_score']].to_string())

log("\nDONE")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
