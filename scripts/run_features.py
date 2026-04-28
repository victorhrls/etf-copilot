from src.utils.logging import setup_logging
from src.features.pipeline import run_pipeline


setup_logging()

if __name__ == "__main__":
    df = run_pipeline()
    print(df[['ticker', 'date', 'mom_1m', 'realized_vol', 'beta', 'vix', 'yield_slope']].tail(10))
