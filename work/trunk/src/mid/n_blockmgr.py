# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys,logging

sys.path.append(os.path.abspath(os.path.join(__file__,"../../db")))
import configuredb

sys.path.append(os.path.abspath(os.path.join(__file__,"../../storage")))
import n_phydisk,n_lvmmgr,n_raidmgr

import res_manager

class BlockDisk:
    def __init__(self):
        self.config = None
        self.info   = None
        self.user   = None
        self.online = None
        self.inited = None

class BlockRaid:
    def __init__(self):
        self.config = None
        self.user   = None
        self.info   = None
        self.online = None

class BlockVG:
    def __init__(self):
        self.config = None
        self.info   = None
        self.online = None

class BlockLV:
    def __init__(self):
        self.config = None
        self.info   = None
        self.online = None
        self.user   = None

class BlockOpError:
    SUCCESS = 0
    EINVAL = 1
    EDBR   = 2
    EDBW   = 3
    CEEXIST = 4
    ERAIDOP = 5
    ERESOP = 6
    EDBNOTFOUND = 7
    EUSED = 8
    ELVOP   = 9
    EVGOP   =10
    EPHYDISKOP = 11
    ESYNCDB = 12

    EUNKONW = 13

###############################################
#               DISK  API                     #
###############################################
def block_disk_list():
    configuredb.g_db_rw_lock.read_lock()
    db_handle = configuredb.db_file_load()
    configuredb.g_db_rw_lock.read_unlock()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    ret_objs = []
    try:
        phy_objs = n_phydisk.disk_block_obj_list()
        db_disk_list = configuredb.db_disk_list(db_handle)

        db_disk_stats = configuredb.db_disk_stat_used(db_handle)

        online_list = []
        if phy_objs:
            for i in phy_objs:
                tmp = BlockDisk()
                tmp.info = i
                tmp.online = True
                wwn = n_phydisk.disk_block_wwn(i.name)
                stat = configuredb._db_disk_stat_find(db_disk_stats,wwn)
                if stat:
                    tmp.user = stat[wwn]
                if configuredb._db_disk_check(wwn,db_disk_list):
                    tmp.inited = True
                else:
                    tmp.inited = False
                online_list.append(wwn)
                ret_objs.append(tmp)
        if db_disk_list:
            for i in db_disk_list:
                if not i.name in online_list:
                    tmp = BlockDisk()
                    tmp.config = i
                    tmp.online = False
                    tmp.inited = True
                    stat = configuredb._db_disk_stat_find(db_disk_stats,i.name)
                    if stat:
                        tmp.user = stat[i.name]
                    ret_objs.append(tmp)
    except Exception as e:
        msg = 'phy disk list error,%s' % str(e)
        logging.error(msg)
        return (BlockOpError.EPHYDISKOP,msg)
    return (BlockOpError.SUCCESS,ret_objs)

"""
    disk_name /dev/sda
"""
def _block_disk_init(disk_name):
    db_handle = configuredb.db_file_load()

    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    try:
        db_disk_objs = configuredb.db_disk_list(db_handle)
        phy_objs = n_phydisk.disk_block_obj_list()
        flag = False
        for i in phy_objs:
            if i.name == disk_name:
                flag = True
                wwn = n_phydisk.disk_block_wwn(disk_name)
                if configuredb.db_disk_check(wwn,db_handle):
                    msg = '%s is inited already' % disk_name
                    logging.error(msg)
                    return (BlockOpError.EINVAL,msg)
                disk_config = configuredb.DiskConfig(wwn,i.size,i.slot,i.rotational,i.protocol)
                configuredb.db_disk_add(disk_config,db_handle)
        if flag:
            configuredb.db_file_store(db_handle)
        else:
            raise Exception('BUG!!FIX ME')
    except Exception as e:
        msg = 'phy disk init error,%s' % str(e)
        logging.error(msg)
        return (BlockOpError.EPHYDISKOP,msg)

    return (BlockOpError.SUCCESS,None)

def block_disk_init(disk_name):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_disk_init(disk_name)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)
###############################################
#               RAID  API                     #
###############################################
"""
    md_name must be such md0
    members must be such /dev/sda
"""
def _block_create_raid(res_handle,md_name,level,members,chunk = 0):
    (ret,msg) = n_raidmgr.check_create_param(md_name,level,members,chunk)
    if ret != 0:
        logging.error("md_create exception: the params of creating raid is not vaild")
        return (BlockOpError.EINVAL,msg)

    ###check if members are online
    sys_disk_names = n_phydisk.disk_block_name_list()

    for i in members:
        if not i in sys_disk_names:
            msg = "%s is not online in sys" % i
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
    members_wwns = n_phydisk.disk_block_wwns(members)

    db_handle = configuredb.db_file_load()

    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)

    ##check if md_name
    if configuredb.db_raid_check(md_name,db_handle):
        msg = "%s is exists in db_file" % md_name
        logging.error(msg)
        return (BlockOpError.EEXIST,msg)

    ##check if members_wwns is used or uninited
    db_disk_stats_used = configuredb.db_disk_stat_used(db_handle)
    db_disk_inited = configuredb.db_disk_list(db_handle)
    for i in members_wwns:
        if not configuredb._db_disk_check(i,db_disk_inited):
            msg = "%s is not inited" % i
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
        db_disk_stat = configuredb._db_disk_stat_find(db_disk_stats_used,i)
        if db_disk_stat:
                msg = "disk {0} is used by {1}".format(i,db_disk_stat[i])
                logging.error(msg)
                return (BlockOpError.EUSED,msg)
    logging.info('the check in db of creating %s is ok' % md_name)
    ##sys create raid
    try:
        if n_raidmgr.check_raid_exists(md_name):
            msg = "raid %s exists in sys" % md_name
            logging.error(msg)
            return (BlockOpError.EEXIST,msg)
        n_raidmgr.raid_create(md_name,level,members,chunk)
        logging.info("sys->create_md %s" % md_name)
    except Exception,e:
        msg = "sys->create_md {0} error,{1}".format(md_name,str(e))
        logging.error(msg)
        return (BlockOpError.ERAIDOP,msg)
    ##create cluster raid resource
   # try:
   #     res_manager.res_md_create(res_handle,md_name,members_wwns)
   # except Exception,e:
   #     logging.error("create cluster raid resource failed,%s" % str(e))
   #     return (BlockOpError.ERESOP,str(e))
    ##store infomation into db
    sys_obj = n_raidmgr.construct_raid_obj(md_name)
    configuredb.db_raid_add(configuredb.RaidConfig(md_name,sys_obj.size,sys_obj.level,sys_obj.chunk,members_wwns),db_handle)
    if ret != 0:
        logging.error("store raid {0} configure into db error {1}".format(md_name,msg))
        return (BlockOpError.EDBW,msg)
    logging.info("db->md_create {0}".format(md_name))
    ##flush db
    configuredb.db_file_store(db_handle)

    return (BlockOpError.SUCCESS,None)

def block_create_raid(res_handle,md_name,level,members,chunk = 0):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_create_raid(res_handle,md_name,level,members,chunk)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def _block_remove_raid(res_handle,md_name):
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    raid_config = configuredb.db_raid_check(md_name,db_handle)
    if not raid_config:
        msg = "Can not found raid %s config in db" % md_name
        logging.error(msg)
        return (BlockOpError.EDBNOTFOUND,msg)
    else:
        md_name_db_stat = configuredb.db_raid_stat_find(db_handle,md_name)
        if md_name_db_stat:
            msg = '{0} is used,can not be deleted'.format(md_name,md_name_db_stat[md_name])
            logging.error(msg)
            return (BlockOpError.EUSED,msg)
        ##remove cluster res
        #try:
        #    res_manager.res_md_remove(res_handle,md_name)
        #except Exception,e:
        #    return (BlockOpError.ERESOP,str(e))
        try:
            n_raidmgr.raid_stop(md_name)
            n_raidmgr.raid_stop(md_name)
            logging.info('raid_sop %s' % md_name)
        except Exception as e:
            logging.debug("raid_stop error %s" % str(e))
        ##zero members
        phy_disks = []
        for disk in raid_config.disks:
            phy_disks.append(n_phydisk.wwn_to_local_name(disk))
        n_raidmgr.raid_info_zero_batch(phy_disks)
        logging.info("n_raidmgr,raid_info_zero_batch {0} for {1}".format(phy_disks,md_name))
        ##db remove
        configuredb.db_raid_del(md_name,db_handle)
        logging.info("db->remove_md %s" % md_name)
        ##flush db
        configuredb.db_file_store(db_handle)
    return (BlockOpError.SUCCESS,None)

def block_remove_raid(res_handle,md_name):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = block_remove_raid(res_handle,md_name)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def block_list_raid():
    configuredb.g_db_rw_lock.read_lock()
    db_handle = configuredb.db_file_load()
    configuredb.g_db_rw_lock.read_unlock()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)

    raid_info_list = []
    try:
        db_raid_list = configuredb.db_raid_list(db_handle)
        if not db_raid_list:
            return (BlockOpError.SUCCESS,raid_info_list)
        db_raid_stats = configuredb.db_raid_stat_used(db_handle)
        for db_raid in db_raid_list:
            ##set user filed
            raid_obj = BlockRaid()
            raid_obj.config = db_raid
            db_raid_stat = configuredb._db_raid_stat_find(db_raid_stats,db_raid.name)
            if db_raid_stat and db_raid_stat.has_key(db_raid.name):
                raid_obj.user = db_raid_stat[db_raid.name]
            else:
                raid_obj.user = None
            if n_raidmgr.check_raid_exists(db_raid.name):
                raid_obj.info = n_raidmgr.construct_raid_obj(db_raid.name)
                raid_obj.online = True
                raid_obj.config.disks=n_phydisk.wwns_to_local_names(raid_obj.config.disks)
            else:
                raid_obj.online = False
            raid_info_list.append(raid_obj)
    except Exception as e:
        return (BlockOpError.ERAIDOP,str(e))
    return BlockOpError.SUCCESS,raid_info_list

"""
    Not used
"""
def block_info_raid(md_name):
    (ret,raid_list) = block_list_raid()
    if BlockOpError.SUCCESS != ret:
        return (ret,None)
    for i in raid_list:
        if i.config.name == md_name:
            return BlockOpError.SUCCESS,i
    return BlockOpError.EDBNOTFOUND,None

def block_manage_raid():
    pass
###############################################
#                  VG API                     #
###############################################
def _block_create_vg(vg_name,phy_devices):
    ###check phy_devices
    """
        1. physical devices must be raid
        2. physical devices must be online
        3. physical devices must be not used
        4. can not exists in db
    """
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    raid_stat_used = configuredb.db_raid_stat_used(db_handle)
    raid_name_list_cur = n_raidmgr.raid_name_list()

    for i in phy_devices:
        raid_name  = i.split('/')[2]
        if not raid_name in raid_name_list_cur:
            msg = 'input phy_devices %s is not md device or not found in sys' % raid_name
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
        stat_found = configuredb._db_raid_stat_find(raid_stat_used,raid_name)
        if stat_found:
            msg = 'input phy_devices {0} is used by {1}'.format(raid_name,stat_found[raid_name])
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
    if configuredb.db_vg_check(vg_name,db_handle):
        msg = 'input vg_name %s is exists in db' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    try:
        n_lvmmgr.vg_create(vg_name,phy_devices)
    except Exception as e:
        return (BlockOpError.EVGOP,str(e))
    input_raids = []
    for i in phy_devices:
        input_raids.append(i.split('/')[2])
    try:
        sys_obj = None
        sys_obj = n_lvmmgr.vg_display(vg_name)
    except Exception as e:
        msg = 'BUG!!! FIX ME'
        logging.error(msg)
        return BlockOpError.UNKONW,msg
    db_obj = configuredb.VgConfig(vg_name,sys_obj.total_size(),input_raids)
    configuredb.db_vg_add(db_obj,db_handle)
    configuredb.db_file_store(db_handle)

    return BlockOpError.SUCCESS,None

def block_create_vg(vg_name,phy_devices):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_create_vg(vg_name,phy_devices)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def _block_remove_vg(vg_name):
    """
        1. must be exist in db
        2. there is not lv in vg
    """
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)

    ##check vg
    vg_config = configuredb.db_vg_check(vg_name,db_handle)
    if not vg_config:
        msg = "%s is not exists in db" % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    ###check lv
    if configuredb.db_lv_list_by_vg(vg_name,db_handle):
        msg = "there are lvs in %s" % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    try:
        n_lvmmgr.vg_remove_crashing(vg_name)
    except Exception as e:
        return (BlockOpError.EVGOP,str(e))

    configuredb.db_vg_del(vg_name,db_handle)
    configuredb.db_file_store(db_handle)

    return BlockOpError.SUCCESS,None

def block_remove_vg(vg_name):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_remove_vg(vg_name)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def block_list_vg():
    configuredb.g_db_rw_lock.read_lock()
    db_handle = configuredb.db_file_load()
    configuredb.g_db_rw_lock.read_unlock()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    try:
        vg_list = n_lvmmgr.vg_list()
    except Exception as e:
        msg = 'n_lvmmgr.vg_list error %s' % str(e)
        logging.error(msg)
        return (BlockOpError.OPVG,msg)

    db_vg_list = configuredb.db_vg_list(db_handle)
    if not db_vg_list:
        return BlockOpError.SUCCESS,None
    ret_obj = []
    for vg in db_vg_list:
        vg_obj = BlockVG()
        vg_obj.config = vg
        if vg_list:
            flag = False
            for i in vg_list:
                if i.name == vg.name:
                    vg_obj.online = True
                    vg_obj.info = i
                    flag = True
            if not flag:
                vg_obj.online = False
        ret_obj.append(vg_obj)
    return (BlockOpError.SUCCESS,ret_obj)

def block_info_vg(vg_name):
    configuredb.g_db_rw_lock.read_lock()
    db_handle = configuredb.db_file_load()
    configuredb.g_db_rw_lock.read_unlock()

    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    db_vg = configuredb.db_vg_check(vg_name,db_handle)
    if not db_vg:
        msg = 'not found %s in db' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)
    else:
        vg_sys = None
        try:
            vg_sys = n_lvmmgr.vg_display(vg_name)
        except:
            vg_sys = None
            msg = 'not found %s in sys,is offline' % vg_name
            logging.debug(msg)
        vg_obj = BlockVG()
        vg_obj.config = db_vg
        if not vg_sys:
            vg_obj.online = False
        else:
            vg_obj.online = True
            vg_obj.info = vg_sys
        return (BlockOpError.SUCCESS,vg_obj)

def _block_extend_vg(vg_name,phy_devices):
    """
        1. must be exists in db and sys
        2. phy_devices must be raid devices and exists in sys
        3. phy_devices must be not used by others
    """
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.DBR,msg)
    raid_stat_used = configuredb.db_raid_stat_used(db_handle)
    raid_name_list_cur = n_raidmgr.raid_name_list()

    if not vg_name in n_lvmmgr.vg_name_list():
        msg = '%s is not found in sys' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    if not configuredb.db_vg_check(vg_name,db_handle):
        msg = 'input vg_name %s is not found in db' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    for i in phy_devices:
        raid_name  = i.split('/')[2]
        if not raid_name in raid_name_list_cur:
            msg = 'input phy_devices %s is not md device or not found in sys' % raid_name
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
        stat_found = configuredb._db_raid_stat_find(raid_stat_used,raid_name)
        if stat_found:
            msg = 'input phy_devices {0} is used by {1}'.format(raid_name,stat_found[raid_name])
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
    try:
        n_lvmmgr.vg_add_pv(vg_name,phy_devices)
    except Exception as e:
        msg = str(e)
        logging.error(msg)
        return (BlockOpError.EVGOP,msg)

    pvs = []
    for i in phy_devices:
        pvs.append(i.split('/')[2])
    if -1 == configuredb.db_vg_add_pv(vg_name,pvs,db_handle):
        msg = 'Bug!!! FIX ME'
        loggin.error(msg)
        return (BlockOpError.UNKONW,msg)
    ##mod the size of the vg
    try:
        new_vg_obj = n_lvmmgr.vg_display(vg_name)
    except Exception as e:
        msg = 'Bug!!! FIX ME %s' % str(e)
        loggin.error(msg)
        return (BlockOpError.UNKONW,msg)
    configuredb.db_vg_mod_size(vg_name,new_vg_obj.total_size(),db_handle)
    configuredb.db_file_store(db_handle)

    return (BlockOpError.SUCCESS,None)

def block_extend_vg(vg_name,phy_devices):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_extend_vg(vg_name,phy_devices)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def _block_reduce_vg(vg_name,phy_devices):
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.EDBR,msg)
    raid_stat_used = configuredb.db_raid_stat_used(db_handle)
    raid_name_list_cur = n_raidmgr.raid_name_list()

    if not vg_name in n_lvmmgr.vg_name_list():
        msg = '%s is not found in sys' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    if not configuredb.db_vg_check(vg_name,db_handle):
        msg = 'input vg_name %s is not found in db' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    for i in phy_devices:
        raid_name  = i.split('/')[2]
        stat_found = configuredb._db_raid_stat_find(raid_stat_used,raid_name)
        if not stat_found:
            msg = 'input phy_devices {0} is not used by {1}'.format(raid_name,vg_name)
            logging.error(msg)
            return (BlockOpError.EINVAL,msg)
    try:
        n_lvmmgr.vg_del_pv_crashing(vg_name,phy_devices)
    except Exception as e:
        msg = str(e)
        logging.error(msg)
        return (BlockOpError.EVGOP,msg)

    pvs = []
    for i in phy_devices:
        pvs.append(i.split('/')[2])
    if -1 == configuredb.db_vg_del_pv(vg_name,pvs,db_handle):
        msg = 'Bug!!! FIX ME'
        loggin.error(msg)
        return (BlockOpError.UNKONW,msg)
    try:
        new_vg_obj = n_lvmmgr.vg_display(vg_name)
    except Exception as e:
        msg = 'Bug!!! FIX ME %s' % str(e)
        loggin.error(msg)
        return (BlockOpError.UNKONW,msg)
    configuredb.db_vg_mod_size(vg_name,new_vg_obj.total_size(),db_handle)
    configuredb.db_file_store(db_handle)

    return (BlockOpError.SUCCESS,None)

def block_reduce_vg(vg_name,phy_devices):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_reduce_vg(vg_name,phy_devices)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

###############################################
#                  LV API                     #
###############################################
def _block_create_lv(res_handle,vg_name,lv_name,lv_size,lv_size_unit):
    # check> step 1: if db has vg/lv
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.EDBR,msg)

    if not configuredb.db_vg_check(vg_name,db_handle):
        msg = 'input vg %s is not found in db' % vg_name
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    if configuredb.db_lv_check(vg_name,lv_name,db_handle):
        msg = 'input lv {0}/{1} is exists in db'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    try:
        if not vg_name in n_lvmmgr.vg_name_list():
            raise Exception('Volume Group %s is not found in sys' % vg_name)
        if n_lvmmgr.check_lv_exists(lv_name,vg_name):
            raise Exception("lv: {0}/{1} is exists in sys".format(vg_name,lv_name))
        n_lvmmgr.lv_linear_create(vg_name,lv_name,lv_size,lv_size_unit)
    except Exception as e:
        return  BlockOpError.ELVOP,str(e)
    try:
        res_manager.res_lv_create(res_handle,vg_name,lv_name)
    except Exception as e:
       return  BlockOpError.ERESOP,str(e)

    db_lv_obj = configuredb.LvConfig(lv_name,vg_name,lv_size)
    configuredb.db_lv_add(db_lv_obj,db_handle)
    configuredb.db_file_store(db_handle)

    return (BlockOpError.SUCCESS,None)

def block_create_lv(res_handle,vg_name,lv_name,lv_size,lv_size_unit):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_create_lv(res_handle,vg_name,lv_name,lv_size,lv_size_unit)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def _block_remove_lv(res_handle,vg_name,lv_name):
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.EDBR,msg)

    if not configuredb.db_lv_check(vg_name,lv_name,db_handle):
        msg = 'input lv {0}/{1} is not found in db'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    try:
        res_manager.res_lv_remove(res_handle,vg_name,lv_name)
    except Exception as e:
        return  BlockOpError.ELVOP,str(e)
    try:
        if not n_lvmmgr.check_lv_exists(lv_name,vg_name):
            raise Exception("lv: {0}/{1} is not found in sys".format(vg_name,lv_name))
        n_lvmmgr.lv_remove(vg_name,lv_name)
    except Exception as e:
        logging.error("lvm_handle::remove_lv error,%s" % str(e))
        return  BlockOpError.ERESOP,str(e)

    configuredb.db_lv_del(vg_name,lv_name,db_handle)
    configuredb.db_file_store(db_handle)

    return  BlockOpError.SUCCESS,None

def block_remove_lv(res_handle,vg_name,lv_name):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_remove_lv(res_handle,vg_name,lv_name)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def block_list_lv():
    configuredb.g_db_rw_lock.read_lock()
    db_handle = configuredb.db_file_load()
    configuredb.g_db_rw_lock.read_unlock()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.EDBR,msg)

    try:
        lv_paths = n_lvmmgr.lv_local_path_list()
    except Exception as e:
        msg = 'n_lvmmgr.lv_name_list error %s' % str(e)
        logging.error(msg)
        return  BlockOpError.ELVOP,msg

    db_lv_objs = configuredb.db_lv_list(db_handle)

    if not db_lv_objs:
        logging.info('lv list is empty  in db')
        return  BlockOpError.SUCCESS,None

    ret_objs = []
    for i in db_lv_objs:
        obj = BlockLV()
        obj.config = i
        ##fill user filed

        local_path = i.vg_name + '/' + i.name
        if n_lvmmgr.check_lv_local_path(local_path,lv_paths):
            obj.online = True
        else:
            obj.online = False
        ret_objs.append(obj)

    return  (BlockOpError.SUCCESS,ret_objs)

def block_info_lv():
    pass


def _block_extend_lv(vg_name,lv_name,size,size_unit):
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.EDBR,msg)

    if not configuredb.db_lv_check(vg_name,lv_name,db_handle):
        msg = 'input lv {0}/{1} is not found in db'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    if not n_lvmmgr.check_lv_exists(lv_name,vg_name):
        msg = 'input lv {0}/{1} is not found in sys'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    try:
        n_lvmmgr.lv_extend(vg_name,lv_name,size,size_unit)
    except Exception as e:
        msg ='n_lvmmgr.lv_extend %s' % str(e)
        logging.error(msg)
        return  BlockOpError.ELVOP,msg
    try:
        new_obj = n_lvmmgr.lv_display(vg_name + '/' + lv_name)
    except Exception as e:
        msg =  'n_lvmmgr.lv_display error %s' % str(e)
        logging.error('BUG! FIX ME %s' % msg)
        return (BlockOpError.UNKONW,msg)
    if configuredb.db_lv_mod_size(vg_name,lv_name,new_obj.size(),db_handle):
        msg = 'Flush new size into db failed,not found {0}/{1} in db'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.UNKONW,msg)
    configuredb.db_file_store(db_handle)
    return  (BlockOpError.SUCCESS,None)

def block_extend_lv(vg_name,lv_name,size,size_unit):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_extend_lv(vg_name,lv_name,size,size_unit)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)

def _block_reduce_lv(vg_name,lv_name,size,size_unit):
    db_handle = configuredb.db_file_load()
    if None == db_handle:
        msg = "load db_file %s error" % configuredb.database_file
        logging.error(msg)
        return (BlockOpError.EDBR,msg)

    if not configuredb.db_lv_check(vg_name,lv_name,db_handle):
        msg = 'input lv {0}/{1} is not found in db'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    if not n_lvmmgr.check_lv_exists(lv_name,vg_name):
        msg = 'input lv {0}/{1} is not found in sys'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.EINVAL,msg)

    try:
        n_lvmmgr.lv_reduce(vg_name,lv_name,size,size_unit)
    except Exception as e:
        msg ='n_lvmmgr.lv_reduce %s' % str(e)
        logging.error(msg)
        return  BlockOpError.ELVOP,msg
    try:
        new_obj = n_lvmmgr.lv_display(vg_name + '/' + lv_name)
    except Exception as e:
        msg =  'n_lvmmgr.lv_display error %s' % str(e)
        logging.error('BUG! FIX ME %s' % msg)
        return (BlockOpError.UNKONW,msg)

    if configuredb.db_lv_mod_size(vg_name,lv_name,new_obj.size(),db_handle):
        msg = 'Flush new size into db failed,not found {0}/{1} in db'.format(vg_name,lv_name)
        logging.error(msg)
        return (BlockOpError.UNKONW,msg)
    configuredb.db_file_store(db_handle)
    return  (BlockOpError.SUCCESS,None)

def block_reduce_lv(vg_name,lv_name,size,size_unit):
    configuredb.g_db_rw_lock.write_lock()
    (ret,msg) = _block_reduce_lv(vg_name,lv_name,size,size_unit)
    configuredb.g_db_rw_lock.write_unlock()
    return (ret,msg)
