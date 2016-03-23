#!/usr/bin/env python

import CResourceBase
import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CResourceLVM(CResourceBase.CResourceBase):
    def __init__(self,resName,resType,resOptions):
        CResourceBase.CResourceBase.__init__(self,resName,resType,resOptions)
        self._sVolgrpname=""
        self._state = []
    def Create(self):
        cmd = 'pcs -f '+self._cibCfg+' resource create '+self._sResName +' '+ self._sResType + ' '
        if self._options.has_key('volgrpname'):
            cmd += 'volgrpname=' + self._options.get('volgrpname')
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def Update(self,newOptions):
        cmd = 'pcs -f '+self._cibCfg+' resource update '+ self._sResName +' '
        if newOptions.has_key('volgrpname'):
            cmd += 'volgrpname=' + newOptions.get('volgrpname')
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def GetState(self):
        self._state = []
        op = 'res_name,'+self._sResName
        self._state.append(op.split(','))
        op = 'res_type,'+self._sResType
        self._state.append(op.split(','))
        op = 'volgrpname,'+self._sVolgrpname
        self._state.append(op.split(','))
        return self._state
