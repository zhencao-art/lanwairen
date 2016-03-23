#!/usr/bin/env python

import CStonithBase
import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CStonithIPMI(CStonithBase.CStonithBase):
    def __init__(self,stName,stType,stOpt):
        CStonithBase.CStonithBase.__init__(self,stName,stType,stOpt)
        self._stOpt = stOpt

    def Create(self):
        try:
            cmd = 'pcs -f '+self._cibCfg+' stonith create '+ self._stName + ' ' + self._stType
            if self._stOpt.has_key('ip'):
                cmd += ' ipaddr=' + self._stOpt.get('ip')
            if self._stOpt.has_key('username'):
                cmd += ' login=' + self._stOpt.get('username')
            if self._stOpt.has_key('passwd'):
                cmd += ' passwd=' + self._stOpt.get('passwd')
            if self._stOpt.has_key('pcmk_host_list'):
                cmd += ' pcmk_host_list=' + self._stOpt.get('pcmk_host_list')
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            if rtn != 0 :
                raise Exception(str(out))
        except Exception as e:
            raise e
        logging.debug('stonith '+self._stName+' add success')
        return True

    def Update(self,newOpt):
        try:
            self._stOpt = newOpt
            cmd = 'pcs -f '+self._cibCfg+' stonith update ' + self._stName
            if self._stOpt.has_key('ip'):
                cmd += ' ipaddr=' + self._stOpt.get('ip')
            if self._stOpt.has_key('username'):
                cmd += ' login=' + self._stOpt.get('username')
            if self._stOpt.has_key('passwd'):
                cmd += ' passwd=' + self._stOpt.get('passwd')
            if self._stOpt.has_key('pcmk_host_list'):
                cmd += ' pcmk_host_list=' + self._stOpt.get('pcmk_host_list')
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            if rtn != 0 :
                raise Exception(str(out))
        except Exception as e:
                raise e
        logging.debug('stonith '+self._stName+' update success')
        return True

    def GetState(self):
        pass
