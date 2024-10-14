# 🫀 market-pulse
A real-time data visualization tool designed to showcase various market metrics across different exchanges. Its purpose is to provide insights into how each exchange reacts to specific market conditions and to evaluate each exchange's behavior in relation to others.

## Quick start
```
pip install -r requirements.txt
jupyter lab
```

## Currently available visuzalition types
#### Prices (aka best ask/bid prices)
```py
v = MarketVisualization(exchanges, "prices")
v.start()
```
![ab_0](https://github.com/user-attachments/assets/22f63518-48aa-4251-add2-b42db131db20)

#### Midpoints
```py
v = MarketVisualization(exchanges, "midpoints")
v.start()
```
![ao_1](https://github.com/user-attachments/assets/58386fb8-04a7-43a4-baf5-0508638d865f)

#### Spreads
```py
v = MarketVisualization(exchanges, "spreads")
v.start()
```
![bb_2](https://github.com/user-attachments/assets/1a09d234-6b53-4e03-98dd-d29ff257c083)

## Adding new exchanges

To add a new exchange, create a class that inherits from the abstract `Exchange` class and implements the following functions:

- `get_orders`: Fetches order data (best ask, bid, etc.) from the exchange.
- `get_colors`: Defines the color scheme used for visualizing the exchange's data.
- `name`: Returns the name of the exchange.

Based on the exchange type, place the new class in one of the following directories:
- `cexes/` for centralized exchanges
- `dexes/` for decentralized exchanges
- `aggregators/` for aggregation services

An example implementation:
```py
class NewExchange(Exchange):
    def get_orders(self):
        # Returns an order-book with 1 ask:
        # @1 w size 10
        # and 1 bid:
        # @0.5 w size 20
        return [[[1,10],[0.5,20]]]

    def get_colors(self):
        return ["red", "green"]

    def name(self):
        return "NewExchange"
```
