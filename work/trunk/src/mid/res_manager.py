# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../cluster/resource")))
import CResourceFactory
import logging

"""
    create raid and add resource into the cluster
    @param md_name  raid name,for example /dev/md0
"""
def res_md_create(res_handle,md_name,wwns):
    try:
        res_type = CResourceFactory.GetResourceType('raid')
        res_name = CResourceFactory.GetResName('raid','/dev/' + md_name)
        res_opt = {}
        wwn_ = []
        for w in wwns:
            wwn_.append(w.replace('wwn-',''))

        res_opt['wwns'] = ','.join(wwn_)
        res_opt['raiddev'] = '/dev/' + md_name
        res_opt['force_clones'] = 'true'
        res_handle.AddResource(res_name,res_type,res_opt)
        res_handle.SetClone('clone',res_name,resType=res_type)
    except Exception as e:
        logging.error('res_handle::AddResource error ,%s'%str(e))
        raise e

def res_md_remove(res_handle,md_name):
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

"""
    create a dnt_lv resource into the cluster
    @param vg_name the name of the lv's vg
    @param lv_name the name of the lv
"""
def res_lv_create(res_handle,vg_name,lv_name):
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
    delete dnt_lv resource from the cluster
    
    when the resource is used by the other resource in
    the cluster,this resource can not be deleted,raise exception

    @param vg_name the name of the lv's vg
    @param lv_name the name of the lv
"""
def res_lv_remove(res_handle,vg_name,lv_name):
    try:
        lvname = '/dev/' + vg_name + '/' +lv_name
        ret = CResourceFactory.JudgeLvRes(lvname)
        if ret == 1:
            #not found
            logging.info("the lv resource %s is not found" % lvname)
            return ret
        if ret == -1:
            #in using
            raise Exception("the lv resource %s is in using" % lvname)
    except Exception as e:
        logging.error("CResourceFactory::JudgeLvRes %s" % str(e))
        raise e
    try:
        lvname = '/dev/' + vg_name + '/' +lv_name
        res_dict = CResourceFactory.GetResByLv(lvname)
        if not res_dict:
            raise Exception('lv[%s] do not config in the cluster'%lvname)
        res_handle.DeleteResourced(res_dict.get('id'),res_dict.get('type'))
    except Exception as e:
        logging.error('res_handle::DeleteResource error ,%s'%str(e))
        raise e

