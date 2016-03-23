#!/usr/bin/env python
#
#common resource options must be unique,all the key in the
#options must be the key of the resource
#
import CResourceBase
import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CResourceCommon(CResourceBase.CResourceBase):
    def __init__(self,resName,resType,resOptions):
        CResourceBase.CResourceBase.__init__(self,resName,resType,resOptions)
    def Create(self):
        cmd = 'pcs -f '+self._cibCfg+' resource create '+ self._sResName +' '+ self._sResType 
        for k in self._options:
            cmd += ' '+ k + '=' + self._options.get(k)
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn != 0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return rtn
    def Update(self,newOptions):
        cmd = 'pcs -f '+self._cibCfg+' resource update ' + self._sResName + ' '
        for k in newOptions:
            cmd += ' '+ k + '=' + newOptions.get(k)
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn != 0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def GetState(self):
        return ""
