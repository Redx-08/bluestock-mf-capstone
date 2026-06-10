import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set professional plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load the summary
summary = pd.read_csv('reports/fund_performance_summary.csv')

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Mutual Fund Performance Analysis', fontsize=16, fontweight='bold')

# 1. Top 10 by 5-Year CAGR
top10_cagr = summary.nlargest(10, 'cagr_5yr')
axes[0, 0].barh(top10_cagr['scheme_name'].str[:30], top10_cagr['cagr_5yr'])
axes[0, 0].set_xlabel('5-Year CAGR (%)')
axes[0, 0].set_title('Top 10 Funds by 5-Year CAGR')
axes[0, 0].invert_yaxis()

# 2. Sharpe Ratio vs Max Drawdown
scatter = axes[0, 1].scatter(summary['sharpe_ratio'], summary['max_drawdown'], 
                              c=summary['cagr_5yr'], cmap='RdYlGn', s=100, alpha=0.6)
axes[0, 1].set_xlabel('Sharpe Ratio')
axes[0, 1].set_ylabel('Max Drawdown (%)')
axes[0, 1].set_title('Risk-Return Profile (Color = 5Y CAGR)')
plt.colorbar(scatter, ax=axes[0, 1], label='5Y CAGR (%)')

# 3. Top 10 by Sharpe Ratio
top10_sharpe = summary.nlargest(10, 'sharpe_ratio')
axes[1, 0].barh(top10_sharpe['scheme_name'].str[:30], top10_sharpe['sharpe_ratio'], color='green')
axes[1, 0].set_xlabel('Sharpe Ratio')
axes[1, 0].set_title('Top 10 Funds by Risk-Adjusted Returns')
axes[1, 0].invert_yaxis()

# 4. Category Performance (if you have category data)
# For now, show distribution of 5Y CAGR
axes[1, 1].hist(summary['cagr_5yr'].dropna(), bins=15, edgecolor='black', alpha=0.7)
axes[1, 1].axvline(summary['cagr_5yr'].mean(), color='red', linestyle='--', label=f"Mean: {summary['cagr_5yr'].mean():.1f}%")
axes[1, 1].set_xlabel('5-Year CAGR (%)')
axes[1, 1].set_ylabel('Number of Funds')
axes[1, 1].set_title('Distribution of 5-Year Returns')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('reports/performance_dashboard.png', dpi=150, bbox_inches='tight')
print("Saved: reports/performance_dashboard.png")

# Generate summary statistics
print("\n" + "=" * 60)
print("PORTFOLIO STATISTICS")
print("=" * 60)

print(f"\nAverage 5-Year CAGR: {summary['cagr_5yr'].mean():.2f}%")
print(f"Median 5-Year CAGR: {summary['cagr_5yr'].median():.2f}%")
print(f"Best 5-Year CAGR: {summary['cagr_5yr'].max():.2f}%")
print(f"Worst 5-Year CAGR: {summary['cagr_5yr'].min():.2f}%")

print(f"\nAverage Sharpe Ratio: {summary['sharpe_ratio'].mean():.3f}")
print(f"Average Max Drawdown: {summary['max_drawdown'].mean():.2f}%")

# Identify best balanced funds (high return, low risk, low drawdown)
summary['score'] = (summary['cagr_5yr'] * 0.5 + 
                    summary['sharpe_ratio'] * 20 - 
                    abs(summary['max_drawdown']) * 0.3)

best_balanced = summary.nlargest(5, 'score')[['scheme_name', 'cagr_5yr', 'sharpe_ratio', 'max_drawdown', 'score']]
print("\n" + "=" * 60)
print("TOP 5 BEST BALANCED FUNDS (Return + Risk + Protection)")
print("=" * 60)
print(best_balanced.to_string(index=False))

# Save recommendations
best_balanced.to_csv('reports/top_recommended_funds.csv', index=False)
print("\nSaved: reports/top_recommended_funds.csv")