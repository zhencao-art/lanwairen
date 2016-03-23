#!/usr/bin/env python

import CMessage
import logging
import pxssh,getpass

class CMessageSSH(CMessage.CMessage):
    def __init__(self):
        try:
            self._ssh = pxssh.pxssh()
        except pxssh.ExceptionPxssh,e:
            logging.debug(str(e))

    def Login(self,hostname,user,pwd):
        #  try:
            rtn = self._ssh.login(str(hostname),str(user),str(pwd))
            logging.debug('login {0} success'.format(hostname))
            return rtn
        #  except pxssh.ExceptionPxssh,e:
        #      print str(e)
    def Action(self,cmd):
        try:
            self._ssh.sendline(cmd)
            logging.debug('do action:{0} success'.format(cmd))
        except pxssh.ExceptionPxssh,e:
            print str(e)
    def GetResult(self):
        self._ssh.prompt()
        result = self._ssh.before
        return result
    def Logout(self):
        self._ssh.logout()
