#!/usr/bin/env python


import commands,logging,sys
sys.path.append('../resource')
import CResourceBase
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CStonithBase():
    def __init__(self,stName,stType,stOpt):
        self._stName = stName
        self._stType = stType
        self._stOpt = stOpt
        self._cibCfg = CResourceBase.g_cib_filename

    def Create(self):
        pass

    def Delete(self):
        cmd = 'pcs -f '+self._cibCfg+' stonith delete '+ self._stName
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn != 0 :
            raise Exception(out)
        logging.debug('stonith '+self._stName+' delete success')
        return True

    def Update(self,netOpt):
        pass

    def GetState(self):
        pass
