import pandas as pd

fund_df = pd.read_csv("data/raw/01_fund_master.csv")
nav_df = pd.read_csv("data/raw/02_nav_history.csv")

fund_codes = set(fund_df['amfi_code'].astype(str))
nav_codes = set(nav_df['amfi_code'].astype(str))

missing_in_nav = fund_codes - nav_codes
extra_in_nav = nav_codes - fund_codes

print("=" * 50)
print("AMFI CODE VALIDATION REPORT")
print("=" * 50)

print(f"\nCodes in fund_master: {len(fund_codes)}")
print(f"Codes in nav_history: {len(nav_codes)}")

print(f"\nCodes MISSING from nav_history: {len(missing_in_nav)}")
if missing_in_nav:
    print(f"Missing codes: {sorted(missing_in_nav)}")

print(f"\nCodes in nav_history NOT in fund_master: {len(extra_in_nav)}")
if extra_in_nav:
    extra_list = sorted(extra_in_nav)
    print(f"Extra codes (first 10): {extra_list[:10]}")

print("\n" + "=" * 50)
print("DATA QUALITY SUMMARY")
print("=" * 50)

if len(missing_in_nav) == 0:
    print("All fund_master codes exist in nav_history")
else:
    print(f"Warning: {len(missing_in_nav)} funds have no NAV data")

print(f"\nnav_history total rows: {len(nav_df):,}")
print(f"Date range: {nav_df['date'].min()} to {nav_df['date'].max()}")