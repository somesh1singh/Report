import pandas as pd
import numpy as np
from stock_report_agent import StockReportAgent


def make_price_df(days=300):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq='B')
    price = np.linspace(100, 150, len(dates)) + np.random.normal(scale=1.0, size=len(dates))
    high = price + np.random.uniform(0.1, 1.0, size=len(dates))
    low = price - np.random.uniform(0.1, 1.0, size=len(dates))
    open_ = price + np.random.normal(scale=0.5, size=len(dates))
    volume = np.random.randint(100000, 500000, size=len(dates))
    df = pd.DataFrame({'Open': open_, 'High': high, 'Low': low, 'Close': price, 'Volume': volume}, index=dates)
    return df


def test_calculate_technicals_basic():
    df = make_price_df(300)
    agent = StockReportAgent(output_dir="tmp")
    tech = agent._calculate_technicals(df)
    # sma and ema dicts should contain integer keys like 20 and 50
    assert 'sma' in tech and 20 in tech['sma']
    assert 'ema' in tech and 20 in tech['ema']
    # rsi should be a pandas Series and not contain inf
    assert 'rsi' in tech
    assert not np.isinf(tech['rsi'].replace([np.inf, -np.inf], np.nan)).any()
    # mfi should be present and finite or NaN (no inf)
    assert 'mfi' in tech
    assert not np.isinf(tech['mfi'].replace([np.inf, -np.inf], np.nan)).any()


def test_mfi_with_zero_volume():
    df = make_price_df(50)
    df['Volume'] = 0
    agent = StockReportAgent(output_dir="tmp")
    tech = agent._calculate_technicals(df)
    # with zero volume, mfi should not produce infinities but be NaN or series of NaNs
    mfi = tech.get('mfi')
    assert mfi is not None
    assert mfi.isna().all() or not np.isinf(mfi.replace([np.inf, -np.inf], np.nan)).any()
