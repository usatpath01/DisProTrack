# Universal Log File Generation 
1. parsetojson.py : to parse the audit logs into a json format. 

    ```
    Usage :python3  parsetojson.py <path of audit log> > output.txt
    ```
    output.txt will contain the logs in json format.

2. merge_json.py : to combine the json formatted audit logs based on the srn . Make sure the input to this scipt is first sorted. 

    Usage:
    ```
    sort output.txt

    python3 merge_json.py output.txt > output_merged.txt
    ```
3. ULF_gen.py: combine the application logs and audit log into a single file named data1.json
    Usage:

    Need to add the files to parse manually in this script

    To parse the audit file use funciton :: parse_audit_log

    To parse application log files use function :: parse_error_log

4. sort_ULF.py: sort the universal log file based on date/ts, generates the universal_log.json

