# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os,sys,stat
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
import exception,toolbox
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../storage")))
import n_lvmmgr,n_raidmgr,n_phydisk
#from puma_pb2 import ListPhyDiskReq
from puma_pb2 import MdadmConfigSetReq
import database
import logging

"""
    if the specified device is a block device,return True,
    otherwise False
"""
def check_block_dev(dev_name):
    if not os.path.exists(dev_name):
        return False

    statinfo = os.stat(dev_name)

    return stat.S_ISBLK(statinfo[stat.ST_MODE])

"""
"""
def check_block_is_phy(dev_name):
    if dev_name.startswith('/dev/sd'):
        return True
    return False

"""
"""
def lvm_check_pv_dev_type(db_handle,dev_name):
    if check_block_is_phy(dev_name):
        return 'Physical Disk'
    if database.check_dev_is_md(db_handle,db_ID_dev(dev_name)):
        return "Raid Device"
    return "Unkonw"

"""
"""
def get_db_identify_phy_disk(dev_name):
    return n_phydisk.disk_block_wwn(dev_name)

"""
    /dev/xx/yy ---> xx_yy
    /dev/md0 ---> md0
"""
def format_db_block_dev_name(dev_name):
    if not dev_name.startswith('/dev/'):
        return dev_name

    dev_name = dev_name.replace('/dev/','')

   # items = dev_name.split('/')
   # ret = ''
   # for i in range(1,len(items)):
   #     if i != 1:
   #         ret = ret + '_'
   #     ret = ret + items[i]
    return dev_name

"""
"""
def db_ID_dev(dev_name):
    if check_block_is_phy(dev_name):
        identify = get_db_identify_phy_disk(dev_name)
        if not identify:
            logging.error("db_ID_dev,Can not found the wwn of the physical device %s" % dev_name)
            raise Exception("Can not found the wwn of the physical device %s" % dev_name)
        return identify
    return format_db_block_dev_name(dev_name)

"""
"""
def db_ID_dev_list(dev_list):
    ret = []
    for dev in dev_list:
        ret.append(db_ID_dev(dev))
    return ret


def block_disk_used_in(db_handle,dev_name):
    (db_in,msg) = database.device_is_used(db_handle,db_ID_dev(dev_name))
    if db_in:
        return True
    else:
        return False

##"""
##"""
##def db_identify_block_dev(phy_disk_list,dev_name):
##    if check_block_is_phy(phy_disk_list,dev_name):
##        identify = get_db_identify_phy_disk(dev_name)
##        if not identify:
##            raise Exception("Can not found the wwn of the physical device %s" % dev_name)
##
##    return format_db_block_dev_name(dev_name)
##
##"""
##"""
##def db_identify_block_dev_list(phy_disk_list,dev_list):
##    ret = []
##    for dev in dev_list:
##        ret.append(get_db_identify_block_dev(phy_disk_list,dev))
##    return ret
"""
"""
def cluster_mdadm_config_set(client_handle,client_stub,home_host,device = '/dev/null'):
    ##remote setting
    try:
        request = MdadmConfigSetReq()
        request.home_host = home_host
        request.device = device

        client_stub.mdadm_config_set(None,request,None)
    except Exception,e:
        logging.error("RPC call of the remote failed,%s" % str(e))
        raise e

    response = client_handle.get_response()

    if response.ret.retcode != 0:
        logging.error("Remote Call error, %s" % response.ret.msg)
        raise Exception("Remote Call error, %s" % response.ret.msg)

    ##local setting
    try:
        n_raidmgr.mdadm_config_set(home_host,device)
    except Exception,e:
        logging.error("cluster_mdadm_config_set,exception: %s" % str(e))
        raise Exception("Local Call error, %s" % response.ret.msg)
#
#"""
#    set the shared filed of the physical disk
#    this required getting the list of the remote
#    node physical disk
#"""
#def cluster_phy_disk_list(db_handle,phy_disk_mgr,client_handle):
#    flag = False
#    local_disks = phy_disk_mgr.phy_disk_list()
#    request = ListPhyDiskReq()
#
#    try:
#        client_handle.stub().list_phy_disk(None,request,None)
#    except Exception,e:
#        logging.info("RPC call of the remote failed,%s" % str(e))
#        return local_disks
#
#    response = client_handle.get_response()
#
#    if response.ret.retcode != 0:
#        logging.error("RPC error when it gets the disk list of the remote node %s" % response.ret.msg)
#        raise Exception("Get remote the list of the physical disk error %s" % response.ret.msg)
#    for local_disk in local_disks:
#        local_wwn = local_disk.wwn()
#        if not local_wwn:
#            continue
#
#        (db_in,msg) = database.device_is_used(db_handle,db_ID_dev(local_disk.name()))
#        if db_in:
#            local_disk.set_used(True)
#
#        for remote_disk in response.disks:
#            if not remote_disk.HasField("dev_wwn"):
#                continue
#            if local_wwn == remote_disk.dev_wwn:
#                local_disk.set_shared()
#                flag = True
#                break
#
#        if not flag:
#            local_disk.set_unshared()
#
#    return local_disks
#
#"""
#    Get the list of the shared disk
#"""
#def get_shared_disk_list(phy_disk_mgr,client_handle):
#    ret = []
#    disk_list = cluster_phy_disk_list(phy_disk_mgr,client_handle)
#    for disk in disk_list:
#        if disk.shared():
#            ret.append(disk)
#
#    return ret

"""
    create raid
    @param db_handle database operation handle
    @param md_name  raid name,for example /dev/md0
    @param level    raid level,such as 0,1,4,5,6,10
    @param phy_devices physical devices ,such as /dev/sda /dev/sdb
    @param chunk    raid chunk size,only valid for 0,4,5,6,10,its unit is kib
"""
def md_create(db_handle,md_name,level,phy_devices,chunk = 0):
    ##params check
    (ret,msg) = n_raidmgr.check_create_param(md_name,level,phy_devices,chunk)
    if ret != 0:
        logging.error("md_create exception: the params of creating raid is not vaild")
        raise Exception("the params of creating raid is not vaild,%s" % msg)

    database.database_md_create(db_handle,db_ID_dev(md_name),db_ID_dev_list(phy_devices))
    logging.info("db->md_create {0}".format(md_name))
    try:
        if n_raidmgr.check_raid_exists(md_name):
            raise Exception("raid %s exists in sys" % md_name)
        n_raidmgr.raid_create(md_name,level,phy_devices,chunk)
        logging.info("sys->create_md %s" % md_name)
    except Exception,e:
        logging.error("sys->create_md {0} error,{1}".format(md_name,str(e)))
        try:
            database.database_md_remove_crashing(db_handle,db_ID_dev(md_name))
        except Exception,x:
            logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % md_name)
            raise exception.HandleError("critical exception,\
                    possible disagree,the reason: {0} delete from xml: {1}".format(e,x))
        raise e

"""
    Getting a list of the md-devices,requires the following steps:
    step one:
            get a list of the md-devices from operation system
    step two:
            traverse every item of the list and check if every item
            is in db,if true,return,otherwise continue next item
"""
def md_list(db_handle):
    ret = []
    mds = n_raidmgr.raid_list()
    for md in mds:
        if database.database_md_in_db(db_handle,db_ID_dev(md.name)):
            ret.append(md)
    return ret

"""
    remove raid
    @param db_handle database operation handle
    @param md_name  raid name,for example /dev/md0
"""
def md_remove(db_handle,md_name):
    ##params check
    (ret,msg) = n_raidmgr.check_raid_name_valid(md_name)
    if ret != 0:
        raise Exception("the params of creating raid is not vaild,%s" % msg)

    n_raidmgr.raid_remove_nor(md_name)
    logging.info("sys->remove_md %s" % md_name)
    try:
        database.database_md_remove(db_handle,db_ID_dev(md_name))
        logging.info("db->remove_md %s" % md_name)
    except Exception,e:
        logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % md_name)
        raise exception.HandleError("critical exception,possible disagree,the reason:" % str(e))

"""
    remove raid crashing
    @param db_handle database operation handle
    @param md_name  raid name,for example /dev/md0
"""
def md_remove_crashing(db_handle,md_name):
    ##params check
    (ret,msg) = n_raidmgr.check_raid_name_valid(md_name)
    if ret != 0:
        raise Exception("the params of raid removing is not vaild,%s" % msg)
    try:
        phy_disks_db = database.database_md_device_phys(db_handle,db_ID_dev(md_name))
        phy_disks = n_phydisk.wwns_to_local_names(phy_disks_db)
        ##zero those physical disks
        logging.info("n_raidmgr.raid_info_zero_batch %s" % md_name)
        n_raidmgr.raid_info_zero_batch(phy_disks)

        logging.info("database.database_md_remove %s" % md_name)
        database.database_md_remove_crashing(db_handle,db_ID_dev(md_name))
        logging.info('db->remove_md %s' % md_name)
    except Exception,e:
        logging.error("md_remove_crashing error,%s" % str(e))
        raise e

"""
    erase the raid information of the physical devices
    @param db_handle database operation handle
    @param phy_device physical device ,such as /dev/sda
"""
def md_phy_zero(db_handle,phy_device):
    database.database_md_phy_zero(db_handle,db_ID_dev(phy_device))
    logging.info("db-> md_phy_zero %s" % phy_device)
    try:
        n_raidmgr.raid_info_zero(phy_device)
        logging.info("sys-> md_phy_zero %s" % phy_device)
    except Exception,e:
        logging.error('sys->md_phy_zero error,%s' % str(e))
        raise exception.HandleError("critical exception,possible disagree,the reason:" % str(x))

"""
    lvm,create vg
    @param db_handle database operation handle
    @param name volume group name
    @param pvs physical volume,such as ["/dev/sda","/dev/sdb"]
    @return a VolumeGroup instance
"""
def vg_create(db_handle,name,pvs):
    database.database_vg_create(db_handle,name,db_ID_dev_list(pvs))
    logging.debug("db->vg_create %s" % name)
    try:
        n_lvmmgr.vg_create(name,pvs)
        logging.debug('sys->vg_create %s' % name)
    except Exception,e:
        try:
            database.database_vg_remove_crashing(db_handle,name)
        except Exception,x:
            logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % name)
            raise exception.HandleError("critical exception,possible disagree,the reason: create vg {0} failed,\
                    but delete it from failed ".format(x,e))
        raise e

#"""
#    Getting a list of the vgs,requires the following steps:
#    step one:
#            get a list of the vgs from current operation system
#    step two:
#            traverse every item of the list and check if every item
#            is in db,if true,return,otherwise continue next item
#"""
#def vg_list(db_handle):
#    ret = []
#    vgs = lvm.vgscan()
#    for vg in vgs:
#        if database.database_vg_in_db(db_handle,vg.name):
#            ret.append(vg)
#    return ret

"""
    NOW IS NOT USED !!!!

    lvm,remove vg
    @param db_handle database operation handle
    @param lvm lvm handle
    @param name volume group name
"""
def vg_remove(db_handle,lvm,name):
    pass
    #logging.debug("FOR DEBUG....163")
    #vg = lvm.get_vg(name,"w")
    #logging.debug("FOR DEBUG....165")
    #lvm.remove_vg_cover(name)
    #logging.debug("FOR DEBUG....167")
    #try:
    #    database.database_vg_remove(db_handle,name)
    #except Exception,e:
    #    logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % name)
    #    raise exception.HandleError("critical exception,possible disagree,the reason:" % str(e))

"""
    lvm,remove vg
    @param db_handle database operation handle
    @param lvm lvm handle
    @param name volume group name
"""
def vg_remove_crashing(db_handle,name):
    if not n_lvmmgr.vg_remove_check(name):
        raise exception.HandleError("Can't remove vg %s,there are lvs in it" % name)
    n_lvmmgr.vg_remove_crashing(name)

    try:
        database.database_vg_remove_crashing(db_handle,name)
    except Exception,e:
        logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % name)
        raise exception.HandleError("critical exception,possible disagree,the reason:" % str(e))

"""
    Initializes a device as a physical volume and adds it to the volume group
    @param db_handle database operation handle
    @param vg,VolumeGroup
    @param device,physical devices,such as /dev/sda
"""
def vg_add_pv(db_handle,vg_name,device):
    database.database_vg_add_pv(db_handle,vg_name,db_ID_dev(device))
    logging.debug("db vg_add_pv:add {0} into {1}".format(device,vg_name))
    try:
        n_lvmmgr.vg_add_pv(vg_name,[device])
    except Exception,e:
        try:
            database.database_vg_del_pv_crashing(db_handle,vg_name,db_ID_dev(device))
        except Exception,x:
            logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % vg_name)
            raise exception.HandleError("critical exception,possible disagree,the reason:" % str(x))
        raise e

"""
    NOW IS NOT USED !!!!!
    delete pv from the vg
    @param db_handle database operation handle
"""
def vg_del_pv(db_handle,lvm,vg_name,device):
    pass
    #database.database_vg_del_pv(db_handle,vg_name,db_ID_dev(device))
    #logging.debug("db vg_del_pv:del {0} from {1}".format(device,vg_name))
    #try:
    #    n_lvmmgr.vg_del_pv_crashing(vg_name,[device])
    #except Exception,e:
    #    try:
    #        database.database_vg_add_pv(db_handle,vg_name,db_ID_dev(device))
    #    except Exception,x:
    #        logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % device)
    #        raise exception.HandleError("critical exception,possible disagree,the reason:" % str(x))
    #    raise e

"""
    delete pv from the vg drastically,
    in other words,erase lvm information
    from the physical device
    @param db_handle database operation handle
"""
def vg_del_pv_crashing(db_handle,vg_name,device):
    database.database_vg_del_pv_crashing(db_handle,vg_name,db_ID_dev(device))
    try:
        n_lvmmgr.vg_del_pv_crashing(vg_name,[device])
    except Exception,e:
        try:
            database.database_vg_add_pv(db_handle,vg_name,db_ID_dev(device))
        except Exception,x:
            logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % device)
            raise exception.HandleError("critical exception,possible disagree,the reason:" % str(x))
        raise e

"""
    pvremove
"""
def pv_remove(db_handle,pv_name):
    n_lvmmgr.pv_remove(pv_name)
    try:
        database.database_pv_del(db_handle,db_ID_dev(pv_name))
    except Exception,e:
        logging.error("remove the information of %s from database,but failed,ERROR,ERROR!BUG,FIX ME" % pv_name)
        raise exception.HandleError("critical exception,possible disagree,the reason:" % str(e))
    
"""
    create drbd
    @param db_handle database operation handle
"""
def drbd_create(db_handle):
    pass
