'''
Graph class in graph.py: This class represents the graph network. It would contain the following properties:

nodes: A list of nodes in the graph network.
edges: A list of edges in the graph network.
calculate_gradient method: This method calls the calculate_gradient method for each node in the graph network.
update_flow method: This method calls the update_flow method for each node in the graph network.
'''
import csv
from node import Node
from edge import Edge

class Graph:
    def __init__(self, src_path):
        self.nodes = {}
        self.edges = {}
        self.src_path = src_path
        self.load_csv()

    def load_csv(self):
        nodes = {}
        edges = {}
        id = 0
        with open(self.src_path, 'r') as file:
            reader = csv.reader(file)
            next(reader) # skip header row
            for row in reader:
                flow = row[4]
                neighbors = []
                node = Node(id, flow, neighbors)
                #print('node', node.id, node.flow)
                nodes[id] = node
                id += 1

        orig_edges = [Edge(0, 0, 1, 10), Edge(1, 1, 2, 20), Edge(2, 2, 3, 30),
                Edge(3, 3, 4, 40), Edge(4, 4, 5, 50), Edge(5, 5, 6, 60),
                Edge(6, 6, 7, 70), Edge(7, 7, 8, 80), Edge(8, 8, 9, 90),
                Edge(9, 9, 0, 100)]
        
        for e in orig_edges:
            node1 = nodes[e.node1]
            node2 = nodes[e.node2]
            if node2 not in node1.neighbors:
                node1.neighbors.append(node2)
            if node1 not in node2.neighbors:
                node2.neighbors.append(node1)
            flow = float(node1.flow) - float(node2.flow)
            edge = Edge(e.edge_id, e.node1, e.node2, flow)
            #print('edge', edge.edge_id, edge.node1, edge.node2, edge.flow)
            edges[e.edge_id] = edge

        self.nodes = nodes
        self.edges = edges

    def calculate_gradient(self):
        for node in self.nodes.values():
            node.calculate_gradient()

    def update_flow(self, step_size):
        for node in self.nodes.values():
            node.update_flow(node.calculate_gradient(), step_size)

'''
In this implementation, the calculate_gradient method calculates the gradient of the flow for all nodes in the graph network by calling the calculate_gradient method for each node. The update_flow method then updates the flow for all nodes in the graph network by calling the update_flow method for each node and passing in its calculated gradient and the step size.
'''