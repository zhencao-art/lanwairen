# coding:utf-8
#!/usr/bin/env python

import commands,logging
import sys,os , re ,time
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../ip")))
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../common')
import CResourceMgr , CIPMgr ,CXmlMgr ,CResourceBase

g_res_name_dict = {'IPaddr2':'float_ip_','dnt_lv':'lv_','iSCSITarget':'target_','iSCSILogicalUnit':'lun_'}
g_res_cons_dict = {'IPaddr2':'','dnt_lv':'iSCSITarget','iSCSITarget':'IPaddr2','iSCSILogicalUnit':'dnt_lv'}

class CLunStruct():
    def __init__(self):
        self._res_group_list = []
        self._res_all_list = []
        self._res_all_detail_list = []
        self._cfg_xml = CXmlMgr.CXmlMgr()

    def FlushXml(self):
        self._cfg_xml = CXmlMgr.CXmlMgr()

    def InitGroup(self, stat_falg = True):
        if not self._res_group_list:
            self._res_group_list = CResourceMgr.GetGroup(self._cfg_xml,stat_falg)
    
    def InitAll(self, stat_falg = True):
        if not self._res_all_list:
            self._res_all_list = CResourceMgr.GetAllResource(self._cfg_xml,stat_falg)

    def InitAllDetail(self, stat_falg = True):
        if not self._res_all_detail_list:
            self._res_all_detail_list = CResourceMgr.GetAllSubResource(self._cfg_xml,stat_falg)

    def IsInGroup(self,res_id, stat_falg = True):
        self.InitGroup(stat_falg)
        for grp in self._res_group_list:
            for res in grp:
                if res.get('id') == res_id:
                    return True,res.get('group')
        return False,None

    def IsGroup(self,res_id, stat_falg = True):
        self.InitGroup(stat_falg)
        for grp in self._res_group_list:
            if grp[0].get('group') == res_id:
                return True
        return False

    def GetGroup(self,grp_id = None, stat_falg = True):
        self.InitGroup(stat_falg)
        if not grp_id:
            return self._res_group_list
        for grp in self._res_group_list:
            if grp[0].get('group') == grp_id:
                return grp
        return []

    def GetResByType(self, res_type, stat_falg = True):
        self.InitAllDetail(stat_falg)
        result = []
        for res in self._res_all_detail_list:
            if res.get('type') == res_type:
                result.append(res)
        return result

    def GetResByLv(self,device, stat_falg = True):
        reslist = self.GetResByType('dnt_lv', stat_falg)
        for res in reslist:
            if device == res.get('lv_name'):
                return res
        return None

    #构建LUN资源组的顺序，资源名，资源间依赖关系
    #返回有序的资源属性字典的序列
    def GetResStructure(self,resOpt,used):
        g_res_rel_dict = {}
        def get_group_name(index =1):
            gname = None
            for res in used:
                rtn,grp = self.IsInGroup(res.get('id'))
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
            g_res_count = 1
            for res in self._res_group_list:
                grp = res[0].get('group')
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

    #根据resOpt查找满足条件的LUN组，返回匹配的资源和LUN组
    #若未找到或找到的资源不同组或找到的资源数量不匹配，则抛异常
    def CheckResUsed(self,resOpt):
        result = []
        if not resOpt.has_key('ip') or not resOpt.has_key('path'):
            raise Exception('miss required option,you should specify "ip" and "path"')
        ipFlag = dFlag = False
        for k in resOpt:
            if k == 'ip':
                reslist = self.GetResByType('IPaddr2')
                for res in reslist:
                    if res.get('ip') and res.get('ip') == resOpt[k]:
                        reslist = self.GetResByType('iSCSITarget')
                        for re in  reslist:
                            if re.get('portals') and re.get('portals').split(':')[0] == resOpt[k]:
                                raise Exception(k+'='+resOpt[k]+' has been used by ['+re.get('id')+']')
                        result.append(res)
                        ipFlag = True
                        break
            elif k == 'path':
                reslist = self.GetResByType('iSCSILogicalUnit')
                for res in  reslist:
                    if res.get('path') and res.get('path') == resOpt[k]:
                        grp = res.get('group')
                        if not grp:
                            raise Exception('resource[%s] not in group'%res.get('id'))
                        grplist = self.GetGroup(grp)
                        if len(grplist) > 3:
                            raise Exception(k+'='+resOpt[k]+' has been used by ['+res.get('id')+']')
                        else:
                            result += grplist
                            dFalg = True
                            break
        if not ipFlag:
            CIPMgr.CheckIpForResource(resOpt.get('ip'),resOpt.get('nic'),resOpt.get('cidr_netmask'))
        for res in result:
            if res.get('type') == 'dnt_lv':
                return result
        lv_res = self.GetResByLv(resOpt.get('path'))
        if not lv_res:
            raise Exception('lv[%s] resource do not exist,please create it before add a lun'%resOpt.get('path'))
        if lv_res.get('node_state') == 'NOT running':
            if lv_res.has_key('group'):
                self.Enable(lv_res.get('group'))
            self.Enable(lv_res.get('id'))
            import time
            time.sleep(0.5)
            lv_res_status = CResourceMgr.GetNodeState(lv_res.get('id'))
            if lv_res_status == 'NOT running':
                raise Exception('lv resource[%s] occur exception,please check and repaire it' % lv_res.get('id'))
        result.append(lv_res)
        return result
   
    def Enable(self,resName):
        lv_resObj = CResourceBase.CResourceBase(resName,None,None)
        lv_resObj.Enable()


#log_level = logging.DEBUG
#log_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
#log_datefmt = '%a, %d %b %Y %H:%M:%S'
#log_file_path = "/var/log/puma.log"
#logging.basicConfig(level=log_level,format=log_format,stream=sys.stderr,filemode='w')
#
#logging.debug('start')
#obj = CLunStruct()
#resOpt = {'ip':'172.16.9.14','path':'/dev/grp10/lv4'}
#logging.debug('init')
#used = obj.CheckResUsed(resOpt)
#logging.debug('get used')
#struct =  obj.GetResStructure(resOpt,used)
#logging.debug('get struct')
