-- Query 1: Top 5 funds by AUM (latest quarter)
SELECT f.fund_house, f.scheme_name, a.aum_crore
FROM fact_aum a
JOIN dim_fund f ON a.fund_house = f.fund_house
WHERE a.date = (SELECT MAX(date) FROM fact_aum)
ORDER BY a.aum_crore DESC
LIMIT 5;

-- Query 2: Average NAV per month for HDFC Top 100
SELECT strftime('%Y-%m', date) as month, AVG(nav) as avg_nav
FROM fact_nav
WHERE amfi_code = '125497'
GROUP BY month
ORDER BY month;

-- Query 3: SIP inflows YoY growth
SELECT strftime('%Y', month) as year, SUM(sip_inflow_crore) as total_sip
FROM monthly_sip_inflows
GROUP BY year;

-- Query 4: Transaction volume by state
SELECT state, COUNT(*) as transaction_count, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;

-- Query 5: Funds with expense ratio < 1%
SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;

-- Query 6: Best performing funds by 3-year return
SELECT f.scheme_name, f.fund_house, p.return_3yr_pct, p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 10;

-- Query 7: Monthly NAV volatility for each fund
SELECT amfi_code, 
       strftime('%Y-%m', date) as month,
       AVG(nav) as avg_nav,
       (MAX(nav) - MIN(nav)) / AVG(nav) as monthly_volatility
FROM fact_nav
GROUP BY amfi_code, month
HAVING COUNT(*) > 20;

-- Query 8: Investor distribution by age group and city tier
SELECT age_group, city_tier, 
       COUNT(DISTINCT investor_id) as unique_investors,
       SUM(amount_inr) as total_investment
FROM fact_transactions
GROUP BY age_group, city_tier
ORDER BY total_investment DESC;

-- Query 9: Funds with negative alpha (underperforming benchmark)
SELECT f.scheme_name, p.alpha, p.beta
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.alpha < 0
ORDER BY p.alpha;

-- Query 10: AUM growth trend for SBI Mutual Fund
SELECT date, aum_lakh_crore
FROM fact_aum
WHERE fund_house = 'SBI Mutual Fund'
ORDER BY date;