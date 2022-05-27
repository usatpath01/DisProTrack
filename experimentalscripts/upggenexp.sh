#For lookahead 12
cp outputs_s1_1639762173/universal_log.json outputs/universal_log.json 
python3 UPG_construction/upg_gen.py 12
python3 UPG_construction/upg_gen.py 15
python3 UPG_construction/upg_gen.py 18

#For lookahead 15
cp outputs_s2_1639807887/universal_log.json outputs/universal_log.json 
python3 UPG_construction/upg_gen.py 12
python3 UPG_construction/upg_gen.py 15
python3 UPG_construction/upg_gen.py 18

#For lookahead 18
cp outputs_s3_1640089505/universal_log.json outputs/universal_log.json 
python3 UPG_construction/upg_gen.py 12
python3 UPG_construction/upg_gen.py 15
python3 UPG_construction/upg_gen.py 18