# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
import exception
import CIPMgr
##import blkid

class CMdPhyDeviceSuperBlock:
    def __init__(self):
        self.array_uuid = None
        self.array_level = None
        self.update_time = None
        self.create_time = None
        self.device_uuid = None

    def __str__(self):
        return "array_uuid:{0} array_level:{1} update_time:{2} create_time:{3} device_uuid:{4}".format(self.array_uuid,self.array_level,\
                self.update_time,self.create_time,self.device_uuid)
    @property
    def array_uuid(self):
        return self.array_uuid
    @array_uuid.setter
    def array_uuid(self,value):
        self.array_uuid = value

    @property
    def array_level(self):
        return self.array_level
    @array_level.setter
    def array_level(self,value):
        self.array_level = value
    
    @property
    def create_time(self):
        return self.create_time
    @create_time.setter
    def create_time(self,value):
        self.create_time = value

    @property
    def update_time(self):
        return self.update_time
    @update_time.setter
    def update_time(self,value):
        self.update_time = value

    @property
    def device_uuid(self):
        return self.device_uuid
    @device_uuid.setter
    def device_uuid(self,value):
        self.device_uuid = value
    
class CMdPhyDevice:
    def __init__(self,md,name):
        self.dev_name = name
        self.md = md

    def name(self):
        return self.dev_name

    def __str__(self):
        return self.dev_name

    def md(self):
        return self.md

    def zero_superblock(self):
        if not os.path.exists("/usr/sbin/mdadm"):
            raise exception.HandleError("mdadm is not installed")
        cmd = "mdadm --zero-superblock " + self.dev_name
        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        if status != 0:
            raise exception.CommitError("command {0} run error,{1}!".format(cmd,status))

class CMdDevice:
    def __init__(self,name):
        self.dev_name = name
    
    def __str__(self):
        return self.dev_name

    def name(self):
        return self.dev_name

    def size(self):
        size_file_path = self.sys_path() + "/size"
        
        if not os.path.exists(size_file_path):
            raise exception.HandleError("file %s is not exists" % size_file_path)
    
        size_file_handle = open(size_file_path)
        try:
            size = size_file_handle.read()
        except:
            raise IOError("read file %s error" % size_file_path)
        finally:
            size_file_handle.close()

        return int(size)
    
    def sys_path(self):
        return "/sys/block/" + self.dev_name.split("/")[2]
    
    def phy_device_list(self):
        md_path = self.sys_path() + "/md"
        dev_list = []
    
        if not os.path.exists(md_path):
            raise exception.HandleError("path %s is not exists" % md_path)
        for ele in os.listdir(md_path):
            if ele.find("dev-") != 0:
                continue
            dev_list.append(CMdPhyDevice(self,"/dev/" + ele.split("-")[1]))

        return dev_list

    def level(self):
        level_file_path = self.sys_path() + "/md/level"
        
        if not os.path.exists(level_file_path):
            raise exception.HandleError("file %s is not exists" % level_file_path)

        level_file_handle = open(level_file_path)
        try:
            level = level_file_handle.read()
        except:
            raise IOError("read file %s error" % level_file_path)
        finally:
            level_file_handle.close()

        return level.replace("\n","")

    def chunk(self):
        csize_file_path = self.sys_path() + "/md/chunk_size"
        
        if not os.path.exists(csize_file_path):
            raise exception.HandleError("file %s is not exists" % csize_file_path)

        csize_file_handle = open(csize_file_path)
        try:
            csize = csize_file_handle.read()
        except:
            raise IOError("read file %s error" % csize_file_path)
        finally:
            csize_file_handle.close()

        return int(csize)

class CRaidMgr:
    def __init__(self):
        pass

    def create_md(self,md_name,level,phy_devices,chunk = 0):
        if not self.mdadm_exists():
            raise exception.HandleError("mdadm is not installed")
        
        if os.path.exists(md_name):
            raise ValueError("md device %s is exists" % md_name)
        
        if not self.raid_level_vaild(level):
            raise ValueError("param chunk={0} level={1} is not vaild".format(chunk,level))
        if level != 1 and chunk < 4:
            raise ValueError("param chunk={0} level={1} is not vaild".format(chunk,level))

        if not os.path.exists("/" + md_name.split("/")[1]):
            raise ValueError("Param mdName=%s is not valid" % md_name)

        cmd = "echo y | mdadm --create " + md_name + " --chunk=" + str(chunk) + " --level=" + str(level) + " --raid-devices="
        
        if len(phy_devices) < 1:
            raise ValueError("param phyDevices's len is %d" % len(phy_devices))
        else:
            cmd = cmd + str(len(phy_devices)) + " "

        for device in phy_devices:
            if not os.path.exists(device):
                raise ValueError("%s is not exists" % device)

            ##dev_type = blkid.get_dev_type(device)

            ##if dev_type != None:
            ##    raise exception.HandleError("physical device {0} has metadata,type is {1}".format(device,dev_type))

           ## superblock = self.md_phy_device_by_name(device)
           ## if superblock:
           ##     raise exception.HandleError("physical device {0} already exists raid information {1}".format(device,superblock))
            cmd = cmd + device + " "

        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        if status != 0:
            raise exception.CommitError("command {0} run error,{1}!".format(cmd,status))

    def remove_md(self,md_name):
        if not self.mdadm_exists():
            raise exception.HandleError("mdadm is not installed")
        
        if not os.path.exists(md_name):
            raise ValueError("dm device %s is not found" % md_name)
        
        cmd = "mdadm  --stop " + md_name
        
        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        if status != 0:
            raise exception.CommitError("command {0} run error,{1}!".format(cmd,status))
    
    """
        delete md-device crashing
        Rasie
            HandleError
            CommitError
    """
    def remove_md_crashing(self,md_name):
        md_device = self.find_by_name(md_name)
        if md_device == None:
            raise ValueError("md device %s is not exists" % md_name)
        phy_device_list = md_device.phy_device_list()
        self.remove_md(md_name)
        for phy_device in phy_device_list:
            phy_device.zero_superblock()

    def assemble_md(self,md_name,phy_devices):
        if not self.mdadm_exists():
            raise exception.HandleError("mdadm is not installed")
        if os.path.exists(md_name):
            raise ValueError("dm device %s is exists" % md_name)

        if len(phy_devices) < 1:
            raise ValueError("param phyDevices's len is %d" % len(phy_devices))

        cmd = "mdadm --assemble " + md_name + " "

        for device in phy_devices:
            if not os.path.exists(device):
                raise ValueError("%s is not exists" % device)
            cmd = cmd + device + " "
        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        if status != 0:
            raise exception.CommitError("command {0} run error,{1}!".format(cmd,status))
    
    def assemble_md_scan(self):
        if not self.mdadm_exists():
            raise exception.HandleError("mdadm is not installed")
        
        cmd = "mdadm --assemble --scan"
        
        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        if status != 0:
            raise exception.CommitError("command {0} run error,{1}!".format(cmd,status))
        
    
    def raid_level_vaild(self,level):
        if level == 0 or level == 1 or level == 4 or level == 5 or level == 6 or level == 10:
            return True
        return False

    def mdadm_exists(self):
        return os.path.exists("/usr/sbin/mdadm")

    def find_by_name(self,dev_name):
        if not self.is_md_device(dev_name):
            return None
        return CMdDevice(dev_name)

    def is_md_device(self,dev_name):
        local_name = dev_name.split("/")[2]

        for line in open("/proc/mdstat").readlines():
            if line.find(local_name) == 0:
                return True
        return False
    
    def scan_md_device(self):
        block_sys_path = "/sys/block"
        md_device_list = []

        if not os.path.exists(block_sys_path):
            raise exception.HandleError("path %s is not exists" % block_sys_path)

        for device in os.listdir(block_sys_path):
            if device.find("dm-") >= 0 or device.find("loop") >= 0 or device.find("sr") >= 0:
                continue
            dev_name = "/dev/" + device
            if self.is_md_device(dev_name):
                md_device_list.append(CMdDevice(dev_name))
        return md_device_list

    def md_phy_device_by_name(self,dev_name):
        if not self.mdadm_exists():
            raise exception.HandleError("mdadm is not installed")

        if not os.path.exists(dev_name):
            raise exception.HandleError("device dev_name is not existsed" % dev_name)

        cmd = "mdadm -E " + dev_name

        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        
        if status != 0:
            return None

        superblock = CMdPhyDeviceSuperBlock()

        for line in output.split('\n'):
            if not line.find("Array UUID") < 0:
                superblock.array_uuid = line.split(" : ")[1]

            if not line.find("Creation Time") < 0:
                superblock.create_time = line.split(" : ")[1]

            if not line.find("Device UUID") < 0:
                superblock.device_uuid = line.split(" : ")[1]
            
            if not line.find("Update Time") < 0:
                superblock.update_time = line.split(" : ")[1]

            if not line.find("Raid Level") < 0:
                superblock.array_level = line.split(" : ")[1]

        return superblock

    def zero_md_phy_device(self,dev_name):
        if not os.path.exists("/usr/sbin/mdadm"):
            raise exception.HandleError("mdadm is not installed")

        cmd = "mdadm --zero-superblock " + dev_name
        (status,ouput,stderr) = CIPMgr.Exec_cmd(cmd)
        if status != 0:
            raise exception.CommitError("command {0} run error,{1}!".format(cmd,status))

    def zero_md_phy_devices(self,dev_names):
        for dev in dev_names:
            self.zero_md_phy_device(dev)
