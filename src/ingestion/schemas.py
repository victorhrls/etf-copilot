from pydantic import BaseModel, field_validator
import pandas as pd


class ETFPriceRow(BaseModel):
    ticker: str
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    # runs on each of these fields after the type check passes
    # if any price is zero or negative, it raises an error 
    # catches data corruption
    @field_validator("adj_close", "open", "high", "low", "close") 
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"price must be positive, got {v}")
        return v



    # yfinance return a panda DataFrame of hundreds of rows at once
def validate_price_df(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    validated_rows = []

    for row in df.to_dict(orient="records"):
        try:
            ETFPriceRow(**row)          # validate each row
            validated_rows.append(row)  # if valid keep it 
        except Exception as e:
            from loguru import logger
            logger.warning(f"{ticker} — invalid row skipped: {e}") # invalid log and skip

    return pd.DataFrame(validated_rows)