import pandas as pd
import os

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
AUDIT_BASE = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")

try:
    df = pd.read_csv(AUDIT_BASE, low_memory=False)
    df['dt'] = pd.to_datetime(df['transactionDate'], errors='coerce')
    
    print(f"TotalRows: {len(df)}")
    print(f"UniqueCust: {df['anonymized_card_code'].nunique()}")
    print(f"UniqueBrands: {df['brand'].nunique()}")
    print(f"MinDate: {df['dt'].min()}")
    print(f"MaxDate: {df['dt'].max()}")
    
    eligible = df[df['eligible_for_affinity_v1'] == True].copy()
    print(f"EligibleRows: {len(eligible)}")
    
    train = eligible[eligible['dt'].dt.month <= 9]
    test = eligible[eligible['dt'].dt.month > 9]
    print(f"TrainRows: {len(train)}")
    print(f"TestRows: {len(test)}")
    
except Exception as e:
    print(f"Error: {e}")
