import pandas as pd
import numpy as np

def test_sharpe_calculation():
    # Test with known values
    def sharpe_ratio_calc(returns, risk_free, volatility):
        return (returns - risk_free) / volatility
    
    result = sharpe_ratio_calc(returns=0.15, risk_free=0.065, volatility=0.12)
    expected = 0.70833
    assert abs(result - expected) < 0.001, f"Expected {expected}, got {result}"
    print("Sharpe ratio test passed")

def validate_sharpe_ratios():
    # Check if calculated Sharpe ratios are reasonable
    sharpe = pd.read_csv('data/processed/sharpe_ratio.csv')
    negative_count = (sharpe['sharpe_ratio'] < 0).sum()
    print(f"Funds with negative Sharpe ratio: {negative_count}")
    print(f"Sharpe ratio range: {sharpe['sharpe_ratio'].min():.3f} to {sharpe['sharpe_ratio'].max():.3f}")
    
    if negative_count > 0:
        print("WARNING: Negative Sharpe ratios detected - check risk-free rate assumption")

if __name__ == "__main__":
    test_sharpe_calculation()
    validate_sharpe_ratios()
