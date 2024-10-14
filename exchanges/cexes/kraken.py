from exchanges.exchange import Exchange
from typing import List
import requests

KRAKEN_API = "https://api.kraken.com/0/public"

class Kraken(Exchange):
    def __init__(self, pair, polling_interval):
        super().__init__(polling_interval)
        self.url = KRAKEN_API
        self.pair = pair

    # TODO: this function returns only best ask and bid.
    def _get_orders(self) -> List[List[List[float]]]:
        payload = {"pair": self.pair}
        response = requests.get(self.url+"/Ticker", params=payload)
        
        result = response.json().get("result", {})
        data = result[self.pair]
        
        orders = [[[0,0]],[[0,0]]]
        orders[0][0][0] = float(data["a"][0]) # ask's price
        orders[0][0][1] = float(data["a"][2]) # ask's quantity
        
        orders[1][0][0] = float(data["b"][0]) # bid's price
        orders[1][0][1] = float(data["b"][2]) # bid's quantity
            
        return orders

    def get_colors(self):
        return ["blue", "orange"]

    def name(self):
        return "kraken"