import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

print("Loading nav_history.csv...")
nav_df = pd.read_csv(RAW_PATH / "02_nav_history.csv")

print(f"Original rows: {len(nav_df):,}")

nav_df['date'] = pd.to_datetime(nav_df['date'])

nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
print(f"After removing duplicates: {len(nav_df):,}")

invalid_nav = nav_df[nav_df['nav'] <= 0]
if len(invalid_nav) > 0:
    print(f"Warning: {len(invalid_nav)} rows with invalid NAV (<=0)")
    nav_df = nav_df[nav_df['nav'] > 0]

nav_df = nav_df.sort_values(['amfi_code', 'date'])

print("Forward-filling missing dates...")
all_dates = pd.date_range(start=nav_df['date'].min(), end=nav_df['date'].max(), freq='D')
filled_dfs = []

for code in nav_df['amfi_code'].unique():
    fund_data = nav_df[nav_df['amfi_code'] == code].copy()
    fund_data = fund_data.set_index('date').reindex(all_dates)
    fund_data['amfi_code'] = code
    fund_data['nav'] = fund_data['nav'].ffill()
    fund_data = fund_data.dropna(subset=['nav'])
    fund_data = fund_data.reset_index()
    fund_data = fund_data.rename(columns={'index': 'date'})
    filled_dfs.append(fund_data)

nav_df_clean = pd.concat(filled_dfs, ignore_index=True)
nav_df_clean['date'] = pd.to_datetime(nav_df_clean['date'])

# Calculate daily returns for each fund
print("Calculating daily returns...")
nav_df_clean['daily_return'] = nav_df_clean.groupby('amfi_code')['nav'].pct_change()

print(f"Final rows after forward-fill: {len(nav_df_clean):,}")

nav_df_clean.to_csv(PROCESSED_PATH / "02_nav_history_clean.csv", index=False)
print(f"Saved to: {PROCESSED_PATH}/02_nav_history_clean.csv")