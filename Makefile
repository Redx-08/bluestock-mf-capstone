.PHONY: all clean ingest analyze report

all: ingest clean analyze report

ingest:
python3 scripts/data_ingestion.py

clean:
python3 scripts/clean_nav.py
python3 scripts/clean_performance.py
python3 scripts/clean_transactions.py

analyze:
python3 scripts/performance_analytics.py
python3 run_analysis.py

report:
python3 visualize_performance.py

validate:
python3 scripts/validate_amfi_codes.py
python3 validate_metrics.py

clean-files:
rm -f reports/fund_performance_summary.csv
rm -f reports/top_recommended_funds.csv
rm -f data/processed/*.csv
