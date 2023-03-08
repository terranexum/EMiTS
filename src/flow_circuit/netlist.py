# This code defines a Graph class that represents a graph network, with nodes numbered from 0 to num_nodes-1. 
# The add_edge method is used to add edges to the graph, where capacity represents the capacity of the edge and resistance represents the "resistance" of the edge.

from heapq import heappop, heappush
from math import inf

class Graph:
    def __init__(self, num_nodes):
        self.adj_list = [[] for _ in range(num_nodes)]
    
    def add_edge(self, node1, node2, capacity, resistance):
        self.adj_list[node1].append((node2, capacity, resistance))
        self.adj_list[node2].append((node1, capacity, resistance))

def dijkstra(graph, start, end):
    # Initialize distances and visited list
    distances = [inf] * len(graph.adj_list)
    visited = [False] * len(graph.adj_list)
    distances[start] = 0
    
    # Initialize heap with starting node and distance
    heap = [(0, start)]
    
    while heap:
        # Pop the node with the smallest distance
        curr_dist, curr_node = heappop(heap)
        
        # If we've reached the end node, return the distance
        if curr_node == end:
            return distances[end]
        
        # If we've already visited this node, continue
        if visited[curr_node]:
            continue
        
        # Mark node as visited
        visited[curr_node] = True
        
        # Update distances for neighbors
        for neighbor, capacity, resistance in graph.adj_list[curr_node]:
            if not visited[neighbor]:
                new_distance = curr_dist + resistance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heappush(heap, (new_distance, neighbor))
    
    # If we can't reach the end node, return infinity
    return inf
