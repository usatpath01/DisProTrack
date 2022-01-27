import networkx as nx
import json
import matplotlib.pyplot as plt
from queue import LifoQueue
import argparse

G = nx.DiGraph()
SG = nx.DiGraph()
G.add_edges_from([(1,2),(1,3),(2,4),(2,5),(3,5),(3,7),(5,8),(5,6)])
list_edges_traversed = {}
SG = nx.DiGraph()
pnode = 2
stack = LifoQueue()
stack.put(pnode)
while not stack.empty():
    k = stack.get()
    outed = G.out_edges(k)
    if outed:
        for i in outed:
            stack.put(i[1])
            list_edges_traversed[i] = "write"    
        SG.add_edges_from(outed)
        
print(list_edges_traversed)                    

pos = nx.spring_layout(SG)
nx.draw_networkx_nodes(SG,pos,node_size=500)
nx.draw_networkx_edges(SG,pos,edgelist=SG.edges(),edge_color='black')
nx.draw_networkx_labels(SG,pos)
nx.draw_networkx_edge_labels(SG,pos,edge_labels=list_edges_traversed,font_color='red')
plt.show()
   
