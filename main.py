"""Main file for spawning processes and running experiments"""
import sys
from node import Node
from modules.utils import Edge
from multiprocessing import Process, Queue


def spawn_process(edges, name, msg_q):
    node = Node(edges, name, msg_q)
    completed = node.start_operation()
    return completed


input_file = sys.argv[1]
output_file = sys.argv[2]

# Read from the input file
with open(input_file) as file:
    contents = file.readlines()
contents = [x.strip() for x in contents]

num_nodes = int(contents[0])
raw_edges = []
for line in contents[1:]:
    line = line[1:-1].split()
    raw_edges.append(line)

# Attach a queue for each process
queues = []
for _ in range(num_nodes):
    q = Queue()
    queues.append(q)

# Form edges for each node from the given input
edges = []
for _ in range(num_nodes):
    edges.append([])

edge_id = 0
for raw_edge in raw_edges:
    node1 = raw_edge[0]
    node2 = raw_edge[1]
    edge1 = Edge(edge_id, raw_edge[2], queues[node2])
    edge2 = Edge(edge_id, raw_edge[2], queues[node1])
    edges[node1].append(edge1)
    edges[node2].append(edge2)

# Spawn processes for each node
for node_id in range(num_nodes):
    p = Process(target=spawn_process,
                args=(edges[node_id], 0, queues[node_id]))
    p.start()

# Join processes before checking the output
p.join()
