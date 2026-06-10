import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import sqlite3
import warnings
warnings.filterwarnings('ignore')

# Paths
DB_PATH = Path("/Users/redxpaliwal/Desktop/Bluestock_MF_Capstone/data/db/bluestock_mf.db")
REPORTS_PATH = Path("reports")
PROCESSED_PATH = Path("data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
REPORTS_PATH.mkdir(parents=True, exist_ok=True)

# Connect to database
conn = sqlite3.connect(DB_PATH)

RISK_FREE_RATE = 0.065
TRADING_DAYS = 252

# Load NAV data
query = """
SELECT n.amfi_code, f.scheme_name, f.category, f.sub_category, 
       n.date, n.nav, n.daily_return
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
WHERE n.daily_return IS NOT NULL
ORDER BY n.amfi_code, n.date
"""
df = pd.read_sql(query, conn)
df['date'] = pd.to_datetime(df['date'])

print(f"\nLoaded {len(df):,} daily return records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Number of funds: {df['amfi_code'].nunique()}")

# Calculate CAGR
def calculate_cagr(fund_df, years):
    end_date = fund_df['date'].max()
    start_date = end_date - pd.DateOffset(years=years)
    start_nav = fund_df[fund_df['date'] >= start_date]['nav'].iloc[0] if len(fund_df[fund_df['date'] >= start_date]) > 0 else np.nan
    end_nav = fund_df['nav'].iloc[-1]
    if pd.notna(start_nav) and start_nav > 0:
        return (end_nav / start_nav) ** (1/years) - 1
    return np.nan

cagr_results = []
for code in df['amfi_code'].unique():
    fund_data = df[df['amfi_code'] == code].sort_values('date')
    fund_name = fund_data['scheme_name'].iloc[0]
    cagr_results.append({
        'amfi_code': code,
        'scheme_name': fund_name,
        'cagr_1yr_pct': calculate_cagr(fund_data, 1) * 100,
        'cagr_3yr_pct': calculate_cagr(fund_data, 3) * 100,
        'cagr_5yr_pct': calculate_cagr(fund_data, 5) * 100
    })
cagr_df = pd.DataFrame(cagr_results)
cagr_df.to_csv(PROCESSED_PATH / "cagr_returns.csv", index=False)
print(f"\nSaved: cagr_returns.csv")

# Calculate Sharpe Ratio
def calculate_sharpe(fund_returns):
    if len(fund_returns) < 2 or fund_returns.std() == 0:
        return np.nan
    excess_return = fund_returns.mean() - RISK_FREE_RATE / TRADING_DAYS
    return (excess_return / fund_returns.std()) * np.sqrt(TRADING_DAYS)

sharpe_results = []
for code in df['amfi_code'].unique():
    fund_returns = df[df['amfi_code'] == code]['daily_return'].dropna()
    sharpe_results.append({
        'amfi_code': code,
        'scheme_name': df[df['amfi_code'] == code]['scheme_name'].iloc[0],
        'sharpe_ratio': calculate_sharpe(fund_returns)
    })
sharpe_df = pd.DataFrame(sharpe_results).sort_values('sharpe_ratio', ascending=False)
sharpe_df.to_csv(PROCESSED_PATH / "sharpe_ratio.csv", index=False)
print(f"Saved: sharpe_ratio.csv")

# Calculate Sortino Ratio
def calculate_sortino(fund_returns):
    if len(fund_returns) < 2:
        return np.nan
    excess_return = fund_returns.mean() - RISK_FREE_RATE / TRADING_DAYS
    negative_returns = fund_returns[fund_returns < 0]
    downside_std = negative_returns.std() if len(negative_returns) > 0 else fund_returns.std()
    if downside_std == 0:
        return np.nan
    return (excess_return / downside_std) * np.sqrt(TRADING_DAYS)

sortino_results = []
for code in df['amfi_code'].unique():
    fund_returns = df[df['amfi_code'] == code]['daily_return'].dropna()
    sortino_results.append({
        'amfi_code': code,
        'scheme_name': df[df['amfi_code'] == code]['scheme_name'].iloc[0],
        'sortino_ratio': calculate_sortino(fund_returns)
    })
sortino_df = pd.DataFrame(sortino_results).sort_values('sortino_ratio', ascending=False)
sortino_df.to_csv(PROCESSED_PATH / "sortino_ratio.csv", index=False)
print(f"Saved: sortino_ratio.csv")

# Load benchmark
benchmark_df = pd.read_csv("data/raw/10_benchmark_indices.csv")
benchmark_df['date'] = pd.to_datetime(benchmark_df['date'])
nifty100 = benchmark_df[benchmark_df['index_name'] == 'NIFTY100'].copy()
nifty100 = nifty100.sort_values('date')
nifty100['daily_return'] = nifty100['close_value'].pct_change()

# Calculate Alpha and Beta
returns_pivot = df.pivot(index='date', columns='amfi_code', values='daily_return')
benchmark_pivot = nifty100.set_index('date')['daily_return']

alpha_beta_results = []
for code in returns_pivot.columns:
    fund_returns = returns_pivot[code].dropna()
    common_idx = fund_returns.index.intersection(benchmark_pivot.index)
    if len(common_idx) >= 30:
        fund_aligned = fund_returns.loc[common_idx]
        bench_aligned = benchmark_pivot.loc[common_idx]
        slope, intercept, r_value, p_value, std_err = stats.linregress(bench_aligned, fund_aligned)
        alpha_beta_results.append({
            'amfi_code': code,
            'scheme_name': df[df['amfi_code'] == code]['scheme_name'].iloc[0],
            'alpha_annualized_pct': intercept * TRADING_DAYS * 100,
            'beta': slope
        })
    else:
        alpha_beta_results.append({
            'amfi_code': code,
            'scheme_name': df[df['amfi_code'] == code]['scheme_name'].iloc[0],
            'alpha_annualized_pct': np.nan,
            'beta': np.nan
        })
alpha_beta_df = pd.DataFrame(alpha_beta_results).sort_values('alpha_annualized_pct', ascending=False)
alpha_beta_df.to_csv(PROCESSED_PATH / "alpha_beta.csv", index=False)
print(f"Saved: alpha_beta.csv")

# Calculate Maximum Drawdown
def calculate_max_drawdown(fund_nav):
    running_max = fund_nav.expanding().max()
    drawdown = (fund_nav - running_max) / running_max
    return drawdown.min() * 100

drawdown_results = []
for code in df['amfi_code'].unique():
    fund_nav = df[df['amfi_code'] == code].set_index('date')['nav'].sort_index()
    drawdown_results.append({
        'amfi_code': code,
        'scheme_name': df[df['amfi_code'] == code]['scheme_name'].iloc[0],
        'max_drawdown_pct': calculate_max_drawdown(fund_nav)
    })
drawdown_df = pd.DataFrame(drawdown_results).sort_values('max_drawdown_pct')
drawdown_df.to_csv(PROCESSED_PATH / "max_drawdown.csv", index=False)
print(f"Saved: max_drawdown.csv")

# Load expense ratios
expense_df = pd.read_csv("data/raw/01_fund_master.csv")
expense_df = expense_df[['amfi_code', 'scheme_name', 'expense_ratio_pct']]

# Build Scorecard
scorecard = sharpe_df[['amfi_code', 'scheme_name', 'sharpe_ratio']].copy()
scorecard = scorecard.merge(cagr_df[['amfi_code', 'cagr_3yr_pct']], on='amfi_code', how='left')
scorecard = scorecard.merge(alpha_beta_df[['amfi_code', 'alpha_annualized_pct']], on='amfi_code', how='left')
scorecard = scorecard.merge(drawdown_df[['amfi_code', 'max_drawdown_pct']], on='amfi_code', how='left')
scorecard = scorecard.merge(expense_df[['amfi_code', 'expense_ratio_pct']], on='amfi_code', how='left')

scorecard['rank_3yr_return'] = scorecard['cagr_3yr_pct'].rank(ascending=False)
scorecard['rank_sharpe'] = scorecard['sharpe_ratio'].rank(ascending=False)
scorecard['rank_alpha'] = scorecard['alpha_annualized_pct'].rank(ascending=False)
scorecard['rank_expense'] = scorecard['expense_ratio_pct'].rank(ascending=True)
scorecard['rank_drawdown'] = scorecard['max_drawdown_pct'].rank(ascending=True)

max_rank = len(scorecard)
scorecard['composite_score'] = (
    0.30 * (1 - (scorecard['rank_3yr_return'] - 1) / (max_rank - 1)) * 100 +
    0.25 * (1 - (scorecard['rank_sharpe'] - 1) / (max_rank - 1)) * 100 +
    0.20 * (1 - (scorecard['rank_alpha'] - 1) / (max_rank - 1)) * 100 +
    0.15 * (1 - (scorecard['rank_expense'] - 1) / (max_rank - 1)) * 100 +
    0.10 * (1 - (scorecard['rank_drawdown'] - 1) / (max_rank - 1)) * 100
)
scorecard = scorecard.sort_values('composite_score', ascending=False)
scorecard.to_csv(PROCESSED_PATH / "fund_scorecard.csv", index=False)
print(f"Saved: fund_scorecard.csv")

# Benchmark Comparison Chart
top_funds = scorecard.head(5)['amfi_code'].tolist()
nav_query = f"""
SELECT f.scheme_name, n.date, n.nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
WHERE n.amfi_code IN ({','.join(["'"+str(c)+"'" for c in top_funds])})
ORDER BY n.date
"""
top_nav = pd.read_sql(nav_query, conn)
top_nav['date'] = pd.to_datetime(top_nav['date'])

pivot_nav = top_nav.pivot(index='date', columns='scheme_name', values='nav')
normalized = pivot_nav / pivot_nav.iloc[0] * 100

nifty_clean = nifty100[nifty100['date'] >= normalized.index.min()]
nifty_clean = nifty_clean.set_index('date')
nifty_normalized = nifty_clean['close_value'] / nifty_clean['close_value'].iloc[0] * 100

plt.figure(figsize=(14, 7))
for col in normalized.columns:
    plt.plot(normalized.index, normalized[col], linewidth=1.5, label=col[:30])
plt.plot(nifty_normalized.index, nifty_normalized, linewidth=2.5, color='black', linestyle='--', label='NIFTY 100')
plt.xlabel('Date')
plt.ylabel('Normalized Performance (Base 100)')
plt.title('Top 5 Funds vs NIFTY 100 Benchmark')
plt.legend(loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(REPORTS_PATH / 'benchmark_comparison.png', dpi=150)
plt.close()
print(f"Saved: reports/benchmark_comparison.png")

# Summary
print("\n" + "=" * 60)
print("PERFORMANCE METRICS SUMMARY")
print("=" * 60)
print(f"\nBest Sharpe Ratio: {sharpe_df.iloc[0]['scheme_name']} ({sharpe_df.iloc[0]['sharpe_ratio']:.2f})")
print(f"Best Sortino Ratio: {sortino_df.iloc[0]['scheme_name']} ({sortino_df.iloc[0]['sortino_ratio']:.2f})")
print(f"Highest Alpha: {alpha_beta_df.iloc[0]['scheme_name']} ({alpha_beta_df.iloc[0]['alpha_annualized_pct']:.2f}%)")
print(f"Lowest Expense: {expense_df.loc[expense_df['expense_ratio_pct'].idxmin(), 'scheme_name']} ({expense_df['expense_ratio_pct'].min():.2f}%)")
print(f"Smallest Drawdown: {drawdown_df.iloc[-1]['scheme_name']} ({drawdown_df.iloc[-1]['max_drawdown_pct']:.1f}%)")
print(f"\nTop Overall Fund: {scorecard.iloc[0]['scheme_name']} (Score: {scorecard.iloc[0]['composite_score']:.1f}/100)")


conn.close()