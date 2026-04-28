import pandas as pd
from src.storage.database import ETFDatabase
from src.features.momentum import compute_momentum
from src.features.volatility import compute_volatility
from src.features.beta import compute_beta
from src.features.macro import compute_macro
from loguru import logger
from configs.settings import settings


def run_pipeline() -> pd.DataFrame:
    db = ETFDatabase()  # read all 25 etfs from db
    # all data
    all_prices = db.query('SELECT * FROM raw_prices')
    
    # Spy for S&P500
    spy_data = db.query("SELECT * FROM raw_prices Where ticker = 'SPY'")
    
    # Macro
    macro_data = compute_macro(start="2018-01-01", end="2024-12-31")
    macro_data.index = pd.to_datetime(macro_data.index)
    
    results = []
    for ticker in all_prices['ticker'].unique():
        
        etf_df = all_prices[all_prices['ticker'] == ticker].copy()
        etf_df = etf_df.sort_values('date').reset_index(drop=True)

        # calculate features
        
        etf_df = compute_momentum(etf_df)     # adds mom_1m, mom_3m, mom_12m
        etf_df = compute_volatility(etf_df) # adds realized_vol , vol_of_vol
        etf_df = compute_beta(etf_df,spy_data)    # adds beta
        
        
        # left join and then append
        
        etf_df['date'] = pd.to_datetime(etf_df['date'])
        etf_df = etf_df.merge(macro_data, left_on='date', right_index=True, how='left')

        results.append(etf_df)
        logger.info(f"{ticker} — features computed")

    df_pipeline = pd.concat(results, ignore_index=True)
    
    df_pipeline.to_parquet("data/features/features_v1.parquet", index=False)

    logger.info(f"Pipeline complete — shape: {df_pipeline.shape}")
    
    
    return df_pipeline
