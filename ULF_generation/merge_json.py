#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 18:37:21 2021

@author: rst1996
"""

import networkx as nx
import matplotlib.pyplot as plt
import socket
import struct
import sys
import time
import psutil
import os

def memory_usage_psutil():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem


def decodeHexToASCII(hex_string):
    try:
        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")
        
        return ascii_string.replace('\x00',' ')
    except:
        return hex_string

def hexToIP(hex_string):
    addr_long = int(hex_string, 16)
    return socket.inet_ntoa(struct.pack("<L", addr_long))



def generate(fname):
    lastSRN = -1
    file = open(fname,"r")
    data = {}
    for line in file.readlines():
        line = line.strip()
        j = eval(line)
        if(j['srn'] != lastSRN):
            # analyze the last data record
            # for now just printing it
            if( len(data.keys()) > 1 ):
                print(data)
            # Flush the data record
            data = {}
            data['srn'] = j['srn']
            data['ts'] = j['ts']
            lastSRN = j['srn']
            
        if(j['type'] == 'SYSCALL'):
            if ('data' in j ):
                j_data = j['data']
                if('syscall' in j_data):
                    data['syscall_id'] = j_data['syscall']
                if('SYSCALL' in j_data):
                    data['syscall_name'] = j_data['SYSCALL']
                if('a0' in j_data):
                    data['arg0'] = j_data['a0']
                    
                if('a1' in j_data):
                    data['arg1'] = j_data['a1']
                    
                if('a2' in j_data):
                    data['arg2'] = j_data['a2']
                    
                if('a3' in j_data):
                    data['arg3'] = j_data['a3']
                    
                if('pid' in j_data):
                    data['pid'] = j_data['pid']
                    
                if('ppid' in j_data):
                    data['ppid'] = j_data['ppid']
                
                if('exe' in j_data):
                    data['exe'] = j_data['exe']
                
                if('exit' in j_data):
                    data['exit'] = j_data['exit']
            
        elif (j['type'] == 'CWD'):
            if('data' in j and 'cwd' in j['data']):
                data['cwd'] = j['data']['cwd']
            
        elif ((j['type'] == 'PATH')):
            if ('data' in j ):
                j_data = j['data']

                if('nametype' in j_data and (j_data['nametype'] == 'CREATE' or j_data['nametype'] == 'NORMAL')) or ('nametype' not in j_data):
                    if('name' in j_data):
                        data['path_name'] = j_data['name']
                
                    if('inode' in j_data):
                        data['inode'] = j_data['inode']

                    if('mode' in j_data):
                        data['path_perm'] = j_data['mode']
                elif('nametype' in j_data and j_data['nametype'] == 'DELETE'):
                    if('name' in j_data):
                        data['path_name_old'] = j_data['name']
                
                    if('inode' in j_data):
                        data['inode_old'] = j_data['inode']

                    if('mode' in j_data):
                        data['path_perm_old'] = j_data['mode']

                

            
        elif((j['type'] == 'PROCTITLE')):
            if('data' in j and 'proctitle' in j['data']):
                proc = j['data']['proctitle']
                data['cmdline'] = decodeHexToASCII(proc)

        elif(j['type'] == 'SOCKADDR'):

            if ('data' in j ):
                j_data = j['data']

                # Added Else case for this instances:
                # saddr=00000000000000000000000000000000 SADDR=unknown-family(0)

                if('SADDR' in j_data and 'unknown-family' in j_data['SADDR']):
                    data['sock_path'] = 'unknown-family(0)'
                    

                if('path' in j_data):
                    data['sock_path'] = j_data['path']
                


                
                if('laddr' in j_data):
                    data['sock_laddr'] = j_data['laddr']
                
                
                if('lport' in j_data):
                    data['sock_lport'] = j_data['lport']
    if( len(data.keys()) > 1 ):
        print(data)
            
            
        


#generate('audit_1625813282.stxt')

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        start_time = time.time()
        generate(sys.argv[1])
    else:
        print("Please provide the log file in the cmdline")

with open("outputs/time_resource_util.txt","a+") as logfile:
	stats = "ULF_gen - merge_json - "+ ", Memory: " + str(memory_usage_psutil()) + ", Execution Time: " + str((time.time() - start_time)) + ", CPU utilization as a % " + str(psutil.cpu_percent()) + ", CPU Stats" + str(psutil.cpu_stats()) + ", CPU Frequency" + str(psutil.cpu_freq()) + "\n"
	# logfile.seek(0)
	# data = logfile.read(100)
	# if len(data) > 0:
	# 	logfile.write("\n")
	logfile.write(stats)
	logfile.close()

