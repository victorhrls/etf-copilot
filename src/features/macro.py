import pandas as pd 
from fredapi import Fred
from configs.settings import settings
from loguru import logger


def compute_macro(start:str, end:str) -> pd.DataFrame:
        
    fred = Fred(api_key=settings.fred_api_key)
    vix = fred.get_series('VIXCLS', observation_start=start, observation_end=end)
    dgs10 = fred.get_series('DGS10', observation_start=start, observation_end=end)
    dgs2 = fred.get_series('DGS2', observation_start=start, observation_end=end)
    
    yield_slope = dgs10 - dgs2
    
    df_macro = pd.DataFrame({'yield_slope': yield_slope,
                             'vix' : vix})

    
    logger.info('Macro statements computed')

    
    return df_macro
    
    
    
    
    
    
    
    