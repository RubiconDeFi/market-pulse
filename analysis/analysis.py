from exchanges.exchange import Exchange
from analysis.helpers import sma
import matplotlib.pyplot as plt
import math
import csv

SAVE_PATH = "./_plots_/"

class Analysis:
    def __init__(self, exchange_names):
        self.exchange_names = exchange_names
        self.data_set = {}

        for name in exchange_names:
            data = []
            reader = csv.DictReader(open('./_data_sets_/'+name+'.csv'))
            for r in reader:
                data.append(r)
                self.data_set[name] = data

    def midpoints_sma(self):
        for name in self.exchange_names:
            data = self.data_set[name]
            window_size = int(math.sqrt(len(data)))
            midpoints = [float(d['midpoint']) for d in data]
            
            sma_list = sma(window_size, midpoints)
            plt.plot([i for i in range(len(sma_list))],
                     [sma for sma in sma_list], label=name)

        # TODO: move the name into ~'metrics' list.
        plt.title("midpoints SMA")
        plt.legend()
        plt.savefig(SAVE_PATH+"midpoints_sma.png")
        plt.show()