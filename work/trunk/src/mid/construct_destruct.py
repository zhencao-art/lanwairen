# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../storate")))
import n_lvmmgr,n_raidmgr
sys.path.append(os.path.abspath(os.path.join(__file__,"../../cluster/resource")))
import block_mgr, CResourceFactory
import logging , database

"""
    create raid and add resource into the cluster
    @param db_handle database operation handle
    @param md_name  raid name,for example /dev/md0
    @param level    raid level,such as 0,1,4,5,6,10
    @param phy_devices physical devices ,such as /dev/sda /dev/sdb
    @param chunk    raid chunk size,only valid for 0,4,5,6,10,its unit is kib
"""
def res_md_create(res_handle,db_handle,md_name,level,phy_devices,chunk = 0):
    try:
        block_mgr.md_create(db_handle,md_name,level,phy_devices,chunk)
    except Exception as e:
        logging.error("block_mgr::md_create error,%s" % str(e))
        raise e
    try:
        res_type = CResourceFactory.GetResourceType('raid')
        res_name = CResourceFactory.GetResName('raid','/dev/' + md_name)
        res_opt = {}
        wwn = block_mgr.db_ID_dev_list(phy_devices)
        wwn_ = []
        for w in wwn:
            wwn_.append(w.replace('wwn-',''))

        res_opt['wwns'] = ','.join(wwn_)
        res_opt['raiddev'] = '/dev/' + md_name
        res_opt['force_clones'] = 'true'
        res_handle.AddResource(res_name,res_type,res_opt)
        res_handle.SetClone('clone',res_name,resType=res_type)
    except Exception as e:
        logging.error('res_handle::AddResource error ,%s'%str(e))
        raise e

"""
    remove raid and delete resource from the cluster

    when the resource is used by the other resource in 
    the cluster,this resource can not be deleted,raise exception

    @param db_handle database operation handle
    @param md_name  raid name,for example /dev/md0
"""
def res_md_remove(res_handle,db_handle,md_name,crashing):
    res_rm = False
    sys_rm = True
    flag  = False

    try:
        (ret,msg) = database.device_is_used(db_handle,block_mgr.db_ID_dev(md_name))
        if ret:
            flag = True
            raise Exception("remove md {0} error,used by {1}".format(md_name,msg))
    except Exception,e:
        logging.debug("res_md_remove %s" % str(e))
        raise e

    try:
        ret = CResourceFactory.JudgeRaidRes('/dev/' + md_name)
        if ret == 1:
            #not found
            logging.info("the md resource %s is not found" % md_name)
            #raise Exception("the md resource %s is not found" % md_name)

        if ret == -1:
            #in using
            raise Exception("the md resource %s is in using" % md_name)

        if ret == 0:
            res_rm = True
    except Exception as e:
        logging.error("CResourceFactory::JudgeRaidRes %s" % str(e))
        raise e

    if res_rm:
        try:
            # add code here
            res_dict = CResourceFactory.GetResByMd('/dev/' + md_name)
            if not res_dict:
                raise Exception('raid[%s] do not config in the cluster')
            logging.info("res_handle.DeleteResource: %s" % md_name)
            res_handle.DeleteResourced(res_dict.get('clone'),res_dict.get('type'))
        except Exception as e:
            logging.error('res_handle::DeleteResource error ,%s'%str(e))
            raise e

    if sys_rm:
        try:
            logging.info("block_mgr.md_remove_crashing %s" % md_name)
            if not crashing:
                block_mgr.md_remove(db_handle,md_name) ##not use
            else:
                block_mgr.md_remove_crashing(db_handle,md_name)
        except Exception as e:
            logging.error("delete the md device error,%s" % str(e))
            raise e

"""
    create a lv and add a resource into the cluster
    @param lvm_handle lvm operation handle
    @param vg_name the name of the lv's vg
    @param lv_name the name of the lv
    @param lv_size the size of the lv
    @param lv_size_unit the unit of the lv's size
"""
def res_lv_create(res_handle,vg_name,lv_name,lv_size,lv_size_unit):
   try:
       if n_lvmmgr.check_lv_exists(lv_name,vg_name):
           raise Exception("lv: {0}/{1} is exists in sys".format(vg_name,lv_name))

       n_lvmmgr.lv_linear_create(vg_name,lv_name,lv_size,lv_size_unit)
   except Exception as e:
       logging.error("lvm_handle::create_linear_vol error,%s" % str(e))
       raise e

   try:
       lvname = '/dev/' + vg_name + '/' +lv_name
       res_type = CResourceFactory.GetResourceType('lv')
       res_name = CResourceFactory.GetResName('lv',lvname)
       res_opt = {}
       res_opt['lv_name'] = lvname
       res_handle.AddResource(res_name,res_type,res_opt)
   except Exception as e:
       logging.error('res_handle::AddResource error ,%s'%str(e))
       raise e

"""
    delete a lv and delete its resource from the cluster
    
    when the resource is used by the other resource in
    the cluster,this resource can not be deleted,raise exception

    @param lvm_handle lvm operation handle
    @param vg_name the name of the lv's vg
    @param lv_name the name of the lv
"""
def res_lv_remove(res_handle,vg_name,lv_name):
    sys_rm = False
    res_rm = False

    try:
        lvname = '/dev/' + vg_name + '/' +lv_name
        ret = CResourceFactory.JudgeLvRes(lvname)
        if ret == 1:
            #not found
            logging.info("the lv resource %s is not found" % lvname)
            sys_rm = True

        if ret == -1:
            #in using
            raise Exception("the lv resource %s is in using" % lvname)

        if ret == 0:
            res_rm = True
            sys_rm = True
    except Exception as e:
        logging.error("CResourceFactory::JudgeLvRes %s" % str(e))
        raise e

    if res_rm:
        try:
            lvname = '/dev/' + vg_name + '/' +lv_name
            res_dict = CResourceFactory.GetResByLv(lvname)
            if not res_dict:
                raise Exception('lv[%s] do not config in the cluster'%lvname)
            res_handle.DeleteResourced(res_dict.get('id'),res_dict.get('type'))
        except Exception as e:
            logging.error('res_handle::DeleteResource error ,%s'%str(e))
            raise e

    if sys_rm:
        try:
            if not n_lvmmgr.check_lv_exists(lv_name,vg_name):
                raise Exception("lv: {0}/{1} is not found in sys".format(vg_name,lv_name))
            n_lvmmgr.lv_remove(vg_name,lv_name)
        except Exception as e:
            logging.error("lvm_handle::remove_lv error,%s" % str(e))
            raise e
