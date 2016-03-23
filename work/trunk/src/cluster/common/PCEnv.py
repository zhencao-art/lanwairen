#!/usr/bin/env python
#    env class
# used to check disks,cluster's nodes and store them
#
#
import PCDisk
import pyudev

class PCEnv(object):
    def __init__(self):
        self.device_list=[]
        self.cluster_nodes=[]
        self.InitClusterNode()
        self.InitDevices()
    def GetDevices(self):
        return self.device_list
    def GetClusterNode(self):
        return self.cluster_nodes
    def InitDevices(self):
        disk=PCDisk.PCDisk()
        remoteDisk=disk.GetDiskList('node2','root','root123')
        localDisk = disk.GetLocalDisk()
        if remoteDisk == None:
            print 'get {0} disk list failed'.format('node2')
            return None
        print "remote disk list:"
        print remoteDisk
        print 'local disk list:'
        print localDisk
        for device in remoteDisk:
            if device in localDisk:
                self.device_list.append(device)
    def InitClusterNode(self):
        self.cluster_nodes=['172.16.9.243','172.16.9.245']

env = PCEnv()
nodes=env.GetDevices()
devices=env.GetClusterNode()
print nodes
print devices
