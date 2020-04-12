"""Generate test cases for the MST Problem"""
import sys
import random

num_nodes = sys.argv[1]
nodes = list(range(num_nodes))  # List of all nodes
added = [0]  # List of nodes added in the connected graph

edges = []  # Store edges for the connected graph
weight = 5  # Weight of edges shall be 5 onwards
for node in nodes[1:]:
    # Decide number of edges
    num_edges = random.randint(1, len(added))
    temp = added.copy()

    for _ in range(num_edges):
        end = random.choice(temp)
        edges.append((node, end, weight))
        temp.remove(end)
        weight += 1

# Write into input file
with open('files/inp.txt', 'w') as file:
    file.write(str(num_nodes) + '\n')
    for edge in edges:
        file.write(str(edge) + '\n')
