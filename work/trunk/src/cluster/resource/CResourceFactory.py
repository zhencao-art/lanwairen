#!/usr/bin/env python

import CResourceBase,CResourceLVM,CResourceTarget,CResourceLogicalUtil,CResourceIP , CResourceCommon ,CResourceMgr ,CLunStruct
import sys,logging,os,socket,commands,time , subprocess
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../mid')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../storage')
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../server")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../ip")))
import globalvar , CIPMgr , CCoroFile , CHostFile
import puma_pb2
from common import CXmlMgr
import block_mgr ,n_lvmmgr

#### global var ######
cfg = None
g_res_type_dict = {'raid':'ocf:heartbeat:md_raid','lv':'ocf:heartbeat:dnt_lv','target':'ocf:heartbeat:iSCSITarget','ip':'ocf:heartbeat:IPaddr2','lun':'ocf:heartbeat:iSCSILogicalUnit'}
g_res_name_dict = CLunStruct.g_res_name_dict
g_res_cons_dict = CLunStruct.g_res_cons_dict



def SetCfg(_cfg = None):
    global cfg
    if _cfg:
        cfg = _cfg
    else:
        cfg = CXmlMgr.CXmlMgr()
    return cfg

def Deletecfg():
    if cfg:
        del cfg

def GetResourceType(key):
    if not g_res_type_dict.has_key(key):
        raise Exception('resource type key[%s] is not a vaild key'%key)
    return g_res_type_dict.get(key)
    
def GetResource(resName,resType=None,resOptions=None):
    if resType == 'group':
        res = CResourceBase.CResourceBase(resName,resType,resOptions)
        return res
    if resType== None :
        rtn = CheckResource(resName)
        if rtn==False:
            raise Exception('resource '+resName+' do not exist in the cluster')
        resType = GetType(resName,'class')
        resType +=':'+GetType(resName,'provider')
        resType +=':'+GetType(resName,'type')
    if resType == 'ocf:heartbeat:LVM':
        res = CResourceLVM.CResourceLVM(resName,resType,resOptions)
    elif resType == 'ocf:heartbeat:iSCSITarget':
        res = CResourceTarget.CResourceTarget(resName,resType,resOptions)
    elif resType == 'ocf:heartbeat:iSCSILogicalUnit' :
        res = CResourceLogicalUtil.CResourceLogicalUtil(resName,resType,resOptions)
    elif resType == 'ocf:heartbeat:IPaddr2':
        res = CResourceIP.CResourceIP(resName,resType,resOptions)
    else:
        res = CResourceCommon.CResourceCommon(resName,resType,resOptions)
        #raise Exception(str(resType) + " is not a vaild resource type")
        #res = None
    return res

def Check(resName,nodelist):
    #cfg = CXmlMgr.CXmlMgr('cib_cfg')
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        for res in reslist :
            name = cfg.GetValue(res,'id')
            if resName==name :
                return True
            if res.tag != 'primitive':
                rlist = cfg.GetNode(res,['primitive'])
                if not len(rlist):
                    continue
                for re in rlist:
                    name = cfg.GetValue(re,'id')
                    if resName==name :
                        return True
    return False

def CheckResource(resName):
    nodelist = ['configuration','resources','primitive']
    rtn = Check(resName,nodelist)
    if rtn:
        return rtn
    nodelist = ['configuration','resources','clone']
    rtn = Check(resName,nodelist)
    if rtn:
        return rtn
    nodelist = ['configuration','resources','master']
    rtn = Check(resName,nodelist)
    if rtn:
        return rtn
    nodelist = ['configuration','resources','group']
    rtn = Check(resName,nodelist)
    if rtn:
        return rtn
    return False

def GetType(resName,prop):
    #cfg = CXmlMgr.CXmlMgr('cib_config')
    nodelist = ['configuration','resources','primitive']
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        for res in reslist :
            name = cfg.GetValue(res,'id')
            if resName==name :
                return cfg.GetValue(res,prop)
    nodelist = ['configuration','resources','clone']
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        for res in reslist :
            name = cfg.GetValue(res,'id')
            if resName==name :
                rlist = cfg.GetNode(res,['primitive'])
                return cfg.GetValue(rlist[0],prop)
            else:
                rlist = cfg.GetNode(res,['primitive'])
                if resName == cfg.GetValue(rlist[0],'id'):
                    return  cfg.GetValue(rlist[0],prop)
    nodelist = ['configuration','resources','master']
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        for res in reslist :
            name = cfg.GetValue(res,'id')
            if resName==name :
                rlist = cfg.GetNode(res,['primitive'])
                return cfg.GetValue(rlist[0],prop)
            else:
                rlist = cfg.GetNode(res,['primitive'])
                if resName == cfg.GetValue(rlist[0],'id'):
                    return  cfg.GetValue(rlist[0],prop)
    nodelist = ['configuration','resources','group']
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        for res in reslist :
            name = cfg.GetValue(res,'id')
            if resName==name :
                rlist = cfg.GetNode(res,['primitive'])
                return cfg.GetValue(rlist[0],prop)
            else:
                rlist = cfg.GetNode(res,['primitive'])
                if not rlist:
                    continue
                for re in rlist:
                    if resName == cfg.GetValue(re,'id'):
                        return  cfg.GetValue(re,prop)
    return None

def get_sub_attr(cfg,res):
    result = {}
    nodepath = ['instance_attributes','nvpair']
    elist = cfg.GetNode(res,nodepath)
    for e in elist:
        result[e.get('name')] = e.get('value')
    return result


def GetState(resName,spli= True):
    if resName == 'all':
        return CResourceMgr.GetAllResource(cfg,spli)
    else:
        return CResourceMgr.GetResourceAttr(cfg , resName , spli)

def GetNodeState(resName):
    cmd = 'crm_resource -r '+ resName + ' --locate'
    (rtn,out) = commands.getstatusoutput(cmd)
    if rtn!= 0:
        raise Exception(out)
    result = ''
    nodelist = out.split('\n')
    for node in nodelist:
        if node == '':
            continue
        index = node.rfind(':') + 1
        if 'NOT running' in node :
            if result == '':
                result = 'NOT running '
            continue
        if result == 'NOT running ':
            result =  node[index:len(node)] + ','
        else:
            result +=  node[index:len(node)] + ','
    logging.debug('resName:%s , state:%s' %(resName , result[:-1]))
    return result[:-1]

def GetNode():
    cfg = CXmlMgr.CXmlMgr('cib_cfg')
    nodelist = ['configuration','nodes','node']
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        result = []
        for res in reslist :
            node = []
            name = cfg.GetValue(res,'uname')
            node.append(name)
            node.append(name)
            #ip = socket.gethostbyname(name)
            #node.append(ip)
            result.append(node)
    return result

def CheckIsci(opt):
    #cfg = CXmlMgr.CXmlMgr('cib_cfg')
    nodelist = ['configuration','resources']
    reslist = cfg.GetNode(None,nodelist)
    if reslist!=None :
        childlist = reslist[0].getchildren()
        for child in childlist:
            if child.tag == 'primitive':
                name = cfg.GetValue(child,'id')
            else:
                rlist = cfg.GetNode(child,['primitive'])
                name = cfg.GetValue(rlist[0],'id')
            attr = GetState(name)
            if attr.get('path') == opt.get('path'):
                return True
           # if attr.get('path') == opt.get('path'):
           #     raise Exception('device['+attr.get('path')+'] has been used by target['+name+']')

    return False
            
def CheckSecurity(resName,resType,opt):
    resAttr = GetState('all',True)
    for attr in resAttr:
        if resName == attr.get('id') or resName == attr.get('master') or resName == attr.get('clone'):
            raise Exception('resource['+resName+'] has already exist in the cluster') 
        if len(opt)==0 :
            continue
        if resType == 'ocf:heartbeat:IPaddr2':
            if dict(opt).get('ip')== attr.get('ip') and dict(opt).get('ip'):
                raise Exception('opiton ip='+attr.get('ip')+' has been used by '+attr.get('id'))
        elif resType == 'ocf:heartbeat:iSCSILogicalUnit' :
            if attr.get('path') == dict(opt).get('path') and dict(opt).get('path'):
                raise Exception('opiton path='+attr.get('path')+' has been used by '+attr.get('id'))
        elif resType == 'ocf:heartbeat:iSCSITarget':
            if attr.get('iqn') == dict(opt).get('iqn') and dict(opt).get('iqn'):
                raise Exception('opiton iqn='+attr.get('iqn')+' has been used by '+attr.get('id'))
        elif resType == 'ocf:heartbeat:LVM':
            if attr.get('volgrpname') == dict(opt).get('volgrpname') and dict(opt).get('volgrpname'):
                raise Exception('opiton volgrpname='+attr.get('volgrpname')+' has been used by '+attr.get('id'))
    return False

def GetClusterState(detail_flag):
    #get corosync heartbeat address and nodeid
    #get cib nodeid state
    logging.debug('start')
    nodelist = ['status','node_state']
    reslist = cfg.GetNode(None,nodelist)
    result = []
    if not reslist:
        return result
    for res in reslist:
        tmp = {}
        tmp['id'] = cfg.GetValue(res,'id')
        hb_address = CCoroFile.GetCoroValue(['nodelist','node'],'ring0_addr','nodeid='+tmp['id'])
        tmp['hb_addr'] = hb_address[0]
        tmp['uname'] = cfg.GetValue(res,'uname')
        tmp['crmd'] = cfg.GetValue(res,'crmd')
        if detail_flag:
            nic_dict = CIPMgr.GetNicByIp(tmp.get('hb_addr'))
            tmp.update(nic_dict)
        result.append(tmp)
    logging.debug('end')
    return result
    
def GetResourceByNode(nodestr):
    
    def get_resource_by_node(node):
        #cfg = CXmlMgr.CXmlMgr('cib_cfg')
        nodelist = ['status','node_state']
        reslist = cfg.GetNode(None,nodelist)
        result = []
        if not reslist:
            return result
        for res in reslist:
            if cfg.GetValue(res,'uname') == node:
                nlist = ['lrm','lrm_resources','lrm_resource']
                rlist = cfg.GetNode(res,nlist)
                if not rlist:
                    continue
                for re in rlist:
                    result.append(re.attrib)
        return result

    result = []
    nodelist = nodestr.split(' ')
    for node in nodelist:
        result += get_resource_by_node(node)
    return result

def GroupAdd(grpName,grpMem):
    cmd = 'pcs -f '+ CResourceBase.g_cib_filename + ' resource group add ' + grpName + ' ' + grpMem
    (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
    if rtn!=0 :
        raise Exception(out)
    logging.debug('do command[%s] success' % cmd)
    return out

def GroupRemove(grpName,grpMem):
    cmd = 'pcs -f '+ CResourceBase.g_cib_filename + ' resource group remove ' + grpName + ' ' + grpMem
    (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
    if rtn!=0 :
        raise Exception(out)
    logging.debug('do command[%s] success' % cmd)
    return out

def Move(resName,cluNode):
    cmd = 'pcs resource move ' + resName + ' ' + cluNode
    (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
    if rtn!=0 :
        raise Exception(out)
    logging.debug('do command[%s] success' % cmd)
    return out

def Clear(resName):
    cmd = 'pcs resource clear ' + resName
    (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
    if rtn!=0 :
        raise Exception(out)
    logging.debug('do command[%s] success' % cmd)
    return out

def GetDetail(nodelist):
    cfg = CXmlMgr.CXmlMgr('cib_cfg')
    reslist = cfg.GetNode(None,nodelist)
    result = []
    if reslist!=None :
        for res in reslist :
            attr = {}
            attr.update(res.attrib)
            sub = get_sub_attr(cfg,res)
            attr.update(sub)
            result.append(attr)
    return result

def GetNormal(nodelist):
    #cfg = CXmlMgr.CXmlMgr('cib_cfg')
    reslist = cfg.GetNode(None,nodelist)
    result = []
    if reslist!=None :
        for res in reslist :
            tmp = dict(res.attrib)
            #tmp['node_state'] = GetNodeState(res.get('id'))
            result.append(tmp)
    return result

def IsGroup(resName):
    reslist = GetNormal(['configuration','resources','group'])
    for res in reslist:
        if res.get('id') == resName:
            return True
    return False

def IsInGroup(resName):
    reslist = GetNormal(['configuration','resources','group'])
    for res in reslist:
        rlist = GetState(res.get('id'),False)
        for re in rlist:
            if re.get('id') == resName:
                return (True,res.get('id'))
    return (False,None)

def SortRes(src_list):
    def get_sub_list(cur_type,result):
        sub_flag = False
        for src in src_list:
            if src.get('type') == cur_type:
                sub_flag = True
                if src in result:
                    break
                sub = g_res_cons_dict.get(src.get('type'))
                if sub:
                    result = get_sub_list(sub,result)
                result.append(src)
                break
        if not sub_flag:
            sub = g_res_cons_dict.get(cur_type)
            if sub:
                result = get_sub_list(sub,result)
        return result

    result = []
    for src in src_list:
        if src in result:
            continue
        sub = g_res_cons_dict.get(src.get('type'))
        if sub:
            result = get_sub_list(sub,result)
        result.append(src)
    result.reverse()
    return result

def GetResStructure(resOpt,used):
    g_res_rel_dict = {}
    def get_group_name(index =1):
        gname = None
        for res in used:
            rtn,grp = IsInGroup(res.get('id'))
            if rtn:
                if gname and gname != grp:
                    raise Exception('uesd resources[%s] not in one group'%str(used))
                gname = grp
        return gname
    g_grp_name = get_group_name()
    def get_name_index():
        if len(used):
            grp = g_grp_name
            if grp:
                index = grp.rfind('_') +1
                return int(grp[index:len(grp)])
        reslist = GetNormal(['configuration','resources','group'])
        g_res_count = 1
        if len(reslist):
            for res in reslist:
                grp = res.get('id')
                index = grp.rfind('_') +1
                if index == 0:
                    continue
                count = int(grp[index:len(grp)]) + 1
                if g_res_count < count:
                    g_res_count = count
        return g_res_count
    def get_res_by_type(rtype):
        for res in used:
            if res.get('type')==rtype:
                return res
        return None
    def get_lun():
        rtn = 1
        return str(rtn)
    def set_resource(res_type,g_res_count):
        res_dict = {}
        res = get_res_by_type(res_type)
        if not res:
            res_dict['id'] = g_res_name_dict.get(res_type) + str(g_res_count)
            res_dict['type'] = 'ocf:heartbeat:' + res_type
            res_dict['state'] = True
        else:
            res_dict['state'] = False
            res_dict.update(res)
        sub = g_res_cons_dict.get(res_type)
        if sub != '':
            tmp = []
            for res in sub.split(','):
                if not g_res_rel_dict.has_key(res):
                    raise Exception('unknown error occur,please connect to manager,error_code:12')
                tmp.append(g_res_rel_dict.get(res))
            res_dict['sub'] = tmp
        g_res_rel_dict[res_type] = res_dict
        return res_dict
    def set_option(resOpt,g_res_count):
        if not resOpt.has_key('iqn_name'):
            mon = str(time.localtime().tm_mon)
            if len(mon)==1 :
                mon = '0'+mon
            resOpt['iqn_name'] = 'iqn.'+str(time.localtime().tm_year)+'-'+str(mon)+'.phegda.com.cn:'+str(g_res_count)
        #resOpt['implementation'] = 'lio-t'
        if not resOpt.has_key('implementation'):
            resOpt['implementation'] = 'lio-t'
        if not resOpt.has_key('lun'):
            resOpt['lun'] = get_lun()
        if g_grp_name:
            grpname = g_grp_name
        else:
            grpname = 'grp_' + str(g_res_count)
        resOpt['grp_name'] = grpname
    def sort_resource(res_dict):
        res_list = []
        for k in res_dict:
            if res_dict.get(k) == '':
                res_list.append(k)
        for k in res_dict:
            if res_dict.get(k) == '':
                continue
            reslist = res_dict.get(k).split(',')
            reslist.reverse()
            for res in reslist:
                if res not in res_list:
                    res_list.append(res)
            if k not in res_list:
                res_list.append(k)
        return res_list


    g_res_count = get_name_index()
    st = []
    res_structure_list = sort_resource(g_res_cons_dict)
    for res in res_structure_list:
        res_st = set_resource(res,g_res_count)
        st.append(res_st)
    set_option(resOpt,g_res_count)
    return st


def CheckOption(resOpt):
    if resOpt.has_key('ip'):
        CheckIp(resOpt.get('ip'),resOpt.get('nic'),resOpt.get('cidr_netmask'))
    if resOpt.has_key('path'):
        #CheckDevice(resOpt.get('path'))
        pass

def CheckIp(ip,nic,mask):
    CIPMgr.CheckIpForResource(ip,nic,mask)
    pass

def CheckDevice(device):
    if not block_mgr.check_block_dev(device):
        raise Exception('please input a vaild block-device,you input path['+device+']')

def CheckIpRes(ip):
    reslist = GetResByType('IPaddr2')
    for res in reslist:
        if ip == res.get('ip'):
            tgtlist = GetResByType('iSCSITarget')
            for tgt in  tgtlist:
                if tgt.get('portals') and tgt.get('portals').split(':')[0] == ip:
                    return 'lun'
            return 'float_ip'
    return 'free'

#check resOpt vaild
#if options in resOpt are used by exist resource,except
def CheckResUsed(resOpt):
    result = []
    if not resOpt.has_key('ip') or not resOpt.has_key('path'):
        raise Exception('miss required option,you should specify "ip" and "path"')
    ipFlag = dFlag = False
    for k in resOpt:
        if k == 'ip':
            reslist = GetResByType('IPaddr2')
            for res in reslist:
                if res.get('ip') and res.get('ip') == resOpt[k]:
                    reslist = GetResByType('iSCSITarget')
                    for res in  reslist:
                        if res.get('portals') and res.get('portals').split(':')[0] == resOpt[k]:
                            raise Exception(k+'='+resOpt[k]+' has been used by ['+res.get('id')+']')
                    result.append(res)
                    ipFlag = True
                    break
        elif k == 'path':
            reslist = GetResByType('iSCSILogicalUnit')
            for res in  reslist:
                if res.get('path') and res.get('path') == resOpt[k]:
                    grp = GetGroupByRes(res.get('id'))
                    if not grp:
                        raise Exception('resource[%s] not in group'%res.get('id'))
                    grplist = GetState(grp.get('id'))
                    if len(grplist) > 3:
                        raise Exception(k+'='+resOpt[k]+' has been used by ['+res.get('id')+']')
                    else:
                        result += grplist
                        dFalg = True
                        break
    if not dFlag:
        #CheckDevice(resOpt.get('path'))
        pass
    if not ipFlag:
        CheckIp(resOpt.get('ip'),resOpt.get('nic'),resOpt.get('cidr_netmask'))
    for res in result:
        if res.get('type') == 'dnt_lv':
            return result
    lv_res = GetResByLv(resOpt.get('path'))
    if not lv_res:
        raise Exception('lv[%s] resource do not exist,please create it before add a lun'%resOpt.get('path'))
    if lv_res.get('node_state') == 'NOT running':
        raise Exception('lv resource[%s] occur exception,please check and repaire it' % lv_res.get('id'))
    result.append(lv_res)
    return result

def GetResByType(rtype, stat_flag = True):
    #result = []
    #reslist = GetState('all')
    #for res in reslist:
    #    rlist = GetState(res.get('id'))
    #    for re in rlist:
    #        if re.get('type')==rtype:
    #            result += GetState(re.get('id'))
    return CResourceMgr.GetResByType(None,rtype, stat_flag)

def GetResByType2(res_type):
    pass

def GetAllPri():
    pass

#get groupname by specify resource name
#if resource not in a group return none
def GetGroupByRes(resname):
    reslist = GetState('all')
    for res in reslist:
        if res.get('tag') != 'group':
            continue
        rlist = GetState(res.get('id'))
        for re in rlist:
            if re.get('id')==resname:
                return res
    return None

###############################
#find resources which properties
#are same to specify options
##############################
def GetResByOpt(resOpt):
    def get_res_by_type(rtype,res_list):
        for res in res_list:
            if res.get('type') == rtype:
                if (rtype == 'IPaddr2' and res.get('ip') == resOpt.get('ip'))\
                    or (rtype == 'iSCSILogicalUnit' and res.get('path') == resOpt.get('path'))\
                    or (rtype == 'iSCSITarget'):
                        return res
        return None

    grp_list = CResourceMgr.GetGroup(cfg , False)
    result = []
    for grp in grp_list:
        if resOpt.has_key('ip'):
            res = get_res_by_type('IPaddr2' , grp)
            if res:
                result.append(res)
        if resOpt.has_key('path'):
            res = get_res_by_type('iSCSILogicalUnit' , grp)
            if res:
                result.append(res)
            else:
                continue
            res = get_res_by_type('iSCSITarget' , grp)
            if res:
                result.append(res)
        if result and \
                ((resOpt.has_key('ip') and resOpt.has_key('path') and len(result) != 3)\
                or (resOpt.has_key('ip') and not resOpt.has_key('path') and len(result) != 1)\
                or (not resOpt.has_key('ip') and resOpt.has_key('path') and len(result) != 2)):
            raise Exception('you input ip[%s] and lv[%s] no lun matched' %(resOpt.get('ip'),resOpt.get('path')))
        if len(result) > 0:
            result = SortRes(result)
            return result,grp
    raise Exception('you input ip[%s] and lv[%s] no lun matched' %(resOpt.get('ip'),resOpt.get('path')))
    return result,[]


def GetResByLv(device):
    reslist = GetResByType('dnt_lv')
    for res in reslist:
        if device == res.get('lv_name'):
            return res
    return None

def GetUsedLv(stat_flag = False):
    reslist = GetResByType('iSCSILogicalUnit',stat_flag)
    result = []
    for res in reslist:
        result.append(res.get('path'))
    return result

def GetLvResList(stat_flag = False):
    reslist = GetResByType('dnt_lv',stat_flag)
    result = []
    for res in reslist:
        result.append(res.get('lv_name'))
    return result

def GetResByMd(device):
    reslist = GetResByType('md_raid')
    for res in reslist:
        if device == res.get('raiddev'):
            return res
    return None

def GetLvResByMd(lv_name,stObj = None):
    vg_name = lv_name
    lv_list = n_lvmmgr.vg_lv_gname_list(vg_name)
    if stObj:
        lv_res_list = stObj.GetResByType('dnt_lv')
    else:
        lv_res_list = GetResByType('dnt_lv')
    result = []
    for lv in lv_list:
        for res in lv_res_list:
            if  lv == res.get('lv_name'):
                result.append(res)
    if not result:
        logging.info('vg[%s] has no lv resource0' % lv_name)
    return result

def GetMdRes(lv_name,stObj = None):
    vg_name = lv_name.split('/')[2]
    pvlist = n_lvmmgr.vg_pv_name_list(vg_name)
    if stObj:
        md_res_list = stObj.GetResByType('md_raid')
    else:
        md_res_list = GetResByType('md_raid')
    result = []
    for pv in pvlist:
        for res in md_res_list:
            if pv == res.get('raiddev'):
                result.append(res)
    return result

def GetResName(rtype,name): 
    name = name.replace('/dev','')
    name = name.replace('/','_')
    return rtype + name

def JudgeLvRes(lv_name):
    lv_res = GetResByLv(lv_name)
    if not lv_res:
        return 1
    reslist = GetResByType('iSCSILogicalUnit')
    for res in reslist:
        if res.has_key('path') and res.get('path') == lv_name:
            return -1
    return 0
    #raise Exception('lv[%s] resource do not exist in cluster'%lv_name)
    
#@rtn-- -1:resource is used
#       0 :resource is free
#       1 :resource not exist
def JudgeRaidRes(rd_name):
    logging.debug(rd_name)
    rd_res = GetResByMd(rd_name)
    if not rd_res:
        return 1
    reslist = GetResByType('dnt_lv')
    for res in reslist:
        lv_name = res.get('lv_name')
        vg_name = lv_name.split('/')[2]
        pvlist = n_lvmmgr.vg_pv_name_list(vg_name)
        if rd_name in pvlist:
            return -1
    return 0

def GetPvByVg(vg_name):
    pvlist = n_lvmmgr.vg_pv_name_list(vg_name)
    return pvlist

#get LUN infomation:
#include all the properties of IPaddr2,iSCSITarget,iSCSILogicalUnit
def GetLunInfo():
    lun_info_list = []
    grplist = CResourceMgr.GetGroup(cfg)
    for grp in grplist:
        lun_info = {}
        if len(grp) < 2:
            continue
        lun_info['lun_status'] = grp[0].get('node_state')
        for res in grp:
            if res.get('node_state') == 'NOT running':
                lun_info['lun_status'] = res.get('node_state')
            #res_detail = GetState(res.get('id'))[0]
            lun_info.update(res)
        lun_info.pop('node_state')
        lun_info.pop('class')
        lun_info.pop('provider')
        lun_info.pop('type')
        lun_info.pop('tag')
        lun_info['id'] = lun_info.get('group')
        lun_info_list.append(lun_info)
    return lun_info_list

def GetLun(lun_info_dict):
    grplist = GetNormal(['configuration','resources','group'])
    lun_res = []
    for grp in grplist:
        reslist = GetState(grp.get('id'))
        lun_res = []
        ip_flag = False;path_flag = False
        for res in reslist:
            res_detail = GetState(res.get('id'))[0]
            if res_detail.has_key('ip'):
                if res_detail.get('ip') == lun_info_dict.get('ip'):
                    ip_flag = True
                else:
                    break
            if res_detail.has_key('path'):
                if res_detail.get('path') == lun_info_dict.get('path'):
                    path_flag = True
                else:
                    break
            lun_res.append(res_detail)
        if ip_flag and path_flag:
            return lun_res
    return lun_res

def GetLun1(lun_info_dict):
    stObj = CLunStruct.CLunStruct()
    grp_list = stObj.GetGroup()
    for grp in grp_list:
        lun_res = []
        ip_flag = False;path_flag = False
        for res in grp:
            if res.has_key('ip'):
                if res.get('ip') == lun_info_dict.get('ip'):
                    ip_flag = True
                else:
                    break
            if res.has_key('path'):
                if res.get('path') == lun_info_dict.get('path'):
                    path_flag = True
                else:
                    break
            lun_res.append(res)
        if ip_flag and path_flag:
            return lun_res
    return []

def GetLunResToUP(lun_info_dict):
    lun_res = GetLun1(lun_info_dict)
    logging.debug('get_lun')
    if not len(lun_res):
        raise Exception('lun[ip:%s,lv:%s] do not exist in cluster' % (lun_info_dict.get('ip'),lun_info_dict.get('path')))
    res_type_up = GetResProperty(lun_info_dict)
    logging.debug('get res type')
    result = []
    if not len(res_type_up):
        return result
    for res in lun_res:
        if res.get('type') in res_type_up:
            result.append(res)
    return result

def GetResProperty(lun_info_dict):
    res_property_dict = {'IPaddr2':['nic','cidr_netmask'],'iSCSITarget':['iqn','tid','portals','incoming_username','incoming_password','additional_parameters'],'iSCSILogicalUnit':['iqn','lun','allowed_initiators']}
    result = []
    for k in lun_info_dict:
        for res in res_property_dict:
            if k in res_property_dict.get(res) and res not in result:
                result.append(res)
    return result

def GetHb():
    return CIPMgr.get_corosync_node()

def GetCluName():
    return CIPMgr.GetClusterName()

def IsClusterHostname(hostname):
    reslist = GetNormal(['configuration','nodes','node'])
    for res in reslist:
        if res.get('uname') == hostname:
            return True
    return False

#check input heartbeat options
#if the ip is not exist then create,do the same at two nodes
#return new heartbeat address list
def CheckAndSetIp(heartb_list):
    old_hb_list = CIPMgr.get_corosync_node()
    new_hb_list = []
    hb_ip1 = heartb_list[0].get('hb_ip')
    hb_ip2 = heartb_list[1].get('hb_ip')
    hb_mask1 = heartb_list[0].get('cidr_netmask')
    hb_mask2 = heartb_list[1].get('cidr_netmask')
    for hb in heartb_list:
        if not IsClusterHostname(hb.get('host')):
            raise Exception('input hostname[%s] are not the cluster nodes' % hb.get('host'))
    #get default heartbeat nic
    hb_nic = CIPMgr.GetHeartBeatNic()
    #judge two hearbeat address if there in the same subnet
    CIPMgr.JudgeSubnet2(hb_ip1,hb_mask1,hb_ip2,hb_mask2)
    for hb in heartb_list:
        if hb.get('hb_ip') not in old_hb_list:
            if CIPMgr.GetHostname() == hb.get('host'):
                #judge server ip and heartbeat address if there in the same subnet
                CIPMgr.JudgeSubnet1(hb.get('hb_ip'),hb_nic,hb.get('cidr_netmask'))
                CIPMgr.SetIP(hb.get('hb_ip'),hb.get('nic'),hb.get('cidr_netmask'))
            else:
                peer_ip = CIPMgr.get_peer_ip()
                cli = client.CClient(str(peer_ip),globalvar.listen_port)
                stub = cli.stub()
                req = puma_pb2.SetIpReq()
                req.ipOpt.ip = hb.get('hb_ip')
                req.ipOpt.nic = hb.get('nic')
                if hb.has_key('cidr_netmask'):
                    req.ipOpt.cidr_netmask = hb.get('cidr_netmask')
                stub.add_ip(None,req,None)
                resp = cli.get_response()
                if resp.ret.retcode != 0:
                    raise Exception(resp.ret.msg)
        new_hb_list.append(hb.get('hb_ip'))
    return old_hb_list,new_hb_list

def DeleteOldHb(old_hb_list,new_hb_list):
    index = 0
    logging.debug('start delete old hb')
    hb_nic = CIPMgr.GetHeartBeatNic()
    while index < len(old_hb_list):
        if old_hb_list[index] != new_hb_list[index].get('hb_ip'):
            if CIPMgr.CheckIp(old_hb_list[index]):
                CIPMgr.DeleteIp(old_hb_list[index] , hb_nic)
            else:
                peer_ip = new_hb_list[index].get('hb_ip')
                logging.debug(peer_ip)
                cli = client.CClient(str(peer_ip),globalvar.listen_port)
                stub = cli.stub()
                req = puma_pb2.SetIpReq()
                req.ipOpt.ip = old_hb_list[index]
                req.ipOpt.nic = hb_nic
                stub.delete_ip(None,req,None)
                resp = cli.get_response()
                if resp.ret.retcode != 0:
                    raise Exception(resp.ret.msg)
        index += 1
    logging.debug('end delete old hb')

def GetClient(hblist):
    for hb in hblist:
        if not CIPMgr.CheckIp(hb):
            cli = client.CClient(str(hb),globalvar.listen_port)
            stub = cli.stub()
            return cli,stub
    return None,None

def GetRequest(hblist,passwd,clu_name):
    request = puma_pb2.ClusterInitReq()
    request.cNodelist = ' '.join(hblist)
    if not passwd:
        passwd = 'hacluster'
    request.cPasswd = passwd
    request.clusterName = clu_name
    return request

def SetCoroFile(hblist,heartb_list):
    old_hb_list = CIPMgr.get_corosync_node()
    if len(hblist) != len(old_hb_list):
        raise Exception('set heartbeat address error:bad address number')
    f_coro = CCoroFile.CCoroFile(CCoroFile.g_corosync_filename)
    index = 0
    while index < len(hblist):
            f_coro.Update('ring0_addr',old_hb_list[index],hblist[index])
            f_coro.Write()
            index += 1
    cli,stub = GetClient(old_hb_list)
    f_cont = CHostFile.SetHosts(heartb_list)
    req = puma_pb2.FileInfoReq()
    req.file_name = CCoroFile.g_corosync_filename
    req.file_cont = f_coro._fileContent
    stub.syn_file(None,req,None)
    resp = cli.get_response()
    if resp.ret.retcode != 0:
        raise Exception(resp.ret.msg)
    req.file_name = CHostFile.g_host_filename
    req.file_cont = f_cont
    stub.syn_file(None,req,None)
    resp = cli.get_response()
    if resp.ret.retcode != 0:
        raise Exception(resp.ret.msg)
    return

def CheckRaidToStop(stObj = None):
    if not stObj:
        stObj = CLunStruct.CLunStruct()
    raid_res_list = stObj.GetResByType('md_raid')
    lv_res_list = stObj.GetResByType('dnt_lv')
    for raid_res in raid_res_list:
        lv_list = n_lvmmgr.lv_list_for_pv(raid_res.get('raiddev'))
        if not lv_list:
            continue
        unres_lv_list = GetUnusedLv(lv_list,stObj,lv_res_list)
        logging.debug(unres_lv_list)
        for res_lv in unres_lv_list:
            n_lvmmgr.lv_deactivate(res_lv)
    return

def GetUnusedLv(lv_list,stObj = None , lv_res_list = []):
    if not lv_res_list:
        if not stObj:
            stObj = CLunStruct.CLunStruct()
        lv_res_list = stObj.GetResByType('dnt_lv')
    result = []
    for lv in lv_list:
        exist_flag = False
        for lv_res in lv_res_list:
            if lv == lv_res.get('lv_name'):
                exist_flag = True
                break
        if not exist_flag:
            result.append(lv)
    return result

