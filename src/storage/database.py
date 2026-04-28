import duckdb
import pandas as pd
from loguru import logger
from configs.settings import settings


class ETFDatabase:

    def __init__(self, db_path: str = "data/etf_copilot.duckdb"):
        self.conn = duckdb.connect(db_path)
        self._create_tables()
        logger.info(f"Database connected: {db_path}")

    def _create_tables(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_prices (
                ticker    VARCHAR,
                date      DATE,
                open      DOUBLE,
                high      DOUBLE,
                low       DOUBLE,
                close     DOUBLE,
                adj_close DOUBLE,
                volume    BIGINT,
                PRIMARY KEY (ticker, date)
            )
        """)

    def insert_prices(self, df: pd.DataFrame, ticker: str) -> None:
        self.conn.execute("""
        INSERT OR REPLACE INTO raw_prices
        SELECT ticker, date, open, high, low, close, adj_close, volume
        FROM df
    """)
        logger.info(f"{ticker} — stored in DuckDB")

    def query(self, sql: str) -> pd.DataFrame:
        return self.conn.execute(sql).df()

    def coverage_report(self) -> pd.DataFrame:
        return self.query("""
            SELECT
                ticker,
                COUNT(*)        AS trading_days,
                MIN(date)       AS first_date,
                MAX(date)       AS last_date
            FROM raw_prices
            GROUP BY ticker
            ORDER BY ticker
        """)