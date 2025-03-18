from exchanges.exchange import Exchange
from analysis.helpers import SMA, FMPs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import csv

SAVE_PATH = "./_plots_/"

class Analysis:
    def __init__(self, exchange_names, dir):
        self.exchange_names = exchange_names
        self.data_set = {}

        for name in exchange_names:
            data = []
            reader = csv.DictReader(open("./_data_sets_"+dir+name+".csv"))
            for r in reader:
                data.append(r)                
                self.data_set[name] = data

    def spreads_sma(self, size_shift):
        return self._sma("spread", size_shift)
        
    def asks_sma(self, size_shift):
        return self._sma("ask_price", size_shift)
        
    def bids_sma(self, size_shift):
        return self._sma("bid_price", size_shift)        

    def midpoints_sma(self, size_shift):
        return self._sma("midpoint", size_shift)

    def _sma(self, metric, size_shift):
        means = []
        for name in self.exchange_names:
            data = self.data_set[name]
            window_size = self._window_size(data) + size_shift
            values = [float(d[metric]) for d in data]

            means.append(np.mean(values))
            sma_list = SMA(window_size, values)
            plt.plot([i for i in range(len(sma_list))],
                     [sma for sma in sma_list], label=name)

        # TODO: move the name into ~'metrics' list.
        plt.title(metric+" SMA")
        plt.legend()
        plt.style.use("seaborn-v0_8-deep")        
        plt.savefig(SAVE_PATH+"_"+metric+"_sma.png")
        plt.show()
        return means
        
    def volatility_reaction_lag(self, exchange_name):
        fmps = FMPs(self._get_midpoints())
        returns = pd.Series(fmps).pct_change()
        volatility = returns.rolling(self._window_size(fmps)).std()
            
        vol_spikes = volatility > (volatility.mean() + 2 * volatility.std())
        lags = []

        for i in vol_spikes[vol_spikes].index:
            spike_time = i
            fmp_at_spike = vol_spikes[spike_time]

            midpoints = self._midpoints(exchange_name)
            lag_time = None
            
            # Find the first point where price adjusts by threshold after spike.
            for future_time in midpoints[spike_time]:
                price_change = abs((midpoints[future_time] - fmp_price_at_spike) / fmp_price_at_spike)
                if price_change >= 0.01:  # 1% price adjustment as example threshold
                    lag_time = (future_time - spike_time).total_seconds()
                    break
        
            if lag_time is not None:
                lags[exchange].append(lag_time)

        print(lags)

        #plt.plot([i for i in range(len(self.data_set[exchange_name]))], volatility)
        #plt.show()

    def _get_midpoints(self):    
        return [self._midpoints(n) for n in self.exchange_names]

    def _midpoints(self, name):
        return [float(d["midpoint"]) for d in self.data_set[name]]

    @staticmethod
    def _window_size(l):
        return int(math.sqrt(len(l)))