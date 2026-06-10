# Bluestock Mutual Fund Capstone Project

## Overview
Performance analysis of 40 Indian mutual funds using NAV history from 2022-2026.

## Key Metrics
- CAGR (1, 3, 5 year)
- Sharpe Ratio
- Sortino Ratio
- Alpha/Beta
- Maximum Drawdown

## Top 5 Recommended Funds (Balanced Score)
1. Mirae Asset Large Cap Fund (Sharpe: 1.07, Drawdown: -11.3%)
2. Kotak Flexicap Fund (Sharpe: 0.97, Drawdown: -13.0%)
3. Mirae Asset Tax Saver Fund (Sharpe: 0.92, Drawdown: -16.4%)
4. ICICI Pru Midcap Fund (CAGR: 28.9%, Sharpe: 0.88)
5. HDFC Mid-Cap Opportunities Fund (CAGR: 26.4%, Sharpe: 0.81)

## Setup
```bash
pip install -r requirements.txt
make all
cat > fix_sharpe_calculation.py << 'EOF'
import pandas as pd
import numpy as np

# Load the original NAV data
nav = pd.read_csv('data/raw/02_nav_history.csv')
nav['date'] = pd.to_datetime(nav['date'])

# Load fund master
funds = pd.read_csv('data/raw/01_fund_master.csv')

# Calculate Sharpe ratio correctly for one fund to verify
def calculate_correct_sharpe(fund_amfi):
    fund_nav = nav[nav['amfi_code'] == fund_amfi].sort_values('date')
    returns = fund_nav['nav'].pct_change().dropna()
    
    # Use 6.5% annual risk-free rate, convert to daily
    risk_free_daily = 0.065 / 252
    
    excess_returns = returns - risk_free_daily
    sharpe_daily = excess_returns.mean() / excess_returns.std()
    sharpe_annualized = sharpe_daily * np.sqrt(252)
    
    return sharpe_annualized

# Test a few funds
test_funds = [119551, 148567, 120505]  # SBI Bluechip, Mirae Large Cap, ICICI Midcap
for code in test_funds:
    fund_name = funds[funds['amfi_code'] == code]['scheme_name'].iloc[0]
    calculated = calculate_correct_sharpe(code)
    reported = pd.read_csv('data/processed/sharpe_ratio.csv')
    reported_val = reported[reported['amfi_code'] == code]['sharpe_ratio'].iloc[0]
    print(f"{fund_name[:40]}:")
    print(f"  Calculated: {calculated:.4f}")
    print(f"  Reported:   {reported_val:.4f}")
    print(f"  Difference: {abs(calculated - reported_val):.4f}")
    print()

# Check risk-free rate appropriateness
print("=" * 50)
print("Risk-Free Rate Analysis")
print("=" * 50)
print("Current assumption: 6.5% (India 10-year G-Sec yield)")
print("Alternative benchmarks:")
print("  - 5-year G-Sec: ~7.2%")
print("  - 1-year T-Bill: ~6.8%")
print("  - Savings account: ~3.5%")
print()
print("Recommendation: Use 6.0% for equity fund analysis")
