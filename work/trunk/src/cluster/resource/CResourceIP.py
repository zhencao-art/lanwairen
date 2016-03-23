#!/usr/bin/env python

import CResourceBase
import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CResourceIP(CResourceBase.CResourceBase):
    def __init__(self,resName,resType,resOptions):
        CResourceBase.CResourceBase.__init__(self,resName,resType,resOptions)
        self._sIP=""
        self._sNic = ''
        self._iCidrNetMask = 0
    def Create(self):
        cmd = 'pcs -f '+self._cibCfg+' resource create '+ self._sResName +' '+ self._sResType 
        if self._options.has_key('ip'):
            cmd += ' ip=' + self._options.get('ip')
        if self._options.has_key('nic'):
            cmd += ' nic=' + self._options.get('nic')
        if self._options.has_key('cidr_netmask'):
            cmd += ' cidr_netmask=' + self._options.get('cidr_netmask')
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn != 0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return rtn

    def Update(self,newOptions):
        cmd = 'pcs -f '+self._cibCfg+' resource update ' + self._sResName + ' '
        if newOptions.has_key('ip'):
            cmd += ' ip=' + newOptions.get('ip')
        if newOptions.has_key('nic'):
            cmd += ' nic=' + newOptions.get('nic')
        if newOptions.has_key('cidr_netmask'):
            cmd += ' cidr_netmask=' + newOptions.get('cidr_netmask')
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn != 0 :
            logging.error('do command['+cmd+'] failed')
            raise Exception(out)
        logging.debug('do command[%s] success' % cmd)
        return True
    def GetState(self):
        result = 'res_name='+self._sResName+',res_type='+self._sResType+',ip='+self._sIP+',nic='+self._sNic+',cidr_netmask='+str(self._iCidrNetMask)
        return result
