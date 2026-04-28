from src.utils.logging import setup_logging
from src.ingestion.fetcher import ETFIngester
from src.storage.database import ETFDatabase

setup_logging()

def main():
    ingester = ETFIngester(start="2018-01-01", end="2024-12-31")
    db = ETFDatabase()

    results = ingester.run()

    for ticker, df in results.items():
        db.insert_prices(df, ticker)

    print("\n--- COVERAGE REPORT ---")
    print(db.coverage_report().to_string(index=False))

if __name__ == "__main__":
    main()