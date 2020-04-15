"""Plot the results into matplotlib graphs"""
import math
import matplotlib.pyplot as plt

# Read results from file
with open('../files/results.txt') as f:
    lines = f.readlines()
lines = [l.strip().split(',') for l in lines]

num_messages = []
nlogn = []
edges = []
for line in lines:
    n = int(line[2])
    n_edges = int(line[3])
    num_messages.append(int(line[1]))
    nlogn.append(n * math.log(n))
    edges.append(n_edges)

plt.plot(nlogn, num_messages, 'bs-')
plt.xlabel('N logN')
plt.ylabel('#Messages')
plt.show()

plt.plot(edges, num_messages, 'g^-')
plt.xlabel('Edges')
plt.ylabel('#Messages')
plt.show()
