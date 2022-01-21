#start the audit service
service auditd start

sudo auditctl -D
sudo auditctl -a always,exit -F arch=b64 -S bind -S connect -S accept -S accept4 -S clone -S close -S creat -S dup -S dup2 -S dup3 -S execve -S exit -S exit_group -S fork -S open -S openat -S rename -S renameat -S unlink -S unlinkat -S vfork -S read -S write -F success=1 -F exe=/usr/sbin/apache2

# Add the audit rules
#python3  /home/rst1996/MTP/AVL/wrapper2.py nf

#start mysql service 
#service mysql start

#start apache2 service 
service apache2 start
