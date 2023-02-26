import networkx as nx
import numpy as np
import copy

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

print(G.nodes(data=True))

p_up=0.85
p_down=0.65

stage = [['S'], ['A','B'], ['C','D','E'],['F','G','H','I']]
root = 'S'
value = {}

for i in np.arange(2,0,-1):
    print(f"Current Stage: {i+1}")
    for stage_node in stage[i]:
        paths = list(nx.all_simple_paths(G,root,stage_node))
        print(f'''paths from source to current stage: 
{paths}''')
        for path in paths:
            print(f"path = {path}")
            #check if have ever travelled up
            check=0
            check_path = copy.copy(path) #copy path for checking

            while len(check_path)>=2:
                check+=G[check_path[0]][check_path[1]]["action"]
                check_path.pop(0)
            
            #if check>0, have travelled up
            if check>0:
                check=1
            else:
                check=0
            p = p_up*(1-check)+p_down*check #check=1,p=p_down; check=0,p=p_up
            
            current_src = path[-1] #end node of a path
            neighbors = list(nx.neighbors(G,current_src))
            current_value = 0

            for nbr in neighbors:
                if p==p_down:
                    #action: up=1, down=0
                    if G[current_src][nbr]['action']==0:
                        current_value += p*G[current_src][nbr]['weight']
                    else:
                        current_value += (1-p)*G[current_src][nbr]['weight']
                
                else:
                    # choose to travel up
                    if G[current_src][nbr]['action']==1:
                        current_value += p*G[current_src][nbr]['weight']
                    else:
                        current_value += (1-p)*G[current_src][nbr]['weight']
            print(f"current value = {current_value}")
            print("*******************")
            
            value.update({str(path): current_value})
            # also update the edge weight
            G[path[-2]][path[-1]]['weight'] += current_value

print(f"value function in iterations: {value}")

# calculate final value
exp_val=0
for nbr in nx.neighbors(G,root):
    if G[root][nbr]['action']==0:
        exp_val += p_down*G[root][nbr]['weight']
    else:
        exp_val += (1-p_down)*G[root][nbr]['weight']

print(f'expected valuie = {exp_val}')
