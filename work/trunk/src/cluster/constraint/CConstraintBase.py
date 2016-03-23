#!/usr/bin/env python

import commands,logging,sys
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr
sys.path.append('../resource')
import CResourceBase

class CConstraintBase():
    def __init__(self,consType,consOpt):
        self._consType = consType
        self._consOpt = consOpt
        self._consId = None
        self._cibCfg = CResourceBase.g_cib_filename
        if not  self._cibCfg:
            self._cfgCfg = '/etc/cib_config_file'

    def Create(self):
        pass
    def Delete(self):
        cmd = 'pcs -f '+self._cibCfg+' constraint delete ' + self._consId
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error(out)
            return False
        logging.debug('constraint '+self._consId+' delete success')
        return True
    def GetState(self):
        pass
    def SetConsId(self,Id):
        self._consId = Id

