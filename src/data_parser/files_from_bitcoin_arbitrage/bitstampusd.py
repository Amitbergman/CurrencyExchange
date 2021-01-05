import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("\\".join(os.path.dirname(__file__).split("\\")[:-3]))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from bitcoin_arbitrage.arbitrage.public_markets._bitstamp import Bitstamp


# class BitstampUSD(Bitstamp):
#     def __init__(self):
#         super().__init__("USD", "btcusd")

class BitstampExchange(Bitstamp):
    def __init__(self, exchange_code):
        super().__init__("USD", exchange_code)


if __name__ == "__main__":
    market = BitstampExchange(exchange_code="btcusd")
    market.update_depth()
    print(market.get_ticker())
