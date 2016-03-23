#!/usr/bin/env python

import commands,logging
import CConstraintBase
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CConsOrder(CConstraintBase.CConstraintBase):
    def __init__(self,consType,consOpt):
        CConstraintBase.CConstraintBase.__init__(self,consType,consOpt)
    def Create(self):
        try:
            cmd = 'pcs -f '+self._cibCfg+' constraint order '
            op = self._consOpt.get('first-action')
            cmd += op + ' '
            op = self._consOpt.get('first')
            cmd += op + ' '
            op = self._consOpt.get('then-action')
            cmd += ' then ' + op + ' '
            op = self._consOpt.get('then')
            cmd += op
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            if rtn!=0 :
                raise Exception(out)
        except Exception as e:
            raise e
        logging.debug('constraint order create success')
        return True
    def Delete(self):
        if self._consId==None:
            return False
        cmd = 'pcs -f '+self._cibCfg+' constraint delete '+ self._consId
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            raise Exception(out)
        logging.debug('constraint '+self._consId+' delete success')
        return True
    def GetState(self):
        pass


