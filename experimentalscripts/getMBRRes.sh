python3 static_analysis/lms_cfg_gen.py --exe=binaries/php-fpm --mb=2 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/php-fpm --mb=3 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/php-fpm --mb=4 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/php-fpm --mb=5 > /dev/null 2>&1
echo "PHP-FPM DONE"
python3 static_analysis/lms_cfg_gen.py --exe=binaries/httpd --mb=2 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/httpd --mb=3 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/httpd --mb=4 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/httpd --mb=5 > /dev/null 2>&1
echo "ApacHE2 DONE"
python3 static_analysis/lms_cfg_gen.py --exe=binaries/mysql --mb=2 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/mysql --mb=3 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/mysql --mb=5 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/mysql --mb=4 > /dev/null 2>&1
echo "MYSQL DONE"
