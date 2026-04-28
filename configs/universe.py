ETF_UNIVERSE = {
    "us_equity": ["SPY", "QQQ", "IWM", "VTI", "VOO"],
    "fixed_income": ["TLT", "IEF", "SHY", "BND", "LQD"],
    "commodities": ["GLD", "SLV", "USO", "DJP", "PDBC"],
    "international": ["EFA", "EEM", "VEU", "IDEV", "VXUS"],
    "alternatives": ["VNQ", "REET", "BTAL", "CTA", "DBMF"],
}

ALL_TICKERS = [t for tickers in ETF_UNIVERSE.values() for t in tickers]