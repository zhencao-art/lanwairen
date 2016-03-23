#!/usr/bin/env python


import CStonithSCSI , CStonithIPMI
import commands,logging
import sys,os
sys.path.append(os.path.abspath(os.path.join(__file__,"../resource")))
from common import CXmlMgr
import CResourceFactory

def GetStonith(stName,stType,stOpt):
    st = CStonithIPMI.CStonithIPMI(stName,stType,stOpt)
    return st

def CheckStonith(stName):
    return CResourceFactory.CheckResource(stName)

def CheckSafy(stName,stType,stOpt):
    stAttr = CResourceFactory.GetState('all')
    opt = dict(stOpt)
    for attr in stAttr:
        if stName == attr.get('id'):
            raise Exception('fencing agent['+stName+'] has already exist in the cluster')
        if stType == 'fence_scsi':
            if opt.get('devices')==attr.get('devices'):
                raise Exception('fencing devices='+opt.get('devices')+' has been used by '+attr.get('id'))
        elif stType == 'fence_ipmilan':
            if opt.get('ip')==attr.get('ipaddr'):
                raise Exception('fencing ipaddr='+opt.get('ipaddr')+' has been used by '+attr.get('id'))
    return False

def GetStState(stName):
    try:
        result = []
        cfg = CXmlMgr.CXmlMgr('cib_cfg')
        nodelist = ['configuration','resources','primitive']
        reslist = cfg.GetNode(None,nodelist)
        if reslist!=None :
            for res in reslist :
                stType = cfg.GetValue(res,'class')
                name = cfg.GetValue(res,'id')
                if stType=='stonith' and (name==stName or 'all' == stName) :
                    tmp = {}
                    tmp.update(res.attrib)
                    sub = CResourceFactory.get_sub_attr(cfg,res)
                    tmp.update(sub)
                    tmp['node_state'] = CResourceFactory.GetNodeState(res.get('id'))
                    result.append(tmp)

    except Exception as e:
        raise e
    return result

