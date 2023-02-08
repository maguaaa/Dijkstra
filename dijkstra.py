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
                if edge[0] == n:
                    prev_node[n].append([edge[1],edge[2]])
        return prev_node

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])



def IstVisited(dict_): # return a dict of the unvisited nodes
    Visited_keys = []
    Visited_vals = []
    NotVisited_keys = []
    NotVisited_vals = []
    for k, v in dict_.items():
        if v == False:
            NotVisited_keys.append(k)
            NotVisited_vals.append(v)
        else:
            Visited_keys.append(k)
            Visited_vals.append(v)
    visited = dict(zip(Visited_keys, Visited_vals))
    not_visited = dict(zip(NotVisited_keys, NotVisited_vals))
    return not_visited, visited

def argmin(S_bar): #return a node (with the least value in S_bar)
    return min(S_bar, key=S_bar.get)


def dijkstra(graph, src, val=None, S=None):

    prev_node = graph.prev_node()
    src = src
    graph = graph

    if S==None: #check if a node is visited or not
        S = dict(zip(graph.nodes(), [False]*graph.V))
    else:
        pass

    if val == None: #store the dist value of each node
        val = dict(zip(graph.nodes(), [inf]*graph.V))
        val[src] = 0
    else:
        pass

    S_bar, S = IstVisited(S)

    if S_bar != {}:
        #get the argmin in S_bar
        cur_node = argmin({k:v for k,v in val.items() if k in S_bar.keys()})
        S_bar[cur_node] = True #update the visited node

        for succ, c in prev_node[cur_node]:
            cost_to_go = val[cur_node]+c
            if cost_to_go < val[succ]: #choose the less value
                val.update({succ:cost_to_go})
                graph.cache.update({succ:[cur_node]}) #{node: [pred]}
            elif cost_to_go == val[succ]:
                if cur_node not in graph.cache[succ]: # prevent duplicates
                    graph.cache[succ].append(cur_node)
                else:
                    pass
    else:
        return val

    dijkstra(graph, src, val, S_bar)#recursive
    return val

#input 1
# start, end = "A", "D"
# g = Graph(8)
# g.addEdge("A", "B", 2)
# g.addEdge("A", "E", 4)
# g.addEdge("B", "E", 1)
# g.addEdge("B", "F", 3)
# g.addEdge("B", "C", 4)
# g.addEdge("E", "C", 2)
# g.addEdge("E", "F", 1)
# g.addEdge("C", "D", 2)
# g.addEdge("C", "G", 3)
# g.addEdge("F", "G", 5)
# g.addEdge("D", "H", 4)
# g.addEdge("D", "G", 2)
# g.addEdge("G", "H", 3)

#input 2
start, end = "J", "I"
g = Graph(4)
g.addEdge("J", "I", 15)
g.addEdge("J", "L", 7)
g.addEdge("I", "K", 3)
g.addEdge("I", "J", 6)
g.addEdge("L", "I", 7)
g.addEdge("L", "K", 4)
g.addEdge("K", "L", 5)
g.addEdge("K", "J", 15)
g.addEdge("J", "K", 15)
g.addEdge("K", "I", 1)




val = dijkstra(g, start)
print(dijkstra(g, start))
print(g.cache)



# Use a depth-first search to identify optimal paths
optimal_paths = []
def find_paths(prev_node, path, node, start=start):
    # Check if we've reached the start node
    if node == start:
        # Append path to optimal paths
        optimal_paths.append(
            [start] + path[::-1]
        )  # Reversed the path as nodes were added in reverse order
        return

    # Find optimal paths backward for the optimal previous node(s)
    for prev in prev_node[node]:
        find_paths(prev_node, path + [node], prev)
    return


prev_node = g.cache
prev_node[start] = []
print(prev_node)
find_paths(prev_node, path=[], node=end, start=start)
print("Optimal Path(s):")
for path in optimal_paths:
    print("\t" + ", ".join(path) + ".")
print("Optimal Cost:")
print(f"\t{val[end]}")


