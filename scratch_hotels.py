import sys
import pandas as pd
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("google_hotel_data_clean_v2.csv")
print(f"Total rows: {len(df)}")
print("Cities covered:")
print(df["City"].value_counts().head(30))
print("\nFeature_1 distribution:")
print(df["Feature_1"].value_counts().head(10))

print("\nPrice statistics by star rating / tier:")
for star in ["5-star hotel", "4-star hotel", "3-star hotel"]:
    sub = df[df["Feature_1"] == star]
    if len(sub) > 0:
        prices = sub["Hotel_Price"]
        print(f"  {star}: count={len(sub)}, min={prices.min()}, median={prices.median()}, mean={prices.mean():.0f}, max={prices.max()}")

print("\nTop 10 most expensive hotels:")
print(df.sort_values(by="Hotel_Price", ascending=False)[["Hotel_Name", "City", "Feature_1", "Hotel_Price", "Hotel_Rating"]].head(10))
