# Installation of services

## Install Auditd on Ubuntu Linux
1. Install Bash if not present, on your Ubuntu system
```bash
   sudo apt update
   sudo apt install bash-completion
```
2. Now Install Auditd
```bash
   sudo apt-get install auditd
```

## Install & Configure Apache Web Server on Ubuntu Linux
1. Install Bash if not present, on your Ubuntu system
```bash
   sudo apt update
```
2. Now Install Apache2
```bash
   sudo apt install apache2
   apache2 -version
```
3. Firewall configuration
```bash
   sudo ufw app list
```
The above cmd will show different apache profiles.

We will use the highly restrictive profile ‘Apache’ to enable network ctivity on port 80.
```bash
   sudo ufw allow ‘Apache’
```
```bash
   sudo ufw status
```
The above cmd will show Apache allowed in firewall.
4. To check apache service is operational or not
```bash
   sudo systemctl status apache2
```
5. Go to browser and search http://10.5.20.130:8800 or http://10.5.20.130:8800/webapp/todo/login.php

It will redirect to the apache homepage.

Else, in cmd type :
```bash
   wget http://10.5.20.130:8800 
   wget http://10.5.20.130:8800/webapp/todo/login.php
```

# Audit Rules
Script Name :: wrapper2.py
To set the rules for the auditd module.

Usage
------
wrapper2.py network : for setting rules to track network related syscalls only for the PIDs od the specidifed process and theier child

wrapper2.py all : for setting rules to track all the syscall mentioned in the lists for the PIDs od the specidifed process and theier child

wrapper2.py nf : for setting rules to track all the syscall mentioned in the list for all the process

# To generate Logs
#### Note: First load the LKM (new_lkm.ko) to get enhanced log i.e. the pid and datetime will be prefixed
1. First stop all the services (auditd, mysql, apache2)
```bash
   $ sudo bash stopScript.sh
```
2. It will start the audit service, add the audit rules and start the apache2 and mysql services
```bash
   $ sudo bash startScript.sh
```
3. check the status
```bash
   $ ps -eall | grep 'apache2'
```
4. Then do some web browsing to generate logs
5. Run the following script to stop the services and collect the logs for that session
```bash
   $ sudo bash stopnCollect.sh
```
The logs will be generated in a folder "LOGS_0311" in the current directory i.e. in "audit_rules" directory.

These logs are the input for the "ULF_generation" Phase
## Appendix
1. https://dev.to/ajaykdl/how-to-setup-auditd-on-ubuntu-jfk
2. https://linuxhint.com/install_apache_web_server_ubuntu/
