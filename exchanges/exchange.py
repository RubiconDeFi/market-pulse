from abc import ABC, abstractmethod
from typing import List
import threading
import time

class Exchange(ABC):
    def __init__(self, polling_interval):
        self.shared_book = None
        self.polling_interval = polling_interval

        self.stop_polling = threading.Event()
        self.polling_thread = threading.Thread(target=self._poll)

    def _poll(self, *args):
        while not self.stop_polling.is_set():
            book = self._get_orders()
            if book:
                self.shared_book = book
            time.sleep(self.polling_interval)

    def start_polling(self):
        self.polling_thread.start()

    def stop_polling(self):
        self.stop_polling.set()
        self.polling_thread.join()    

    @abstractmethod
    def _get_orders(self) -> List[List[List[float]]]:
        """
        Returns an order-book object with sorted sides:
        - [ [ [ask_0],...,[ask_n] ], [ [bid_0],...,[bid_n] ] ]
        where each {ask_i, bid_i} are:
        - [price, quantity]
        Sorting of sides should be done on the implementation side.
        """
        ...

    @abstractmethod
    def get_colors(self):
        ...

    @abstractmethod
    def name(self):
        ...    

    def get_current_midpoint(self) -> float:
        prices = self.get_best_ask_bid_prices()
        return self.midpoint(prices)

    def get_current_spread(self) -> float:
        prices = self.get_best_ask_bid_prices()
        return self.spread(prices)

    def get_best_ask_bid(self) -> List[List[float]]:
        return self.get_best_orders_from_book()

    def get_best_ask_bid_prices(self) -> List[float]:
        best = self.get_best_orders_from_book()
        return [best[0][0], best[1][0]]

    # Best prices are:
    # [ask_price, bid_price]
    def midpoint(self, best_prices):        
        return (best_prices[0]+best_prices[1]) / 2.0

    def spread(self, best_prices):
        return (best_prices[0]-best_prices[1])

    def get_best_orders_from_book(self):
        best_orders = [[0,0],[0,0]]
        book = self.shared_book
        
        if not book:
            return best_orders
            
        if len(book[0]) != 0:
                best_orders[0] = book[0][0]
    
        if len(book[1]) != 0:
                best_orders[1] = book[1][0]
    
        return best_orders