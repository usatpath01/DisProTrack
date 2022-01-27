import json
import sys
from networkx.readwrite import json_graph
import networkx as nx
from pyvis.network import Network
import argparse
from networkx.exception import NetworkXError


def load_graph(): #Function to load the graph from json file
	f = open("../UPG_construction/upg.json",)
	data = json.load(f)
    
	G = json_graph.node_link_graph(data)
	# print(type(G))
	return G
def predecessors(graph, n):
     try:
            return iter(graph._pred[n])
     except KeyError as e:
            raise NetworkXError(f"The node {n} is not in the digraph.") from e
def rec (graph,n,i):
    
         #print(len(n))
         nodex2= predecessors(graph,n)
         i=i+1
         x=list(nodex2)
         print(x)
         if len(x) == 0:
         #if x not in end_points:
             return 
         else:
            return rec(graph,x[i],i)

def dfs(graph,n):
    visit[n] = "black"
    print(n)
    
    nodex= predecessors(graph,n)

    #print(list(nodex))
    x=list(nodex)
    #print(n,x)
    #print(visit)
    for item  in x:
        if(item not in visit):
         #print (dict)
         #dict= {item: "black"}
             dfs(graph,item)




data = load_graph()
print(data)
x= sys.argv[1]

e = data.nodes

visit = { x:"black"}
#print(x)
dfs(data,x)






