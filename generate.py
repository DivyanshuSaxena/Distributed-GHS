"""Generate test cases for the MST Problem"""
import sys
import random


def write_to_file(num_nodes, edges):
    """Write the edges on the input file
    
    Arguments:
        num_nodes {Integer} -- Number of nodes in the graph
        edges {List} -- List of edges with unique edges
    """
    # Write into input file
    with open('files/inp.txt', 'w') as file:
        file.write(str(num_nodes) + '\n')
        for edge in edges:
            file.write(str(edge) + '\n')


def generate_random(num_nodes):
    """Generate a random connected graph with unique weight edges
    
    Arguments:
        num_nodes {Integer}
    """
    nodes = list(range(num_nodes))  # List of all nodes
    added = [0]  # List of nodes added in the connected graph

    edges = []  # Store edges for the connected graph
    weights = list(range(5, (num_nodes * num_nodes) // 2))
    random.shuffle(weights)
    for node in nodes[1:]:
        # Decide number of edges
        num_edges = random.randint(1, len(added))
        temp = added.copy()

        for _ in range(num_edges):
            end = random.choice(temp)
            weight = random.choice(weights)

            edges.append((node, end, weight))
            temp.remove(end)
            weights.remove(weight)

        # Add the current node in the graph too
        added.append(node)

    write_to_file(num_nodes, edges)


def generate_connected(num_nodes):
    """Generate a fully connected random graph with unique edge weights
    
    Arguments:
        num_nodes {Integer}
    """
    edges = []
    weights = list(range(5, (num_nodes * num_nodes) // 2))
    random.shuffle(weights)
    for _in in range(num_nodes):
        for _jn in range(_in + 1, num_nodes):
            weight = random.choice(weights)
            edges.append((_in, _jn, weight))
            weights.remove(weight)

    write_to_file(num_nodes, edges)


def generate_tree(num_nodes):
    """Generate a tree with unique branch weights
    
    Arguments:
        num_nodes {Integer}
    """
    queue = [0]
    max_branches = 4
    count = 1
    edges = []
    weights = list(range(5, (num_nodes * num_nodes) // 2))
    random.shuffle(weights)
    print(len(weights))
    flag = False
    while not flag:
        node = queue.pop()
        neighbours = random.randint(1, max_branches)
        for neighbour in range(neighbours):
            weight = random.choice(weights)
            queue.append(count)
            edges.append((node, count, weight))

            weights.remove(weight)
            count += 1
            if count == num_nodes:
                flag = True
                break

        if flag:
            break

    write_to_file(num_nodes, edges)


def generate_linear(num_nodes):
    """Generate a linear tree with unique edge weights
    
    Arguments:
        num_nodes {Integer}
    """
    edges = []
    weights = list(range(5, (num_nodes * num_nodes) // 2))
    nodes = list(range(num_nodes))
    random.shuffle(weights)
    random.shuffle(nodes)
    for _in in range(num_nodes - 1):
        weight = random.choice(weights)
        edges.append((nodes[_in], nodes[_in + 1], weight))
        weights.remove(weight)

    write_to_file(num_nodes, edges)

def generate_ring(num_nodes):
    """Generate a ring graph with unique edge weights
    
    Arguments:
        num_nodes {Integer}
    """
    edges = []
    weights = list(range(5, (num_nodes * num_nodes) // 2))
    nodes = list(range(num_nodes))
    random.shuffle(weights)
    random.shuffle(nodes)
    for _in in range(num_nodes - 1):
        weight = random.choice(weights)
        edges.append((nodes[_in], nodes[_in + 1], weight))
        weights.remove(weight)

    # Add the final edge
    weight = random.choice(weights)
    edges.append((nodes[-1], nodes[0], weight))

    write_to_file(num_nodes, edges)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('To run the file: python generate.py <num-nodes-to-generate> ' +
              '<graph-type (tree/connected/linear/random/ring)>')
        sys.exit()

    num_nodes = int(sys.argv[1])
    gen_type = sys.argv[2]
    print(gen_type)
    if gen_type == 'linear':
        generate_linear(num_nodes)
    elif gen_type == 'tree':
        generate_tree(num_nodes)
    elif gen_type == 'connected':
        generate_connected(num_nodes)
    elif gen_type == 'ring':
        generate_ring(num_nodes)
    else:
        generate_random(num_nodes)
