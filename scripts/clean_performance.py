import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")

print("Loading scheme_performance.csv...")
perf_df = pd.read_csv(RAW_PATH / "07_scheme_performance.csv")

print(f"Original rows: {len(perf_df)}")

# Convert numeric columns (force errors to NaN)
numeric_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 
                'sharpe_ratio', 'sortino_ratio', 'alpha', 'beta',
                'std_dev_ann_pct', 'max_drawdown_pct', 'expense_ratio_pct']

for col in numeric_cols:
    if col in perf_df.columns:
        perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')

# Flag anomalies
perf_df['expense_ratio_valid'] = (perf_df['expense_ratio_pct'] >= 0.1) & (perf_df['expense_ratio_pct'] <= 2.5)
invalid_expense = perf_df[~perf_df['expense_ratio_valid']]
if len(invalid_expense) > 0:
    print(f"Warning: {len(invalid_expense)} funds have expense ratio outside 0.1-2.5% range")

# Remove rows where critical metrics are null
perf_df = perf_df.dropna(subset=['return_3yr_pct', 'sharpe_ratio'])

print(f"Final rows after cleaning: {len(perf_df)}")

# Save
perf_df.to_csv(PROCESSED_PATH / "07_scheme_performance_clean.csv", index=False)
print(f"Saved to: {PROCESSED_PATH}/07_scheme_performance_clean.csv")