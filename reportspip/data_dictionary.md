# Bluestock MF Capstone – Data Dictionary

## 01_fund_master.csv (40 rows)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Unique scheme identifier (e.g., 119551 = SBI Bluechip) |
| fund_house | TEXT | AMC name (SBI, HDFC, ICICI, etc.) |
| scheme_name | TEXT | Full fund name from AMFI |
| category | TEXT | Equity / Debt / Hybrid |
| sub_category | TEXT | Large Cap / Mid Cap / Liquid |
| plan | TEXT | Regular or Direct |
| launch_date | DATE | Fund inception date |
| benchmark | TEXT | Benchmark index name |
| expense_ratio_pct | REAL | Annual expense ratio (%) |
| exit_load_pct | REAL | Exit load percentage |
| fund_manager | TEXT | Primary fund manager name |
| risk_category | TEXT | Low / Moderate / High / Very High |
| sebi_category_code | TEXT | EC01=LargeCap, EC03=SmallCap, DC01=Liquid |

## 02_nav_history.csv (46,000 rows)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Links to fund_master |
| date | DATE | Trading day (no weekends/holidays) |
| nav | REAL | Net Asset Value in ₹ |

*Continue for all 10 files...*
# Bluestock MF Capstone - Data Dictionary

## dim_fund (40 rows)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Primary key, 6-digit AMFI scheme code |
| fund_house | TEXT | Asset management company name |
| scheme_name | TEXT | Full mutual fund scheme name |
| category | TEXT | Equity or Debt |
| sub_category | TEXT | Large Cap, Mid Cap, Small Cap, Liquid, etc. |
| plan | TEXT | Regular or Direct |
| launch_date | DATE | Fund inception date |
| benchmark | TEXT | Benchmark index name |
| expense_ratio_pct | REAL | Annual expense ratio (0.1% to 2.5%) |
| exit_load_pct | REAL | Exit load percentage |
| risk_category | TEXT | Low, Moderate, High, Very High |

## fact_nav (46,000+ rows after forward-fill)
| Column | Type | Description |
|--------|------|-------------|
| nav_id | INTEGER | Surrogate primary key |
| amfi_code | TEXT | Foreign key to dim_fund |
| date | DATE | Trading day (includes forward-filled weekends) |
| nav | REAL | Net Asset Value in rupees |
| daily_return | REAL | (nav_t / nav_t-1) - 1 |

## fact_transactions (32,778 rows)
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | INTEGER | Surrogate primary key |
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date of transaction |
| amfi_code | TEXT | Foreign key to dim_fund |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption |
| amount_inr | INTEGER | Transaction amount in rupees |
| state | TEXT | Indian state |
| city_tier | TEXT | T30 (Top 30 cities) or B30 (Beyond Top 30) |
| age_group | TEXT | 18-25, 26-35, 36-45, 46-55, 56+ |
| kyc_status | TEXT | Verified or Pending |

## fact_performance (40 rows)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Primary key, foreign key to dim_fund |
| return_3yr_pct | REAL | 3-year CAGR percentage |
| sharpe_ratio | REAL | Risk-adjusted return (>1 is good) |
| alpha | REAL | Excess return over benchmark |
| beta | REAL | Market sensitivity (1.0 = same as market) |
| max_drawdown_pct | REAL | Worst peak-to-trough decline |

## fact_aum (90 rows)
| Column | Type | Description |
|--------|------|-------------|
| aum_id | INTEGER | Surrogate primary key |
| date | DATE | Quarter-end date |
| fund_house | TEXT | AMC name |
| aum_lakh_crore | REAL | Assets under management in lakh crore |
| aum_crore | INTEGER | Assets under management in crore |

## Source References
- AMFI India: NAV, AUM, folio data
- mfapi.in: Historical NAV API
- Simulated: Investor transactions (based on real demographic distributions)