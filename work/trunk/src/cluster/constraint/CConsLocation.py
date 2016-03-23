#!/usr/bin/env python

import commands,logging
import CConstraintBase
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CConsLocation(CConstraintBase.CConstraintBase):
    def __init__(self,consType,consOpt):
        CConstraintBase.CConstraintBase.__init__(self,consType,consOpt)
    def Create(self):
        cmd = 'pcs -f '+self._cibCfg+' constraint location '
        opt = self._consOpt.get('rsc')
        if opt!=None :
            cmd += opt
        opt = self._consOpt.get('action')
        if not opt:
            cmd += ' prefers '
        else:
            cmd += ' ' + opt + ' '
        opt = self._consOpt.get('node')
        if opt!=None :
            cmd += opt
        opt = self._consOpt.get('score')
        if opt!=None :
            cmd +='='+ opt
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error(out)
            return False
        logging.debug('constraint  create success')
        return True
    def Delete(self):
        cmd = 'pcs -f '+self._cibCfg+' constraint delete ' + self._consId
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            logging.error(out)
            return False
        logging.debug('constraint '+self._consId+' delete success')
        return True
    def GetState():
        pass
