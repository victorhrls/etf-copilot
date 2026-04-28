import yfinance as yf
import pandas as pd
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from configs.settings import settings
from configs.universe import ALL_TICKERS
from src.ingestion.schemas import validate_price_df


class ETFIngester:

    def __init__(self, start: str = "2018-01-01", end: str = "2024-12-31"):
        self.start = start
        self.end = end

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _fetch_one(self, ticker: str) -> pd.DataFrame:
        logger.info(f"Fetching {ticker}")
        df = yf.download(ticker, start=self.start, end=self.end, auto_adjust=False, progress=False)

        if df.empty:
            raise ValueError(f"Empty DataFrame returned for {ticker}")

        df.columns = df.columns.get_level_values(0)
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        })
        df["ticker"] = ticker
        df.index.name = "date"
        df = df.reset_index()
        df["date"] = df["date"].astype(str)
        return df

    def run(self) -> dict[str, pd.DataFrame]:
        results = {}
        for ticker in ALL_TICKERS:
            try:
                df = self._fetch_one(ticker)
                df = validate_price_df(df, ticker)
                results[ticker] = df
                logger.info(f"{ticker} — {len(df)} rows validated")
            except Exception as e:
                logger.error(f"{ticker} failed after retries: {e}")
        return results