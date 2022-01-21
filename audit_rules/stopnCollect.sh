#stop the services...

service auditd stop
# service mysql stop
service apache2 stop

# rename the log files
mkdir LOGS_0311
cp /var/log/audit/audit.log LOGS_0311/audit_$(date '+%s').log
mv /var/log/audit/audit.log /var/log/audit/audit_$(date '+%s').log

cp /var/log/apache2/access.log LOGS_0311/access_$(date '+%s').log
mv /var/log/apache2/access.log /var/log/apache2/access_$(date '+%s').log

cp /var/log/apache2/error.log LOGS_0311/error_$(date '+%s').log
mv /var/log/apache2/error.log /var/log/apache2/error_$(date '+%s').log







