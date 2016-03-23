#!/usr/bin/python
import sys
import subprocess 
import re

def get_params():
    if len(sys.argv)  < 2 :
        sys.exit(1)
    # execute commands with shell pipe.
    cmd = "pcs resource show " + sys.argv[1] +  " | grep Attributes: | awk '{$1=\"\"; print}' "
    
    params = subprocess.check_output(cmd, shell=True)
    
    matches = re.findall(r'(\w+(?:\(\d+\))?)\s*=\s*(.*?)(?=(!|$|\w+(\(\d+\))?\s*=))', params)
    keyval = {}
    for match in matches:
        vals = match[1].strip()
        keyval[match[0]] = vals.strip('"')

    for key in keyval.keys():
        name = "OCF_RESKEY_" + key
        value = keyval[key]
        print "%s=%s" % (name, value)
 
get_params()