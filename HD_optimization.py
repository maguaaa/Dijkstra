import networkx as nx
import numpy as np

G = nx.DiGraph()
G.add_nodes_from("SABCDEFGHI") #add nodes
#add edges
G.add_weighted_edges_from([('S', 'A', 50), 
                           ('S', 'B', 0), 
                           ('A', 'C', 450),
                           ('A', 'D', 0), 
                           ('B', 'D', 200), 
                           ('B', 'E', 100), 
                           ('C', 'F', 70), 
                           ('C', 'G', 0), 
                           ('D', 'G', 1000),	
                           ('D', 'H', 400), 
                           ('E', 'H', 50), 
                           ('E', 'I', 30)])
# print(G.edges)
# print(list(nx.all_simple_paths(G,'S','D')))

#label action of each edge; 1=up, 0=down
attrs = {('S', 'A'): {"action": 1},
        ('S', 'B'): {"action": 0},
        ('A', 'C'): {"action": 1},
        ('A', 'D'): {"action": 0},
        ('B', 'D'): {"action": 1},
        ('B', 'E'): {"action": 0},
        ('C', 'F'): {"action": 1},
        ('C', 'G'): {"action": 0},
        ('D', 'G'): {"action": 1},
        ('D', 'H'): {"action": 0},
        ('E', 'H'): {"action": 1},
        ('E', 'I'): {"action": 0},}
nx.set_edge_attributes(G,attrs)
# print(G['S']['A']["action"])

G.nodes["S"]['optimal']=0
G.nodes["A"]['optimal']=0
G.nodes["B"]['optimal']=0
G.nodes["C"]['optimal']=0
G.nodes["D"]['optimal']=0
G.nodes["E"]['optimal']=0
G.nodes["F"]['optimal']=0
G.nodes["G"]['optimal']=0
G.nodes["H"]['optimal']=0
G.nodes["I"]['optimal']=0
print(G.nodes(data=True))

p_up=0.85
p_down=0.65

stage = [['S'], ['A','B'], ['C','D','E'],['F','G','H','I']]
root = 'S'


for i in np.arange(2,-1,-1):
    print("**************************************")
    print(f"Current Stage: {i+1}")
    print("**************************************")

    for stage_node in stage[i]:
        current_src = stage_node
        print(f"current node: {current_src}")
        neighbors = list(nx.neighbors(G,current_src))
        current_value_up = 0
        current_value_down = 0

        for nbr in neighbors:
            #action: up=1, down=0
            if G[current_src][nbr]['action']==0:
                current_value_down += p_down*(G[current_src][nbr]['weight']+G.nodes[nbr]['optimal'])
            else:
                current_value_down += (1-p_down)*(G[current_src][nbr]['weight']+G.nodes[nbr]['optimal'])

            # choose to travel up
            if G[current_src][nbr]['action']==1:
                current_value_up += p_up*(G[current_src][nbr]['weight']+G.nodes[nbr]['optimal'])
            else:
                current_value_up += (1-p_up)*(G[current_src][nbr]['weight']+G.nodes[nbr]['optimal'])

        current_optimal = min(current_value_up,current_value_down)
        if current_value_up<current_value_down:
            G.nodes[current_src]['policy'] = 'up'
        elif current_value_up == current_value_down:
            G.nodes[current_src]['policy'] = 'up or down'
        else:
            G.nodes[current_src]['policy'] = 'down'

        print(f"current optimal = {current_optimal}")
        print(f"current optimal action = {G.nodes[current_src]['policy']}")
        print("------------------------------")

        G.nodes[current_src]['optimal'] += current_optimal

optimal=G.nodes[root]['optimal']
print(f'optimal valuie = {optimal}')
optimal_policy = nx.get_node_attributes(G,"policy")
print(f"optimal policy: {optimal_policy}")


