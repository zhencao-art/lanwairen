#!/usr/bin/env python

import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../resource')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../clustermgr')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../constraint')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../stonith')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../common')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr
import CResourceFactory,CConsFactory,CStonithFactory,CResourceBase,CXmlMgr ,CLunStruct
import CClusterInit
import os,commands,logging


class CClusterMgr(object):
    def __init__(self,flag = False):
        self._ResourceList=[]
        self._ConstraintList=[]
        self._StonithList=[]
        self._NodeList=[]
        self._Ini = CClusterInit.CClusterInit()
        self._cibFile = CResourceBase.g_cib_filename
        if not flag:
            self.SetPoint()
            cfg = CXmlMgr.CXmlMgr('cib_config')
            CResourceFactory.SetCfg(cfg)
    
    def InitService(self):
        try: 
            #start the cluster service
            ini = self._Ini
            ini.StartPandC()
        except Exception as e:
            raise Exception(str(e))
        return True

    def Setup(self,nodeList,passwd=None,clusterName='pacemaker'):
        try:
        #setup
            ini = self._Ini
            ini.Setup(nodeList,clusterName,passwd)
        except Exception as e:
            raise Exception(str(e))
        return True

    def InitPropety(self):
        ini = self._Ini
        opt_dict = {'migration-threshold':'1','failure-timeout':'30s'}
        ini.SetResDefaults(opt_dict)
        opt_list = [['stonith-enabled','false'],['no-quorum-policy','igonre']]
        self.SetProperty(opt_list,'set')

    def Passwd(self,nodeList,passwd=None,clusterName='pacemaker'):
        #authriocation
        ini = self._Ini
        ini.Authrication(nodeList,passwd)
        return True
        
    def Auth(self,nodeList,passwd=None,clusterName='pacemaker'):
        #authriocation
        ini = self._Ini
        if passwd == None:
            passwd = 'hacluster'
        ini.Auth1(nodeList,passwd)
        return True

    def Start(self,nodeList = None):
        if self._Ini == None :
            raise Exception('please init cluster first')
        ini = self._Ini
        rtn = ini.Start(nodeList)
       # import time
       # time.sleep(5)
       # if not nodeList or not len(nodeList):
       #     reslist = CResourceFactory.GetState('all')
       # else:       #get resources run on the specified nodes
       #     reslist = CResourceFactory.GetResourceByNode(nodeList) 
       # for res in reslist:
       #     #if res.get('type')== 'iSCSILogicalUnit':
       #     self.EnableResource(res.get('id'))
        return rtn

    def Stop(self,nodeList = None):
        ini = self._Ini

        ###stop all the node,before it should stop the resource which will be problem
       # if not nodeList or not len(nodeList):
       #     reslist = CResourceFactory.GetState('all')
       # else:       #get resources run on the specified nodes
       #     reslist = CResourceFactory.GetResourceByNode(nodeList) 
       # for res in reslist:
       #     #if res.get('type')== 'iSCSILogicalUnit':
       #     self.DisableResource(res.get('id'))
        CResourceFactory.CheckRaidToStop()
        rtn = ini.Stop(nodeList)
        return rtn
    def GetClusterState(self,detail_flag = False):
        return CResourceFactory.GetClusterState(detail_flag)

    #options: [[p1,value1],[p2,value2],...]
    def SetProperty(self,options,code,isForce = False):
        if self._Ini == None :
            raise Exception('please init cluster first')
            return False
        ini = self._Ini
        if code == 'set' or code == 'unset':
            rtn = ini.SetProperty(options,code,isForce)
        else:
            rtn = ini.GetProperty(code)
        return rtn

    
    #resource
    def SetResource(self,resOpt):
        def check_update(new,old):
            for k in ['ip','path']:
                for res in old:
                    if res.get('type') == 'iSCSITarget' and k == 'ip':
                        restype = res.get('class')+':'+res.get('provider')+':'+res.get('type')
                        self.UpdateResource(res.get('id'),new,restype,flag=False)
                        continue
        def check_run_state(usedRes):
            for res in usedRes:
                if res.get('node_state')=='NOT running' and res.get('type') != 'dnt_lv':
                    self.EnableResource(res.get('id'))
        import time
        logging.debug('start add a lun')
        try:
            stObj = CLunStruct.CLunStruct()
            usedRes = stObj.CheckResUsed(resOpt)              #return exist but not used resource,if used then exception
            resSt = stObj.GetResStructure(resOpt,usedRes)
            check_update(resOpt,usedRes)
            for res in resSt:
                if not res.get('state') :
                    continue
                rtn = self.AddResource(res.get('id'),res.get('type'),resOpt,commit=False)
            #rtn = self.SetConstraint(resSt,usedRes)
            self.SetGroup(resOpt,resSt,usedRes,stObj)
        except Exception as e:
            self.RollBack()
            raise e
        self.Commit()
        check_run_state(usedRes)
        return rtn
    
    def SetGroup(self,resOpt,reslist,usedRes,stObj):
        grp_name = resOpt.get('grp_name')
        grp_mem = ''
        res_name = []
        for res in usedRes:
            rtn,grp = stObj.IsInGroup(res.get('id'))
            if rtn:
                res_name.append(res.get('id'))
        for res in reslist:
            grp_mem += res.get('id') + ' '
        if len(res_name):
            self.Group('remove',grp_name,' '.join(res_name))
        self.Group('add',grp_name,grp_mem)

    def AddResource(self,resName,resType,resOptions,commit = True):
        res = CResourceFactory.GetResource(resName,resType,resOptions)
        if res==None :
            return False
        rtn = res.Create()
        if resType == 'ocf:heartbeat:dnt_lv':
            self.SetConsForLv(resName,resOptions)
        if commit :
            self.Commit()
        return rtn

    def SetCons(self,vg_name):
        def get_md_resource(stObj,pv_list):
            md_res_list = stObj.GetResByType('md_raid')
            result = []
            for res in md_res_list:
                if res.get('raiddev') in pv_list:
                    result.append(res)
            return result
        pv_list = CResourceFactory.GetPvByVg(vg_name)
        stObj = CLunStruct.CLunStruct()
        md_res_list = get_md_resource(stObj,pv_list)
        lv_res_list = CResourceFactory.GetLvResByMd(vg_name , stObj)
        raid_set_name = []
        for res in md_res_list:
            raid_set_name.append(res.get('clone'))
        cons_id_list = CConsFactory.GetConsByMd(raid_set_name)
        for cons_id in cons_id_list:
            self.DeleteConstraint(cons_id,True,self._cibFile,False)
        self.get_constraint_options(' '.join(raid_set_name),'',lv_res_list)
        self.Commit()
        
    def get_constraint_options(self,res1,res2,res2_list,action = 'start'):
        opt = {}
        opt['first'] = res1
        for res in res2_list:
            res2 += ' ' + res.get('id') 
        opt['then'] = res2
        if not opt.get('first') or not opt.get('then'):
            return False
        return self.AddConstraint('set',opt,False)

    def SetConsForLv(self,resName,resOpt):
        stObj = CLunStruct.CLunStruct()
        md_res_list = CResourceFactory.GetMdRes(resOpt.get('lv_name'),stObj)
        raid_set_name = []
        for res in md_res_list:
            raid_set_name.append(res.get('clone'))
        cons_id_list = CConsFactory.GetConsByMd(raid_set_name)
        for cons_id in cons_id_list:
            self.DeleteConstraint(cons_id,True,self._cibFile,False)
        lv_res_list = CResourceFactory.GetLvResByMd(resOpt.get('lv_name').split('/')[2] , stObj)
        self.get_constraint_options(' '.join(raid_set_name),resName,lv_res_list)

    def SetConstraint(self,reslist,usedRes):
        
        def get_constraint_options(res1,res2,action = 'start'):
            opt = {}
            opt['first'] = res1.get('id')
            opt['then'] = res2.get('id')
            opt['first-action'] = action
            opt['then-action'] = action
            return self.AddConstraint('order',opt,False)

        for res in usedRes:
            self.DeleteConstraint(res.get('id'),False,self._cibFile,False)
        for res in reslist:
            if res.has_key('sub'):
                for sub in res.get('sub'):
                    get_constraint_options(sub,res,'start')
                    get_constraint_options(res,sub,'stop')

    def DeleteResource(self,resOpt):
        try:
            reslist,grplist = CResourceFactory.GetResByOpt(resOpt)
            for res in reslist:
                rtype = res.get('class')+':'+res.get('provider')+':'+res.get('type')
                self.StopRelated1(res.get('id'),res.get('type') , grplist)
                resObj = CResourceFactory.GetResource(res.get('id') , rtype)
                if resObj==None :
                    return False
                resObj.Delete()
                grplist.remove(res)
        except Exception as e:
           # self.RollBack()
            raise e
        #self.Commit()
        self.RollBack()

    def DeleteResourced(self,resName,resType = None):
        stObj = CLunStruct.CLunStruct()
        if stObj.IsGroup(resName):
            res = CResourceFactory.GetResource(resName,'group')
        else:
            bFlag,grp = stObj.IsInGroup(resName)
            if bFlag:
                grplist = stObj.GetGroup(grp)
                self.StopRelated1(resName , resType, grplist)
            res = CResourceFactory.GetResource(resName,'group')
            if resType == 'md_raid':
                cons_id_list = CConsFactory.GetConsByMd([resName])
                for cons_id in cons_id_list:
                    self.DeleteConstraint(cons_id,True,self._cibFile,False)
                self.Commit()
        if res==None :
            return False
        res.Delete()
        self.RollBack()

    def StopRelated1(self,resName , resType , grplist):
        if not resType:
            for res in grplist:
                if res.get('id') == resName:
                    resType = res.get('type')
                    break
        res_con_dict = CResourceFactory.g_res_cons_dict
        for k in res_con_dict:
            if resType not in res_con_dict.get(k):
                continue
            for res in grplist:
                if res.get('type') in k and res.get('type') != 'dnt_lv':
                    self.DisableResource(res.get('id'))

    def StopRelated(self,resName, resType):
        logging.debug('name:%s,type:%s' %(resName,resType))
        cons = CConsFactory.GetConsByRes(resName,self._cibFile)
        for con in cons:
            if con.get('first-action')=='start' and con.get('first')==resName and 'lv' not in con.get('then'):
                self.DisableResource(con.get('then'))
        logging.debug('end disable')

    def DisableResource(self,resName):
        res = CResourceFactory.GetResource(resName,'group')
        if res==None :
            return False
        rtn = res.Disable()
        logging.info('resource '+resName+' disable success')
        return rtn
    def EnableResource(self,resName,file_flag = False):
        res = CResourceFactory.GetResource(resName,'group')
        if res==None :
            return False
        rtn = res.Enable(file_flag)
        logging.info('resource '+resName+' enable success')
        return rtn

    def UpdateResource(self,resName,newOptions,resType = None,flag = True):
        try:
            CResourceFactory.CheckOption(newOptions)
            res = CResourceFactory.GetResource(resName,resType)
            if res==None :
                return False
            rtn = res.Update(newOptions)
        except Exception as e:
            self.RollBack()
            raise e
        if flag:
            self.Commit()
        return rtn
    def GetResState(self,resName,isType = False):
        if isType:
            result = CResourceFactory.GetResByType(resName)
        else:
            result = CResourceFactory.GetState(resName)
        #if not len(result):
        #    raise Exception('resource [' + resName +'] do not exist')
        return result
    def SetClone(self,sAction,resName,opt=[],resType = None):
        res = CResourceFactory.GetResource(resName,resType)
        if res==None :
            return False
        if sAction=='clone' :
            rtn = res.SetClone(opt)
        else:
            rtn = res.DeleteClone()
        return rtn
    def SetMaster(self,sAction,masterName,resName,opt=[]):
        res = CResourceFactory.GetResource(resName)
        if res==None :
            return False
        if sAction=='master' :
            rtn = res.SetMaster(masterName,opt)
        else:
            rtn = res.DeleteMaster()
        return rtn

    def SetManage(self,action,resName):
        res = CResourceFactory.GetResource(resName)
        if res==None :
            return False
        if action == 'manage':
            res.Manage()
        else:
            res.Unmanage()
        return rtn

    def Group(self,action,group_name,group_member):
        if action == 'add':
            rtn = CResourceFactory.GroupAdd(group_name,group_member)
        else:
            rtn = CResourceFactory.GroupRemove(group_name,group_member)
        return rtn

    def Move(self,res_name,clu_node):
        #rtn = CConsFactory.CheckByRes(res_name,'location')
        #if rtn:
        #    raise Exception('resource[%s] has already have location constraint,can not move' % res_name)
        rtn = CResourceFactory.Move(res_name,clu_node)
        #rtn = CResourceFactory.Clear(res_name)
        return rtn

    def DebugStart(self,resName):
        try:
            res = CResourceFactory.GetResource(resName,'group')
            rtn = res.CheckRunState()
        except Exception as e:
            raise e
        return rtn

    #constraint
    def AddConstraint(self,consType,consOpt,commit=True):
        cons = CConsFactory.GetConstraint(consType,consOpt)
        if cons==None :
            return False
        rtn = cons.Create()
        if commit:
            self.Commit()
        return rtn
    def DeleteConstraint(self,consId,isId,cfgName = 'cons_cfg',commit=True):
        try:
            if not isId:
                rtn = CConsFactory.DeleteConsByRes(consId,cfgName)
            else:
                rtn = CConsFactory.DeleteConsById(consId)
            if commit:
                self.Commit()
            return rtn
        except Exception as e:
            raise Exception(str(e))
    def GetConsState(self,consId,isId):
        try:
            if consId == 'all':
                rtn = CConsFactory.GetCons()
                for cons in rtn:
                    for k in cons:
                        if k!='id':
                            cons.pop(k)
            else:
                if isId:
                    rtn = CConsFactory.GetConsById(consId)
                else:
                    rtn = CConsFactory.GetConsByRes(consId)
            if len(rtn)==0:
                raise Exception('no macthed constraint')
            return rtn
        except Exception as e:
            raise Exception(str(e))

    #stonith
    def AddStonith(self,stName,stType,stOp):
        try:
            rtn = CStonithFactory.CheckSafy(stName,stType,stOp)
            st = CStonithFactory.GetStonith(stName,stType,stOp)
            if st != None :
                rtn = st.Create()
            else:
                raise Exception('bad stonith input')
        except Exception as e:
            raise Exception(str(e))
        return rtn
    def DeleteStonith(self,stName):
        try:
            st = CStonithFactory.GetStonith(stName,None,None)
            if st!=None :
                rtn = st.Delete()
            else:
                raise Exception('stonith['+stName+'] do not exist')
        except  Exception as e:
            raise Exception(str(e))
        return rtn
    def UpdateStonith(self,stName,stOp):
        try:
            rtn = CStonithFactory.CheckStonith(stName)
            st = CStonithFactory.GetStonith(stName,None,None)
            if st!=None :
                rtn = st.Update(stOp)
        except  Exception as e:
            raise Exception(str(e))
        return rtn
    def GetStState(self,stName):
        rtn = CStonithFactory.GetStState(stName)
        if len(rtn)==0 and stName != 'all':
            raise Exception('stonith['+stName+'] do not exist')
        return rtn

    def GetClusterNode(self):
        try:
            nodelist = CResourceFactory.GetNode()
        except Exception as e:
            raise e
        return nodelist

    def Commit(self):
        cmd = 'pcs cluster cib-push '+ self._cibFile
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0:
            raise Exception(out)
            self.RollBack()
        self.RollBack()

    def SetPoint(self):
        #if os.path.exists(self._cibFile):
        #    return True
        cmd = 'pcs cluster cib '+ self._cibFile
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0:
            raise Exception(out)
    
    def RollBack(self):
        cmd = 'rm -rf '+ self._cibFile
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0:
            raise Exception(out)
        self.SetPoint()

    def Cleanup(self,resName = ''):
        cmd = 'pcs resource cleanup ' + resName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0:
            raise Exception(out)
        self.RollBack()

    def GetLunInfo(self):
        return CResourceFactory.GetLunInfo()

    def UpdateLun(self,lunopt):
        logging.debug('start update lun')
        reslist = CResourceFactory.GetLunResToUP(lunopt)
        for res in reslist:
            logging.debug('start update resource[%s]' % res.get('id'))
            res_type = res.get('class') + ':' + res.get('provider') + ':' +res.get('type')
            res = CResourceFactory.GetResource(res.get('id'),res_type)
            res.Update(lunopt)
        self.Commit()
        logging.debug('update lun[ip:%s,lv:%s] success' % (lunopt.get('ip'),lunopt.get('path')))
        

    def CheckLun(self,lun_info_dict):
        reslist = CResourceFactory.GetLun(lun_info_dict)
        if len(reslist) != 4:
            return False,'lack resources'
        for res in reslist:
            res_type = res.get('class') + ':' + res.get('provider') + ':' +res.get('type')
            res_obj = CResourceFactory.GetResource(res.get('id'),res_type)
            try:
                logging.debug('check resource [%s]' % res.get('id'))
                res_obj.CheckRunState()
            except Exception as e:
                logging.error(str(e))
                return False,str(e)
        return True,''
        
    def EnableIpmi(self,ipmi_attr_list):
        def get_peer_host(local):
            for attr in ipmi_attr_list:
                if local != attr.get('host'):
                    return attr.get('host')
            raise Exception('bad ipmi paramters:host')
        def get_ipmi_name(host):
            return 'fencing_ipmi_'+host

        try:
            for hb in ipmi_attr_list:
                if not CResourceFactory.IsClusterHostname(hb.get('host')):
                    raise Exception('input hostname[%s] are not the cluster nodes' % hb.get('host'))
            for attr in ipmi_attr_list:
                if not attr.has_key('id'):
                    attr['pcmk_host_list'] = attr.get('host')
                    attr['id'] = get_ipmi_name(attr.get('host'))
                    self.AddStonith(attr.get('id'),'fence_ipmilan',attr)
                    cons_opt_dict = {}
                    cons_opt_dict['node'] = attr.get('host')
                    cons_opt_dict['rsc'] = attr.get('id')
                    cons_opt_dict['action'] = 'avoids'
                    self.AddConstraint('location',cons_opt_dict,False)
                self.EnableResource(attr.get('id'),True)
            property_dict = [['stonith-enabled','true']]
        except Exception as e:
            self.RollBack()
            logging.error(str(e))
            raise e
        self.Commit()
        self.SetProperty(property_dict,'set')

    def DisableIpmi(self,ipmi_attr_list):
        try:
            for attr in ipmi_attr_list:
                self.DisableResource(attr.get('id'))
            property_dict = [['stonith-enabled','false']]
            self.SetProperty(property_dict,'set')
        except Exception as e:
            logging.error(str(e))
            raise e

    def GetIPMI(self):
        result = CStonithFactory.GetStState('all')
        return result

    def UpdateIpmi(self,ipmi_attr_list):
        try:
            for attr in ipmi_attr_list:
                self.UpdateStonith(attr.get('id'),attr)
        except Exception as e:
            self.RollBack()
            raise e
        self.Commit()

    def SetClusterName(self,cluster_name):
        property_dict = [['cluster-name',cluster_name]]
        self.SetProperty(property_dict,'set',True)
        hblist = CResourceFactory.GetHb()
        self.Setup(hblist,None,cluster_name)
        self.Start()

    #warnning:this function has no session control,it will exception when errors occur at anywhere of the process and cannot repaire automatic
    def SetHeartb(self,heartb_list,passwd):
        if len(heartb_list) != 2:
            raise Exception('set heartbeat must input more than one address')
        #add new heartbeat address
        old_hb,hblist = CResourceFactory.CheckAndSetIp(heartb_list)
        logging.info('set heartbeat ip success')
        #stop cluster
        self.Stop()
        #set corosync config file
        CResourceFactory.SetCoroFile(hblist,heartb_list) 
        cluster_name = CResourceFactory.GetCluName()
        #auth new heartbeat
        self.InitCluster(hblist,passwd,cluster_name)
        logging.info('re-init cluster success')
        #start cluster
        self.Start()
        #delete old heartbeat address
        CResourceFactory.DeleteOldHb(old_hb,heartb_list)

    def InitCluster(self,hblist,passwd,clu_name):
        cli,stub = CResourceFactory.GetClient(hblist)
        if not cli:
            raise Exception('get client failed,node info[%s]' % str(hblist))
        self.InitService()
        self.Passwd(hblist,passwd)
        req_passwd = CResourceFactory.GetRequest(hblist,passwd,clu_name)
        stub.start_coro_and_pamk(None,req_passwd,None)
        resp = cli.get_response()
        if resp.ret.retcode != 0:
            raise Exception(resp.ret.msg)
        stub.passwd_cluster(None,req_passwd,None)
        resp = cli.get_response()
        if resp.ret.retcode != 0:
            raise Exception(resp.ret.msg)
        self.Auth(hblist,passwd,clu_name)
        stub.auth_cluster(None,req_passwd,None)
        resp = cli.get_response()
        if resp.ret.retcode != 0:
            raise Exception(resp.ret.msg)
        

    def MoveRaid_LvResource(self,raid_lv_list):
        hostname = CFactoryResource.GetHostname()
        peer_node = CFactoryResource.GetPeerNode(hosname)

        def get_move_lv_res():
            stObj = CLunStruct.CLunStruct()
            lv_res_list = stObj.GetResByType('dnt_lv')
            result = []
            for lv_res in lv_res_list:
                if lv_res.get('lv_name') in raid_lv_list and lv_res.get('node_state') not in ['NOT running','unmanaged',hostname]:
                    result.append(lv_res)
            return result

        move_lv_res_list = get_move_lv_res()
        for res in move_lv_res_list:
            if res.has_key('group'):
                self.Move(res.get('group'),peer_node)
            else:
                self.Move(res.get('id'),peer_node)
        return True

