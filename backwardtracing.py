import json
import sys
from networkx.readwrite import json_graph
import networkx as nx
from pyvis.network import Network
import argparse
from networkx.exception import NetworkXError
#parser = argparse.ArgumentParser()
#parser.add_argument('-s',type=str,required=True)
#args = parser.parse_args()

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



#end_points = ["1_None None", "1_None", "2_None None", "2_None","2_:: 80", "3_None None", "3_None","4_None None", "4_None","5_None None", "5_None","6_None None", "6_None","7_None None", "7_None","8_None None", "8_None""9_None None", "9_None"]
data = load_graph()
print(data)
x= sys.argv[1]

e = data.nodes
#print(e)
#nodex= successors(data, x)
#x=list(nodex)
#print(x)
#i=0
#rec(data,x[i],i)
#data.add_node(x,visit="black")
#dict = {x:"black"}
visit = { x:"black"}
#print(x)
dfs(data,x)
#while x[i] not in end_points:
    
    #nodex2= successors(data,x[i])
    #i=i+1
    #x=list(nodex2)
    #print(x)
#i=0   
        





#f = open('./upg.json','r')
#value = args.sx[i]
#data = json.loads(f.read())

#link_dict = data['links']
#link_len = len(link_dict)
#path = ""
#i=0
#ans = ""
##while value not in end_points:
    #if link_dict[i]['source']==value:
        ##value = link_dict[i]['target']
        #ans = ans+link_dict[i]['source']+"-->"
        #i=0
   # i=i+1
#def successors(data,value)
    
#print(ans+value)
#f.close()
