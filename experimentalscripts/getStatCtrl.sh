bash experimentalscripts/getStat.sh > outputs/usageStatFile_ulf.txt&
FOO_PID=$!
python3 ULF_generation/ULF_gen.py > /dev/null 2>&1
kill $FOO_PID
