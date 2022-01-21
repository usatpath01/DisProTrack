#stop the services...

service auditd stop
service mysql stop
service apache2 stop

# rename the log files
mv /var/log/audit/audit.log /var/log/audit/audit_$(date '+%s').log
mv /var/log/mysql/query.log /var/log/mysql/query_$(date '+%s').log
mv /var/log/mysql/error.log /var/log/mysql/error_$(date '+%s').log
mv /var/log/apache2/access.log /var/log/apache2/access_$(date '+%s').log
mv /var/log/apache2/error.log /var/log/apache2/error_$(date '+%s').log








