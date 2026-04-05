import pandas as pd
import os

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
BAM = os.path.join(BASE, "05_outputs", "brand_addressable_market.csv")
DIM_BRAND = os.path.join(BASE, "03_data_working", "dim_brand.csv")

df_bam = pd.read_csv(BAM)
df_brand = pd.read_csv(DIM_BRAND)[["brand", "brand_history_depth"]]

merged = df_bam.merge(df_brand, on="brand", how="left")
emerging = merged[merged["brand_history_depth"] == "Emerging"].sort_values("total_customers_with_high_affinity_never_purchased", ascending=False)

print("Top 5 Emerging Brands by Addressable Pool:")
for i, row in emerging.head(5).iterrows():
    val = row["total_customers_with_high_affinity_never_purchased"] * 11.49
    print(f"{row['brand']}: {row['total_customers_with_high_affinity_never_purchased']} customers | Value: EUR {val:,.0f}")
