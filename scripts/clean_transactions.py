import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")

print("Loading investor_transactions.csv...")
trans_df = pd.read_csv(RAW_PATH / "08_investor_transactions.csv")

print(f"Original rows: {len(trans_df):,}")

# Fix date format
trans_df['transaction_date'] = pd.to_datetime(trans_df['transaction_date'])

# Standardize transaction_type
valid_types = ['SIP', 'Lumpsum', 'Redemption']
trans_df['transaction_type'] = trans_df['transaction_type'].str.title()
trans_df = trans_df[trans_df['transaction_type'].isin(valid_types)]

# Validate amount > 0
trans_df = trans_df[trans_df['amount_inr'] > 0]

# Check KYC status
valid_kyc = ['Verified', 'Pending']
trans_df = trans_df[trans_df['kyc_status'].isin(valid_kyc)]

print(f"Final rows after cleaning: {len(trans_df):,}")

# Save
trans_df.to_csv(PROCESSED_PATH / "08_investor_transactions_clean.csv", index=False)
print(f"Saved to: {PROCESSED_PATH}/08_investor_transactions_clean.csv")