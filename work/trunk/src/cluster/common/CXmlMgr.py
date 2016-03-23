#!/usr/bin/env python

#import xml.etree.cElementTree as Xml
from lxml import etree as Xml
from xml.dom import minidom
import commands,logging,os,copy
import sys,os , tempfile
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
import CIPMgr

class CXmlMgr():
    def __init__(self,cfgName = None,bStayFlag=False):
        self._cfgName = cfgName
        self._bStayFalg = bStayFlag

        if self._bStayFalg==False:
            fd,filename = tempfile.mkstemp()
            (rtn,out,err) = CIPMgr.Exec_cmd('pcs cluster cib ' + filename)
            self._cfgName = filename
            if rtn == 0:
                self._xml = Xml.parse(filename)
                self.root = self._xml.getroot()
            else:
                self._xml = None
                self.root = None
                msg = out+', please check cluster status to ensure it started'
                logging.error(msg)
                raise Exception(msg)
        else:
            if os.path.exists(cfgName):
                self._xml = Xml.parse(cfgName)
                self.root = self._xml.getroot()
            else:
                self._xml = Xml.ElementTree()
                #e = Xml.Element("block-devices")
                #self._xml._setroot(e)
                self.root = None
                #self._xml.write(cfgName)

    def GetNode(self,e,nodeName,isCreate = False):
        if e==None:
            e = self.root
        if self.root == None and isCreate:
            el = self.AddNodes(e,nodeName)
            return [el]
        if self.root == None:
            raise Exception('xml is not exist')
        node = nodeName[0]
        newNode = copy.copy(nodeName)
        if self.root.tag == node:
            node = newNode[1]
            del newNode[0:2]
        else:
            del newNode[0]

        elist = e.findall(node)
        if len(elist) == 0 and isCreate :
            el = self.AddNodes(e,node.split(' ')+newNode)
            return [el]
        if len(newNode)==0:
            return elist
        for ec in elist :
            res = self.GetNode(ec,newNode,isCreate)
            if res!=None and len(res) != 0 :
                return res
        return None

    def GetElement(self,element,nodeName):
        if element == None :
            logging.error('bad element input')
            return None
        e = element.findall(nodeName)
        return e

    def GetValue(self,element,propName):
        if element== None:
            logging.error('bad element input')
            return None

        result = element.get(propName)
        return result
    
    def GetTag(self,element):
        if element == None:
            raise Exception('can not get tag for a noneType element')
        return element.tag

    def GetChildren(self,element):
        if element == None:
            element = self.root
        return element.getchildren()

            
    #def __del__(self):
    #    if self._xml != None and self._bStayFalg == False :
    #        CIPMgr.Exec_cmd('rm -rf '+self._cfgName)
    
    def GetAttr(self,element,nodeName):
        if element== None:
            return None
        li = element.findall(nodeName)
        if li==None:
            return None
        result = []
        for e in li:
            tmp_dict = dict(e.attrib)
            tmp_dict['tag'] = nodeName
            result.append(tmp_dict)
        return result

    def AddNode(self,element,nodeName,attr = {}):
        if self.root == None:
            e = Xml.Element(nodeName)
            self._xml._setroot(e)
            self.root = e
            return e
        if element is None :
            element = self.root
        sub = Xml.Element(nodeName,attr)
        element.append(sub)
        return sub
    
    def AddNodes(self,element,nodelist):
        for node in nodelist:
            sub = self.AddNode(element,node)
            element = sub
        return element

    def AddKey(self,element,atrrib):
        for k in atrrib :
            self.UpdateKey(element,k,atrrib[k])

    def UpdateNode(self,element,nodeName,attr = {}):
        element.tag = nodeName
        if len(attr)>0 :
            self.AddKey(element,attr)

    def UpdateKey(self,element,keyName,keyValue):
        if element!=None:
            element.set(keyName,keyValue)

    def DeleteNode(self,element,sub):
        if element!=None:
            element.remove(sub)

    def DeleteKey(self,element,key):
        if element!=None:
            element.attrib.pop(key)

    def Format(self,strT,old):
        rtn = strT.find(old)
        if rtn==-1 :
            return strT
        new = old+old
        while strT.find(new)!=-1:
            strT = strT.replace(new,old)
        old += u'\t'
        strT = self.Format(strT,old)
        return strT

    def Write(self):
        if self._xml!=None :
            #strE = Xml.tostring(self.root)
            #strNew = minidom.parseString(strE).toprettyxml()
            #strNew = self.Format(strNew,u'\n')
            #self.root = Xml.fromstring(strNew)
            self.indent(self.root)
            self._xml._setroot(self.root)
            self._xml.write(self._cfgName,pretty_print=True)
            return
        raise Exception('xml[%s] maybe do not exist,please check'%self._cfgName)

    def indent(self,elem, level=0):
        space = "    "
        i = "\n" + level*space
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + space
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def GetString(self):
        if self.root != None:
            strE = Xml.tostring(self.root)
            return strE

    def SetString(self,tree):
        self.root = Xml.fromstring(tree)
        self.Write()
