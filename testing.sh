#! /bin/bash

LOG_FILE_NAME="audit_1639762173"
echo "${LOG_FILE_NAME}"

python3 ~/Project_ALV_2022/static_analysis/lms_cfg_gen.py --exe ~/Project_ALV_2022/binaries/apache2 

python3 ~/Project_ALV_2022/ULF_generation/parsetojson.py ~/Project_ALV_2022/samplelogs/${LOG_FILE_NAME}.log > ~/Project_ALV_2022/samplelogs/${LOG_FILE_NAME}.json

sort ~/Project_ALV_2022/samplelogs/${LOG_FILE_NAME}.json > ~/Project_ALV_2022/samplelogs/${LOG_FILE_NAME}_sorted.json

python3 ~/Project_ALV_2022/ULF_generation/merge_json.py ~/Project_ALV_2022/samplelogs/${LOG_FILE_NAME}_sorted.json > ~/Project_ALV_2022/samplelogs/${LOG_FILE_NAME}_merged.json

python3 ~/Project_ALV_2022/ULF_generation/ULF_gen.py

python3 ~/Project_ALV_2022/ULF_generation/sort_ULF.py

python3 ~/Project_ALV_2022/UPG_construction/upg_gen.py

rm -i ~/Project_ALV_2022/outputs/*.json ~/Project_ALV_2022/outputs/*.html
