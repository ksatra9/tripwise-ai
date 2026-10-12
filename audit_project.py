import os
import json
import sqlite3
import pandas as pd
import numpy as np

print("=" * 80)
print("TRIPWISE AI COMPLETE WORKSPACE AUDIT")
print("=" * 80)

# 1. Databases check
for db_path in ["travel_app.db", "backend/travel_app.db"]:
    print(f"\n--- Checking DB: {db_path} ---")
    if not os.path.exists(db_path):
        print("Does not exist.")
        continue
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cur.fetchall()]
    print(f"Tables ({len(tables)}): {tables}")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cur.fetchone()[0]
        print(f"  {t}: {cnt} rows")
        if t in ["destinations", "transport_routes", "hotels"]:
            cur.execute(f"PRAGMA table_info({t});")
            cols = [col[1] for col in cur.fetchall()]
            print(f"    Columns: {cols[:8]}...")
            cur.execute(f"SELECT * FROM {t} LIMIT 2;")
            samples = cur.fetchall()
            for s in samples:
                print(f"    Sample: {s[:6]}")
    conn.close()

# 2. Datasets check
datasets = [
    "cleaned_zomato_menus.csv",
    "google_hotel_data_clean_v2.csv",
    "india_travel_destinations.csv",
    "india_tourism_dataset.json",
    "destination_names.txt",
    "dataset_schema.json"
]

print("\n" + "=" * 80)
print("DATASET PROFILES")
print("=" * 80)

for ds in datasets:
    if not os.path.exists(ds):
        print(f"\n[NOT FOUND] {ds}")
        continue
    
    size_mb = os.path.getsize(ds) / (1024 * 1024)
    print(f"\n>>> File: {ds} ({size_mb:.2f} MB)")
    
    if ds.endswith(".csv"):
        try:
            df = pd.read_csv(ds)
            print(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"  Columns: {list(df.columns)}")
            print("  Missing values per column:")
            nulls = df.isnull().sum()
            for col, n in nulls[nulls > 0].items():
                print(f"    - {col}: {n} ({n/len(df)*100:.1f}%)")
            duplicates = df.duplicated().sum()
            print(f"  Duplicate rows: {duplicates}")
            
            # Numeric columns
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            print(f"  Numeric columns: {num_cols}")
            for col in num_cols:
                vals = df[col].dropna()
                if len(vals) > 0:
                    print(f"    {col}: min={vals.min()}, max={vals.max()}, mean={vals.mean():.1f}, median={vals.median():.1f}")
                    percentiles = np.percentile(vals, [5, 25, 50, 75, 95])
                    print(f"      p5={percentiles[0]:.1f}, p25={percentiles[1]:.1f}, p50={percentiles[2]:.1f}, p75={percentiles[3]:.1f}, p95={percentiles[4]:.1f}")
                    neg_zero = (vals <= 0).sum()
                    if neg_zero > 0:
                        print(f"      WARNING: {neg_zero} values <= 0")
            
            # Categorical checks
            cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
            for col in cat_cols:
                unique_cnt = df[col].nunique()
                print(f"    {col} ({unique_cnt} unique): {df[col].dropna().unique()[:5].tolist()}")
        except Exception as e:
            print(f"  Error reading CSV: {e}")
            
    elif ds.endswith(".json"):
        try:
            with open(ds, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                print(f"  Type: JSON List of {len(data)} objects")
                if len(data) > 0:
                    print(f"  First item keys: {list(data[0].keys())}")
            elif isinstance(data, dict):
                print(f"  Type: JSON Dict with keys: {list(data.keys())[:10]}")
        except Exception as e:
            print(f"  Error reading JSON: {e}")
            
    elif ds.endswith(".txt"):
        try:
            with open(ds, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            print(f"  Lines count: {len(lines)}")
            print(f"  First 10 lines: {lines[:10]}")
        except Exception as e:
            print(f"  Error reading TXT: {e}")

print("\nAudit completed.")
