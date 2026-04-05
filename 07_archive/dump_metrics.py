import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora"
DIM_CUST = os.path.join(BASE, "03_data_working", "dim_customer.csv")
AUDIT_BASE = os.path.join(BASE, "03_data_working", "sephora_audit_labeled_base.csv")
DIM_BRAND = os.path.join(BASE, "03_data_working", "dim_brand.csv")
# TOP_PAIRS = os.path.join(BASE, "05_outputs", "top10_store_brand_pairs_presentable.csv")
# Let's check the actual name
TOP_PAIRS = [f for f in os.listdir(os.path.join(BASE, "05_outputs")) if "top10_store_brand_pairs" in f][0]
TOP_PAIRS_PATH = os.path.join(BASE, "05_outputs", TOP_PAIRS)

def get_report():
    # Load Data
    df_cust = pd.read_csv(DIM_CUST)
    df_audit = pd.read_csv(AUDIT_BASE, low_memory=False)
    df_brand = pd.read_csv(DIM_BRAND)
    
    # Q1
    q_labels = ["Q1", "Q2", "Q3", "Q4"]
    df_cust["freq_quartile"], bins = pd.qcut(df_cust["velocity_score"], 4, labels=q_labels, retbins=True)
    q1_global = df_cust.groupby("freq_quartile")["loyalist_vs_explorer_index"].mean()
    q1_gen = df_cust.groupby(["age_generation", "freq_quartile"])["loyalist_vs_explorer_index"].mean()
    
    print("QUESTION 1 — FREQUENCY INFLECTION POINT")
    print(f"Velocity Quartile Thresholds (Days): {bins}")
    print("\nGlobal Mean Explorer Index:")
    print(q1_global.to_frame().T.to_string(index=False))
    print("\nMean Explorer Index by Generation:")
    print(q1_gen.unstack().to_string())
    print("-" * 40)
    
    # Q2
    df_audit["date"] = pd.to_datetime(df_audit["transactionDate"])
    df_audit["month"] = df_audit["date"].dt.month
    js = df_audit[df_audit["month"] <= 9]
    od = df_audit[df_audit["month"] > 9]
    hist = js.groupby("anonymized_card_code")["brand"].apply(set).to_dict()
    last = js.groupby("anonymized_card_code")["date"].max()
    adoptions = od[od.apply(lambda r: r["brand"] not in hist.get(r["anonymized_card_code"], set()), axis=1)]
    first_adopt = adoptions.groupby("anonymized_card_code")["date"].min()
    gap = first_adopt.reset_index().merge(last.reset_index(name="last_date"), on="anonymized_card_code")
    gap["days_gap"] = (gap["date"] - gap["last_date"]).dt.days
    gap = gap.merge(df_cust[["anonymized_card_code", "crm_push_eligibility_proxy"]], on="anonymized_card_code")
    medians = gap.groupby("crm_push_eligibility_proxy")["days_gap"].median()
    
    print("\nQUESTION 2 — CRM ADVANCE SIGNAL TIMING")
    print("Median Days to Adoption (Eligible vs Non):")
    print(medians.to_string())
    print("-" * 40)
    
    # Q3
    print("\nQUESTION 3 — THE ACTUAL 11 BRAND PAIRS")
    df_pairs = pd.read_csv(TOP_PAIRS_PATH)
    # The file has: brand_a, brand_b, axis_a, axis_b, mkt_a, mkt_b, lift, p_val, story
    # Standardize column names for output if they differ slightly
    print(df_pairs.to_string(index=False))
    print("-" * 40)
    
    # Q4
    brand_mkt_map = df_brand.set_index("brand")["primary_market"].to_dict()
    adoptions["mkt_fam"] = adoptions["brand"].map(brand_mkt_map)
    final = adoptions.merge(df_cust[["anonymized_card_code", "recruitment_channel"]], on="anonymized_card_code")
    shares = final.groupby(["recruitment_channel", "mkt_fam"]).size().unstack(fill_value=0)
    pct = shares.div(shares.sum(axis=1), axis=0) * 100
    
    print("\nQUESTION 4 — RECRUITMENT CHANNEL SHAP FINDING")
    print("Adoption Share % by Market Family:")
    print(pct.to_string())
    print("-" * 40)

if __name__ == "__main__":
    get_report()
