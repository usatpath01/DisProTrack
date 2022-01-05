import pip
def tryImport(packages):
	''' If import error, then install the module '''
	for package in packages:
		try:
			__import__(package)
		except ImportError:
			pip.main(['install', package])
	return
##################################################################################################
tryImport(['angr','claripy','sys', 'pickle', 'pyvex', 're', 'itertools','pprint', 'string', 'itertools', 'json', 'networkx', 'pyvis', 'copy', 'angr-utils'])

import angr, claripy, sys, pickle, pyvex, re, pprint, string, itertools, json, pyvis, copy

from re import search
import networkx as nx
# import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from angrutils import *
from pyvis.network import Network
##################################################################################################
import argparse
parser = argparse.ArgumentParser(prog='python3 solve.py', usage='%(prog)s [options]')
parser.add_argument('-V', dest='visualize', help='Use this flag for visualizing the graph',action="store_true")
parser.add_argument('--exe', dest='exe', nargs='+', default="./a.out", help='Provide the executable file location')
parser.parse_args([])
args = parser.parse_args()
##################################################################################################
proj = angr.Project(args.exe[0],load_options={'auto_load_libs':False})
##################################################################################################
def log_functions():
  check_func = set()
  not_check_func = set()
  cfg  = proj.analyses.CFGFast(normalize = True,resolve_indirect_jumps = True,data_references=True,cross_references=True)
  entry_func = cfg.kb.functions.items()
  for addr,func in entry_func:
    if "print" in func.name:
      check_func.add(addr)
    elif "syslog" in func.name:
      check_func.add(addr)
    elif "log4c" in func.name:
      check_func.add(addr)
    else:
      not_check_func.add(addr)
  return cfg,check_func,not_check_func

def find_strings(cfg,addr):
  req_strings = []
  try:
    entry_func = cfg.kb.functions[addr]
  except Exception:
    pass
  else:
    try:
      temp_string = entry_func.string_references(vex_only=True)
    except Exception:
      pass
    else:
      for addr,string in temp_string:
        req_strings.append(string)
      return req_strings
    return req_strings
  return req_strings


def extract_call_sites(cfg,check_func):
  req_func = set()
  for func in check_func:
    bb_addr =  cfg.kb.functions[func].block_addrs
    for addr in bb_addr:
      node = cfg.get_any_node(addr)
      predec = node.predecessors
      for predecessors in predec:
        req_func.add(predecessors.addr)
  return req_func

def peephole(cfg,call_sites,max_back_trace):
  req_string = set()
  set_call = set()
  temp_call_sites = tuple(call_sites)
  set_call.add((temp_call_sites,0))
  while len(set_call) != 0:
    iter_list,back_trace = set_call.pop()
    for addr in iter_list:
      l = find_strings(cfg,addr)
      # print(l)
      if len(l)!=0:
        for strings in l:
          req_string.add(strings)
      elif back_trace < max_back_trace:
        node = cfg.get_any_node(addr)
        if node!=None:
          predecessors = node.predecessors
          if predecessors!=None and len(predecessors)!=0:
            predec = []
            for predecessor in predecessors:
              predec.append(predecessor.function_address)
            temp_predec = tuple(predec)
            set_call.add((temp_predec,back_trace+1))
  return req_string


st = proj.factory.entry_state()
loops_have_syscall = []
visited = set()
queue = []
req_graph = {}
loops_not_have_syscall = []
loop_starting = {}
loop_ending = {}


def extract_strings(node,cfg):
  try:
    cfg_node = cfg.get_any_node(node.addr)
    ins_addr = cfg_node.instruction_addrs
  except:
    print("Block does not exist")
    return ''
  else:
    if(len(ins_addr)>0):
      starting = min(ins_addr)
      ending = max(ins_addr)
      references = cfg.kb.xrefs
      temp = references.get_xrefs_by_ins_addr_region(starting, ending)
      tmp = list(temp)
      for temptmp in tmp:
        try:
          t = temptmp.memory_data
        except TypeError:
          continue
        else:
          if t!=None: 
            if t.sort!=None and 'string' in t.sort and t.size>1:
              req_addr = t.address
              yeah = st.memory.load(req_addr,t.size-1)
              temp_string = st.solver.eval(yeah,cast_to=bytes).decode("utf-8")
              if temp_string in req_strings and node.addr not in loops_not_have_syscall:
                return temp_string

  return ''

syscall_list = {"clone":["clone","clone2","clone3"],
"close":["close", "fclose", "fcloseall", "pclose", "closedir", "closefrom", "closelog", "close_range"],
"creat":["creat","creat64"],
"dup":["dup","fcntl"],
"dup2":["dup2"],
"dup3":["dup3"],
"execve":["execl","execle","execlp","execv","execve","execvp","fexecve"],
"exit":["_exit","_Exit","atexit","exit","on_exit","thrd_exit"],
"exit_group":["exit_group"],
"fork":["fork","vfork","_Fork"],
"open":["catopen", "dirfd", "fdopen", "fdopendir", "fopen", "fopen64", "open", "open64", "opendir", "openlog"],
"openat":["openat"],
"rename":["rename"],
"renameat":["renameat"],
"unlink":["unlink"],
"unlinkat":["unlinkat"],
"vfork":["vfork"],
"connect":["connect"],
"accept":["accept"],
"accept4":["accept4"],
"bind":["bind"]
}


def get_predecessor_string2(cfg,node,G,entry,exits):
  node_vis = []
  cur_predecessor = list(G.predecessors(node))
  predecessor = []
  for ele in cur_predecessor:
    if ele not in node_vis:
      predecessor.append(ele)
      node_vis.append(ele)
  strings = set()
  while(len(predecessor)!=0):
    predec = predecessor.pop()
    have_string = extract_strings(predec,cfg)
    if (len(have_string)>0 and have_string in req_strings) or (predec.addr in exits) or (predec.addr==entry):
      strings.add((predec.addr,have_string))
      if(len(predecessor)==0):
        break
    
    else :
      pred_pred = list(G.predecessors(predec))
      for ele in pred_pred:
        if ele not in node_vis:
          node_vis.append(ele)
          predecessor.append(ele)
  return strings

#Add dummy nodes
def do_bfs(G,node,cfg,entry,exits):
  
  visited.add(node)
  queue.append(node)
  while queue:
    s = queue.pop(0)
    neighbours = list(G.successors(s))
    if neighbours!=None and len(neighbours)>0:
      for neighbour in neighbours:
        if neighbour not in visited:
          visited.add(neighbour)
          queue.append(neighbour)
          child_have_string = extract_strings(neighbour,cfg)
          child_node = (neighbour.addr,child_have_string)

          if len(child_have_string)>1 or (neighbour.addr in exits) or (neighbour.addr==entry):
            if child_node not in req_graph:
              req_graph[child_node] = set()
            predecessor_strings = get_predecessor_string2(cfg,neighbour,G,entry,exits)
            for strin in predecessor_strings:
              if strin not in req_graph:
                req_graph[strin] = set()
              req_graph[strin].add(child_node)

  return req_graph

def create_subgraph(G,cfg,entry,exits):
  visited.clear()
  req_graph.clear()
  nodes = list(G.nodes)
  for node in nodes:
    if node not in visited:
      do_bfs(G,node,cfg,entry,exits)
  temp_graph = req_graph.copy()
  return temp_graph

def convert_graph_to_dict(G):
  graph = {}
  nodes = list(G.nodes)
  if len(nodes)==0:
    return graph
  else:
    vis = set()
    queue = set()
    start_node = nodes[2]
    vis.add(start_node)
    queue.add(start_node)
    while queue:
      s = queue.pop()
      parent_string = extract_strings(s,cfg)
      parent_node = (s.addr,parent_string)
      if parent_node not in graph:
        graph[parent_node] = set()
      for n in list(G.successors(s)):
        if n not in vis:
          child_string = extract_strings(n,cfg)
          child_node = (n.addr,child_string)
          graph[parent_node].add(child_node)
          queue.add(n)
          vis.add(n)
    return graph


subgraph_dict = {}
def build_lms_path(cfg,not_check_func):
  for fun in not_check_func:
    exits = set()
    entry_func = cfg.kb.functions[fun]
    func_bbs = entry_func.block_addrs
    returns =  entry_func.get_call_sites()
    for keys in returns:
      exits.add(keys)
    exits.add(max(func_bbs))
    entry =  min(func_bbs)
    graph = entry_func._local_transition_graph

    ########################
    # if(entry_func.name == "execution_unit1"):
      # plot_func_graph(proj, graph, "%s_cfg" % (entry_func.name), asminst=True, vexinst=False)
      # hex_exit = [hex(ele) for ele in exits]
      # hex_entry = [hex(ele) for ele in entry]
      # print(hex_exit)
      # print(hex(entry))
    
    if graph is None:
      continue

    subgraph_graph = create_subgraph(graph,cfg,entry,exits)

    # if(entry_func.name == "execution_unit1"):
      # print(subgraph_graph)
    #   test_exe = {}
    #   temp_temp_temp = []
    #   for key,val in subgraph_graph.items():
    #     # test_exe[key] = list(val)
    #     for ele in val:
    #       temp_temp_temp.append(str(ele))
    #     test_exe[str(key)] = temp_temp_temp

      # test_graph = nx.DiGraph(test_exe)
      # nt = Network('1800px','1200px',directed=True)
      # nt.from_nx(test_graph)
      # nt.show('testGraph2.html')

    if(len(subgraph_graph)>0):
      exit_graph_tuple = (exits,subgraph_graph)
      subgraph_dict[entry_func.addr] = exit_graph_tuple


new_subgraph = {}
# final_graph = {}
def connect_subgraph(subgraph_dict,cfg):
  key_subgraph_dict = list(subgraph_dict.keys())
  for func_addr in subgraph_dict:
    exit_list = subgraph_dict[func_addr][0]
    subgraph = subgraph_dict[func_addr][1]
    subgraph_keys = list(subgraph.keys())
    entry_func = cfg.kb.functions[func_addr]
    for exit_addr in exit_list:
      exit_cfg_node = cfg.get_any_node(exit_addr)
      exit_succs = exit_cfg_node.successors
      if len(exit_succs)==0:
        continue
      else:
        exit_succ = exit_succs[0]
        exit_str = extract_strings(exit_cfg_node,cfg)
        exit_node = (exit_addr,exit_str)
        if (exit_node in subgraph_keys) and (exit_succ.addr in key_subgraph_dict):
          succ_keys = list(subgraph_dict[exit_succ.addr][1].keys())
          for key in succ_keys:
            subgraph[exit_node].add(key)
    new_subgraph.update(subgraph)

def find_predecessors(new_subgraph,del_node,successors):
  if len(successors)>0:
    for node in new_subgraph:
      for ele in new_subgraph[node]:
        if ele==del_node:
          for succ in successors:
            new_subgraph[ele].add(succ)

def del_dummy_nodes(new_subgraph):
  # for node in new_subgraph:
  #   addr,string = node
  #   if len(string)==0:
  #     successors = new_subgraph[node]
  #     predecessors = find_predecessors(new_subgraph,node,successors)
  # for node in new_subgraph:
  #   addr,string = node
  #   if len(string)!=0:
  #     final_graph[node] = new_subgraph[node]
  # for nodes in final_graph:
  #   temp = final_graph[nodes].copy()
  #   for node in temp:
  #     addr,string = node
  #     if(len(string)==0):
  #       final_graph[nodes].remove(node)

  final_graph = copy.deepcopy(new_subgraph) 
  print(final_graph)
  net_new_subgraph =  nx.DiGraph(new_subgraph)
  subgraph_nodes = net_new_subgraph.nodes
  # print(type(subgraph_nodes))
  for node in list(subgraph_nodes):
    # print(type(node))
    addr,string = node
    if len(string)==0:
      successors = net_new_subgraph.successors(node)
      predecessors = net_new_subgraph.predecessors(node)
      for ele in predecessors:
        for succ in successors:
          if ele!=node and succ!=node:
            final_graph[ele].add(succ)
            net_new_subgraph.add_edge(ele,succ)

      if node in final_graph:
        net_new_subgraph.remove_node(node)
        del final_graph[node]

  # final_graph_nodes = list(final_graph.keys())
  # for node in final_graph_nodes:
  #   addr,string = node
  #   if(len(string)==0):
  #     del final_graph[node]

  # print(final_graph)

  for nodes in final_graph:
    temp = final_graph[nodes].copy()
    for node in temp:
      addr,string = node
      if(len(string)==0):
        final_graph[nodes].remove(node)

  # print(final_graph)
  return final_graph

def get_syscall_function_name(function,lvl=4):
  function_names = []
  function_names.append(function.name)
  function_queue = set()
  function_queue.add((function,0))

  while function_queue:
    func,func_lvl = function_queue.pop()
    if func_lvl<lvl:
      function_bbs = func.get_call_sites()
      for bb in function_bbs:
        node = cfg.get_any_node(bb)
        for bb_succ in node.successors:
          func_addr = bb_succ.function_address
          successor_function = cfg.kb.functions[func_addr]
          function_names.append(successor_function.name)
          function_queue.add((successor_function,func_lvl+1))

  return function_names

def find_loops(cfg,functions):
  function_list = []
  for function in functions:
    function_list.append(cfg.kb.functions[function])
  loop_object = proj.analyses.LoopFinder(functions = function_list)
  loops_list = loop_object.loops
  
  #Check if any function has call to syscall functions from it (now checking only for immediate)

  for loop in loops_list:
    flag = 0
    for nodes in loop.body_nodes:
      block = cfg.get_any_node(nodes.addr)
      irsb = proj.factory.block(nodes.addr).vex
      if irsb.jumpkind == "Ijk_Call":
        for node in block.successors:
          try:
            func = cfg.kb.functions[node.addr]
          except:
            print("function not found at this "+str(node.addr))
          else:
            function_names = get_syscall_function_name(func)
            for name in function_names:
              for syscall in syscall_list:
                if name in syscall_list[syscall]:
                  flag = 1

      # elif "Ijk_Sys" in irsb.jumpkind:
      #   print("do something here")
      #   flag = 1

    if flag == 0:
      for nodes in loop.body_nodes:
        loops_not_have_syscall.append(nodes.addr)
    # if flag == 1:
    #   for nodes in loop.body_nodes:
    #     loops_have_syscall.append(nodes.addr)

  for loop in loops_list:
    max_block_addr = float('-inf')
    min_block_addr = float('inf')
    for nodes in loop.body_nodes:
      # print(len(extract_strings(nodes, cfg)))
      if len(extract_strings(nodes, cfg))>0:
        max_block_addr = max(max_block_addr, nodes.addr)
        min_block_addr = min(min_block_addr, nodes.addr)

    
    if max_block_addr!=float('-inf') and min_block_addr!=float('inf'):
      ending_syscall = []
      starting_syscall = []
      for nodes in loop.body_nodes:
        syscalls_made = []
        flag = 0
        block = cfg.get_any_node(nodes.addr)
        irsb = proj.factory.block(nodes.addr).vex
        if irsb.jumpkind == "Ijk_Call":
          for node in block.successors:
            try:
              func = cfg.kb.functions[node.addr]
            except:
              print("function not found at this "+str(node.addr))
              pass
            else:
              function_names = get_syscall_function_name(func)
              for name in function_names:
                for syscall in syscall_list:
                  if name in syscall_list[syscall]:
                    syscalls_made.append(syscall)
                    flag = 1

        # elif "Ijk_Sys" in irsb.jumpkind:
        #   flag = 1

        #min block addr is having address of starting lms
        #node.addr is the address of a syscall 
        if flag == 1:
          if nodes.addr<=min_block_addr:
            for syscall_name in syscalls_made:
              starting_syscall.append(syscall_name)

        #max_block_addr is having address of the ending lms
          if nodes.addr>=max_block_addr:
            for syscall_name in syscalls_made:
              ending_syscall.append(syscall_name)

      start_lms_string = extract_strings(cfg.get_any_node(min_block_addr), cfg)
      end_lms_string = extract_strings(cfg.get_any_node(max_block_addr), cfg)

      loop_starting[(min_block_addr,start_lms_string)] = starting_syscall
      loop_ending[(max_block_addr,end_lms_string)] = ending_syscall

  # print(loop_starting)
  # print(loop_ending)

def build_regex_from_lms(i):
    given_string = i
    given_string = given_string.strip()

    testing = "(%(?:[0-9]*[.][0-9]+)s)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%s", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)d)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%d", given_string)

    
    testing = "(%(?:[0-9]+)d)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%d", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)l)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%l", given_string)

    
    testing = "(%(?:[0-9]+)l)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%l", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)h)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%h", given_string)

    
    testing = "(%(?:[0-9]+)h)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%h", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)u)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%u", given_string)

    
    testing = "(%(?:[0-9]+)u)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%u", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)f)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%f", given_string)

    
    testing = "(%(?:[0-9]+)f)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%f", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)L)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%L", given_string)

    
    testing = "(%(?:[0-9]+)L)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%L", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)p)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%p", given_string)

    
    testing = "(%(?:[0-9]+)p)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%p", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)i)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%i", given_string)

    
    testing = "(%(?:[0-9]+)i)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%i", given_string)

    testing = "(%(?:[0-9]*[.][0-9]+)x)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%x", given_string)

    
    testing = "(%(?:[0-9]+)X)"
    expressions = re.findall(testing,given_string)
    for exp in expressions:
        given_string = re.sub(exp, "%X", given_string)

    given_string = given_string.translate(str.maketrans({"+":  r"\+",
                                          "]": r"\]",
                                          "[": r"\[",
                                          "(": r"\(",
                                          ")": r"\)",
                                          "{": r"\{",
                                          "}": r"\}",
                                          "|": r"\|",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          ".":  r"\."}))


    given_string = re.sub("%c", ".", given_string)
    given_string = re.sub("%s", ".*", given_string)
    given_string = re.sub("%m", ".*", given_string)
    given_string = re.sub("%M", ".*", given_string)
    
    #ADD %0i
    regex_for_oct = "[-+]?[0-7]+"
    given_string = re.sub("%o", regex_for_oct, given_string)

     #ADD %0i
    regex_for_pos_int = "[0-9]+"
    given_string = re.sub("%hu", regex_for_pos_int, given_string)
    given_string = re.sub("%lu", regex_for_pos_int, given_string)
    given_string = re.sub("%llu", regex_for_pos_int, given_string)
    given_string = re.sub("%u", regex_for_pos_int, given_string)

    #ADD %0.0 something
    regex_for_float_double = "[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)"
    given_string = re.sub("%f", regex_for_float_double, given_string)
    given_string = re.sub("%lf", regex_for_float_double, given_string)
    given_string = re.sub("%Lf", regex_for_float_double, given_string)

    # regex_for_address = ""
    regex_for_address = "(0x|0X)?[0-9a-f]{8}/i"
    given_string = re.sub("%p", regex_for_address, given_string)

    regex_for_hexadeciaml = "(0x)?[0-9a-f]{8}/i"
    given_string = re.sub("%x", regex_for_hexadeciaml, given_string)
    given_string = re.sub("%lx", regex_for_hexadeciaml, given_string)
    given_string = re.sub("%X", regex_for_hexadeciaml, given_string)

    #ADD %0i
    regex_for_int = "-?[0-9]+"
    given_string = re.sub("%hd", regex_for_int, given_string)
    given_string = re.sub("%hi", regex_for_int, given_string)
    given_string = re.sub("%i", regex_for_int, given_string)
    given_string = re.sub("%d", regex_for_int, given_string)
    given_string = re.sub("%ld", regex_for_int, given_string)
    given_string = re.sub("%li", regex_for_int, given_string)
    given_string = re.sub("%lld", regex_for_int, given_string)
    given_string = re.sub("%lli", regex_for_int, given_string)
    given_string = re.sub("%l", regex_for_int, given_string)

    return given_string
##################################################################################################
# For visualization use only
def convert_graph_to_regexV(final_graph):

  regex_graph = {}
  regex_loop_starting = {}
  regex_loop_ending = {}

  for node in final_graph:
    #OLd line below
    #new_node = (node[0],build_regex_from_lms(node[1]))
    #Edit to make the node id as an sring 
    new_node = str(node[0]) + ":" + str(build_regex_from_lms(node[1]))
    regex_graph[new_node] = set()
    for edge in final_graph[node]:
      #new_edge = (edge[0],build_regex_from_lms(edge[1]))
      new_edge = str(edge[0]) + ":" + str(build_regex_from_lms(edge[1]))
      regex_graph[new_node].add(new_edge)

  for node in loop_starting:
    # new_node = (node[0],build_regex_from_lms(node[1]))
    new_node = str(node[0]) + ":" +str(build_regex_from_lms(node[1]))
    regex_loop_starting[new_node] = loop_starting[node]

  for node in loop_ending:
    # new_node = (node[0],build_regex_from_lms(node[1]))
    new_node = str(node[0]) + ":" + str(build_regex_from_lms(node[1]))
    regex_loop_ending[new_node] = loop_ending[node]
  return regex_graph,regex_loop_starting,regex_loop_ending
##################################################################################################

  
  
def convert_graph_to_regex(final_graph):

  regex_graph = {}
  regex_loop_starting = {}
  regex_loop_ending = {}

  for node in final_graph:
    new_node = (node[0],build_regex_from_lms(node[1]))
    regex_graph[new_node] = set()
    for edge in final_graph[node]:
      new_edge = (edge[0],build_regex_from_lms(edge[1]))
      regex_graph[new_node].add(new_edge)

  for node in loop_starting:
    new_node = (node[0],build_regex_from_lms(node[1]))
    regex_loop_starting[new_node] = loop_starting[node]

  for node in loop_ending:
    new_node = (node[0],build_regex_from_lms(node[1]))
    regex_loop_ending[new_node] = loop_ending[node]

  


  return regex_graph,regex_loop_starting,regex_loop_ending

def convert_to_networkx(graph,regex_loop_starting,regex_loop_ending):
  G = nx.DiGraph(graph)
  for node in G.nodes:
    if node in regex_loop_starting:
      G.nodes[node]["is_start"] = 1
      G.nodes[node]["start_syscall"] = regex_loop_starting[node]
    else:
      G.nodes[node]["is_start"] = 0
      G.nodes[node]["start_syscall"] = []

    if node in regex_loop_ending:
      G.nodes[node]["is_end"] = 1
      G.nodes[node]["end_syscall"] = regex_loop_ending[node]
    else:
      G.nodes[node]["is_end"] = 0
      G.nodes[node]["end_syscall"] = []

    G.nodes[node]["lms"] = node[1]
  return G

cfg,check_func,not_check_func = log_functions() #Functions having log message strings
# plot_cfg(cfg,"test_cfg", remove_imports=True, remove_path_terminator=True)
req_func = extract_call_sites(cfg,check_func) #Get parent functions 
req_strings = peephole(cfg,req_func,3) #Use peephole to find all log message strings
find_loops(cfg, not_check_func) #Function to find starting and ending lms and syscall after ending lms or before starting lms
build_lms_path(cfg,not_check_func) #Building LMS Graph for each function
connect_subgraph(subgraph_dict,cfg) #Connect subgraphs with each other as mentioned
# print(new_subgraph)
final_graph = del_dummy_nodes(new_subgraph) # To do delete fake node and put all in one dictionary
# print(final_graph)
##################################################################################################
# Generate a graph for visualization
if args.visualize:
    visual_graph,_,_ = convert_graph_to_regexV(final_graph) #convert all lms into regex expression    
    V = nx.DiGraph(visual_graph)
    try:
        nt = Network('1800px','1200px',directed=True)
        nt.show_buttons(filter_=['physics'])
        nt.repulsion(central_gravity=0)
        nt.from_nx(V)
        nt.show('lms_control_flow_graph.html')
    except:
        pass
##################################################################################################
regex_graph,regex_loop_starting,regex_loop_ending = convert_graph_to_regex(final_graph) #convert all lms into regex expression

networkxx_graph = convert_to_networkx(regex_graph,regex_loop_starting,regex_loop_ending)
json_converted = json_graph.node_link_data(networkxx_graph)
with open("graph.json","w") as outfile:
  json.dump(json_converted,outfile,indent = 4)
