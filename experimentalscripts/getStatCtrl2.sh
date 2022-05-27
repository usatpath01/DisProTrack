bash experimentalscripts/getStat2.sh > outputs/usageStatFile_upg.txt&
FOO_PID=$!
python3 UPG_construction/upg_gen.py > /dev/null 2>&1
kill $FOO_PID
