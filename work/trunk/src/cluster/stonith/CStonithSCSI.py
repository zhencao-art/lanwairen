#!/usr/bin/env python

import CStonithBase
import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CStonithSCSI(CStonithBase.CStonithBase):
    def __init__(self,stName,stType,stOpt):
        CStonithBase.CStonithBase.__init__(self,stName,stType,stOpt)
        self._stOpt = stOpt

    def Create(self):
        try:
            cmd = 'pcs -f '+self._cibCfg+' stonith create '+ self._stName + ' ' + self._stType
            for op in self._stOpt :
                cmd += ' ' + op[0] + '=' + op[1]
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            if rtn != 0 :
                logging.error(out)
                raise Exception(str(out))
        except Exception as e:
            raise e
        logging.debug('stonith '+self._stName+' add success')
        return True

    def Update(self,newOpt):
        try:
            cmd = 'pcs -f '+self._cibCfg+' stonith update ' + self._stName
            for op in newOpt:
                cmd += ' ' + op[0] + '=' + op[1]
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            if rtn != 0 :
                logging.error(out)
                raise Exception(str(out))
        except Exception as e:
                raise e
        logging.debug('stonith '+self._stName+' update success')
        return True

    def GetState(self):
        pass
