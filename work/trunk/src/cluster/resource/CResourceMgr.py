# coding:utf-8
#!/usr/bin/env python

import commands,logging
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../common')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../')
import CXmlMgr , CResourceParse

g_all_res_state_dict = {}

#获取所有的primitive资源的详细属性,并记录资源的group clone master关系
def GetAllSubResource(cfg_xml, stat_flag = True):
    if not cfg_xml:
        cfg_xml = CXmlMgr.CXmlMgr()
    if stat_flag:
        SetAllResState()
    first_res_list = GetResource(cfg_xml,stat_flag)
    all_res_list = []
    if not first_res_list :
        return all_res_list
    for first_res in first_res_list:
        if first_res.get('tag') == 'primitive':
            sub_attr = get_sub_attr(cfg_xml , first_res.get('element'))
            first_res.update(sub_attr)
            all_res_list.append(first_res)
        else:
            all_res_list += GetSubRes(cfg_xml,first_res,stat_flag)
    return DeleteElement(all_res_list)


#获取所有一级结点资源，不获取资源的详细属性
def GetAllResource(cfg_xml, stat_flag = True):
    if not cfg_xml:
        cfg_xml = CXmlMgr.CXmlMgr()
    if stat_flag:
        SetAllResState()
    first_res_list = GetResource(cfg_xml,stat_flag)
    return DeleteElement(first_res_list)

#获取指定资源的详细属性，若不是primitive资源，则获取其子资源的详细属性
def GetResourceAttr(cfg_xml , res_name, stat_flag = True):
    if not cfg_xml:
        cfg_xml = CXmlMgr.CXmlMgr()
    if stat_flag:
        SetAllResState()
    first_res_list = GetResource(cfg_xml,stat_flag)
    res_list = []
    if not first_res_list :
        return res_list
    for res in first_res_list:
        if res.get('id') == res_name:
            if res.get('tag') == 'primitive':
                sub_attr = get_sub_attr(cfg_xml , res.get('element'))
                res.update(sub_attr)
                res_list.append(res)
            else:
                res_list = GetSubRes(cfg_xml,res,stat_flag)
            break
        elif res.get('tag') != 'primitive':
            sub_list = GetSubRes(cfg_xml,res,stat_flag)
            for sub in sub_list:
                if sub.get('id') == res_name:
                    res_list.append(sub)
                    return res_list
    return DeleteElement(res_list)
            

def GetResByType(cfg_xml , res_type, stat_flag = True):
    all_res_list = GetAllSubResource(cfg_xml,stat_flag)
    result = []
    for res in all_res_list:
        if res_type == res.get('type'):
            result.append(res)
    return DeleteElement(result)

def GetResByGroup(cfg_xml , grp_name, stat_flag = True):
    grp_list = GetGroup(cfg_xml,stat_flag)
    for grp in grp_list:
        if grp.get('group') == grp_name:
            return grp
    return None

def GetGroup(cfg_xml, stat_flag = True):
    if not cfg_xml:
        cfg_xml = CXmlMgr.CXmlMgr()
    if stat_flag:
        SetAllResState()
    first_res_list = GetResource(cfg_xml,False)
    grp_list = []
    if not first_res_list :
        return grp_list
    for res in first_res_list:
        if res.get('tag') == 'group':
            grp = GetSubRes(cfg_xml , res, stat_flag)
            grp_list.append(grp)
    return grp_list

def GetResource(cfg_xml , stat_flag = True):
    nodelist = ['configuration','resources']
    ele_res_list = cfg_xml.GetNode(None,nodelist)
    if not ele_res_list or not len(ele_res_list):
        return None
    childlist = ele_res_list[0].getchildren()
    result = []
    for ele_res in childlist:
        res_dict = {}
        res_dict['tag'] = ele_res.tag
        if stat_flag:
            res_dict['node_state'] = CResourceParse.FindResState(g_all_res_state_dict,ele_res.get('id'))
        res_dict['element'] = ele_res
        res_dict.update(ele_res.attrib)
        result.append(res_dict)
    return result

def GetSubRes(cfg_xml , father_dict, stat_flag = True):
    element = father_dict.get('element')
    sub_result_list = []
    node_path = ['primitive']
    sub_ele_res_list = cfg_xml.GetNode(element,node_path)
    if sub_ele_res_list:
        for sub_ele in sub_ele_res_list:
            sub_dict = {}
            sub_attr = get_sub_attr(cfg_xml , sub_ele)
            sub_dict.update(sub_attr)
            sub_dict[father_dict.get('tag')] = father_dict.get('id')
            if stat_flag:
                sub_dict['node_state'] = CResourceParse.FindResState(g_all_res_state_dict,sub_ele.attrib.get('id'))
            else:
                #sub_dict['node_state'] = CResourceParse.FindResState(g_all_res_state_dict,sub_ele.attrib.get('id'))
                sub_dict['node_state'] = father_dict.get('node_state')
            sub_dict['tag'] = sub_ele.tag
            sub_dict.update(sub_ele.attrib)
            sub_result_list.append(sub_dict)
    return sub_result_list

def GetNodeState(resName):
    cmd = 'crm_resource -r '+ resName + ' --locate'
    (rtn,out) = commands.getstatusoutput(cmd)
    if rtn!= 0:
        raise Exception(out)
    logging.debug('do command[%s] success' % cmd)
    result = ''
    nodelist = out.split('\n')
    for node in nodelist:
        if node == '':
            continue
        index = node.rfind(':') + 1
        if 'NOT running' in node :
            if result == '':
                result = 'NOT running '
            continue
        if result == 'NOT running ':
            result =  node[index:len(node)] + ','
        else:
            result +=  node[index:len(node)] + ','
    global g_all_res_state_dict
    g_all_res_state_dict[resName] = result[:-1]
    return result[:-1]

def get_sub_attr(cfg,res):
    result = {}
    nodepath = ['instance_attributes','nvpair']
    elist = cfg.GetNode(res,nodepath)
    for e in elist:
        result[e.get('name')] = e.get('value')
    return result

def DeleteElement(res_list):
    for res in res_list:
        if res.has_key('element'):
            res.pop('element')
    return res_list

def GetAllResState():
    global g_all_res_state_dict
    if not g_all_res_state_dict :
        g_all_res_state_dict = CResourceParse.GetAllResState()
    return g_all_res_state_dict

def SetAllResState():
    global g_all_res_state_dict
    g_all_res_state_dict = CResourceParse.GetAllResState()

####test####
