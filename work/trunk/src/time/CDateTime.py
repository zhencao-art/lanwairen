#!/usr/bin/env python
import commands,logging,os,copy ,re , sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../ntp_conf")))
import time
import CIPMgr , client , ntp

class CDateTime():
    def CurrentTime():
        return time.localtime()

    def CurrentTz():
        rtn,out,err = CIPMgr.Exec_cmd('timedatectl status')
        return out

    def SetTz(timezone):
        CIPMgr.Exec_cmd('timedatectl set-timezone ' + timezone)

    def SetTime(time):
        CIPMgr.Exec_cmd('timedatectl set-time ' + time)


def CurrentTime():
    return time.localtime()

def CurrentTz():
    rtn,out,err = CIPMgr.Exec_cmd('timedatectl status')
    regx = 'Timezone:\s\S*'
    proc = re.compile(regx)
    rtnlist = proc.findall(out)
    for tz in rtnlist:
        begin = tz.find(':') + 1
        return tz[begin:].strip()
    return ''

def SetTz(timezone):
    CIPMgr.Exec_cmd('timedatectl set-timezone ' + timezone)

def SetTime(time):
    ntp.ntp_stop()
    ntp.ntp_disable()
    CIPMgr.Exec_cmd('timedatectl set-time ' + time)
    CIPMgr.Exec_cmd('timedatectl set-local-rtc 1')

def ListTimezone():
    rtn,out,err = CIPMgr.Exec_cmd('timedatectl  list-timezones')
    tz_list = []
    begin = out.find('\n')
    end = 0
    if begin == -1:
        tz_list.append(out)
        return tz_list
    while begin != -1 :
        tz_list.append(out[end:begin])
        end = begin + 1
        begin = out.find('\n',end)
    return tz_list

