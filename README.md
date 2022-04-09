
# Project_ALV_2022

# Environment Setup
## Install Oracle VirtualBox using CLI in Ubuntu
1. Update current packages of the system to the latest version.
```bash
   utkalika@smrworkstation3:~$ sudo apt-get update
   utkalika@smrworkstation3:~$ sudo apt-get upgrade
```
2. Configure Apt Repository
Import the Oracle public key to your system signed the Debian packages using the following commands.
```bash
   utkalika@smrworkstation3:~$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
   utkalika@smrworkstation3:~$ wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
```
Now, you need to add Oracle VirtualBox PPA to Ubuntu system.
```bash
   utkalika@smrworkstation3:~$ sudo add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian bionic contrib"
```
This command will add an entry to /etc/apt/sources.list at end of the file.

3. Install Oracle VirtualBox
```bash
   utkalika@smrworkstation3:~$ sudo apt-get update
   utkalika@smrworkstation3:~$ sudo apt-get install virtualbox-5.2
```

## Create & Manage VM using VBoxManage

### Create the Virtual Machine
```bash
   utkalika@smrworkstation3:~$ vboxmanage createvm --name "Ubuntu18.04" --ostype "Ubuntu_64" --register
```
### You can check your machine info:
```bash
   utkalika@smrworkstation3:~$ vboxmanage showvminfo Ubuntu18.04
```
### Set Memory
```bash
   utkalika@smrworkstation3:~$ vboxmanage modifyvm Ubuntu18.04 --memory 2048
```
### Set CpUs
```bash
   utkalika@smrworkstation3:~$ vboxmanage modifyvm Ubuntu18.04 --cpus 2
```
### Set IOAPIC
```bash
   utkalika@smrworkstation3:~$ vboxmanage modifyvm Ubuntu18.04 --ioapic on
```
### Set Network Configuration
```bash
   utkalika@smrworkstation3:~$  vboxmanage modifyvm Ubuntu18.04 --nic1 nat
```
### Create the Hard Drive and Attach It
```bash
   utkalika@smrworkstation3:~$ VBoxManage createhd --filename VirtualBox\ VMs/Ubuntu18.04/Ubuntu18.04.vdi --size 18000 --format VDI
   utkalika@smrworkstation3:~$ vboxmanage storagectl Ubuntu18.04 --name "SATA Controller" --add sata --controller IntelAhci
   utkalika@smrworkstation3:~$ vboxmanage storageattach Ubuntu18.04 --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium VirtualBox\ VMs/Ubuntu18.04/Ubuntu18.04.vdi
```
### Mount CD-ROM
You need to mount a cd/dvd rom to your VM in order to start the OS installation. I've already downloaded and copied the ISO file to smrl3 server so I am mounting it here.
```bash
   utkalika@smrworkstation3:~$ vboxmanage storagectl Ubuntu18.04 --name "IDE Controller" --add ide --controller PIIX4
   utkalika@smrworkstation3:~$ vboxmanage storageattach Ubuntu18.04 --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium ubuntu-20.04.2.0-desktop-amd64.iso
```
### You can check your machine info:
```bash
   utkalika@smrworkstation3:~$ vboxmanage showvminfo Ubuntu18.04
```
### Start the VM
You can either start the VM from the GUI or you can start it up using VRDE.
```bash
   utkalika@smrworkstation3:~$ vboxmanage modifyvm Ubuntu18.04 --vrde on
   utkalika@smrworkstation3:~$ vboxmanage modifyvm Ubuntu18.04 --vrdemulticon on --vrdeport 10001
   utkalika@smrworkstation3:~$ vboxheadless --startvm Ubuntu18.04
   or
   utkalika@smrworkstation3:~$ VBoxManage startvm "Ubuntu18.04" --type headless
```
### Connect to it
Port Forwarding is done at port 2203.

Fisrt time, connected smrl3 through Remote Desktop and made the port Forwarding Configuration for TCP in VM.

Then sshed to VM from host machine.
```bash
   utkalika@smrworkstation3:~$ ssh alv-iitkgp@10.5.20.130 -p 2203
```

## Port Forwarding for SSH & HTTP on VirtualBox

1. Configuring SSH
```bash
   sudo apt-get install openssh-server
```
2. Now make sure your SSH service is running in your background
```bash
   sudo service ssh status
```
3. Add Port forwarding Rules

   VirtualBox -> Ubuntu18.04 VM(Power off) > Setting
```bash
   Name: ssh
   Protocol: TCP
   Host Port: 2203
   Guest Port: 22
```
```bash
   Name: http
   Protocol: TCP
   Host Port: 8800
   Guest Port: 80
```
Port 22 is the default SSH port and the port 80 is reserved for HTTP serving. Now what we have done is, asking the idle port 2203 of our host machine to listen to the port 22 of the guest VM. So through the localhost of our host machine, we can remote login to VM. On the other hand, the same has done for the HTTP serving.


# Testing
## LMS CGF Genearion Phase
Static analysis on binaries to detemine the LMS and CFG to determine the relationship between the LMS
```bash
	python3 lms_cfg_gen.py --exe <path of binary file>
```
E.g.
```bash
	 python3 .\static_analysis\lms_cfg_gen.py --exe ./binaries/apache2 
```
On successful execution of the program, a graph.json file will be created.



## Universal Log File Generation

1. Parsing the audit logs into json format
```bash	
    python3 parsetojson.py <path to audit log> > <output file name>
```	
E.g.
```bash
    python3 ULF_generation/parsetojson.py samplelogs/audit_1640089505.log > samplelogs/audit_1640089505.json
```
The output file will contain the logs in json format
	
2. Combine the json formatted audit logs based on the srn
```bash
    sort samplelogs/audit_1640089505.json > samplelogs/audit_1640089505_sorted.json
```
```bash
    python3 merge_json.py <output filename> > <merged output filename>
```
E.g.
```bash
    python3 ULF_generation/merge_json.py samplelogs/audit_1640089505_sorted.json > samplelogs/audit_1640089505_merged.json
```
3. Combine the application logs and audit log into a single file named data1.json
```bash
    python3 ULF_generation/ULF_gen.py
```
4. Sort the universal log file based on date/ts, generates the universal_log.json
```bash
    python3 ULF_generation/sort_ULF.py
```

## Construction of the Universal Provenance Graph
To-do: Changes are required to the code to take the path of the graph.json and universal_log.json as per the local machine
	
```bash
	python3 ./UPG_construction/upg_gen.py
```	
Generates package-lock, sample_output and provenanceGraph.html as an output.

# Complete Sequence
```bash
	cd static_analysis
	python3 lms_cfg_gen.py --exe ../binaries/apache2
```	
```bash
	cd ULF_generation
	python3 parsetojson.py samplelogs/audit_1640089505.log > audit_164.json
	sort audit_164.json > audit_164s.json
	python3 merge_json.py audit_164s.json > audit_164m.json
	Open the ULF_gen.py in an editor and make the following changes : 
		-> parse_audit_log("../../LOGS_0311/audit_ap2.json")    ---->(change with the line)----> parse_audit_log('./audit_164m.json')
		-> parse_error_log('../../LOGS_0311/access_1640089505.log')   ---->(change with the line)---->  parse_error_log('../samplelogs/access_1640089505.log')
		-> parse_error_log('../../LOGS_0311/error_1640089505.log')    ---->(change with the line)---->   parse_error_log('../samplelogs/error_1640089505.log')
	python3 ULF_gen.py
	python3 sort_ULF.py 	#this will generate an universal_log.json file
```
```bash
    cd ../UPG_construction
	Open the upg_gen file in the text editor and make the following changes
		-> f = open("graph.json",)  ---->(change with the line)----> f = open("../static_analysis/graph.json",)
		-> f = open("universal_log.json",)  ---->(change with the line)----> f = open("../ULF_generation/universal_log.json",)
	python3 upg_gen.py		
```
This will generate a provenanceGraph.html file which is the graph. It can be viewed in a browser.

## Appendix

1. https://www.virtualbox.org/manual/ch08.html#vboxmanage-showvminfo
2. https://networking.ringofsaturn.com/Unix/Create_Virtual_Machine_VBoxManage.php
3. https://tecadmin.net/install-oracle-virtualbox-on-ubuntu/
4. https://www.nakivo.com/blog/virtualbox-network-setting-guide/
5. https://www.oracle.com/technical-resources/articles/it-infrastructure/admin-manage-vbox-cli.html
6.  https://medium.com/platform-engineer/port-forwarding-for-ssh-http-on-virtualbox-459277a888be
