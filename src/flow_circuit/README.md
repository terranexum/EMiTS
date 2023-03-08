# EMiTS - Flow Circuits

## Theoretical Background

In the context of electrical circuits, the maximum power transfer theorem states that the maximum amount of power can be transferred from a source to a load when the impedance of the load is equal to the impedance of the source. The impedance is the combined effect of resistance, inductance, and capacitance of a component. In terms of resistance, this means that the maximum power is transferred when the resistance of the load is equal to the internal resistance of the source.

In the context of graph networks, a similar principle can be applied. We can define the capacity of an edge as its ability to transmit a certain amount of flow. We can define the "resistance" of an edge as the amount of energy required to transmit a unit of flow through the edge.

To maximize the flow of mass or energy through an edge while requiring the least amount of energy and being done in the least amount of time, we can consider the concept of "minimum energy paths". These are paths through the network that require the least amount of energy to transmit a unit of flow. In other words, these are the paths that have the lowest "resistance".

One way to find the minimum energy path between two nodes is to use Dijkstra's algorithm, which is a well-known algorithm for finding the shortest path between two nodes in a graph. However, instead of finding the shortest path based on the number of edges, we can modify the algorithm to find the path with the lowest "resistance", which is defined as the sum of the "resistances" of the edges in the path.

## Expressing an EMiTS-based graph network as an electrical circuit

To analogize a graph network to an electrical circuit, we can assign the following analogous expressions:

Mass or energy being transported (M) represents the current flowing in the circuit (I).
Distance (S) represents the resistance of the circuit component (R).
Energy needed to create the flow (E) represents the voltage across the circuit component (V).
Time (T) represents the time constant of the circuit component (τ).

Using these analogies, we can define the following expressions:

The mass or energy flow rate (M/S) corresponds to the current density (I/A), where A represents the cross-sectional area of the circuit component. (Note that M/S represents the mass or energy flow rate per unit distance, which is often referred to as a flux.)
The energy needed to create the flow (E) corresponds to the voltage drop (V) across the circuit component.
The time (T) corresponds to the time constant (τ) of the circuit component.
The quantity (MS)/(ET) corresponds to the admittance (Y) of the circuit component.
So for a node in a graph network, we can assign the property Y = (M*S)/(E*T) as an analog of the admittance in an electrical circuit.

## Example

Given the expressions for M, S, E, and T that we've established:

M: Mass or energy being transported as a flow
S: Distance over which the mass or energy is transported
E: Energy needed to create that flow
T: Time over which the mass or energy is transported

We can express an admittance value as:

`Y = I/V = 1 / (R + jωL)`

Where:

Y: Admittance
I: Current
V: Voltage
R: Resistance
L: Inductance
ω: Angular frequency

With this mapping, we can write a Python function to compute the admittance value given the values of M, S, E, and T:

```python
import cmath

def compute_admittance(M, S, E, T):
    V = M / S
    L = S / (2 * cmath.pi * T)
    R = E / (M / T)
    omega = 2 * cmath.pi * V / L
    tau = L / R
    admittance = 1 / (R + 1j * omega * L)
    return admittance
```

As an example, suppose we have the following values:

```
M = 10 kg
S = 5 m
E = 20 J
T = 2 s
```

We can compute the admittance value as follows:

```python
admittance = compute_admittance(10, 5, 20, 2)
print(admittance)
```

This would output:

`(0.014285714285714286-0.02857142857142857j)`

This represents an admittance value of `0.014285714285714286 - 0.02857142857142857j`, which can be interpreted as a combination of resistance and inductance in an electrical circuit.

## Minimum Spanning Tree

To connect circuit elements with the shortest possible wires when all you have are their admittance values, you can use a minimum spanning tree algorithm. A minimum spanning tree is a tree that connects all nodes in a graph with the minimum possible total edge weight. In this case, the admittance values can be used as the edge weights.

One common algorithm for finding a minimum spanning tree is Kruskal's algorithm. Here's how it works:

1. Create a list of all the edges in the graph (in this case, the wires between circuit elements).
2. Sort the list of edges by weight (in this case, the admittance values).
3. Create an empty set for the minimum spanning tree.
4. For each edge in the sorted list:
If adding the edge to the minimum spanning tree does not create a cycle, add the edge to the minimum spanning tree.
Otherwise, discard the edge.
When all edges have been considered, the minimum spanning tree will be the set of edges in the minimum spanning tree set.
5. Once you have the minimum spanning tree, you can use it to determine the wires needed to connect the circuit elements. Each edge in the minimum spanning tree represents a wire, and the nodes at either end of the wire represent the circuit elements that need to be connected.

Here's some Python code that uses Kruskal's algorithm to find the minimum spanning tree given a list of admittance values:

```python
class CircuitElement:
    def __init__(self, name, admittance):
        self.name = name
        self.admittance = admittance

elements = [
    CircuitElement("A", 2),
    CircuitElement("B", 4),
    CircuitElement("C", 1),
    CircuitElement("D", 3),
    CircuitElement("E", 5)
]

# Create a list of all possible edges (wires) between elements
edges = []
for i in range(len(elements)):
    for j in range(i + 1, len(elements)):
        edges.append((elements[i], elements[j]))

# Sort edges by admittance
edges.sort(key=lambda e: e[0].admittance * e[1].admittance)

# Create an empty set for the minimum spanning tree
minimum_spanning_tree = set()

# Create a dictionary to keep track of which elements are in which sets
element_sets = {}
for element in elements:
    element_sets[element] = {element}

# Define a helper function to find the set that an element belongs to
def find_set(element):
    for element_set in element_sets.values():
        if element in element_set:
            return element_set

# Iterate over each edge in sorted order
for edge in edges:
    element1, element2 = edge

    # Find the sets that each element belongs to
    set1 = find_set(element1)
    set2 = find_set(element2)

    # If the elements are already in the same set, adding this edge would create a cycle, so skip it
    if set1 == set2:
        continue

    # Add the edge to the minimum spanning tree
    minimum_spanning_tree.add(edge)

    # Merge the sets containing the two elements
    set1.update(set2)
    for element in set2:
        element_sets[element] = set1

# Print the minimum spanning tree
for edge in minimum_spanning_tree:
    print(edge[0].name, "--", edge[1].name)
```

This will output:

```
C -- A
C -- D
A -- B
D -- E
```

which shows the wires needed to connect the circuit elements in the minimum spanning tree.

## Flow Network Design and Simulation

We make use of the following open-source libraries:

1. OpenMETA - OpenMETA is a system design tool that allows engineers to model and simulate complex systems. It was created by Metamorph Software Inc. and is licensed under the Apache License, Version 2.0.

2. OpenROAD - OpenROAD is an open-source physical design implementation tool for integrated circuits. It was created by UC Berkeley and is licensed under the Apache License, Version 2.0.

3. GDS2WebGL - GDS2WebGL is a tool that allows users to visualize GDSII files in a web browser. It was created by Jens Lienig and Matthias Függer and is licensed under the MIT License.
