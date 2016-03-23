#!/usr/bin/env python

import logging,os,sys,commands
sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../cluster/common")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
import CXmlMgr,client , puma_pb2, CIPMgr
import copy

class CConfigMgr():
    def __init__(self,client,config_name,bStayFlag = False):
        self._handle = CXmlMgr.CXmlMgr(config_name,bStayFlag)
        self._action = puma_pb2.XmlSynReq()
        self._client = client
        if client:
            self._stub = self._client.stub()
        pass

    def GetDBHandle(config_name,bStayFlag = False):
        return self._handle

    def GetNode(self,nodelist,element=None,isCreate = False):
        if element==None :
            element = self._handle.root
        elist = self._handle.GetNode(element,nodelist,isCreate)
        if elist==None or len(elist)==0:
            raise Exception('xml path ['+':'.join(nodelist)+'] do not exist')
        return elist

    def GetKey(self,e,key):
        rtn = self._handle.GetValue(e,key)
        return rtn

    def AddNoded(self,nodepath,nodeName,attr={},isCreate = False):
        self.AddAction('AddNode',nodepath,nodeName,attr)
        if nodepath == None:
            e = self._handle.root
        else:
            elist = self.GetNode(nodepath,None,isCreate)
            if len(elist)>1:
                raise Exception('path ['+':'.join(nodepath)+'] not unique')
            e = elist[0]
        self._handle.AddNode(e,nodeName,attr)
    
    def AddNode(self,nodepath,attr = {},isCreate = True):
        if nodepath == None or len(nodepath)==0:
            raise Exception('nodepath is None Type,add node failed')
        newpath = copy.copy(nodepath)
        nodename = newpath[len(newpath)-1]
        del newpath[len(newpath)-1]
        self.AddNoded(newpath,nodename,attr,isCreate)

    def AddKey(self,nodepath,atrrib):
        elist = self.GetNode(nodepath)
        self.AddAction('AddKey',nodepath,None,attrib)
        for element in elist:
            self._handle.AddKey(element,attrib)

    def UpdateNoded(self,nodepath,nodeName,attr = {}):
        elist = self.GetNode(nodepath)
        self.AddAction('UpdateNode',nodepath,nodeName,attr)
        for element in elist:
            self._handle.UpdateNode(element,nodeName,attr)
    
    def UpdateNode(self,nodepath,attr={}):
        if nodepath == None or len(nodepath)==0:
            raise Exception('nodepath is None Type,add node failed')
        nodename = nodepath[len(nodepath)-1]
        self.UpdateNoded(nodepath,nodename,attr)

    def UpdateKey(self,nodepath,keyName,keyValue):
        elist = self.GetNode(nodepath)
        attr = {}
        attr[keyName] = keyValue
        self.AddAction('UpdateKey',nodepath,None,attr)
        for element in elist:
            self._handle.UpdateKey(element,keyName,keyValue)

    def DeleteNoded(self,fatherpath,subname):
        elist = self.GetNode(fatherpath)
        self.AddAction('DeleteNode',fatherpath,subname,{})
        for e in elist:
            sublist = self.GetNode(subname.split(' '),e)
            for sub in sublist:
                self._handle.DeleteNode(e,sub)
    
    def DeleteNode(self,nodepath):
        if nodepath == None or len(nodepath)==0:
            raise Exception('nodepath is None Type,add node failed')
        newpath = copy.copy(nodepath)
        nodename = newpath[len(newpath)-1]
        del newpath[len(newpath)-1]
        self.DeleteNoded(newpath,nodename)

    def DeleteKey(self,nodepath,key):
        elist = self.GetNode(nodepath)
        self.AddAction('DeleteKey',nodepath,key,None)
        for element in elist:
            self._handle.DeleteKey(element,key)

    def Commit(self,isLocal = False):
        if isLocal==False :
            self._action.xml = GetXml(self._handle._cfgName)
            self._stub.syn_xml(None,self._action,None)
            response = self._client.get_response()
            self.Clear()
            if response.ret.retcode != 0:
                raise Exception(response.ret.msg)
        self._handle.Write()
        return True

    def Clear(self):
        del self._action
        self._action = puma_pb2.XmlSynReq()

    def RemoveAction(self,attr):
        pass

    def AddAction(self,action,nodepath,nodename,attr):
        ac = self._action.action.add()
        if nodepath:
            ac.nodepath = ':'.join(nodepath)
        else:
            ac.nodepath = ''

        ac.nodename = nodename
        ac.action   = action
        if attr==None:
            attr = {}
        for k in attr:
            a = ac.attr.add()
            a.key = k
            a.value = attr[k]
    def SetClient(self,client):
        self._client = client

def GetXml(f_name):
    try:
        f = CIPMgr.File(f_name)
        fc = f.GetFile()
    except Exception as e:
        fc = ''
    return fc

def Compare(new,old):
    if new != old:
        return False
    return True

def SetXmlByString(f_name,tree):
    f = CIPMgr.File(f_name)
    f.Write(tree)
