while true; do ps  -o %cpu,%mem,cmd -a |  grep "python3 ULF_generation/ULF_gen.py" | grep -Eiv grep ; sleep 0.01; done
