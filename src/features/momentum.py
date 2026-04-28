import pandas as pd
import numpy as np
from loguru import logger




def compute_momentum(df : pd.DataFrame) -> pd.DataFrame:    
    df['mom_1m'] = np.log(df['adj_close']/df['adj_close'].shift(21))
    df['mom_3m'] = np.log(df['adj_close']/df['adj_close'].shift(63))
    df['mom_12m'] = np.log(df['adj_close']/df['adj_close'].shift(252))
    logger.info('Momentum features computed')
    
    return df

