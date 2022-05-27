python3 static_analysis/lms_cfg_gen.py --exe=binaries/wget --mb=2 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/wget --mb=3 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/wget --mb=4 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/wget --mb=5 > /dev/null 2>&1
echo "WGET DONE"
python3 static_analysis/lms_cfg_gen.py --exe=binaries/apache2 --mb=2 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/apache2 --mb=3 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/apache2 --mb=4 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/apache2 --mb=5 > /dev/null 2>&1
echo "ApacHE2 DONE"
python3 static_analysis/lms_cfg_gen.py --exe=binaries/openvpn --mb=2 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/openvpn --mb=3 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/openvpn --mb=5 > /dev/null 2>&1
python3 static_analysis/lms_cfg_gen.py --exe=binaries/openvpn --mb=4 > /dev/null 2>&1
echo "OPENVPN DONE"
