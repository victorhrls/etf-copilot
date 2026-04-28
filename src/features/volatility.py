import pandas as pd
import numpy as np
from loguru import logger



def compute_volatility(df: pd.DataFrame) -> pd.DataFrame:
    daily_log_return = np.log(df['adj_close'] / df['adj_close'].shift(1))
    df['realized_vol']= daily_log_return.rolling(21).std()
    df['vol_of_vol']   = df['realized_vol'].rolling(63).std()
    logger.info('Volatility features computed')
    
    return df
