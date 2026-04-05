import pandas as pd
import numpy as np

file_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\02_data_raw\BDD#7_Database_Albert_School_Sephora.csv"
out_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\audit_report.txt"

def run_audit():
    with open(out_path, 'w', encoding='utf-8') as f:
        def log(msg):
            print(msg)
            f.write(msg + '\n')
            
        try:
            df = pd.read_csv(file_path, low_memory=False)
            
            log("--- ROW COUNTS ---")
            log(f"Total rows: {len(df)}")
            
            log("\n--- NEGATIVE & ZERO VALUES ---")
            neg_sales = (df['salesVatEUR'] < 0).sum()
            zero_sales = (df['salesVatEUR'] == 0).sum()
            neg_qty = (df['quantity'] < 0).sum()
            zero_qty = (df['quantity'] == 0).sum()
            log(f"Negative salesVatEUR: {neg_sales}")
            log(f"Zero salesVatEUR: {zero_sales}")
            log(f"Negative quantity: {neg_qty}")
            log(f"Zero quantity: {zero_qty}")
            
            log("\n--- DISCOUNT ANOMALIES ---")
            bad_discount = (df['discountEUR'] > df['salesVatEUR']).sum()
            log(f"discountEUR > salesVatEUR: {bad_discount}")
            
            log("\n--- DATE BOUNDARIES ---")
            df['trans_date'] = pd.to_datetime(df['transactionDate'], errors='coerce')
            min_date = df['trans_date'].min()
            max_date = df['trans_date'].max()
            non_2025 = (~df['trans_date'].dt.year.isin([2025, np.nan])).sum()
            log(f"transactionDate range: {min_date} to {max_date}")
            log(f"transactionDate outside 2025: {non_2025}")
            
            df['first_dt'] = pd.to_datetime(df['first_purchase_dt'], errors='coerce')
            min_first = df['first_dt'].min()
            max_first = df['first_dt'].max()
            log(f"first_purchase_dt range: {min_first} to {max_first}")
            
            log("\n--- DUPLICATES ---")
            exact_dupes = df.duplicated().sum()
            ticket_item_dupes = df.duplicated(subset=['anonymized_Ticket_ID', 'materialCode'], keep=False).sum()
            log(f"Exact row duplicates: {exact_dupes}")
            log(f"Identical Ticket+Material code lines: {ticket_item_dupes}")
            
            log("\n--- HIGH MISSINGNESS ANALYSIS (First Purchase Block) ---")
            null_first = df['first_purchase_dt'].isnull().sum()
            log(f"Rows missing first_purchase_dt: {null_first} ({(null_first/len(df))*100:.2f}%)")
            
            log("\n--- OTHER NULL CATEGORICALS ---")
            for col in ['brand', 'Market_Desc', 'age_category', 'age_generation', 'countryIsoCode']:
                count = df[col].isnull().sum()
                log(f"{col} missing: {count}")
                
            log("\n--- ID COLUMNS (Preview Data Types) ---")
            for col in ['anonymized_card_code', 'anonymized_Ticket_ID', 'materialCode']:
                log(f"{col} type: {df[col].dtype}")
            
            log("\nDONE")
        except Exception as e:
            log(f"Error: {e}")

if __name__ == '__main__':
    run_audit()
