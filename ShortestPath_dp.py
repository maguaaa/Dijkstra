
from math import inf

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []
        self.cache = {n:[] for n in self.nodes()}

    # function to return a list of all the nodes
    def nodes(self):
        nodes = []
        for edge in self.graph:
            nodes.append(edge[0])
            nodes.append(edge[1])
        nodes = [*set(nodes)]
        return nodes

    ### only for acyclic networks (using dictionary)
    def prev_node(self):
        prev_node = {n:[] for n in self.nodes()} #edge[1] is a node
        for n in self.nodes():
            for edge in self.graph:
                if edge[1] == n:
                    prev_node[n].append([edge[0],edge[2]])
        return prev_node

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])


def dp_shortest_path(graph, src, tgt, val=None, queue=None):
    cur_node = tgt
    prev_node = graph.prev_node()
    src = src
    graph = graph

    if queue is None:
        queue = [tgt]
    else:
        queue = queue

    if val == None:
        val = dict(zip(graph.nodes(), [inf]*graph.V))
        val[tgt] = 0
    else:
        pass

    while queue != []:
        for pred_cost in prev_node[cur_node]:
            p, c = pred_cost[0], pred_cost[1]
            queue.append(p) #first in first out

            cost_to_go = val[cur_node]+c
            if cost_to_go < val[p]: #choose the less value
                val.update({p:cost_to_go})
                graph.cache.update({p:[cur_node]})
            elif cost_to_go == val[p]:
                if cur_node not in graph.cache[p]: # prevent duplicates caused by queue
                    graph.cache[p].append(cur_node)
                else:
                    pass
            else:
                queue.pop(-1) #pop out level1 child nodes

        queue.pop(0) #pop out level0 child nodes

        for x in queue:
            dp_shortest_path(graph, src, x, val, queue) #recursive

    return val


start, end = "A", "H"

g = Graph(8)
g.addEdge("A", "B", 2)
g.addEdge("A", "E", 4)
g.addEdge("B", "E", 1)
g.addEdge("B", "F", 3)
g.addEdge("B", "C", 4)
g.addEdge("E", "C", 2)
g.addEdge("E", "F", 1)
g.addEdge("C", "D", 2)
g.addEdge("C", "G", 3)
g.addEdge("F", "G", 5)
g.addEdge("D", "H", 4)
g.addEdge("D", "G", 2)
g.addEdge("G", "H", 3)


print(dp_shortest_path(g,"A","H"))
print(g.cache)


val = dp_shortest_path(g,"A","H")
succ_node = g.cache
succ_node[end]= []

# Use a depth-first search to identify optimal paths
optimal_paths = []

def find_paths(succ_node, path, node, end="H"):
    # Check if we've reached the end node
    if node == end:
        # Append path to optimal paths
        optimal_paths.append(
            [end] + path[::-1]
        )  # Reversed the path as nodes were added in reverse order
        return

    # Find optimal paths backward for the optimal previous node(s)
    for prev in succ_node[node]:
        find_paths(succ_node, path + [node], prev)
    return


find_paths(succ_node, path=[], node="A", end="H")

# Print outputs
print("Optimal Path(s):")
for path in optimal_paths:
    path.reverse()
    print("\t" + ", ".join(path) + ".")
print("Optimal Cost:")
print(f"\t{val[start]}")



