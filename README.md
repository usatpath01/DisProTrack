# Project_ALV_2022

```bash
	# static analysis on binaries to detemine the LMS and CFA to determine the relationship between the LMS
	cd static_analysis
	python3 lms_cfg_gen.py --exe <path of binary file>
	#python3 lms_cfg_gen.py --exe ../binaries/apache2
	#a graph.json file will be created after successful completion of the command.
```

```bash
	cd ../ULF_generation
	# parsing the audit logs into json format
	python3 parsetojson.py <path to audit log> > <output file name>
	# python3 ULF_generation/parsetojson.py samplelogs/audit_1640089505.log > audit_164.json
	# the output file will contain the logs in json format
	# Combine the json formatted audit logs based on the srn
	sort audit_164.json > audit_164s.json
	python3 merge_json.py <output filename> > <merged output filename
	#python3 merge_json.py audit_164s.json > audit_164m.json
	# Combine the application logs and audit log into a single file named data1.json
	python3 ULF_gen.py
	# Sort the universal log file based on date/ts, generates the universal_log.json
	python3 sort_ULF.py
```

```bash
	# Construction of the universal provenance graph
	# Changes are required to the code to take the path of the graph.json and universal_log.json as per the local machine
	python3 upg_gen.py
	# Generates package-lock, sample_output and provenanceGraph.html as an output.
```	


	cd static_analysis
	python3 lms_cfg_gen.py --exe ../binaries/apache2
	cd ULF_generation
	python3 parsetojson.py samplelogs/audit_1640089505.log > audit_164.json
	sort audit_164.json > audit_164s.json
	python3 merge_json.py audit_164s.json > audit_164m.json
	Open the ULF_gen.py in an editor and make the following changes : 
		-> parse_audit_log("../../LOGS_0311/audit_ap2.json")    ---->(change with the line)----> parse_audit_log('./audit_164m.json')
		-> parse_error_log('../../LOGS_0311/access_1640089505.log')   ---->(change with the line)---->  parse_error_log('../samplelogs/access_1640089505.log')
		-> parse_error_log('../../LOGS_0311/error_1640089505.log')    ---->(change with the line)---->   parse_error_log('../samplelogs/error_1640089505.log')
	python3 ULF_gen.py
	python3 sort_ULF.py 	#this will generate an universal_log.json file
	cd ../UPG_construction
	Open the upg_gen file in the text editor and make the following changes
		-> f = open("graph.json",)  ---->(change with the line)----> f = open("../static_analysis/graph.json",)
		-> f = open("universal_log.json",)  ---->(change with the line)----> f = open("../ULF_generation/universal_log.json",)
	python3 upg_gen.py		#this will generate a provenanceGraph.html file which the graph, open in the browser to view that.