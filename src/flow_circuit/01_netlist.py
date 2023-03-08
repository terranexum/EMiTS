import cmath
import numpy as np
import csv
import networkx as nx

nodepath = '../static/EMiTS_2976.csv'
incr = 1e-8

def compute_admittance(M, S, E, T):
    if M == 0: M = incr
    if S == 0: S = incr
    if E == 0: E = incr
    if T == 0: T = incr
    V = M / S
    L = S / (2 * cmath.pi * T)
    R = E / (M / T)
    omega = 2 * cmath.pi * V / L
    tau = L / R
    admittance = 1 / (R + 1j * omega * L)
    return admittance

admittance = compute_admittance(10, 5, 20, 2)
#print(admittance)

def load_csv(src_path):
    nodes = []
    id = 1
    with open(src_path, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            Name = str(row[0])
            Lat = str(row[1])
            Lon = str(row[2])
            Typ = str(row[3])
            M = float(row[4])
            S = float(row[5])
            E = float(row[6])
            T = float(row[7])
            BldgID = str(row[8])
            nodes.append({'id':id, 'M':M, 'S':S, 'E':E, 'T':T, 'Name':Name, 'Type':Typ, 'Lat':Lat, 'Lon':Lon, 'BldgID':BldgID})
            id += 1
    return nodes


class CircuitElement:
    def __init__(self, id, admittance, name, typ, lat, lon, bldgID):
        self.id = id
        self.admittance = admittance
        self.name = name
        self.type = typ
        self.lat = lat
        self.lon = lon
        self.bldgID = bldgID

elements = []
    
for node in load_csv(nodepath):
    elements.append(CircuitElement(node['id'], compute_admittance(node['M'], node['S'], node['E'], node['T']), node['Name'], node['Type'], node['Lat'], node['Lon'], node['BldgID']))

# To find edges:


'''
# Kruskal's algorithm implementation - takes forever with a 2976 node graph (4426800 edges)


# Create a list of all possible edges (wires) between elements
edges = []
for i in range(len(elements)):
    for j in range(i + 1, len(elements)):
        edges.append((elements[i], elements[j]))

num_edges = len(edges)

# Sort edges by admittance (which is a complex value, thus we sort by the real part)
edges.sort(key=lambda e: abs(e[0].admittance) * abs(e[1].admittance))

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

iter = 0
# Iterate over each edge in sorted order
for edge in edges:
    print('on iter', iter, '; there are', num_edges, 'number of edges.')
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

    iter += 1

'''

def get_RLC(count, admittance):

    imag_part = np.imag(admittance)
    prefix = ''

    # Check if the number is purely real
    if np.isclose(imag_part, 0):
        prefix = 'R'
        R = np.real(admittance)
        return prefix + str(count), R
    else:
        # Check if the imaginary part is negative or positive
        if imag_part > 0:
            prefix = 'C'
            C = abs(admittance) / (2 * cmath.pi * 1)
            return prefix + str(count), C
        elif imag_part < 0:
            prefix = 'L'
            L = np.imag(admittance) / (2 * cmath.pi * 1)
            return prefix + str(count), L
        else:
            return 'zero'


G = nx.Graph()
G.add_nodes_from(elements)

# add edges with weights to the graph
# (replace this with your own edge weights)
count = 0
for i in range(len(elements)):
    for j in range(i+1, len(elements)):
        type, weight = get_RLC(count, elements[i].admittance + elements[j].admittance) # calculate the weight of the edge between nodes i and j using the effective admittance (sum of both)
        G.add_edge(elements[i].id, elements[j].id, weight=weight)
        count += 1

# find the minimum spanning tree using Boruvka's algorithm
tree = nx.algorithms.tree.minimum_spanning_tree(G, algorithm='boruvka')

# save the minimum spanning tree to a file (replace this with your desired output format)
nx.write_edgelist(tree, 'minimum_spanning_tree.txt', data=['weight'])

minimum_spanning_tree = []

# get a list of edges and their weights in the minimum spanning tree
edges_and_weights = [(u, v, d['weight']) for u, v, d in tree.edges(data=True)]

# print the list of edges and weights
for u, v, weight in edges_and_weights:
    minimum_spanning_tree.append([u, v, weight])


'''
General Rules Following from Admittance:

A complex admittance can be represented as a combination of a conductance (G) and a susceptance (B).

If the susceptance is zero, the admittance value represents a pure resistance and can be represented by a resistor.
If the conductance is zero, the admittance value represents a pure reactance and can be represented by an inductor or capacitor,
depending on whether the imaginary part of the admittance value is negative or positive. 

If the imaginary part is negative, the admittance value represents an inductive reactance, and can be represented by an inductor. 

If the imaginary part is positive, the admittance value represents a capacitive reactance, and can be represented by a capacitor.

In summary, if the admittance value is purely real, it can be represented by a resistor. 
If the admittance value is purely imaginary, it can be represented by an inductor or capacitor, depending on whether the imaginary part is negative or positive. 
If the admittance value is complex, it can be represented by a combination of resistors, capacitors, and inductors.
'''



'''
# Print the minimum spanning tree
for edge in minimum_spanning_tree:
    print(edge[0].name, "--", edge[1].name)
    print(edge[0].admittance, "--", edge[1].admittance)
    print(get_RLC(edge[0].name, edge[0].admittance), "--", get_RLC(edge[1].name, edge[1].admittance))
    print('')
'''

def make_netlist():
    print('on making the netlist')
    i = 0
    count = 1
    netlist = []
    row = ''
    for edge in minimum_spanning_tree:
        #print(edge)
        col1, col4 = get_RLC(count, edge[2])
        col2 = edge[0] # edge[i].id
        col3 = edge[1] # edge[i+1].id
        #col4 = str(np.real(edge[i].admittance)) + 'm'
        #col5 = str(np.imag(edge[i].admittance)) + 'm'
        row = str(col1) + ' ' + str(col2) + ' ' + str(col3) + ' ' + str(col4)
        netlist.append(row)
        count += 1

    return netlist

'''
A netlist for a circuit with two inductors, L1 and L2, connected in series:

* Circuit netlist
L1 1 2 3.98m -3.54m
L2 2 3 7.59m -8.21m

* Inductor admittance equations
Y(L1) = 0 + j * 100.45m
Y(L2) = 0 + j * 193.11m

In this example, the first column lists the component name, the second and third columns list the nodes it connects to, and the fourth and fifth columns 
list the real and imaginary parts of its admittance as a function of frequency (in this case, at a single frequency of 1 Hz). The admittance values are in Siemens (S) units. 
The * character at the beginning of each line indicates a comment line that is ignored by the netlist parser.

'''

def create_cir_file(title, lines):
    print('on creating the .cir file')
    # Add the title line to the beginning of the list
    lines = ['.title ' + title] + lines
    
    # Convert the list of lines to a string
    content = '\n'.join(lines)
    
    # Create the file and write the content
    with open(title + '.cir', 'w') as file:
        file.write(content)

# Example usage
title = 'EMiTS_2976'
lines = make_netlist()
create_cir_file(title, lines)
