from exchanges.exchange import Exchange
from typing import List
import requests

GRAPH_URL = "https://gateway.thegraph.com/api/"
RESOLUTION = 96 # FixedPoint96.RESOLUTION

class UniswapV3(Exchange):    
    UNIV3_SUBGRAPHS = {"10": "/subgraphs/id/Cghf4LfVqPiFw6fp6Y5X5Ubc8UpmUhSfJL82zwiBFLaj", 
                       "8453": "/subgraphs/id/43Hwfi3dJSoGpyas9VwNoDAv55yjgGrPpNSmbQZArzMG", 
                       "42161": "/subgraphs/id/FbCGRftH4a3yZugY7TnbYgPJVEv2LvMT6oF1fxPe9aJM"}
    
    def __init__(self, chain_id, base_symbol, quote_symbol, pool_address, graph_key, polling_interval):
        super().__init__(polling_interval)        
        self.chain_id = chain_id
        self.base_symbol = base_symbol
        self.quote_symbol = quote_symbol
        self.pool_address = pool_address
        self.graph_key = graph_key
    
    ############## Exchange implementation ##############
    
    def _get_orders(self) -> List[List[List[float]]]:
        ask_price, bid_price = self.get_prices()
        return [[[ask_price, 0]],[[bid_price, 0]]]
    
    def get_colors(self) -> List[str]:
        return ["pink", "purple"]

    def name(self) -> str:
        return "univ3"

    ############## Helpers ##############

    def get_prices(self):
        query = """
        {
          pool(id: "%s") {
            sqrtPrice
            liquidity
            token0 {
              symbol
              decimals
            }
            token1 {
              symbol
              decimals
            }
          }
        }
        """ % self.pool_address
        response = requests.post(GRAPH_URL+self.graph_key+self.UNIV3_SUBGRAPHS[self.chain_id], json={"query": query})
        data = response.json()
        return self.prices(data["data"]["pool"])

    def prices(self, pool_data):
        sqrt_price = int(pool_data["sqrtPrice"])
        liquidity = int(pool_data["liquidity"])
        sym0 = pool_data["token0"]["symbol"]
        sym1 = pool_data["token1"]["symbol"]
        decimals0 = int(pool_data["token0"]["decimals"])
        decimals1 = int(pool_data["token1"]["decimals"])

        p = (sqrt_price / 2**96)**2
        price = p * 10**abs(decimals1 - decimals0)

        if sym0 == self.quote_symbol:            
            price = 1/price

        return float(price), float(price)