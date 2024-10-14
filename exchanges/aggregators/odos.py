from exchanges.exchange import Exchange
from typing import List
import requests

ODOS_SOR_URL = "https://api.odos.xyz/sor/quote/v2"

class Odos(Exchange):
    def __init__(self, chain_id, base, base_dec, quote, quote_dec, base_amt, quote_amt, polling_interval):
        super().__init__(polling_interval)
        self.chain_id = chain_id
        self.url = ODOS_SOR_URL
        self.base = base
        self.base_dec = base_dec
        self.quote = quote
        self.quote_dec = quote_dec
        self.base_amt = base_amt
        self.quote_amt = quote_amt

    def _get_orders(self) -> List[List[List[float]]]:
        ask = self.orders(self.chain_id, self.base, self.quote, 
                           self.base_amt, float(self.base_dec), 
                           float(self.quote_dec), False)
        bid = self.orders(self.chain_id, self.quote, self.base,
                           self.quote_amt, float(self.quote_dec), 
                           float(self.base_dec), True)
    
        return [[ask], [bid]]

    def get_colors(self):
        return ["slategray", "gold"]

    def name(self):
        return "odos"

    # TODO: plural "orders" isn't really accurate.
    def orders(self, chain_id, base, quote, base_amt, base_dec, quote_dec, inverse):
        quote_request_body = {
            "chainId": int(chain_id),
            "inputTokens": [
                {
                    "tokenAddress": base,
                    "amount": base_amt
                }
            ],
            "outputTokens": [
                {
                    "tokenAddress": quote,
                    "proportion": 1
                }             
            ],
            "slippageLimitPercent": 0.1, # 0.3% fair enough?
            "userAddr": "0x4200000000000000000000000000000000000006",
            "disableRFQs": False,
        }

        response = requests.post(self.url, headers={"Content-Type": "application/json"}, json=quote_request_body)
        result = response.json()
            
        order = [0,0]
        in_amt = result["inAmounts"][0]
        out_amt = result["outAmounts"][0]
        
        x = float(out_amt) / 10**quote_dec if not(inverse) else float(in_amt) / 10**base_dec
        y = float(in_amt) / 10**base_dec if not(inverse) else float(out_amt) / 10**quote_dec
                
        order[0] = x/y
        order[1] = in_amt if not(inverse) else out_amt
                
        return order
