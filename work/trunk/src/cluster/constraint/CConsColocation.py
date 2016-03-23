#!/usr/bin/env python

import commands,logging
import CConstraintBase
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CConsColocation(CConstraintBase.CConstraintBase):
    def __init__(self,consType,consOpt):
        CConstraintBase.CConstraintBase.__init__(self,consType,consOpt)
    def Create(self):
        cmd = 'pcs -f '+self._cibCfg+' constraint colocation add '
        op = self._consOpt.get('rsc')
        if op==None :
            return False
        cmd += op+' with '
        op = self._consOpt.get('with-rsc')
        if op==None :
            return False
        cmd +=op
        op = self._consOpt.get('score')
        if op!=None :
            cmd +=' ' + op
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            raise Exception(out)
        logging.debug('constraint create success')
        return True
    def Delete(self):
        cmd = 'pcs -f '+self._cibCfg+' constraint delete ' + self._consId
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            raise Exception(out)
        logging.debug('constraint '+self._consId+' delete success')
        return True
    def GetState():
        pass



