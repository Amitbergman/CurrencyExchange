import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("\\".join(os.path.dirname(__file__).split("\\")[:-2]))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from src.search_algorithm.bellmanFord import NegCycleBellmanFord, createGraph
from forex_python.converter import CurrencyRates
import math
import random
import numpy as np
c = CurrencyRates()

if __name__ == "__main__":

    # TODO make concurrent parser of the exchange rates, to construct the exchange_matrix in a parallelized manner
    # TODO try to use an algorithm which looks for multiple global solutions, no just the first one
    # TODO add the expected fees involved with transactions - perhaps 10 dollars fixed price per transaction, for a 1000 dollars transactoin
    # TODO try to get historical data to see how long such oppertunities stay open. (perhaps train a model to predict this)
    # TODO try to get information from a forex company, to see how long their transactions take - to see if they are fast enough to cash in on oppertunities that open up
    
    # get all available currencies
    c = CurrencyRates()
    all_coins = list(c.get_rates("USD").keys()) + ["USD"]
    random.shuffle(all_coins)

    # initialize the relaven coins 
    numberOfVertices = 4
    numberOfEdges = numberOfVertices**2
    coins = all_coins[:numberOfVertices]
    exchange_matrix = np.zeros((numberOfVertices, numberOfVertices))

    # create graph and currency rates parser
    graph = createGraph(numberOfVertices, numberOfEdges)
    c = CurrencyRates()

    # Build a full graph - with inner edges of weight 1 and other edges with a (log of ) a random conversion ratio
    currentEdgeNumber = 0
    for i in range (numberOfVertices):
        for j in range(numberOfVertices):
            graph.edges[currentEdgeNumber].src = i
            graph.edges[currentEdgeNumber].dest = j
            if (i == j):
                #You can take one dollar and convert it to 1 dollar
                graph.edges[currentEdgeNumber].weight = 1
            else:
                # currncy1, currncy2 = coins[i]
                exchange_rate = c.get_rates(coins[i])[coins[j]]
                exchange_matrix[i,j] = exchange_rate
                graph.edges[currentEdgeNumber].weight = math.log(exchange_rate)
                print(f"exchange_rate {coins[i]} -> {coins[j]}: {exchange_rate}")

            currentEdgeNumber = currentEdgeNumber+1

    # Function Call
    cycle = NegCycleBellmanFord(graph, 0)

    # get the relavent exchange rates 
    exchange_rate_values, exchange_rate_names = [], []
    for i in range(len(cycle) - 1):
        exchange_rate_values.append(exchange_matrix[cycle[i], cycle[i+1]])
        exchange_rate_names.append(coins[cycle[i]] + "_" + coins[cycle[i+1]])
    margin_without_fees = np.product(exchange_rate_values)

    print(f"exchange_rate_names = {exchange_rate_names}, margin_without_fees = {margin_without_fees}")
