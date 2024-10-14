from exchanges.exchange import Exchange
from typing import List
import requests

COINBASE_API = "https://api.exchange.coinbase.com"

class Coinbase(Exchange):
    def __init__(self, pair, polling_interval):
        super().__init__(polling_interval)
        self.url = COINBASE_API
        self.pair = pair

    # TODO: this function returns only best ask and bid.
    def _get_orders(self) -> List[List[List[float]]]:
        response = requests.get(f"{self.url}/products/{self.pair}/book")
        book = response.json()
                
        orders = [[[0,0]],[[0,0]]]
        orders[0][0][0] = float(book["asks"][0][0]) # ask's price
        orders[0][0][1] = float(book["asks"][0][1]) # ask's quantity
            
        orders[1][0][0] = float(book["bids"][0][0]) # bid's price
        orders[1][0][1] = float(book["bids"][0][1]) # bid's quantity
                
        return orders

    def get_colors(self):
        return ["black", "springgreen"]

    def name(self):
        return "coinbase"