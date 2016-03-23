#!/usr/bin/env python

import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

g_cib_filename = '/etc/cib_config'

class CResourceBase(object):
    def __init__(self,resName,resType,options):
        self._sResName = resName
        self._sResType = resType
        self._options = options
        self._cibCfg = g_cib_filename
    def Create(self):
        pass
    def Delete(self):
        logging.debug('start delete resource[%s]' % self._sResName)
        cmd = 'pcs resource delete '+ self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True

    def Update(self,newOptions):
        pass
    def GetState(self):
        pass
    def Disable(self):
        cmd = 'pcs resource disable '+ self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def Enable(self, file_flag = False):
        if not file_flag:
            cmd = 'pcs resource enable '+ self._sResName
        else:
            cmd = 'pcs -f '+self._cibCfg+' resource enable '+ self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
        
    def SetClone(self,options = []):
        #cmd = 'pcs -f '+self._cibCfg+' resource clone '+ self._sResName
        cmd = 'pcs resource clone '+ self._sResName
        for op in options:
            cmd += ' '+ op[0] + '=' + op[1]
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def DeleteClone(self):
        cmd = 'pcs -f '+self._cibCfg+' resource unclone '+ self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def SetMaster(self,masterName,options):
        cmd = 'pcs -f '+self._cibCfg+' resource master '+ masterName + ' ' + self._sResName 
        for op in options:
            cmd += ' '+ op[0] + '=' + op[1]
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
         
    def DeleteMaster(self):
        cmd = 'pcs -f '+self._cibCfg+' resource delete '+ self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
       
    def CheckRunState(self):
        cmd = 'pcs -f '+self._cibCfg+' resource debug-start ' + self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
           # import re
           # ref = 'ERROR:'
           # rtn = ''; begin = out.find(ref)
           # while(begin != -1):
           #     end = out.find('\n',begin)
           #     rtn += out[begin:end]
           #     begin = out.find(ref,end)
            raise Exception(err)
        return True

    def Manage(self):
        cmd = 'pcs -f '+self._cibCfg+' resource  manage ' + self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True

    def Unmanage(self):
        cmd = 'pcs -f '+self._cibCfg+' resource unmanage ' + self._sResName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
