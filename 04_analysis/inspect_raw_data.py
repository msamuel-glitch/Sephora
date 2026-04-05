import pandas as pd

file_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\02_data_raw\BDD#7_Database_Albert_School_Sephora.csv"
out_path = r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\schema_report.txt"

try:
    df = pd.read_csv(file_path, low_memory=False)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"ROW COUNT: {len(df)}\n")
        f.write(f"COLUMN COUNT: {len(df.columns)}\n\n")
        
        f.write("COLUMNS AND TYPES:\n")
        for col in df.columns:
            null_count = df[col].isnull().sum()
            null_pct = (null_count / len(df)) * 100
            f.write(f"- {col}: {df[col].dtype} (Missing: {null_count} / {null_pct:.2f}%)\n")
            
        f.write("\nOBVIOUS MISSING-VALUE PATTERNS:\n")
        high_missing = [col for col in df.columns if df[col].isnull().sum() / len(df) > 0.5]
        low_missing = [col for col in df.columns if 0 < df[col].isnull().sum() / len(df) <= 0.5]
        no_missing = [col for col in df.columns if df[col].isnull().sum() == 0]
        
        f.write(f"Columns with >50% missing data: {high_missing}\n")
        f.write(f"Columns with some missing data (<=50%): {low_missing}\n")
        f.write(f"Columns with NO missing data: {len(no_missing)} columns\n")
        
        f.write("\nSAMPLE (First 2 rows, first 10 columns):\n")
        f.write(df.iloc[:2, :10].to_string())
        
    print("Done writing to schema_report.txt")
except Exception as e:
    print(f"Error: {e}")
