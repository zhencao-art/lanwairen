#!/usr/bin/env python

import commands,logging
import CConstraintBase
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CConsSet(CConstraintBase.CConstraintBase):
    def __init__(self,consType,consOpt):
        CConstraintBase.CConstraintBase.__init__(self,consType,consOpt)
    def Create(self):
        try:
            cmd = 'pcs -f '+self._cibCfg+' constraint order set '
            op = self._consOpt.get('first')
            cmd += op + ' sequential=false require-all=true'
            if self._consOpt.has_key('then'):
                op = self._consOpt.get('then')
                cmd += ' set ' + op + ' '
            cmd += ' sequential=false'
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            if rtn!=0 :
                raise Exception(out)
        except Exception as e:
            raise e
        logging.debug('do command[%s] success' % cmd)
        return True
    def Delete(self):
        if self._consId==None:
            return False
        cmd = 'pcs -f '+self._cibCfg+' constraint delete '+ self._consId
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0 :
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def GetState(self):
        pass


