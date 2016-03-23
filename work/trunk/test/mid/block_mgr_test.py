# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/storage")))
import raidmgr
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/mid")))
import block_mgr
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/db")))
import CConfigMgr

import lvm2py

client = client.CClient("127.0.0.1",50001)
db_path = "/tmp/test.xml"
db_mgr_handle = CConfigMgr.CConfigMgr(client,db_path,True)
raid_mgr = raidmgr.CRaidMgr()
lvm_handle = lvm2py.LVM()

def md_print(md_device):
    print "name:%s" % md_device.name()
    print "size:%d" % md_device.size()
    print "level:%s" % md_device.level()
    print "chunk:%d" % md_device.chunk()
    print "phyiscal device:"
    for phy in md_device.phy_device_list():
        print "\t\t %s" % phy

def md_create_TEST():
    block_mgr.md_create(db_mgr_handle,raid_mgr,"/dev/md0",0,['/dev/sdb','/dev/sdc'],4)
    md_device = raid_mgr.find_by_name("/dev/md0")
    md_print(md_device)

def md_remove_TEST():
    block_mgr.md_remove(db_mgr_handle,raid_mgr,"/dev/md0")

def md_remove_crashing_TEST():
    block_mgr.md_remove_crashing(db_mgr_handle,raid_mgr,"/dev/md0")

def vg_create_TEST():
    block_mgr.vg_create(db_mgr_handle,lvm_handle,"grp00",['/dev/sdd','/dev/sde'])

def vg_remove_TEST():
    block_mgr.vg_remove(db_mgr_handle,lvm_handle,"grp00")

def vg_add_pv_TEST():
    block_mgr.vg_add_pv(db_mgr_handle,lvm_handle,"grp00","/dev/sdf")

def vg_del_pv_TEST():
    block_mgr.vg_del_pv(db_mgr_handle,lvm_handle,"grp00","/dev/sdf")

def TEST():
    #md_create_TEST()
    #md_remove_TEST()
    #md_remove_crashing_TEST()
    vg_create_TEST()
    #vg_remove_TEST()
    #vg_add_pv_TEST()
    #vg_del_pv_TEST()

import pdb
#pdb.set_trace()
TEST()

