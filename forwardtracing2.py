import networkx as nx
import json
import matplotlib.pyplot as plt
from queue import LifoQueue
import argparse


G = nx.DiGraph()
G.add_edges_from([(1,2),(1,3),(2,6),(2,4),(4,5),(3,7),(3,8),(7,4),(7,9)])

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos,node_size=500)
nx.draw_networkx_edges(G,pos,edgelist=G.edges(),edge_color='black')
nx.draw_networkx_labels(G,pos)

depth_limit = 4
parent_node = 1
stack = LifoQueue()
leaf_nodes = []
depth = 1
stack.put(parent_node)
while not stack.empty():
    k = stack.get()
    outed = G.out_edges(k)
    if not outed:
        leaf_nodes.append(k)
    else :
        if depth != depth_limit:
            for i in outed:
                stack.put(i[1])
        else:
            while not stack.empty():
                leaf_nodes.append(stack.get())
        depth+=1      
   
print(set(leaf_nodes))