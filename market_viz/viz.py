from matplotlib.animation import FuncAnimation
from exchanges.exchange import Exchange
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import time

DEFAULT_LIMIT = (0, 1)

# TODO: add "midpoint-deltas", "depth", "price-stickiness", "volatility"
class MarketVisualization:
    BOT_SCALE = 0.99
    TOP_SCALE = 1.01

    def __init__(self, exchanges: List[Exchange], comparison_type, interval=1000, limit=50):
        self.exchanges = exchanges
        self.comparison_type = comparison_type
        self.interval = interval
        self.limit = limit

        self.fig, self.ax = plt.subplots()
        self.x_data = []
        self.data_lines = {}

        
        for e in exchanges:
            self.init_lines(e)
        
        self.init_plot()

    def init_lines(self, exchange):
        colors = exchange.get_colors()
        name = exchange.name()
        
        if self.comparison_type == "prices":
            self.data_lines[name] = {
                'ask_data': [],
                'bid_data': [],
                'line_ask': self.ax.plot([], [], color=colors[0], label=f'{name}_ask')[0],
                'line_bid': self.ax.plot([], [], color=colors[1], label=f'{name}_bid')[0]
            }

        if self.comparison_type == "spreads":
            self.data_lines[name] = {
                'spread_data': [],
                'line_spread': self.ax.plot([], [], color=colors[0], label=f'{name}_spread')[0]
            }
                
        if self.comparison_type == "midpoints":
            self.data_lines[name] = {
                'midpoint_data': [],
                'line_midpoint': self.ax.plot([], [], color=colors[0], label=f'{name}_midpoint')[0]
            }

    def init_plot(self):
        self.ax.set_xlim(0, self.limit)
        self.ax.set_ylim(DEFAULT_LIMIT)

    def get_prices(self, exchange):
        return exchange.get_best_ask_bid_prices()

    def update(self, frame):
        now = time.time()
        self.x_data.append(now)
        updated_lines = []
        
        for exchange in self.exchanges:
            name = exchange.name()
            prices = self.get_prices(exchange)

            if self.comparison_type == "prices":
                ask_price, bid_price = prices
                self.data_lines[name]['ask_data'].append(ask_price)
                self.data_lines[name]['bid_data'].append(bid_price)
                self.update_line_data(name, 'ask_data', 'line_ask')
                self.update_line_data(name, 'bid_data', 'line_bid')
                updated_lines.extend([self.data_lines[name]['ask_data'],
                                     self.data_lines[name]['bid_data']])

            elif self.comparison_type == "spreads":
                spread = exchange.spread(prices)
                self.data_lines[name]['spread_data'].append(spread)
                self.update_line_data(name, 'spread_data', 'line_spread')
                updated_lines.append(self.data_lines[name]['spread_data'])

            elif self.comparison_type == "midpoints":
                midpoint = exchange.midpoint(prices)
                self.data_lines[name]['midpoint_data'].append(midpoint)
                self.update_line_data(name, 'midpoint_data', 'line_midpoint')
                updated_lines.append(self.data_lines[name]['midpoint_data'])                

        self.adjust_limits()
        
        return updated_lines

    def update_line_data(self, name, data_key, line_key):
        if len(self.data_lines[name][data_key]) > self.limit:
            self.data_lines[name][data_key].pop(0)
        self.data_lines[name][line_key].set_data(np.arange(len(self.data_lines[name][data_key])),
                                                   self.data_lines[name][data_key])
        

    def adjust_limits(self):
        if len(self.x_data) > self.limit:
            self.x_data.pop(0)

        all_data = []
        for venue_data in self.data_lines.values():
            # TODO: reuse these mfs
            for key in ['ask_data', 'bid_data', 'spread_data', 'midpoint_data']:
                if key in venue_data:
                    all_data.extend(venue_data[key])

        if all_data:
            min_value = min(all_data) * self.BOT_SCALE
            max_value = max(all_data) * self.TOP_SCALE
            self.ax.set_ylim(min_value, max_value)    

    def start(self):
        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init_plot, interval=self.interval, blit=True)
        plt.legend()
        plt.ion()
        plt.show()