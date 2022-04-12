bash experimentalscripts/getStat.sh > outputs/usageStatFile.txt&
FOO_PID=$!
python3 static_analysis/lms_cfg_gen.py --exe=binaries/apache2 > /dev/null 2>&1
kill $FOO_PID
