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