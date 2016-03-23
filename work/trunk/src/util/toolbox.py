# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
    for example:
        '/dev/sda' -> 'sda'
"""
def FullToShort(name):
    if name.find("/dev/") < 0:
        return name
    return name.split('/')[2]

"""
    for example:
      ['/dev/sdb','/dev/sda'] -> ['sda','sdb']
"""
def FullToShortList(name_list):
    ret = []
    for name in name_list:
        ret.append(FullToShort(name))
    return ret

"""
    for example:
        'sda' -> '/dev/sda'
"""
def ShortToFull(name):
    return "/dev/" + name

"""
    for example:
    ['sda','sdb'] -> ['/dev/sdb','/dev/sda']
"""
def ShortToFullList(name_list):
    ret = []
    for name in name_list:
        ret.append(ShortToFull(name))
    return ret

"""
"""
def MibToGib(size):
    return size >> 10


def Sectors2Gib(size):
    return (512*size) >> 30

"""
"""
def GibToMib(size):
    return size << 10

def unit2bits(unit):
    if unit == "GiB":
        return 30
    elif unit == "MiB":
        return 20
    elif unit == "KiB":
        return 10
    elif unit == "Byte":
        return 0
    raise Exception("unkonw unit %s" % unit)

## 
def block_sysfs_path():
    return '/sys/block';

def read_sysfs_file(path):
    file_handle = open(path)
    content = file_handle.read()
    file_handle.close()
    return content.replace('\n','')
