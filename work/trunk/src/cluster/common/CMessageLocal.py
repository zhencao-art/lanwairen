#!/usr/bin/env python

import CMessage
import logging,commands

class CMessageLocal(CMessage):
    def __init__(self):
        self._result = None

    def Login(self,hostname,user,pwd):
        return true
    def Action(self,cmd):
        (rtn,out) = commands.getstatusoutput(cmd)
        if rtn !=0 :
            return False
        self._result = out
        return True
    def GetResult(self):
        return self._result
    def Logout(self):
        return true
