# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/storage")))
import raidmgr

def raidMgrCreateTest(name,chunk,level,raidDevices):
    raidMgr = raidmgr.CRaidMgr()
    
    try:
        raidMgr.create_md(name,level,raidDevices,chunk)
    except Exception as X:
        print X.args[0]

def raidMgrRemoveTest(name):
    raidMgr = raidmgr.CRaidMgr()
    
    try:
        raidMgr.remove_md(name)
    except Exception as X:
        print X.args[0]

def raidMgrScanTest():
    raidMgr = raidmgr.CRaidMgr()
    for md in raidMgr.scan_md_device():
        print md
    
def raidAssembleTest(name,devices):
    raidMgr = raidmgr.CRaidMgr()
    
    try:
        raidMgr.assemble_md(name,devices)
    except Exception as X:
        print X.args[0]

def raidAssembleScanTest():
    raidMgr = raidmgr.CRaidMgr()
    
    try:
        raidMgr.assemble_md_scan()
    except Exception as X:
        print X.args[0]

def printCMdDevice(md):
    print md.name()
    print md.size()
    print md.level()
    print md.chunk()

def raidScanMdDevice():
    raidMgr = raidmgr.CRaidMgr()
    
    try:
        for md in raidMgr.scan_md_device():
            printCMdDevice(md)
            raidMgr.remove_md(md.name())
    except Exception as X:
        print X.args[0]

def md_phy_device_by_name_TEST(dev_name):
    raidMgr = raidmgr.CRaidMgr()
    
    try:
        print raidMgr.md_phy_device_by_name(dev_name)
    except Exception as X:
        print X.args[0]

def Test():
   raidMgrCreateTest("/dev/md1",4,0,['/dev/sdf','/dev/sdc'])
   # raidMgrCreateTest("/dev/md1",4,0,['/dev/sdb','/dev/sdc'])
   # raidMgrRemoveTest("/dev/md1")
   # raidMgrRemoveTest("/dev/md1")
   # 
   # raidMgrCreateTest("/dev/md1",3,0,['/dev/sdb','/dev/sdc'])
   # raidMgrCreateTest("/dev/md1",4,0,[])

   # raidAssembleTest("/dev/md1",['/dev/sdb','/dev/sdc'])
   # raidMgrRemoveTest("/dev/md1")
   # raidAssembleTest("/dev/md1",[])
    
   # raidAssembleScanTest()
   # raidScanMdDevice()
   #md_phy_device_by_name_TEST("/dev/sdd")
Test()
