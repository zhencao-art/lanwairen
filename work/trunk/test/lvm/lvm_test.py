# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/storage")))
from n_lvmmgr import *

E_lv_vg_name = "grp10"

N_PVS = ['/dev/sdi','/dev/sdj','/dev/sdk']
A_PVS = ['/dev/sde']

N_LV = 'LV_TEST'
C_vg_name = "VG_TEST"


def TEST_lv_remove():
    print "TEST_lv_remove"
    lv_remove(C_vg_name,N_LV)
    print "remove lv {0}/{1} success".format(C_vg_name,N_LV)

def TEST_lv_linear_create():
    print "TEST_lv_linear_create"
    lv_linear_create(C_vg_name,N_LV,10,'G')
    print "create lv {0}/{1} success".format(C_vg_name,N_LV)

def TEST_vg_del_pv_crashing():
    print "TEST_vg_del_pv_crashing"
    vg_del_pv_crashing(C_vg_name,A_PVS)
    print "vg  {0} del pv {1} success".format(C_vg_name,A_PVS)

def TEST_vg_add_pv():
    print "TEST_vg_add_pv"
    vg_add_pv(C_vg_name,A_PVS)
    print "vg  {0} add pvs {1} success".format(C_vg_name,A_PVS)

def TEST_vg_create():
    print "TEST_vg_create"
    vg_create(C_vg_name,N_PVS)
    print "create vg %s success" % C_vg_name

def TEST_vg_remove():
    print "TEST_vg_remove"
    vg_remove_crashing(C_vg_name)
    print "remove vg %s success" % C_vg_name

def TEST_vg_lv_list(vg_name):
    print "TEST_vg_lv_list"
    print vg_lv_list(vg_name)

def TEST_vg_pv_list(vg_name):
    print "TEST_vg_pv_list"
    print vg_pv_list(vg_name)


def TEST_lv_list():
    print "TEST_lv_list"
    for lv in lv_list():
        out = {}
        lv.format(out)
        print out

def TEST_vg_list():
    print "TEST_vg_list"
    for vg in vg_list():
        out = {}
        vg.format(out)
        print out

def TEST_pv_list():
    print "TEST_pv_list"
    for pv in pv_list():
        out = {}
        pv.format(out)
        print out

def RUN_ALL_TEST():
   # TEST_lv_list()
    TEST_vg_list()
   # TEST_vg_list()
   # TEST_vg_pv_list(E_lv_vg_name)
   # TEST_vg_lv_list(E_lv_vg_name)
   # TEST_vg_create()
   # TEST_vg_list()

   # TEST_vg_add_pv()
   # TEST_vg_pv_list(C_vg_name)

   # TEST_vg_del_pv_crashing()
   # TEST_vg_pv_list(C_vg_name)

   # TEST_lv_linear_create()
   # TEST_vg_lv_list(C_vg_name)

   # TEST_lv_remove()
   # TEST_vg_lv_list(C_vg_name)

   # TEST_vg_remove()
   # TEST_vg_list()

import pdb
pdb.set_trace()
if __name__ == '__main__':
    RUN_ALL_TEST()
