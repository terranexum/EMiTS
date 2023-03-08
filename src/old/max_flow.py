'''
MaxFlow class in max_flow.py: This class implements the consensus-based distributed max-flow algorithm. It contains the following properties:

graph: An instance of the Graph class.
alpha: The step size for updating the flow of the single metric.
maximize_flow method: This method implements the consensus-based distributed max-flow algorithm. It initializes the flow values at each node, calculates the gradient and updates the flow of the single metric until a steady state is reached. The final values of the nodes and edges can then be outputted for visualization.

'''

class MaxFlow:
    def __init__(self, graph, alpha):
        self.graph = graph
        self.alpha = alpha
        self.maximize_flow(10)

    def maximize_flow(self, num_iterations):
        for i in range(num_iterations):
            self.graph.calculate_gradient()
            self.graph.update_flow(self.alpha)

    def get_final_values(self):
        final_node_values = []
        final_edge_values = []
        for node in self.graph.nodes.values():
            final_node_values.append({'id':int(node.id), 'name':int(node.id), 'val':float(node.flow)})

        for edge in self.graph.edges.values():
            final_edge_values.append({'source':edge.node1, 'target':edge.node2})
        
        return {'nodes':final_node_values, 'links':final_edge_values}

'''
In this implementation, the maximize_flow method implements the consensus-based distributed max-flow algorithm by looping for a specified number of iterations and for each iteration calling the calculate_gradient and update_flow methods for the graph. The get_final_values method outputs the final flow values for each node in the graph network as a dictionary, where the node id is the key and the node flow is the value.
'''