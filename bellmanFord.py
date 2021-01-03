# Structure to represent a weighted
# edge in graph
class Edge:   
    def __init__(self):
        self.src = 0
        self.dest = 0
        self.weight = 0
 
# Structure to represent a directed
# and weighted graph
class Graph:
 
    def __init__(self):
         
        # V. Number of vertices, E.
        # Number of edges
        self.numberOfVertices = 0
        self.numberOfEdges = 0
         
        # Graph is represented as
        # an array of edges.
        self.edges = []
      
# Creates a new graph with V vertices
# and E edges
def createGraph(V, E):
    graph = Graph();
    graph.numberOfVertices = V;
    graph.numberOfEdges = E;
    graph.edges = [Edge() for i in range(graph.numberOfEdges)]
    return graph;
   
# Function runs Bellman-Ford algorithm
# and prints negative cycle(if present)
def NegCycleBellmanFord(graph, src):
    V = graph.numberOfVertices;
    E = graph.numberOfEdges;
    dist =[1000000 for i in range(V)]
    parent =[-1 for i in range(V)]
    dist[src] = 0;
  
    # Relax all edges |V| - 1 times.
    for i in range(1, V):
        for j in range(E):
     
            u = graph.edges[j].src;
            v = graph.edges[j].dest;
            weight = graph.edges[j].weight;
  
            if (dist[u] != 1000000 and
                dist[u] + weight < dist[v]):
             
                dist[v] = dist[u] + weight;
                parent[v] = u;
  
    # Check for negative-weight cycles
    vertexOfTheCycle = -1;    
    for i in range(E):   
        u = graph.edges[i].src;
        v = graph.edges[i].dest;
        weight = graph.edges[i].weight;
  
        if (dist[u] != 1000000 and
            dist[u] + weight < dist[v]):
              
            # Store one of the vertex of
            # the negative weight cycle
            vertexOfTheCycle = v;
            break;
          
    if (vertexOfTheCycle != -1):       
        for i in range(V):       
            vertexOfTheCycle = parent[vertexOfTheCycle];
  
        # To store the cycle vertex
        cycle = []       
        v = vertexOfTheCycle
         
        while (True):
            cycle.append(v)
            if (v == vertexOfTheCycle and len(cycle) > 1):
                break;
            v = parent[v]
  
        # Printing the negative cycle
        print("Found negative cycle, vertices:")       
        for vertex in cycle:
            print(vertex, end = " ");             
        print()   
    else:
        print("Did not find negative cycle, vertices:")       

import random
import math
if __name__=='__main__':
      
    numberOfVertices = 5;
    numberOfEdges = 5*5; 

    graph = createGraph(numberOfVertices, numberOfEdges)
  
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
                graph.edges[currentEdgeNumber].weight = math.log(random.uniform(0, 1))
            currentEdgeNumber = currentEdgeNumber+1
  
    # Function Call
    NegCycleBellmanFord(graph, 0)
