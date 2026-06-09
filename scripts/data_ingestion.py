import pandas as pd
from pathlib import Path


RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")


PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


csv_files = list(RAW_PATH.glob("*.csv"))

print(f"Found {len(csv_files)} CSV files. Loading...")

for file in csv_files:
    df = pd.read_csv(file)
    print(f"\n {file.name} -> {df.shape[0]} rows, {df.shape[1]} columns")
    print(df.dtypes.value_counts().to_string())
    print("First 2 rows:\n", df.head(2))