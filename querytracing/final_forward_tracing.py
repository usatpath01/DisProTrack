#=============================================================
#  Title : SubGraph Generation
#  Author : Abhyanand Sharma
#  Date : 27th Jan, 2022
#=============================================================
#  ==================  USAGE  ================================
#  python3 final_forward_tracing.py -B <symptom node>
#  python3 final_forward_tracing.py -S <parent node>
#  python3 final_forward_tracing.py -G y
#  ===========================================================

import json
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import networkx as nx
from pyvis.network import Network
from queue import LifoQueue
import argparse

f = open('outputs_s3_1640089505/upg.json','r')                                             #opening the upg.json file(node-link data format)
json_data = json.loads(f.read())                                                        #reading the json data
H = json_graph.node_link_graph(json_data,directed=True,attrs=None)                      #returns a graph from node-link data format (H is a network graph object)
labels = nx.get_edge_attributes(H,'label')                                              #returns all the edge labels in the parent graph
SG = nx.DiGraph()                                                                       #instance of subgraph 
edge_labels = {}  

#View the original UPG
def viewgraph():
    pos = nx.spring_layout(H)
    nx.draw_networkx_nodes(H,pos,node_size=500)
    nx.draw_networkx_edges(H,pos,edgelist=H.edges(),edge_color='black')
    nx.draw_networkx_labels(H,pos)
    nx.draw_networkx_edge_labels(H,pos,edge_labels=labels)
    plt.show()

# Backward Tracing algorithm
def backward_tracing(child_node):                                                               
    stack = LifoQueue()
    visited = []
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


# BFS forward tracing algorithm and subgraph generation                                                                       
def subgraph_gen(parent_node):
                                               
    stack = LifoQueue()
    visited = []
    stack.put(parent_node)
    while not stack.empty():
        k = stack.get()
        outed = H.out_edges(k)
        if outed:
            for i in outed:
                if i[1] not in visited:
                    stack.put(i[1])
                    visited.append(i[1])
                    if i in labels:
                        edge_labels[i] = labels[i]
                SG.add_edges_from(outed)
 
    pos = nx.spring_layout(SG)
    nx.draw_networkx_nodes(SG,pos,node_size=500)
    nx.draw_networkx_edges(SG,pos,edgelist=SG.edges(),edge_color='black')
    nx.draw_networkx_labels(SG,pos)
    nx.draw_networkx_edge_labels(SG,pos,edge_labels=edge_labels)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-B','--back',help='Specify symptom')
    parser.add_argument('-S','--subg',help='Specify cause')
    parser.add_argument('-G','--viewg',help='View UPG')
    args = parser.parse_args()
    with open("outputs_s3_1640089505/aud_map.json") as json_file:
        data = json.load(json_file)
    if args.back in data:
        name = data[args.back]
        backward_tracing(name)
            
    if args.subg in data:
        name1 = data[args.subg]
        subgraph_gen(name1)
    if args.viewg == 'y':
        viewgraph()
    
if __name__ == "__main__":
   main() 
