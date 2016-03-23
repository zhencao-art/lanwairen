# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from pyudev import Context

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
import exception
import CIPMgr

import partition,mounted

def wwn_to_local_name(wwn):
    disk_by_id_path = "/dev/disk/by-id"
    
    if not os.path.exists(disk_by_id_path):
        raise exception.HandleError("path %s is not exists" % disk_by_id_path)
    
    for link in os.listdir(disk_by_id_path):
        if link.find("wwn") < 0:
            continue
        link_path = disk_by_id_path + "/" + link
    
        if not os.path.islink(link_path):
            continue
        if link == wwn:
            return os.path.realpath(link_path)
    return None

def wwns_to_local_names(wwns):
    devs = []

    for wwn in wwns:
        dev = wwn_to_local_name(wwn)
        if None == dev:
            raise Exception("wwn %s can not be convert to local name" % wwn)
        devs.append(dev)

    return devs

class CPhyDisk:
    def __init__(self,name):
        self.dev_name = name
        self.shared = False
        self.shared_setted = False
        self._used = False
        self._user = None
    
    def set_used(self,flag):
        self._used = flag

    def set_user(self,user):
        self._user = user

    def used(self):
        return self._used

    def user(self):
        return self._user
    
    def set_shared(self):
        self.shared_setted = True
        self.shared = True
    
    def set_unshared(self):
        self.shared_setted = True
        self.shared = False

    def __str__(self):
        return "%s" % self.dev_name

    def name(self):
        return self.dev_name

    def mounted(self):
        for mount in mounted.host_mounted():
            splits = mount.split(" ")
            if splits[0] == self.dev_name:
                return splits[1]
        return None

    def set_size(size):
        self.size = size

    def rotational(self):
        rotational_path = "/sys/block/" + self.dev_name.split("/")[2] + "/queue/rotational"
        try:
            rotational_file = open(rotational_path)
            rotational = rotational_file.read()
            rotational_file.close()
        except:
            return None
        return int(rotational)

    def size(self):
        dev_size_path = "/sys/block/" + self.dev_name.split("/")[2] + "/size"
        try:
            dev_size_file = open(dev_size_path)
            disk_size = dev_size_file.read()
            dev_size_file.close()
        except:
            return None
        return int(disk_size)
    
    def sas_address(self):
        path = '/sys/block/' + self.dev_name.split('/')[2] + '/device/sas_address'
        if not os.path.exists(path):
            return None
        try:
            file_ = open(path)
            address = file_.read()
        except:
            return None

        return address.strip()
    
    #private
    """
        5003048-0-170a-af63->0x50030480170aaf63
    """
    @staticmethod
    def sas_address_format(address):
        return '0x' + address.replace('-','')

    def slot(self,hard_disks):
        sas_address = self.sas_address()
        if not hard_disks:
            return None
        for hard_disk in hard_disks:
            if CPhyDisk.sas_address_format(hard_disk.sas_address) == sas_address:
                return hard_disk.enclosure + ":" + hard_disk.slot
        return None

    def set_wwn(wwn):
        self.wwn = wwn

    ##get the wwn of the physical disk
    def wwn(self):
        disk_by_id_path = "/dev/disk/by-id"
        
        if not os.path.exists(disk_by_id_path):
            raise exception.HandleError("path %s is not exists" % disk_by_id_path)

        for link in os.listdir(disk_by_id_path):
            if link.find("wwn") < 0:
                continue
            link_path = disk_by_id_path + "/" + link

            if not os.path.islink(link_path):
                continue
            if self.dev_name == os.path.realpath(link_path):
                return link
        return None

    def set_partition_list(parts):
        for part in parts:
           self.partition_list.append(part)

    def partition_list(self):
        partitions = []
        context = Context()

        for part in context.list_devices(subsystem='block',DEVTYPE='partition'):
            partition_name = "{0}".format(part.device_node)

            if self.dev_name == "{0}".format(part.find_parent('block').device_node):
                instance = partition.CPartition(partition_name)
                partitions.append(instance)

        return partitions


class CHardDisk:
    def __init__(self):
        self.enclosure = ""
        self.slot = ""
        self.sas_address = ""
        self.state = ""
        self.size = ""
        self.manufacturer = ""
        self.model_number = ""
        self.firmware_revision = ""
        self.serial_no = ""
        self.guid = ""
        self.protocol = ""
        self.drive_type = ""

    def string(self):
        ret = {}
        ret['enclosure'] = self.enclosure
        ret['slot'] = self.slot
        ret['sas_address'] = self.sas_address
        ret['state'] = self.state
        ret['size'] = self.size
        ret['manufacturer'] = self.manufacturer
        ret['model_number'] = self.model_number
        ret['firmware_revision'] = self.firmware_revision
        ret['serial_no'] = self.serial_no
        ret['guid'] = self.guid
        ret['protocol'] = self.protocol
        ret['drive_type'] = self.drive_type

        return ret

class CSASUtil:
    @staticmethod
    def sasutil_path():
        return os.path.abspath(os.path.join(__file__,"../sas2ircu"))

    @staticmethod
    def lsi_adapter_list():
        sas_path = CSASUtil.sasutil_path()
        if not sas_path:
            raise Exception('sas2ircu is not found')
        ret = []
        cmd = sas_path + ' list'
        import commands
        (status,output) = commands.getstatusoutput(cmd)
        if 0 != status:
            raise Exception("Run commands {0} error ,{1}".format(cmd,output))
        out_lines = output.split('\n')
        start_line = 8
        end_line = len(out_lines) - 2 
        for x in range(start_line,end_line + 1):
            ret.append(out_lines[x].strip())

        return ret

    @staticmethod
    def parser_hard_disk_str(disk_str):
        lines = disk_str.split('\n')
        hard_disk = CHardDisk()
        for line in lines:
            if line.find('Enclosure #') >= 0:
                key_values = line.split(':')
                hard_disk.enclosure = key_values[1].strip()
            if line.find('Slot #') >= 0:
                key_values = line.split(":")
                hard_disk.slot = key_values[1].strip()
            if line.find('SAS Address') >= 0:
                key_values = line.split(":")
                hard_disk.sas_address = key_values[1].strip()
            if line.find('State') >= 0:
                key_values = line.split(":")
                hard_disk.state = key_values[1].strip()
            if line.find('Size') >= 0:
                key_values = line.split(":")
                hard_disk.size = key_values[1].strip()
            if line.find('Manufacturer') >= 0:
                key_values = line.split(":")
                hard_disk.manufacturer = key_values[1].strip()
            if line.find('Model Number') >= 0:
                key_values = line.split(":")
                hard_disk.model_number = key_values[1].strip()
            if line.find('Firmware Revision') >= 0:
                key_values = line.split(":")
                hard_disk.firmware_revision = key_values[1].strip()
            if line.find('Serial No') >= 0:
                key_values = line.split(":")
                hard_disk.serial_no = key_values[1].strip()
            if line.find('GUID') >= 0:
                key_values = line.split(":")
                hard_disk.guid = key_values[1].strip()
            if line.find('Protocol') >= 0:
                key_values = line.split(":")
                hard_disk.protocol = key_values[1].strip()
            if line.find('Drive Type') >= 0:
                key_values = line.split(":")
                hard_disk.drive_type = key_values[1].strip()
                break
        return hard_disk

    @staticmethod
    def hard_disk_list():
        sas_path = CSASUtil.sasutil_path()
        if not sas_path:
            raise Exception('sas2ircu is not found')
        cmd = sas_path + ' '
        i = 0
        ret = []
        adapters = CSASUtil.lsi_adapter_list()
        for adapter in adapters:
            cmd = cmd + str(i) + ' display'
            i = i + 1
            (status,output,stderr) = CIPMgr.Exec_cmd(cmd)
            if 0 != status:
                raise Exception("Run commands {0} error ,{1}".format(cmd,output))
            out_splits = output.split("Device is a Hard disk\n")
            for i in range(1,len(out_splits)):
                hard_disk_str = out_splits[i]
                ret.append(CSASUtil.parser_hard_disk_str(hard_disk_str))

        return ret


##### Physical Disk Manager
class CPhyDiskMgr:
    def __init__(self):
        pass

    def phy_disk_list(self):
        disks = []
        context = Context()
        #get system disk
        boot_dev = mounted.boot_dev()

        for block_dev in context.list_devices(subsystem='block',DEVTYPE='disk'):
            if block_dev.__str__().find("/sys/devices/pci") < 0:
                continue
            else:
                disk = CPhyDisk('{0}'.format(block_dev.device_node))
                ##filter the system disk
                if boot_dev.find(disk.name()) >= 0:
                    continue
                disks.append(disk)
        
        return disks
