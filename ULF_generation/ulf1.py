# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 23:57:20 2021

@author: utkal
"""

import json
from shlex import shlex
import re
import sys
import datetime
from datetime import datetime
import time
#from pandas import json_normalize
#import sort_log_files

def parse_kv_pairs(text, item_sep=" ", value_sep="="):
    lexer = shlex(text, posix=True)
    lexer.whitespace = item_sep
    lexer.wordchars += value_sep + ":().{}\"'_-/"
    d = {}
    for w in lexer:
        try:
            a,b =  w.split(value_sep, maxsplit=1)
            if(a == "msg" and not b.startswith("audit")):
                d[a] = parse_kv_pairs(b)
            else:
                d[a] = b
        except:
            pass
    return d
    #return dict(word.split(value_sep, maxsplit=1) for word in lexer)


# file = open("aduitdemo.txt","r")


'''
Method 1 || Drawback :: msg gets overwritten
for line in file.readlines():
    line = line.strip();
    print(parse_kv_pairs(line))
file.close()
'''

# msg gets overwritten 
def parse1(fname):
    file = open(fname,"r")
    for line in file.readlines():
        line = line.strip();
        line.replace("\x1d"," ")
        print(parse_kv_pairs(line))
    file.close()


# override fixed
def parse_audit_log(fname):
    file = open(fname,"r")
    for line in file.readlines():
        line = line.strip()
        
        # line.replace("\x1d"," ")
        # tkns = line.split('):')
        # tt = re.findall(r'type=(.*) msg=audit\((\d*.\d*):(\d*)',tkns[0])
        
        # pid = re.findall(r'pid = \d*',tkns[0])   
        # date = re.findall(r'date = \[\d*]',tkns[0])
        
        # tmpDate = int(float(tt[0][1]) * 1000000000)

        # # dt = datetime.fromtimestamp(tmpDate // 1000000000)
        # dt = datetime.fromtimestamp(float(tt[0][1]))
        # s = dt.strftime('%Y-%m-%d %H:%M:%S')
        # s += '.' + str(int(tmpDate % 1000000000)).zfill(9)
        


       
        # j = {}
        # j["Date"] = s
        # for i in pid:
        #     j["pid"] = i.split('=')[1].strip()

        # j["srn"] = tt[0][2]
        # j["ts"] = tt[0][1]
        # j["type"] = tt[0][0]
        # j["data"] = parse_kv_pairs(tkns[1])

        j = eval(line)

        # Append the date field 

        tmpDate = int(float(j['ts']) * 1000000000)
        # j["ts"] = tmpDate
        dt = datetime.fromtimestamp(float(j['ts']))
        s = dt.strftime('%Y-%m-%d %H:%M:%S')
        s += '.' + str(int(tmpDate % 1000000000)).zfill(9)
        j["Date"] = s
        j["ts"] = tmpDate


        print(j)
        with open('data.json', 'a') as f:
            json.dump(j, f, indent=2)
        
        
        #the_datetime = datetime.datetime.fromtimestamp( epoch_time )  
        
        #epoch_time = datetime.datetime(1960, 6, 10, 0, 0).timestamp()  
        #print( "Unix epoch time:", epoch_time )  
        #print( "DateTime:", datetime_str )  
        #print( "DateTime:", the_datetime ) 
        
        #print(parse_kv_pairs(tkns[1]))
    file.close()

# parse2('audit_1625813282.log')

def parse_acess_log(fname):
    file = open(fname,"r")
    for line in file.readlines():
        line = line.strip();
        tkns = line.split('- -')

        pid = re.findall(r'pid = \d*',tkns[0])  
        date = re.findall(r'date = \[\d*]',tkns[0])
        ip = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3})', tkns[0])
        
       
        j = {}
        for i in pid:
            j["pid"] = i.split('=')[1]
        for i in date:
            temp = i.split('=')[1].strip();
            result = re.search(r"\[([0-9_]+)\]", temp)
            temp = int(result.group(1))
            dt = datetime.fromtimestamp(temp // 1000000000)
            s = dt.strftime('%Y-%m-%d %H:%M:%S')
            s += '.' + str(int(temp % 1000000000)).zfill(9)
            #print(s)
            j["Date"] = s
            #j['epoch'] = result.group(1)
        
        j["lms"] = tkns[1]
            #j["ip"] = ip
        #tkns1 = tkns[1].split('] ')
        #print(tkns1)

        
        print(j)
        with open('data.json', 'a') as f:
            json.dump(j, f, indent=2)             
        
        #the_datetime = datetime.datetime.fromtimestamp( epoch_time )  
        
        #epoch_time = datetime.datetime(1960, 6, 10, 0, 0).timestamp()  
        #print( "Unix epoch time:", epoch_time )  
        #print( "DateTime:", datetime_str )  
        #print( "DateTime:", the_datetime ) 
        
        #print(parse_kv_pairs(tkns[1]))
    file.close()
    


def parse_error_log(fname):
    file = open(fname,"r")
    for line in file.readlines():
        line = line.strip();
        try:        
            pid = re.findall(r'pid = \d*',line)  
            date = re.findall(r'date = \[\d*]',line)
            #tt3 = re.findall(r'(\w{3})\s(\w{3})\s(\d{2})\s(\d+)(\:)(\d+)(\:)(\d+)(\.)(\d+)\s(\d{4})', tkns[0])
                    
            tt3 = re.findall(r"^(pid \= \d+)\, (date \= \[\d+\])(.*)", line)
            print('tt3', tt3)
            j = {}
            for i in pid:
                j["pid"] = int(i.split('=')[1])
                
            for i in date:
                temp = i.split('=')[1].strip();
                result = re.search(r"\[([0-9_]+)\]", temp)
                temp = int(result.group(1))
                j["ts"] = temp
                dt = datetime.fromtimestamp(temp // 1000000000)
                s = dt.strftime('%Y-%m-%d %H:%M:%S')
                s += '.' + str(int(temp % 1000000000)).zfill(9)
                #print(s)
                j["Date"] = s
                #j['epoch'] = result.group(1)
                    

            j["lms"] = tt3[0][2].strip()
        
        
            print(j)
            with open('data.json', 'a') as f:
                json.dump(j, f, indent=2)             
        except:
            pass

        #the_datetime = datetime.datetime.fromtimestamp( epoch_time )  
        
        #epoch_time = datetime.datetime(1960, 6, 10, 0, 0).timestamp()  
        #print( "Unix epoch time:", epoch_time )  
        #print( "DateTime:", datetime_str )  
        #print( "DateTime:", the_datetime ) 
        
        #print(parse_kv_pairs(tkns[1]))
    file.close()
    
# For parsing audit log use parse_audit_log
# For parsing other log files use parse_error_log
if __name__ == '__main__':
    #if(len(sys.argv) > 1):
    #    parse2(sys.argv[1])
    #else:
    #    print("Please provide the log file in the cmdline")

    # Parding teh audit log
    parse_audit_log("./audit_164m.json")

    # #print("ACCESS LOG--->")
    # parse_acess_log("../logs/apache/rst1996/home/augumentedLogs/access.log")
    # #parse_acess_log("access.log")
    # #print("\nERROR LOG---->")
    # #parse_error_log("../omegalog_implementation/logs/apache/rst1996/home/augumentedLogs/error.log")
    # parse_error_log("../logs/apache/testerror.log")
    
    parse_error_log('../samplelogs/access_1640089505.log')
    # print('\n\n************Apache access log parsed\n\n')

    parse_error_log('../samplelogs/error_1640089505.log')
    # print('\n\n************Apache access log parsed\n\n')

    # parse_error_log('mysql_logs/error_1633698258.log')
    # print('\n\n************MySQL error log parsed\n\n')

    # parse_error_log('mysql_logs/query_1633698258.log')
    # print('\n\n************MySQL query log parsed\n\n')

    
    fin = open("data.json", "rt")
    fout = open("data1.json", "wt")
    
    for line in fin:
        	fout.write(line.replace('}\n}{',"}\n},{").replace('}{', '},{'))
        #close input and output files
    fin.close()
    fout.close()
    
    #exec(open('sort_log_files.py').read())
