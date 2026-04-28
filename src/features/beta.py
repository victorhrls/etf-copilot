import pandas as pd
import numpy as np
from loguru import logger



def compute_beta(df: pd.DataFrame, df_spy: pd.DataFrame) -> pd.DataFrame:
    
   daily_etf_return = np.log(df['adj_close'] / df['adj_close'].shift(1))
   daily_spy_return = np.log(df_spy['adj_close'] / df_spy['adj_close'].shift(1))
   
   # Rolling covariance
   
   rolling_cov = daily_etf_return.rolling(63).cov(daily_spy_return)
   spy_var = daily_spy_return.rolling(63).var()
   
   beta = rolling_cov/spy_var
   
   df['beta'] = beta
   logger.info("Beta features computed")

   
   return df