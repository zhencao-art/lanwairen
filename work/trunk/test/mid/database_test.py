# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/storage")))
import raidmgr
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/mid")))
import block_mgr,database
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/db")))
import CConfigMgr

client = client.CClient("127.0.0.1",50001)
db_path = "/tmp/test.xml"
db_mgr_handle = CConfigMgr.CConfigMgr(client,db_path,True)

def printdb():
    cmd = "cat " + db_path
    os.system(cmd)

def cleardb():
    cmd = "rm -f " + db_path
    os.system(cmd)

def db_md_create_TEST():
    database.database_md_create(db_mgr_handle,"md0",['sda','sdb'])
    printdb()

def db_md_remove_TEST():
    database.database_md_remove(db_mgr_handle,"md0")
    printdb()

def db_md_remove_crash_TEST():
    database.database_md_remove_crashing(db_mgr_handle,"md0")
    printdb()

def db_md_phy_zero_TEST():
    database.database_md_phy_zero(db_mgr_handle,"sda")
    database.database_md_phy_zero(db_mgr_handle,"sdb")
    printdb()

def db_vg_create_TEST():
    database.database_vg_create(db_mgr_handle,"grp00",['sdc','sdd'])
    printdb()

def db_vg_remove_TEST():
    database.database_vg_remove(db_mgr_handle,"grp00")
    printdb()

def db_vg_remove_crashing_TEST():
    database.database_vg_remove_crashing(db_mgr_handle,"grp00")
    printdb()

def db_vg_add_pv_TEST():
    database.database_vg_add_pv(db_mgr_handle,"grp00","sdf")
    printdb()

def db_vg_del_pv_TEST():
    database.database_vg_del_pv(db_mgr_handle,"grp00","sdf")
    printdb()

def db_vg_del_pv_crashing_TEST():
    database.database_vg_del_pv_crashing(db_mgr_handle,"grp00","sdf")
    printdb()

def TEST():
    #db_md_create_TEST()
    #db_md_remove_TEST()
    #db_md_phy_zero_TEST()
    #db_md_remove_crash_TEST()
#    db_vg_create_TEST()
#    db_vg_add_pv_TEST()
    #db_vg_del_pv_TEST()
    db_vg_del_pv_crashing_TEST()
    #db_vg_remove_TEST()
    #db_vg_remove_crashing_TEST()

import pdb
#pdb.set_trace()
TEST()
