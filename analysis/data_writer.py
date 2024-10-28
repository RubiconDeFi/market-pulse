from market_viz.viz import MarketVisualization
from exchanges.exchange import Exchange
from typing import List
import threading
import time
import csv

# TODO: kinda ugly guy, but will use it for now.
class DataWriter:
    def __init__(self, market_viz: MarketVisualization, exchanges: List[Exchange], data_file, fieldnames, polling_interval):
        self.market_viz = market_viz
        self.exchanges = exchanges
        self.polling_interval = polling_interval
        self.data_file = data_file
        self.fieldnames = fieldnames

        self.stop_polling = threading.Event()
        self.polling_thread = threading.Thread(target=self._poll)

    def _poll(self):
        while not self.stop_polling.is_set():
            for e in self.exchanges:
                name = e.name()
                latest_data = self.market_viz.query_data(name)
                filename = self.data_file+name+'.csv'

                with open(filename, mode='w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(latest_data)
                                        
            time.sleep(self.polling_interval)

    def start_polling(self):
        self.polling_thread.start()

    def stop_polling(self):
        self.stop_polling.set()
        self.polling_thread.join()  