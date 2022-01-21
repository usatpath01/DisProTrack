#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 21:13:53 2021

@author: rst1996
"""

import sys
import os
from subprocess import check_output


# process_names =  ["apache2","vsftpd","mysqld"]
process_names = ["apache2"]


def getPIDs(pname):
    try:
        return list(map(int,check_output(["pidof",pname]).split()))
    except:
        return []



def getParent(pidlist):
    for pid in pidlist:
        p = int(check_output(['ps','-o','ppid=-p', str(pid) ]).split()[-1])
        if(p == 1):
            return pid
        else:
            return p
        
        
cmd = "auditctl"
arg1 = "-a always,exit -F arch=b64"
syscall_network = "-S bind -S connect -S accept -S accept4"
syscall_all = "-S bind -S connect -S accept -S accept4 -S clone -S close -S creat -S dup -S dup2 -S dup3 -S execve -S exit -S exit_group -S fork -S open -S openat -S rename -S renameat -S unlink -S unlinkat -S vfork "
syscall_rw = "-S read -S write "
filter1 = "-F success=1 "
pidfilter = "-F pid="
ppidfilter = "-F ppid="

if __name__ == "__main__":
    if( len(sys.argv) > 1 ):
        if(sys.argv[1] == 'network'):
            for pname in process_names:
                pidlist = getPIDs(pname)
                
                ppid = getParent(pidlist)
                
                # Set the rule for the parent process
                pf = pidfilter+str(ppid)
                rname = "-k " + sys.argv[1]+ "_parent"
                #check_output([cmd,arg1,syscall,pf,filter1,rname]);
                ruleCmd = " ".join([cmd,arg1,syscall_network,pf,filter1,rname])
                os.system(ruleCmd)
                
                # set the rule for the child process
                pf = ppidfilter+str(ppid)
                rname = "-k " + sys.argv[1]+ "_child"
                # check_output([cmd,arg1,syscall,pf,filter1,rname]);
                ruleCmd = " ".join([cmd,arg1,syscall_network,pf,filter1,rname])
                os.system(ruleCmd)
        elif(sys.argv[1] == 'all'):
            for pname in process_names:
                pidlist = getPIDs(pname)
                
                ppid = getParent(pidlist)
                
                # Set the rule for the parent process
                pf = pidfilter+str(ppid)
                rname = "-k " + pname+ "_parent"
                #check_output([cmd,arg1,syscall,pf,filter1,rname]);
                # ruleCmd = " ".join([cmd,arg1,syscall_all,pf,filter1,rname])
                ruleCmd = " ".join([cmd,arg1,syscall_all,syscall_rw,pf,filter1,rname])
                
                os.system(ruleCmd)
                
                # set the rule for the child process
                pf = ppidfilter+str(ppid)
                rname = "-k " + pname+ "_child"
                # check_output([cmd,arg1,syscall,pf,filter1,rname]);
                # ruleCmd = " ".join([cmd,arg1,syscall_all,pf,filter1,rname])
                ruleCmd = " ".join([cmd,arg1,syscall_all, syscall_rw,pf,filter1,rname])
                
                os.system(ruleCmd)
        elif(sys.argv[1] == 'nf'):
            ruleCmd = " ".join([cmd,arg1,syscall_all,syscall_rw,filter1])
            print(ruleCmd)
            os.system(ruleCmd)
        else:
            print("No rules impemented")
    else:
        print("Please provide the tracking option e.g. network")
