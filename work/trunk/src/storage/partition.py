# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

class CPartition:
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return "%s" % self.name

    def mounted(self):
        for mount in hostmounts.hostMounts():
            splits = mount.split(" ")
            if splits[0] == self.name:
                return splits[1]
        return None

    def size(self):
        name_local  = self.name.split("/")[2]
        parent_name = split("\d+$",name_local)[0] 

        dev_size_path = "/sys/block/" + parent_name + "/" + name_local + "/size"
        try:
            dev_size_file = open(dev_size_path)
            disk_size = dev_size_file.read()
            dev_size_file.close()
        except:
            return None

        return int(disk_size)
