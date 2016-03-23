#!/usr/bin/env python
import CIPMgr
import commands,logging,os,copy ,re , sys

g_corosync_filename = '/etc/corosync/corosync.conf'
class CCoroFile():
    def __init__(self,cfgName,mode = 'r'):
        self._cfgName = cfgName
        #self.Backup()
        self._handle = open(self._cfgName,'r')
        self._fileContent = self._handle.read()

    def __def__(self):
        self._handle.close()

    def Backup(self):
        cmd = 'cp ' + self._cfgName + ' '+ self._cfgName +'.backup'
        (rtn,out) = commands.getstatusoutput(cmd)
        if rtn!= 0:
            raise Exception(out)

    def Update(self,key_words,old_value,new_value):
        all_text = self._fileContent
        if key_words not in all_text:
            raise Exception('corosync file update failed,key['+key_words+'] not found')
        if self.CheckExist(key_words,new_value):
            #raise Exception('option['+ key_words +':'+ str(new_value) + '] exist in corosync file')
            return
        index = all_text.find(key_words)
        while(index != -1):
            begin = index + len(key_words) + 2
            end = all_text.index('\n',begin)
            old = all_text[begin:end].strip()
            if old == str(old_value):
                all_text = all_text.replace(old,str(new_value))
                self._fileContent = all_text
                break
            index = all_text.find(key_words,end)

    def Write(self):
        f_handle = open(self._cfgName,'w')
        f_handle.write(self._fileContent)
        f_handle.close()

    def CheckExist(self,key,value):
        all_text = self._fileContent
        if key not in all_text:
            return False
        index = all_text.find(key)
        while(index != -1):
            begin = index + len(key) + 2
            end = all_text.index('\n',begin)
            old = all_text[begin:end].strip()
            if old == str(value):
                return True 
            index = all_text.find(key,end)
        return False

    def GetItemValue(self,path,key,constraint = {}):
        content = self.GetValue(path,self._fileContent)
        result = []
        for con in content:
            tmp = self.GetItem(con,key)
            cst_flag = True
            for cst in constraint:
                cst_value = self.GetItem(con,cst)
                if cst_value != constraint.get(cst):
                    cst_flag = False
            if cst_flag:
                result.append(tmp)
        return result

    def GetValue(self,path,fc):
        if path == []:
            return []
        node = path[0]
        result = []
        ref = node + '\s*{'
        regx = re.compile(ref)
        relist = regx.findall(fc)
        begin = 0
        for key in relist:
            begin = fc.find(key,begin) + len(key)
            tmp = self.FindIndex(fc[begin:],'}')
            if len(path) == 1:
                result.append(tmp)
            else:
                result += self.GetValue(path[1:],tmp)
        return result


    def GetItem(self,src,item):
        ref = item + ':\s\S*'
        regx = re.compile(ref)
        relist = regx.findall(src)
        if len(relist) == 0:
            raise Exception('key[%s] do not exist in file[%s]'%(item,self._cfgName))
        if len(relist) > 1:
            raise Exception('key[%s] not unique in the file[%s]'%(item,self._cfgName))
        begin = relist[0].find(':') + 1
        return relist[0][begin:].strip()
        

    def FindIndex(self,fc,key):
        flag = 1;begin = 0
        while(flag > 0 and begin < len(fc)):
            if fc[begin] == '}':
                flag -= 1
            elif fc[begin] == '{':
                flag += 1
            begin += 1
        if flag != 0:
            raise Exception('bad format in file[%s]'%self._cfgName)
        return fc[:begin]

def GetCoroValue(path,key,cons = ''): 
    global g_corosync_filename
    f = CCoroFile(g_corosync_filename)
    con_dict = {}
    if cons != '' :
        conlist = cons.split(',')
        for con in conlist:
            tmp = con.split('=')
            con_dict[tmp[0]] = tmp[1]
    return f.GetItemValue(path,key,con_dict)
