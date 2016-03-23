# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.opath.join(__file__,'../../ip')))
import CIPMgr

"""
    return Type of the device
"""
def get_dev_type(dev_name):
    blkid_cmd = 'blkid ' + dev_name
    (status,output,stderr) = CIPMgr.Exec_cmd(blkid_cmd)
    if status != 0:
        return None
    if output:
        out_line = output.strip().split(' ')
        return dev_type_format(out_line[-1])
    return None

def dev_type_format(dev_type):
    ret = dev_type.split('=')[1]
    return ret.strip('\"')

"""
"""
def empty_dev_meta(dev_name):
    pass
