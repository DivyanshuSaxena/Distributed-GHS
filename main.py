"""Main file for spawning processes and running experiments"""
import sys
from node import Node
from modules.utils import Edge, EdgeStatus
from multiprocessing import Process, Queue, Lock

wake_count = 0
input_file = sys.argv[1]
output_file = sys.argv[2]
wake_processes = int(sys.argv[3])
debug_level = sys.argv[4]


def spawn_process(node_id, edges, name, msg_q, l):
    """Spawn a new process for node with given name and adjacent edges
    
    Arguments:
        edges {List} -- List of Edge instances associated with node
        name {Float} -- Fragment Name, initially zero for all
        msg_q {Multiprocessing Queue} -- Queue for the node
        l {Multiprocessing Lock} -- Synchronization of wake count
    
    Returns:
        Bool -- Whether the MST was completed or not
    """
    global wake_count, wake_processes, debug_level
    node = Node(node_id, edges, name, msg_q, debug_level)

    # Wake up certain processes.
    l.acquire()
    try:
        if wake_count < wake_processes:
            wake_count += 1
            node.wakeup()
    finally:
        l.release()

    completed = node.start_operation()


# Read from the input file
with open(input_file) as file:
    contents = file.readlines()
contents = [x.strip() for x in contents]

num_nodes = int(contents[0])
raw_edges = []
for line in contents[1:]:
    line = line[1:-1].split(',')
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
    node1 = int(raw_edge[0])
    node2 = int(raw_edge[1])
    # Same edge_id for both edges between node1 and node2
    edge1 = Edge(edge_id, node1, node2, float(raw_edge[2]), queues[node2])
    edge2 = Edge(edge_id, node1, node2, float(raw_edge[2]), queues[node1])
    edges[node1].append(edge1)
    edges[node2].append(edge2)
    edge_id += 1

# Spawn processes for each node
lock = Lock()
for node_id in range(num_nodes):
    p = Process(target=spawn_process,
                args=(node_id, edges[node_id], 0, queues[node_id], lock))
    p.start()

# Join processes before checking the output
p.join()

# Get the edges in the resultant MST
outfile = open(output_file, 'w')
mst = []  # Store the edge_ids
for node_edges in edges:
    for edge in node_edges:
        if edge.get_status() == EdgeStatus.branch:
            edge_id = edge.get_id()
            if edge_id not in mst:
                outfile.write(str(edge) + '\n')
                mst.append(edge_id)

assert len(mst) == num_nodes - 1
print('[SUCCESS]: Completed Execution')
