while true; do ps  -o %cpu,%mem,cmd -a |  grep "python3 static_analysis/lms_cfg_gen.py" | grep -Eiv grep ; sleep 1; done
