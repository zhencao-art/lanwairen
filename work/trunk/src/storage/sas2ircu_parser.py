# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
import CIPMgr

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


def sasutil_path():
    return os.path.abspath(os.path.join(__file__,"../sas2ircu"))

def sasutil_lsiadapter_list():
    sas_path = sasutil_path()
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

def parser_harddisk_str(disk_str):
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

def sasutil_harddisk_list():
    sas_path = sasutil_path()
    if not sas_path:
        raise Exception('sas2ircu is not found')
    cmd = sas_path + ' '
    i = 0
    ret = []
    adapters = sasutil_lsiadapter_list()
    for adapter in adapters:
        cmd = cmd + str(i) + ' display'
        i = i + 1
        (status,output,stderr) = CIPMgr.Exec_cmd(cmd)
        if 0 != status:
            raise Exception("Run commands {0} error ,{1}".format(cmd,output))
        out_splits = output.split("Device is a Hard disk\n")
        for i in range(1,len(out_splits)):
            hard_disk_str = out_splits[i]
            ret.append(parser_harddisk_str(hard_disk_str))

    return ret
