# Configuration parameters for mutual fund analysis

# Risk metrics
RISK_FREE_RATE = 0.065  # 6.5% annual
TRADING_DAYS = 252

# Date ranges
START_DATE = '2022-01-01'
END_DATE = '2026-05-29'

# File paths
RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
REPORTS_DIR = 'reports'
DATABASE_PATH = 'data/mutual_funds.db'

# Analysis parameters
MIN_NAV_RECORDS = 1000
CAGR_YEARS = [1, 3, 5]
