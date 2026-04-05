import pandas as pd
import numpy as np
import os

in_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\02_data_raw\BDD#7_Database_Albert_School_Sephora.csv"
out_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\03_data_working\sephora_audit_labeled_base.csv"
report_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\cleaning_report.txt"

def load_and_clean():
    f_log = open(report_path, 'w', encoding='utf-8')
    def log(msg):
        print(msg)
        f_log.write(str(msg) + '\n')

    log("Loading raw dataset...")
    df = pd.read_csv(in_path, low_memory=False)
    initial_rows = len(df)
    
    # 1. Exact Row Duplicates
    df = df.drop_duplicates()
    exact_dropped = initial_rows - len(df)
    log(f"Exact row duplicates permanently dropped: {exact_dropped}")
    
    # 2. ID Columns
    df['anonymized_card_code'] = df['anonymized_card_code'].astype(str)
    df['anonymized_Ticket_ID'] = df['anonymized_Ticket_ID'].astype(str)
    log("ID columns cast to string.")
    
    # 3. Negative / Zero Flags
    df['flag_negative_sales'] = df['salesVatEUR'] < 0
    df['flag_zero_sales'] = df['salesVatEUR'] == 0
    df['flag_negative_quantity'] = df['quantity'] < 0
    df['flag_zero_quantity'] = df['quantity'] == 0
    df['flag_discount_gt_sales'] = df['discountEUR'] > df['salesVatEUR']
    
    log("\n--- ANOMALY FLAG COUNTS ---")
    log(f"flag_negative_sales: {df['flag_negative_sales'].sum()}")
    log(f"flag_zero_sales: {df['flag_zero_sales'].sum()}")
    log(f"flag_negative_quantity: {df['flag_negative_quantity'].sum()}")
    log(f"flag_zero_quantity: {df['flag_zero_quantity'].sum()}")
    log(f"flag_discount_gt_sales: {df['flag_discount_gt_sales'].sum()}")

    # 4. Missing brand / Market_Desc Recovery
    missing_brand_initial = df['brand'].isnull().sum()
    missing_market_initial = df['Market_Desc'].isnull().sum()
    log(f"\nInitial Missing brand: {missing_brand_initial}")
    log(f"Initial Missing Market_Desc: {missing_market_initial}")
    
    # Create lookup from materialCode where values are not null
    brand_lookup = df.dropna(subset=['brand']).groupby('materialCode')['brand'].first().to_dict()
    market_lookup = df.dropna(subset=['Market_Desc']).groupby('materialCode')['Market_Desc'].first().to_dict()
    
    # Impute
    df['brand'] = df['brand'].fillna(df['materialCode'].map(brand_lookup))
    df['Market_Desc'] = df['Market_Desc'].fillna(df['materialCode'].map(market_lookup))
    
    recovered_brand = missing_brand_initial - df['brand'].isnull().sum()
    recovered_market = missing_market_initial - df['Market_Desc'].isnull().sum()
    
    # Remaining to UNKNOWN
    df['brand'] = df['brand'].fillna("UNKNOWN")
    df['Market_Desc'] = df['Market_Desc'].fillna("UNKNOWN")
    
    log(f"\n--- RECOVERY RESULTS ---")
    log(f"Recovered brand values: {recovered_brand}")
    log(f"Recovered Market_Desc values: {recovered_market}")
    log(f"Remaining brand values filled with UNKNOWN: {missing_brand_initial - recovered_brand}")
    log(f"Remaining Market_Desc filled with UNKNOWN: {missing_market_initial - recovered_market}")

    # 5. Ticket + Product Duplicates Profiling
    ticket_product_dupes = df[df.duplicated(subset=['anonymized_Ticket_ID', 'materialCode'], keep=False)]
    log(f"\n--- TICKET + PRODUCT DUPES PROFILING ---")
    log(f"Total rows involved in such duplicates: {len(ticket_product_dupes)}")
    if len(ticket_product_dupes) > 0:
        log("Sample of duplicates (to inspect if repeated scan vs split line):")
        cols = ['anonymized_Ticket_ID', 'materialCode', 'salesVatEUR', 'quantity', 'discountEUR']
        log(ticket_product_dupes.sort_values(['anonymized_Ticket_ID', 'materialCode'])[cols].head(10).to_string())

    # 6. Eligible for Affinity Rule (Proposed)
    # Our proposed rule: Do not use negative/zero transactions, which represent returns or invalid basket interactions.
    df['eligible_for_affinity_v1'] = ~(df['flag_negative_sales'] | df['flag_zero_sales'] | df['flag_negative_quantity'] | df['flag_zero_quantity'])
    excluded_count = (~df['eligible_for_affinity_v1']).sum()
    
    log(f"\n--- ELIGIBILITY PROPOSAL ---")
    log(f"Total rows in dataset after duplicate drop: {len(df)}")
    log(f"Rows excluded by 'eligible_for_affinity_v1' rule: {excluded_count}")
    
    # Ensure directory exists and save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    log(f"\nSaved labeled dataset to {out_path}")
    f_log.close()

if __name__ == "__main__":
    load_and_clean()
