#!/usr/bin/env python

import CConstraintBase,CConsLocation,CConsColocation,CConsOrder,CConsSet
import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../')
from common import CXmlMgr
sys.path.append(os.path.abspath(os.path.join(__file__,"../resource")))
import CResourceFactory

def GetConstraint(consType,consOpt):
    if consType == 'order' :
        cons = CConsOrder.CConsOrder(consType,consOpt)
    elif consType == 'colocation' :
        cons = CConsColocation.CConsColocation(consType,consOpt)
    elif consType == 'location' :
        cons = CConsLocation.CConsLocation(consType,consOpt)
    elif consType == 'set' :
        cons = CConsSet.CConsSet(consType,consOpt)
    elif consType == 'base':
        cons = CConstraintBase.CConstraintBase(None,None)
    else:
        logging.error('constraint type:'+ consType+' is not a vaild type')
        cons = None
    return cons

def CheckCons(resName):
    cfg = CResourceFactory.cfg
    nodelist = ['configuration','constraints']
    conlist = cfg.GetNode(None,nodelist)
    if conlist!=None :
        for res in conlist :
            consId = cfg.GetAttr(res,'rsc_colocation')
            for l in consId:
                if l.get('id') == resName:
                    return l
            consId = cfg.GetAttr(res,'rsc_location')
            for l in consId:
                if l.get('id') == resName:
                    return l
            consId = cfg.GetAttr(res,'rsc_order')
            for l in consId:
                if l.get('id') == resName:
                    return l
    return None

def GetOrderCons(cfg_name = ''):
    if not cfg_name:
        cfg = CResourceFactory.cfg
    else:
        cfg = CXmlMgr.CXmlMgr(cfg_name,True)
    nodelist = ['configuration','constraints']
    conlist = cfg.GetNode(None,nodelist)
    result = []
    if conlist!=None :
        for res in conlist :
            att = cfg.GetAttr(res,'rsc_order')
            if att!= None:
                result += att
    return result
    
def GetLocationCons(cfg_name = ''):
    if not cfg_name:
        cfg = CResourceFactory.cfg
    else:
        cfg = CXmlMgr.CXmlMgr(cfg_name,True)
    nodelist = ['configuration','constraints']
    conlist = cfg.GetNode(None,nodelist)
    result = []
    if conlist!=None :
        for res in conlist :
            att = cfg.GetAttr(res,'rsc_location')
            if att!= None:
                result += att
    return result

def CheckByRes(res_name,cons_type = 'location',cfg_name = ''):
    if cons_type == 'location':
        cons_list = GetLocationCons(cfg_name)
    elif cons_type == 'order':
        cons_list = GetOrderCons(cfg_name)
    elif cons_type == 'colocation':
        cons_list = GetColocationCons(cfg_name)
    else:
        cons_list = GetCons(cfg_name)
    for con in cons_list:
        rsc = con.get('rsc')
        first = con.get('first')
        then = con.get('then')
        wrsc = con.get('with-rsc')
        if (rsc!=None and rsc == res_name) or\
            (first!=None and first==res_name) or\
            (wrsc!=None and wrsc==res_name) or\
            (then!=None and then==res_name) :
            return True
    return False


def GetColocationCons(cfg_name = ''):
    if not cfg_name:
        cfg = CResourceFactory.cfg
    else:
        cfg = CXmlMgr.CXmlMgr(cfg_name,True)
    nodelist = ['configuration','constraints']
    conlist = cfg.GetNode(None,nodelist)
    result = []
    if conlist!=None :
        for res in conlist :
            att = cfg.GetAttr(res,'rsc_colocation')
            if att!= None:
                result += att
    return result

#get all constraint
def GetCons(cfg_name = 'cons_cfg'):
    try:
        if cfg_name=='cons_cfg':
            cfg = CResourceFactory.cfg
        else:
            cfg = CXmlMgr.CXmlMgr(cfg_name,not cfg_name=='cons_cfg')
        nodelist = ['configuration','constraints']
        conlist = cfg.GetNode(None,nodelist)
        result = []
        if conlist!=None :
            for res in conlist :
                att = cfg.GetAttr(res,'rsc_colocation')
                if att!= None:
                    result += att
                att = cfg.GetAttr(res,'rsc_location')
                if att!= None:
                    result += att
                att = cfg.GetAttr(res,'rsc_order')
                if att!= None:
                    result += att
    except Exception as e:
        raise e
    return result

def GetConsByRes(resName,cfg_name='cons_cfg'):
    cons = GetCons(cfg_name)
    result = []
    try:
        for con in cons:
            rsc = con.get('rsc')
            first = con.get('first')
            then = con.get('then')
            wrsc = con.get('with-rsc')
            if (rsc!=None and rsc == resName) or\
                (first!=None and first==resName) or\
                (wrsc!=None and wrsc==resName) or\
                (then!=None and then==resName) :
                result.append(con)
    except Exception as e:
        raise e
    return result

def GetConsByMd(md_name,cfg_name = 'cons_cfg'):
    cons_list = GetCons(cfg_name)
    result = []
    for con in cons_list:
        bFlag = False
        for md in md_name:
            if md in con.get('id'):
                bFlag = True
                break
        if bFlag and con.get('tag') == 'rsc_order' and len(con) == 2:
            result.append(con.get('id'))
    return result
    #raise Exception('resource[%s] has no constraint' % md_name)

def GetConsById(consId):
    cons = GetCons()
    result = []
    for con in cons:
        if con.get('id')== consId:
            result.append(con)
    return result

def DeleteConsByRes(resName,cfgName = 'cons_cfg'):
    try:
        cons = GetConsByRes(resName,cfgName)
        if len(cons)==0 :
            return
        for con in cons:
            c = CConstraintBase.CConstraintBase(None,None)
            c.SetConsId(con.get('id'))
            rtn = c.Delete()
    except Exception as e:
        raise e
    return rtn

def DeleteConsById(consId):
    cons = GetConsById(consId)
    c = CConstraintBase.CConstraintBase(None,None)
    c.SetConsId(cons[0].get('id'))
    return c.Delete()
