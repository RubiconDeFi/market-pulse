from exchanges.exchange import Exchange
from typing import List
import requests

MARKET_SPLIT = "_"

class RubiconRFQ(Exchange):
    def __init__(self, url, chain_id, base, quote, tag, auth_key, no_fee, polling_interval):
        super().__init__(polling_interval)        
        self.url = url
        self.chain_id = chain_id
        self.base = base
        self.quote = quote
        self.tag = tag
        self.auth_key = auth_key
        self.no_fee = no_fee
    
    ############## Exchange implementation ##############
    
    def _get_orders(self) -> List[List[List[float]]]:
        market = self.get_market()

        if market != None:
            return [market["asks"], market["bids"]]

    def get_colors(self) -> List[str]:
        return ["red", "green"]

    def name(self) -> str:
        return "rubicon_rfq"

    ############## Helpers ##############

    def get_market(self):
        markets = self.markets()
        market_id = self.to_market_id(self.base, self.quote)
        opposite_market_id = self.to_opposite_market_id(market_id)
    
        if market_id in markets:
            m = markets[market_id]
            self.side_to_float(m["asks"], False)
            self.side_to_float(m["bids"], False)          
            
            return m
        elif opposite_market_id in markets:
            m = markets[opposite_market_id]
            self.inverse_market(m)
                
            return m
        else:
            return None

    def markets(self):
        payload = {"chainId": self.chain_id, "tag": self.tag, "noFee": self.no_fee}
        response = requests.get(self.url+"/markets", params=payload, headers={"x-api-key": self.auth_key})
        result = response.json()            
        markets = result.get("markets", {})
        return {key.lower(): value for key, value in markets.items()}

    def inverse_market(self, market):
        self.side_to_float(market["asks"], True)
        self.side_to_float(market["bids"], True)
        asks = market["asks"]
        market["asks"] = market["bids"]
        market["bids"] = asks    

    @staticmethod
    def to_opposite_market_id(market_id):
        tokens = market_id.split(MARKET_SPLIT)
        return (tokens[1]+MARKET_SPLIT+tokens[0]).lower()

    @staticmethod
    def to_market_id(base,quote):
        return (base+MARKET_SPLIT+quote).lower()

    @staticmethod    
    def side_to_float(side, inverse):    
        p = 0.0
        q = 0.0    
        
        for i in range(len(side)):
                if inverse:
                    p = 1.0 / float(side[i][0])
                    q = float(side[i][0]) * float(side[i][1])
                else:
                    p = float(side[i][0])
                    q = float(side[i][1])           
        
                side[i][0] = p
                side[i][1] = q