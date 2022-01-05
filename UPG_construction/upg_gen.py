#This code if for one application need to modify some modules to be able to run multiple applications
import json
from networkx.readwrite import json_graph
import networkx as nx
import re
from re import search 
import pprint
import time
from pyvis.network import Network

syscall_cnt = {}

def load_graph(): #Function to load the graph from json file
	f = open("graph.json",)
	data = json.load(f)
	G = json_graph.node_link_graph(data)
	return G

def load_log(): #Function to load the log file from json file
	f = open("testing_universal_log.json",)
	data = json.load(f)

	# print(data[71110]["pid"])
	return data

def isAppEntry(event): #To find the lms log as the entry log(This is for apache for now update the json to add a field for application logs)
	if len(event)==3 and "lms" in event:
		return 1
	return 0

def calculate_rank(string): #Function to find the rank of regex_lms
    total_words = len(re.findall(r'\w+', string))
    regex_for_float_double = "[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)"
    regex_for_oct = "[-+]?[0-7]+"
    regex_for_int = "-?[0-9]+"
    regex_for_pos_int = "[0-9]+"
    regex_for_address = "(0x|0X)?[0-9a-f]{8}/i"
    regex_for_hexadeciaml = "(0x)?[0-9a-f]{8}/i"
    special_chars = [r"\*",r"\.",r"\{",r"\}",r"\[",r"\]",r"\<",r"\>",r"\(",r"\)",r"\+",r"\\",r"\|"]

    for ele in special_chars:
        string = string.replace(ele,"")

    cnt = 0
    
    cnt += string.count(regex_for_float_double)
    string = string.replace(regex_for_float_double,"")
    
    cnt += string.count(regex_for_int)
    string = string.replace(regex_for_int,"")

    cnt += string.count(regex_for_pos_int)
    string = string.replace(regex_for_pos_int,"")

    cnt += string.count(regex_for_oct)
    string = string.replace(regex_for_oct,"")

    cnt += string.count(regex_for_address)
    string = string.replace(regex_for_address,"")

    cnt += string.count(regex_for_hexadeciaml)
    string = string.replace(regex_for_hexadeciaml,"")

    cnt += string.count(".*") 
    string = string.replace(".*","")

    cnt += string.count(".")

    return total_words-cnt

def match_lms(lms_cand, lms_graph, lms_state, eventUnit, data):
	lvl = 15 #lookahead level
	final_regex_node = None #if the node having lms is found
	for dis in range(1,lvl): #iterate for all levels from 1 to lvl
		nodes = nx.algorithms.descendants_at_distance(lms_graph,lms_state,dis)
		candidates_lms = []
		for node in nodes:
			regex_lms = ".*" + lms_graph.nodes[node]["lms"]
			pattern = re.compile(regex_lms)
			if pattern.fullmatch(data["lms"]):
				candidates_lms.append(node)

		if len(candidates_lms)>0: #find the node with the highest rank if it matches
			mx = 0
			for node in candidates_lms:
				temp_cmp = calculate_rank(lms_graph.nodes[node]["lms"])
				if temp_cmp>mx:
					mx = temp_cmp
					final_regex_node = node
			break

	if final_regex_node!=None: 
		if len(list(lms_graph.successors(final_regex_node)))==0 or lms_graph.nodes[final_regex_node]["is_end"]:	
			if len(lms_graph.nodes[final_regex_node]["end_syscall"]) == 0:
				return final_regex_node,1

			else:
				pid = str(data["pid"]).strip()
				syscall_cnt[pid] = len(lms_graph.nodes[node]["end_syscall"])
				return final_regex_node,0

		else:
			return final_regex_node,0


	if final_regex_node==None: #If the lookahead matching fails then we will try exhaustive search (lookback matching)
		final_regex_node = get_lms_regex(data["lms"],lms_graph)
		if final_regex_node != None: #if the found lms is ending lms then set endunit as 1
			if len(lms_graph.nodes[final_regex_node]["end_syscall"]) == 0:
				return final_regex_node,1
			else:
				pid = str(data["pid"]).strip()
				syscall_cnt[pid] = len(lms_graph.nodes[final_regex_node]["end_syscall"])
				return final_regex_node,0

		else: #else set endunit as 0
			return final_regex_node,0
	# return final_regex_node

#Function to do the exhaustive search to find all the node containing lms
def get_lms_regex(event,G):
	candidates_lms = []
	for node in G.nodes:
		regex_lms = G.nodes[node]["lms"]
		regex_lms = ".*" + regex_lms
		pattern = re.compile(regex_lms)
		if pattern.fullmatch(event):
			candidates_lms.append(node)

	final_regex_node = None
	mx = 0
	for node in candidates_lms:
		temp_cmp = calculate_rank(G.nodes[node]["lms"])
		if temp_cmp>mx:
			mx = temp_cmp
			final_regex_node = node
	return final_regex_node


data = load_log()
lms_graph = load_graph()


eventUnit = {}
lms_state = None #This has to be made a list if trying for multiple applications(It is for 1 application only for now)
end_unit = 0
G = []
net_graph = nx.DiGraph()
#Now interating only for first 20 logs
logs_range = len(data)
for i in range(0,logs_range):
	print(i)
	if isAppEntry(data[i]): 
		if lms_state == None: #if the log is the first log of the application 
			lms_cand = get_lms_regex(data[i]["lms"],lms_graph) #Do exhaustive search to find lms node
			lms_state = lms_cand
			if lms_graph.nodes[lms_state]["is_end"]:
				end_unit = 1
		else:
			temp,end_unit = match_lms(lms_cand, lms_graph, lms_state, eventUnit, data[i]) #else use their neighbours to find the lms node
			if temp!=None:
				lms_state = temp
			else:
				continue
			# break

	if end_unit: #if end_unit=1 then we have partiotned the graph so initialize the eventUnit and end_unit
		lms_pid = str(data[i]["pid"]).strip()
		if lms_pid not in eventUnit:
			eventUnit[lms_pid] = []
		eventUnit[lms_pid].append(data[i]["lms"])
		G.append(eventUnit[lms_pid])
		end_unit = 0
		if lms_pid in eventUnit:
			del eventUnit[lms_pid]

	else: #if not end_unit then add the log event to its corresponding pid
		# if "data" in data[i]:
		if "pid" in data[i]:
			lms_pid = str(data[i]["pid"]).strip()
			if lms_pid not in eventUnit:
				eventUnit[lms_pid] = []

			temp_dict = {}
			if "exe" in data[i]:
				temp_dict["exe"] = data[i]["exe"]
			else:
				temp_dict["exe"] = None

			if "path_name" in data[i]:
				temp_dict["path_name"] = data[i]["path_name"]
			else:
				temp_dict["path_name"] = None

			if "exe" in data[i]:
				temp_dict["exe"] = data[i]["exe"]
			else:
				temp_dict["exe"] = None

			if "syscall_name" in data[i]:
				temp_dict["syscall_name"] = data[i]["syscall_name"]
			else:
				temp_dict["syscall_name"] = None

			if "syscall_id" in data[i]:
				temp_dict["syscall_id"] = data[i]["syscall_id"]
			else:
				temp_dict["syscall_id"] = None

			temp_dict["pid"] = lms_pid

			if "sock_laddr" in data[i]:
				temp_dict["sock_laddr"] = data[i]["sock_laddr"]
			else:
				temp_dict["sock_laddr"] = None

			if "sock_lport" in data[i]:
				temp_dict["sock_lport"] = data[i]["sock_lport"]
			else:
				temp_dict["sock_lport"] = None


			eventUnit[lms_pid].append(temp_dict)
			if lms_pid in syscall_cnt and syscall_cnt[lms_pid]>0:
				syscall_cnt[lms_pid]-=1
				if syscall_cnt[lms_pid]==0:
					G.append(eventUnit[lms_pid])
					del eventUnit[lms_pid]

		# elif "pid" in data[i]:
		# 	lms_pid = str(data[i]["pid"]).strip()
		# 	if lms_pid not in eventUnit:
		# 		eventUnit[lms_pid] = []
		# 	if "lms" in data[i]:
		# 		eventUnit[lms_pid].append(data[i]["lms"])
	# final = time.time_ns()
	# print(final-initial)
# print(eventUnit)
# pp = pprint.PrettyPrinter(indent=4)
# for node in G:
# 	pp.pprint(node)

# with open("sample_output_eventUnit.json","w") as outfile:
#   json.dump(eventUnit,outfile,indent = 4)

with open("sample_output.json","w") as outfile:
  json.dump(G,outfile,indent = 4)

partition = 0
for execution_unit in G:
	partition+=1
	for log in execution_unit:
		if "exe" in log:
			# net_graph.add_edge(str(log["exe"]),str(log["path_name"]))
			if "syscall_name" in log:
				if str(log["syscall_name"]) in ["openat","open","creat","unlink","unlinkat","execve"]:
					net_graph.add_edge(str(log["exe"])+str(partition),str(log["path_name"]),label = str(log["syscall_name"]))
				
				# else if str(log["syscall_name"]) in ["dup","dup2","dup3","close"]:

				# else if str(log["syscall_name"]) in ["exit","exit_group"]:
				
				elif str(log["syscall_name"]) in ["connect","bind"]:
					net_graph.add_edge(str(log["exe"])+str(partition),str(log["sock_laddr"])+" "+str(log["sock_lport"]),label = str(log["syscall_name"]))

				elif str(log["syscall_name"]) in ["accept4","accept"]:
					net_graph.add_edge(str(log["sock_laddr"])+" "+str(log["sock_lport"]),str(log["exe"])+str(partition),label = str(log["syscall_name"]))


json_converted = json_graph.node_link_data(net_graph)
with open("upg.json","w") as outfile:
  json.dump(json_converted,outfile,indent = 4)



nt = Network('1800px','1200px',directed=True)
nt.from_nx(net_graph)
nt.show('provenanceGraph2.html')

