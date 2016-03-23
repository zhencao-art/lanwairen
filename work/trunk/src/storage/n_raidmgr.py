# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
import exception,toolbox,logging
import CIPMgr

class RaidDevStat:
    def __init__(self):
        self.raid_name   = None
        self.stat        = None
        self.phy_dev_num = None
        self.phy_devs    = None

class RaidDev:
    def __init__(self):
        self.name  = None
        self.size  = None #unit is sectors
        self.level = None
        self.chunk = None #unit is byte
        self.array_size = None
        self.array_stat = None
        self.raid_disks = None

    def format(self,out = {}):
        out["name"]  = self.name
        out["size"]  = self.size
        out["level"] = self.level
        out["chunk"] = self.chunk
        out["array_size"] = self.array_size
        out["array_stat"]  = self.array_stat
        out["raid_disks"]  = self.raid_disks

def Run_cmd(cmd):
    (status,output,stderr) = CIPMgr.Exec_cmd(cmd)

    logging.debug("Run cmd %s" % cmd)
    if status != 0:
        ##cmd run error
        logging.error("Run cmd {0} error,{1}".format(cmd,stderr))
        raise Exception("Run cmd {0} error,{1}".format(cmd,stderr))

    return (status,output,stderr)

"""
"""
def mdadm_config_set(home_host,device):
    mdadm_conf = '/etc/mdadm.conf'
    content = "DEVICE " + device + "\nHOMEHOST " + home_host + "\n"

    file_h = open(mdadm_conf,"w")
    file_h.write(content)

    file_h.close()

"""
"""
def check_raid_name_valid(name):
    if name.startswith('/dev/'):
        return (-1,'raid name %s is not vaild' % name)
    return (0,"")

"""
"""
def check_create_param(name,level,devices,width = None):
    (ret,msg) =  check_raid_name_valid(name)
    if ret != 0:
        return (-1,msg)

    if level == 1:
        if len(devices) < 2:
            return (-1,"raid 1 acquire two disks at less")
    elif level == 0:
        if width:
            if width % 4 != 0:
                return(-1,'raid 0 acquire width must be a multiple of 4kb')
    elif level == 4 and level == 5 and level == 6:
        if width:
            if width % 2 != 0:
                return(-1,'raid %s acquire width must be a power of 2')
    return (0,"")

"""
"""
def construct_create_cmd(name,level,devices,width):
    cmd = 'echo y | mdadm --create ' + '/dev/' + name + ' -l ' + str(level)

    if level != 1:
        cmd = cmd + ' -c ' + str(width)

    cmd = cmd + ' --raid-disks=' + str(len(devices))

    sub_cmd = ''
    for dev in devices:
        sub_cmd = sub_cmd + ' ' + dev

    cmd = cmd + sub_cmd

    return cmd

"""
"""
def raid_create(name,level,devices = [],width = None):
    cmd = construct_create_cmd(name,level,devices,width)
    Run_cmd(cmd)

"""
"""
def sys_path_of_raid(raid):
    return toolbox.block_sysfs_path() + '/' + raid

def check_raid_exists(raid):
    return os.path.exists(sys_path_of_raid(raid))

"""
"""
def device_of_raid_cur(raid):
    base_path = sys_path_of_raid(raid)
    slaves_path = base_path + '/slaves'
    ret= []
    for dev in os.listdir(slaves_path):
        ret.append('/dev/' + dev)
    return ret

"""
"""
def raid_info_zero(dev_name):
    cmd = 'mdadm --zero-superblock ' + dev_name
    Run_cmd(cmd)

"""
"""
def raid_info_zero_batch(dev_names):
    for dev in dev_names:
        raid_info_zero(dev)

"""
"""
def raid_stop(raid):
    cmd = 'mdadm --stop ' + '/dev/' + raid
    Run_cmd(cmd)

"""
"""
def raid_remove_nor(raid):
    devices = device_of_raid_cur(raid)
    raid_stop(raid)
    raid_info_zero_batch(devices)

"""
"""
def raid_name_list():
    ret = []
    cmd = 'find /sys/devices/virtual/block/*/ -name md'
    (status,output,stderr) = Run_cmd(cmd)
    items = output.split('\n')

    for item in items:
        if item == "":
            continue
        ret.append(item.split('/')[-2])
    return ret

"""
"""
def construct_raid_obj(raid_name):
    obj = RaidDev()
    base_path = sys_path_of_raid(raid_name)

    obj.name  = raid_name
    obj.size  = int(toolbox.read_sysfs_file(base_path + '/size'))
    obj.level = toolbox.read_sysfs_file(base_path + '/md/level')
    obj.chunk = int(toolbox.read_sysfs_file(base_path + '/md/chunk_size'))
    obj.array_size = toolbox.read_sysfs_file(base_path + '/md/array_size')
    obj.raid_disks = int(toolbox.read_sysfs_file(base_path + '/md/raid_disks'))
    obj.array_stat = toolbox.read_sysfs_file(base_path + '/md/array_state')

    return obj

"""
"""
def raid_list():
    objs = []

    for name in raid_name_list():
        objs.append(construct_raid_obj(name))

    return objs

"""
"""
def raid_detail(raid_path):
    cmd = 'mdadm --detail ' + raid_path
    (status,output,stderr) = Run_cmd(cmd)
    items = output.split('\n')
