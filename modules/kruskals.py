"""Implementation of prims algorithm to check if the Distributed GHS returned
correctly or not"""
import sys

INF = sys.maxsize


class Kruskals:
    """Class for implementation of kruskals algorithm"""
    def __init__(self, num_nodes):
        """Ctor
        
        Arguments:
            num_nodes {Integer} -- Number of nodes in the graph
        """
        self.num_nodes = num_nodes
        self.parent = list(range(num_nodes))

    def get_parent(self, node):
        """Traverse up the sub-tree to get the parent of node
        
        Arguments:
            node {Integer}
        
        Returns:
            Integer -- Parent node
        """
        if self.parent[node] == node:
            return node
        return self.get_parent(self.parent[node])

    def union(self, parent1, parent2):
        """Combine two sub-trees
        
        Arguments:
            parent1 {Integer}
            parent2 {Integer}
        """
        self.parent[parent1] = parent2

    def get_mst(self, edges):
        """Get the MST using Kruskal's algorithm
        
        Arguments:
            edges {List} -- List of raw edges
        
        Returns:
            Float -- Tree Weight
        """
        # Sort the edges in order of increasing weights
        edges.sort(key=lambda x: float(x[2]))

        # Pick the least edge at a time, and check if it doesn't form a cycle
        mst_set = []
        for edge in edges:
            node1 = int(edge[0])
            node2 = int(edge[1])
            node1_parent = self.get_parent(node1)
            node2_parent = self.get_parent(node2)
            if node1_parent != node2_parent:
                # Add edge to mst
                mst_set.append(edge)
                self.union(node1_parent, node2_parent)
                if len(mst_set) == self.num_nodes - 1:
                    break

        # Find and return the sum of weights of the tree edges
        tree_weight = 0
        for tree_edge in mst_set:
            tree_weight += float(tree_edge[2])
        return tree_weight


if __name__ == '__main__':
    # Read from the input file
    input_file = sys.argv[1]

    with open(input_file) as file:
        contents = file.readlines()
    contents = [x.strip() for x in contents]

    num_nodes = int(contents[0])
    raw_edges = []
    for line in contents[1:]:
        if len(line) > 1:
            line = line[1:-1].split(',')
            raw_edges.append(line)
        else:
            break

    k = Kruskals(num_nodes)
    weight = k.get_mst(raw_edges)
    print('[SUCCESS]: Completed Execution. MST Weight: ' + str(weight))
