# Flask code in app.py

from flask import Flask, jsonify, render_template
from node import Node
from edge import Edge
from graph import Graph
from max_flow import MaxFlow

app = Flask(__name__)

json_data = []

# Example edge definition
edges = [Edge(0, 0, 1, 10), Edge(1, 1, 2, 20), Edge(2, 2, 3, 30),
         Edge(3, 3, 4, 40), Edge(4, 4, 5, 50), Edge(5, 5, 6, 60),
         Edge(6, 6, 7, 70), Edge(7, 7, 8, 80), Edge(8, 8, 9, 90),
         Edge(9, 9, 0, 100)]


@app.route("/data", methods=["GET"])
def get_data():
    graph = Graph('static/EMiTS_10.csv')   
    alpha = 1 #step size for the update of the EMiTS metric
    netflow = MaxFlow(graph, alpha)
    final_values = netflow.get_final_values()
    json_data = jsonify(final_values)
    return json_data

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
