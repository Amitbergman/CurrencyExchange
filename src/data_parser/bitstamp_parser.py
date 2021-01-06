import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("\\".join(os.path.dirname(__file__).split("\\")[:-2]))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from bitcoin_arbitrage.arbitrage.public_markets._bitstamp import Bitstamp

class BitstampExchange(Bitstamp):
    def __init__(self, exchange_code):
        super().__init__("USD", exchange_code)

class BitstampParser:
    def __init__(self, coin_a, coin_b):
        market = BitstampExchange(coin_a + coin_b)
        tick = market.get_ticker()
        edge_ab_value = tick["ask"]["price"]
        edge_ba_value = 1. / tick["bid"]["price"]
        edge_ab_name = coin_a + "_" + coin_b
        edge_ba_name = coin_b + "_" + coin_a
        self.coin_a = coin_a
        self.coin_b = coin_b
        self.edges = {edge_ab_name: edge_ab_value, edge_ba_name: edge_ba_value}

if __name__ == "__main__":


    # parser = BitstampParser(coin_a="xrp", coin_b="btc")
    # print(parser.edges)

    # parser = BitstampParser(coin_a="eth", coin_b="btc")
    # print(parser.edges)

    parser = BitstampParser(coin_a="ltc", coin_b="btc")
    print(parser.edges)

    # parser = BitstampParser(coin_a="eth", coin_b="xrp")
    # print(parser.edges)