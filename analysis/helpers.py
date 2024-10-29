from typing import List
import pandas as pd

def sma(window_size, values: List[float]):
    windows = pd.Series(values).rolling(window_size)
    return windows.mean().tolist()[window_size -1:]
    
    
    