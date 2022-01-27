# author : Abhyanand Sharma


import networkx as nx
import json
import matplotlib.pyplot as plt
from queue import LifoQueue
import argparse



#this code works fine for finding all the children from a given parent node (bfs)
def forward_tracing(G):  
   parent_node = 1
   stack = LifoQueue()
   leaf_nodes = []
   stack.put(parent_node)
   while not stack.empty():
      k = stack.get()
      outed = G.out_edges(k)
      if not outed:
         leaf_nodes.append(k)
      else:
         for i in outed:
            stack.put(i[1])
   print(set(leaf_nodes))
    
    
#this code works fine for finding all the parent node from a given child node
def backward_tracing(G):
   child_node = 8
   parent_nodes = []
   stack = LifoQueue()
   stack.put(child_node)
   while not stack.empty():
      k = stack.get()
      indeg = G.in_edges(k)
      if not indeg:
         parent_nodes.append(k)
      else:
         for i in indeg:
            stack.put(i[0])
   print(set(parent_nodes))
   
# this code returns the subgraph from the given node till the leaf node   
   

def main():
   G = nx.DiGraph()
   SG = nx.DiGraph()
   G.add_edges_from([(1,2),(1,3),(2,4),(2,5),(3,5),(3,7),(5,8),(5,6)])
   parser = argparse.ArgumentParser()
   parser.add_argument("-t")
   parser.add_argument("-n")
   parser.add_argument("--show")
   args = parser.parse_args()
   if args.t == "back":
      backward_tracing(G)
   if args.t == "forward":
      forward_tracing(G)
   if args.show == 'y':
#      SG = subgraph(G)
      pos = nx.spring_layout(G)
      nx.draw_networkx_nodes(G,pos,node_size=500)
      nx.draw_networkx_edges(G,pos,edgelist=G.edges(),edge_color='black')
      nx.draw_networkx_labels(G,pos)
      plt.show()      
      
if __name__ == "__main__":
   main()   