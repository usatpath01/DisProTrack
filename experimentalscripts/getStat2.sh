while true; do ps  -o %cpu,%mem,cmd -a |  grep "python3 UPG_construction/upg_gen.py" | grep -Eiv grep ; sleep 0.5; done
