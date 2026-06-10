import pandas as pd

fund_df = pd.read_csv("data/raw/01_fund_master.csv")

print("=" * 50)
print("FUND MASTER EXPLORATION")
print("=" * 50)

print(f"\nTotal schemes: {len(fund_df)}")
print(f"Columns: {list(fund_df.columns)}\n")

print("UNIQUE FUND HOUSES:")
print(fund_df['fund_house'].unique())
print(f"\nTotal AMCs: {fund_df['fund_house'].nunique()}\n")

print("UNIQUE CATEGORIES:")
print(fund_df['category'].unique())
print(f"\nTotal categories: {fund_df['category'].nunique()}\n")

print("UNIQUE SUB-CATEGORIES:")
print(fund_df['sub_category'].unique())
print(f"\nTotal sub-categories: {fund_df['sub_category'].nunique()}\n")

print("UNIQUE RISK GRADES:")
print(fund_df['risk_category'].unique())
print(f"\nTotal risk levels: {fund_df['risk_category'].nunique()}\n")

print("AMFI CODE STRUCTURE (first 5):")
print(fund_df['amfi_code'].astype(str).head())