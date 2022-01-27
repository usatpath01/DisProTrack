from cProfile import label
import json
import sys
from networkx.readwrite import json_graph
import networkx as nx
from pyvis.network import Network
import argparse
from networkx.exception import NetworkXError
import numpy as np
import matplotlib.pyplot as plt


def load_graph(): #Function to load the graph from json file
	f = open("../UPG_construction/upg.json",)
	data = json.load(f)
    
	G = json_graph.node_link_graph(data)
    
	#print(type(G))
	return G
def successors(graph, n):
     try:
            return iter(graph._succ[n])
     except KeyError as e:
            raise NetworkXError(f"The node {n} is not in the digraph.") from e

#forwardtracing
def dfs(graph,n):
    visit[n] = "black"
    print(n)
   
    nodex= successors(graph,n)

   
    x=list(nodex)
    
    for item  in x:
        G.add_node(item)
        G.add_edge(n,item)
        outed=graph.out_edges(n)   
        if outed:
            for i in outed:
                if i in labels:
                    edge_label[i]=labels[i]   
        if(item not in visit):
         
             dfs(graph,item)




data = load_graph()
print(data)
x= sys.argv[1]

e = data.nodes
labels=nx.get_edge_attributes(data,'label')

edge_label={}

G = nx.DiGraph()
visit = { x:"black"}
G.add_node(x)

dfs(data,x)
i=0

#subgraph generation
pos= nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos,node_size=300)
nx.draw_networkx_edges(G,pos,edgelist=G.edges(),edge_color='black')
nx.draw_networkx_labels(G,pos)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_label,font_color="red")
plt.show()







