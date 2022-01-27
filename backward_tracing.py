import json
import matplotlib as plt
from networkx.readwrite import json_graph
import networkx as nx
from pyvis.network import Network
from queue import LifoQueue

f = open('./UPG_construction/upg.json','r')                                             
json_data = json.loads(f.read())                                                        
H = json_graph.node_link_graph(json_data,directed=True,attrs=None)                      

#backward tracing algorithm                                                             
child_node = '[2608]/usr/sbin/apache2_5'                                                            
stack = LifoQueue()
visited = []
visited.append(child_node)
parent_nodes = []
stack.put(child_node)
while not stack.empty():
   k = stack.get()
   outed = H.in_edges(k) 
   if not outed:
      parent_nodes.append(k)
   else :
      for i in outed:
         if i[0] not in visited:
            stack.put(i[0])
            visited.append(i[0])
    
print(parent_nodes)    

