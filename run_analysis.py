import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Database connection
conn = sqlite3.connect('data/mutual_funds.db')

print("=" * 60)
print("MUTUAL FUND PERFORMANCE ANALYSIS")
print("=" * 60)

# Load fund master data
fund_master = pd.read_csv('data/raw/01_fund_master.csv')
print(f"\n1. Fund Master Data: {len(fund_master)} funds loaded")

# Load NAV history
nav_history = pd.read_csv('data/raw/02_nav_history.csv')
nav_history['date'] = pd.to_datetime(nav_history['date'])
print(f"2. NAV History: {len(nav_history)} records from {nav_history['date'].min()} to {nav_history['date'].max()}")

# Load processed metrics
sharpe_ratio = pd.read_csv('data/processed/sharpe_ratio.csv')
max_drawdown = pd.read_csv('data/processed/max_drawdown.csv')
cagr_returns = pd.read_csv('data/processed/cagr_returns.csv')

print(f"3. Sharpe Ratio: {len(sharpe_ratio)} funds")
print(f"4. Max Drawdown: {len(max_drawdown)} funds")
print(f"5. CAGR Returns: {len(cagr_returns)} funds")

# Display column names for debugging
print("\nDEBUG - Available columns:")
print(f"CAGR columns: {list(cagr_returns.columns)}")
print(f"Sharpe columns: {list(sharpe_ratio.columns)}")
print(f"Drawdown columns: {list(max_drawdown.columns)}")

# TOP 10 FUNDS BY 5-YEAR CAGR
print("\n" + "=" * 60)
print("TOP 10 FUNDS BY 5-YEAR CAGR")
print("=" * 60)

if 'cagr_5yr_pct' in cagr_returns.columns:
    top_funds = cagr_returns.nlargest(10, 'cagr_5yr_pct')[['scheme_name', 'cagr_1yr_pct', 'cagr_3yr_pct', 'cagr_5yr_pct']]
    print(top_funds.to_string(index=False))
elif 'cagr_5yr' in cagr_returns.columns:
    top_funds = cagr_returns.nlargest(10, 'cagr_5yr')[['scheme_name', 'cagr_1yr', 'cagr_3yr', 'cagr_5yr']]
    print(top_funds.to_string(index=False))
else:
    print("CAGR columns not found")

# TOP 10 FUNDS BY SHARPE RATIO
print("\n" + "=" * 60)
print("TOP 10 FUNDS BY SHARPE RATIO")
print("=" * 60)

if 'sharpe_ratio' in sharpe_ratio.columns:
    top_sharpe = sharpe_ratio.nlargest(10, 'sharpe_ratio')[['scheme_name', 'sharpe_ratio']]
    print(top_sharpe.to_string(index=False))
else:
    print("Sharpe ratio column not found")

# FUNDS WITH LOWEST MAX DRAWDOWN
print("\n" + "=" * 60)
print("FUNDS WITH LOWEST MAX DRAWDOWN (Best Downside Protection)")
print("=" * 60)

if 'max_drawdown_pct' in max_drawdown.columns:
    best_protection = max_drawdown.nsmallest(10, 'max_drawdown_pct')[['scheme_name', 'max_drawdown_pct']]
    print(best_protection.to_string(index=False))
elif 'max_drawdown' in max_drawdown.columns:
    best_protection = max_drawdown.nsmallest(10, 'max_drawdown')[['scheme_name', 'max_drawdown']]
    print(best_protection.to_string(index=False))
else:
    print("Max drawdown column not found")

# Generate comprehensive report
print("\n" + "=" * 60)
print("GENERATING REPORTS")
print("=" * 60)

# Create reports directory if not exists
Path('reports').mkdir(exist_ok=True)

# Merge all metrics correctly
analysis_summary = cagr_returns[['amfi_code', 'scheme_name']].copy()

# Add CAGR columns
if 'cagr_1yr_pct' in cagr_returns.columns:
    analysis_summary['cagr_1yr'] = cagr_returns['cagr_1yr_pct']
    analysis_summary['cagr_3yr'] = cagr_returns['cagr_3yr_pct']
    analysis_summary['cagr_5yr'] = cagr_returns['cagr_5yr_pct']
else:
    analysis_summary['cagr_1yr'] = cagr_returns.get('cagr_1yr', np.nan)
    analysis_summary['cagr_3yr'] = cagr_returns.get('cagr_3yr', np.nan)
    analysis_summary['cagr_5yr'] = cagr_returns.get('cagr_5yr', np.nan)

# Add Sharpe ratio
if 'sharpe_ratio' in sharpe_ratio.columns:
    analysis_summary = analysis_summary.merge(
        sharpe_ratio[['amfi_code', 'sharpe_ratio']], 
        on='amfi_code', 
        how='left'
    )
else:
    analysis_summary['sharpe_ratio'] = np.nan

# Add Max Drawdown
if 'max_drawdown_pct' in max_drawdown.columns:
    analysis_summary = analysis_summary.merge(
        max_drawdown[['amfi_code', 'max_drawdown_pct']], 
        on='amfi_code', 
        how='left'
    )
    analysis_summary.rename(columns={'max_drawdown_pct': 'max_drawdown'}, inplace=True)
elif 'max_drawdown' in max_drawdown.columns:
    analysis_summary = analysis_summary.merge(
        max_drawdown[['amfi_code', 'max_drawdown']], 
        on='amfi_code', 
        how='left'
    )
else:
    analysis_summary['max_drawdown'] = np.nan

# Sort by 5-year CAGR
analysis_summary = analysis_summary.sort_values('cagr_5yr', ascending=False)

# Save to CSV
analysis_summary.to_csv('reports/fund_performance_summary.csv', index=False)
print("Saved: reports/fund_performance_summary.csv")

# Display top 10 overall performers
print("\n" + "=" * 60)
print("TOP 10 OVERALL PERFORMERS (by 5-Year CAGR)")
print("=" * 60)
print(analysis_summary[['scheme_name', 'cagr_5yr', 'sharpe_ratio', 'max_drawdown']].head(10).to_string(index=False))

# Close database connection
conn.close()

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)