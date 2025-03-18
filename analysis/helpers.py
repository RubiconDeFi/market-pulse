from typing import List
import pandas as pd
import numpy as np

def SMA(window_size, values: List[float]):
    windows = pd.Series(values).rolling(window_size)
    return windows.mean().tolist()[window_size -1:]

def AVG(values: List[float]):
    return np.average(values)

# TODO: ugly stuff.
def FMPs(prices: List[List[float]]):
    """
    Produces a list of Fair Market Prices,
    where each FMP is an average price
    of provided set of prices.
    """
    fmp_series = {}
    for p in prices:
        for i, price in enumerate(p):
            fmp_series.setdefault(i, []).append(price)
            
    return [float(AVG(prices)) for prices in fmp_series.values()]
    