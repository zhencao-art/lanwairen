# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from pyudev import Context
import os,sys
import mounted
import sas2ircu_parser

def wwn_to_local_name(wwn):
    disk_by_id_path = "/dev/disk/by-id"
    
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

def disk_block_name_list():
    names = []
    context = Context()
    #get system disk
    boot_dev = mounted.boot_dev()
    
    for block_dev in context.list_devices(subsystem='block',DEVTYPE='disk'):
        if block_dev.__str__().find("/sys/devices/pci") < 0:
            continue
        else:
            ##filter the system disk
            if boot_dev.find(block_dev.device_node) >= 0:
                continue
            names.append(block_dev.device_node)
    return names

class CPhyDisk:
    def __init__(self):
        self.name = None
        self.size = None
        self.slot = None
        self.wwn  = None
        self.rotational = None
        self.protocol = None

    def string(self):
        ret = {}
        ret['name'] = self.name
        ret['size'] = self.size
        ret['slot'] = self.slot
        ret['wwn'] = self.wwn
        ret['rotational'] = self.rotational
        ret['protocol'] = self.protocol
        return ret


def disk_block_sasaddress(disk_block_name):
    path = '/sys/block/' + disk_block_name.split('/')[2] + '/device/sas_address'
    if not os.path.exists(path):
        return None
    try:
        file_ = open(path)
        address = file_.read()
    except:
        return None
    
    return address.strip()


def disk_block_slot_protocol(hard_disks,disk_block_name):
    def sas_address_format(address):
        return '0x' + address.replace('-','')
    if not hard_disks:
        return None
    for hard_disk in hard_disks:
        if sas_address_format(hard_disk.sas_address) == disk_block_sasaddress(disk_block_name):
            return (hard_disk.enclosure + ":" + hard_disk.slot,hard_disk.protocol)
    return None

def disk_block_size(disk_block_name):
    dev_size_path = "/sys/block/" + disk_block_name.split("/")[2] + "/size"
    try:
        dev_size_file = open(dev_size_path)
        disk_size = dev_size_file.read()
        dev_size_file.close()
    except:
        return None
    return int(disk_size)

def disk_block_roational(disk_block_name):
    rotational_path = "/sys/block/" + disk_block_name.split("/")[2] + "/queue/rotational"
    try:
        rotational_file = open(rotational_path)
        rotational = rotational_file.read()
        rotational_file.close()
    except:
        return None
    return int(rotational)

def disk_block_wwn(disk_block_name):
    disk_by_id_path = "/dev/disk/by-id"
    for link in os.listdir(disk_by_id_path):
        if link.find("wwn") < 0:
            continue
        link_path = disk_by_id_path + "/" + link
    
        if not os.path.islink(link_path):
            continue
        if disk_block_name == os.path.realpath(link_path):
            return link
    return None

def disk_block_wwns(disk_block_names):
    wwns = []
    for name in disk_block_names:
        wwns.append(disk_block_wwn(name))
    return wwns

def _disk_block_obj_list(hard_disks):
    objs = []
    for name in disk_block_name_list():
        obj = CPhyDisk()
        obj.name = name
        obj.size = disk_block_size(name)
        obj.wwn  = disk_block_wwn(name)
        obj.rotational  = disk_block_roational(name)

        if hard_disks:
            (slot,protocol) = disk_block_slot_protocol(hard_disks,name)
            obj.slot = slot
            obj.protocol = protocol
        objs.append(obj)
    return objs

def disk_block_obj_list():
    hard_disks = sas2ircu_parser.sasutil_harddisk_list()
    return _disk_block_obj_list(hard_disks)
