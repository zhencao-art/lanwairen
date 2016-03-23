#!/usr/bin/env python
import getpass,pxssh
import commands

class PCDisk(object):
    def __init__(self):
        print 'hello'
    def GetDiskList(self,hostname,usrname,passwd):
        try:
            server=pxssh.pxssh()
            server.login(hostname,usrname,passwd)
            server.sendline('cd /dev/disk/by-id')
            server.prompt()
            server.before
            server.sendline('ls wwn-0x*')
            server.prompt()
            disklist=server.before
            server.logout()
            return disklist
        except pxssh.ExceptionPxssh,e:
            print "pxssh occur error."
            print str(e)
        return None
    def GetLocalDisk(self):
        (rtx,out)=commands.getstatusoutput('ls /dev/disk/by-id/wwn-0x*')
        if rtx!=0 :
            print out
            return None
        localDisk=out.split('\n')
        return localDisk


d = PCDisk()
st = d.GetDiskList('172.16.9.239','root','root123')
print st
