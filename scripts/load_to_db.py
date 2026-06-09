import pandas as pd
import sqlite3
from pathlib import Path

PROCESSED_PATH = Path("data/processed")
DB_PATH = Path("data/db/bluestock_mf.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Load dimension tables
print("Loading dim_fund...")
fund_df = pd.read_csv(PROCESSED_PATH / "01_fund_master.csv")  # original, not cleaned
fund_df.to_sql('dim_fund', conn, if_exists='replace', index=False)

print("Loading dim_date...")
# Generate date dimension
date_range = pd.date_range(start='2022-01-01', end='2026-12-31', freq='D')
dim_date = pd.DataFrame({
    'date': date_range,
    'year': date_range.year,
    'quarter': date_range.quarter,
    'month': date_range.month,
    'month_name': date_range.month_name(),
    'day_of_week': date_range.dayofweek,
    'is_weekend': (date_range.dayofweek >= 5).astype(int),
    'is_holiday': 0  # placeholder, can be updated later
})
dim_date.to_sql('dim_date', conn, if_exists='replace', index=False)

# Load fact tables
print("Loading fact_nav...")
nav_df = pd.read_csv(PROCESSED_PATH / "02_nav_history_clean.csv")
nav_df.to_sql('fact_nav', conn, if_exists='replace', index=False)

print("Loading fact_transactions...")
trans_df = pd.read_csv(PROCESSED_PATH / "08_investor_transactions_clean.csv")
trans_df.to_sql('fact_transactions', conn, if_exists='replace', index=False)

print("Loading fact_performance...")
perf_df = pd.read_csv(PROCESSED_PATH / "07_scheme_performance_clean.csv")
perf_df.to_sql('fact_performance', conn, if_exists='replace', index=False)

print("Loading fact_nav...")
nav_df = pd.read_csv(PROCESSED_PATH / "02_nav_history_clean.csv")
nav_df.to_sql('fact_nav', conn, if_exists='replace', index=False)

# Verify row counts
print("\n=== VERIFICATION ===")
tables = ['dim_fund', 'dim_date', 'fact_nav', 'fact_transactions', 'fact_performance', 'fact_aum']
for table in tables:
    count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn).iloc[0,0]
    print(f"{table}: {count:,} rows")

conn.close()
print(f"\nDatabase saved to: {DB_PATH}")