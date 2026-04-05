import pandas as pd
import os

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
GUIDE = os.path.join(BASE, "05_outputs", "store_brand_pairing_guide.csv")

# Load Guide
df_guide = pd.read_csv(GUIDE)

# Define the 15 Guardrail Pairs (anchor, recommended, reason)
guardrail_pairs = [
    ("CHAMPO", "DIOR", "Luxury Planogram Conflict"),
    ("BY TERRY", "GUERLAIN", "Luxury Planogram Conflict"),
    ("AVEDA", "GUERLAIN", "Luxury Planogram Conflict"),
    ("KIEHLS", "LANCOME", "Price Segment Mismatch"),
    ("KIEHLS", "LAUDER", "Price Segment Mismatch"),
    ("ILIA", "LANCOME", "Price Segment Mismatch"),
    ("HOURGLASS", "LAUDER", "Price Segment Mismatch"),
    ("AVEDA", "CHANEL", "Luxury Planogram Conflict"),
    ("AVEDA", "CLARINS", "Price Segment Mismatch"),
    ("DRUNK ELEPHANT", "LAUDER", "Price Segment Mismatch"),
    ("FRESH SAS", "LANCOME", "Price Segment Mismatch"),
    ("BOBBI BROWN", "CHARLOTTE TILBURY", "Planogram Conflict"),
    ("BOBBI BROWN", "TOO FACED", "Planogram Conflict"),
    ("CLINIQUE", "LAURA MERCIER", "Planogram Conflict"),
    ("CLINIQUE", "ILIA", "Planogram Conflict")
]

log = []
found_count = 0
not_found = []

# Populate guardrail_flags
df_guide['guardrail_flags'] = 0

for anchor, rec, reason in guardrail_pairs:
    mask = (df_guide['anchor_brand'] == anchor) & (df_guide['recommended_brand'] == rec)
    if mask.any():
        df_guide.loc[mask, 'guardrail_flags'] = 1
        found_count += 1
        log.append(f"{anchor} -> {rec} | {reason}")
    else:
        not_found.append(f"{anchor} -> {rec}")

# Save Guide
df_guide.to_csv(GUIDE, index=False)

print("### STEP 1: IDENTIFIED GUARDRAIL PAIRS")
for item in log:
    print(item)

print(f"\nFound in Guide: {found_count}")
if not_found:
    print(f"NOT FOUND in Guide: {not_found}")

print(f"\nStep 2: store_brand_pairing_guide.csv updated with {found_count} flags.")
