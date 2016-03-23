# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/storage")))
import phydiskmgr

def print_phy_disk(phy):
    print "name={0} size={1} wwn={2} mounted={3}".format(phy.name(),phy.size(),phy.wwn(),phy.mounted())
    for part in phy.partition_list():
        print part


def phy_disk_list_TEST():
    phy_disk_mgr = phydiskmgr.CPhyDiskMgr()

    for disk  in phy_disk_mgr.phy_disk_list():
        print_phy_disk(disk)


def Test():
    phy_disk_list_TEST()

Test()
