#!/usr/bin/env python
import CIPMgr
import commands,logging,os,copy ,re , sys

g_host_filename = '/etc/hosts'
class CHostFile():
    def __init__(self,cfgName):
       # CIPMgr.File.__init__(self,cfgName)
        self._file = CIPMgr.File(cfgName)

    def GetHosts(self):
        f_cont = self._file.GetFile()
        f_cont_line_list = f_cont.split('\n')
        result = []
        for content in f_cont_line_list:
            if content == '':
                continue
            line_list = content.split(' ')
            if line_list[0] == '127.0.0.1' or line_list[0] == '::1':
                continue
            host_dict = {}
            host_dict['ip'] = line_list[0]
            host_dict['host'] = line_list[1]
            result.append(host_dict)
        return result

    def SetHost(self,ip,host):
        f_cont = self._file.GetFile()
        begin = f_cont.find(host)
        if begin == -1 :
            f_cont += '\n' + ip + ' ' + host
        else:
            end = begin -1
            while f_cont[end] != '\n':
                if f_cont[end] == ' ':
                    begin = end
                end -= 1
            #f_cont = f_cont.replace(f_cont[end+1:begin],ip,1)
            f_cont = f_cont[:end+1] + ip + f_cont[begin:]
        self._file.Write(f_cont)

def SetHosts(hblist):
    f = CHostFile(g_host_filename)
    for hb in hblist:
        f.SetHost(hb.get('hb_ip'),hb.get('host'))
    return f._file.GetFile()

