# coding:utf-8
#!/usr/bin/env python

import commands,logging
import sys,os , re

def get_resource_state():
    cmd = 'pcs status resources'
    rtn,out = commands.getstatusoutput(cmd)
    if rtn!= 0:
        raise Exception(out)
    result = out
    cmd = 'pcs stonith'
    rtn,out = commands.getstatusoutput(cmd)
    if rtn!= 0:
        raise Exception(out)
    result += '\n' + out
    return result

def get_line(result):
    if result and result[0] == '\n':
        index = 1
    else:
        index = 0
    begin = result.find('\n',index)
    if begin == -1:
        line = result
        result = ''
    else:
        line = result[:begin]
        result = result[begin+1:]
    return line,result

def get_item(src,first,then = ''):
    begin = src.find(first) + 1
    if then:
        end = src.find(then)
    else:
        end = len(src)
    return src[begin:end].strip()

def get_group(line,result):
    grp_id = get_item(line,':')
    grp_dict = {}
    while result:
        line,result = get_line(result)
        if line[1] != ' ':
            break
        rtn = result
        grp_dict.update(get_primite(line))
    state_list = grp_dict.values()
    if state_list.count(state_list[0]) == len(grp_dict):
        grp_dict[grp_id] = state_list[0]
    else:
        grp_dict[grp_id] = 'NOT running'
    return rtn,grp_dict

def get_clone(line,result):
    clone_res_id = get_item(line,':','[')
    res_id = get_item(line,'[',']')
    line,result = get_line(result)
    if line.find('Started:') != -1:
        res_state = get_item(line,'[',']')
        if res_state.find(' ') == -1:
            line,result = get_line(result)
    else:
        res_state = 'NOT running'
    clone_dict = {}
    clone_dict[res_id] = res_state
    clone_dict[clone_res_id] = res_state
    return result,clone_dict

def get_master(line,result):
    master_id = get_item(line,':','[')
    res_id = get_item(line,'[',']')
    line,result = get_line(result)
    if line.find('Slaves') != -1:
        res_state = get_item(line,'[',']')
        if res_state.find(' ') == -1:
            line,result = get_line(result)
    else:
        res_state = 'NOT running'
    clone_dict = {}
    clone_dict[res_id] = res_state
    clone_dict[master_id] = res_state
    return result,clone_dict

def get_primite(line):
    regx = '\S*'
    proc = re.compile(regx)
    reslist = proc.findall(line)
    count = reslist.count('')
    index = 0
    while index < count:
        reslist.remove('')
        index += 1
    res_id = reslist[0]
    if 'Stopped' in reslist:
        res_state = 'NOT running'
    elif 'FAILED' in reslist:
        res_state = 'FAILED'
    elif 'unmanaged' in reslist:
        res_state = 'unmanaged'
    else:
        res_state = reslist[-1]
    tmp_dict = {}
    tmp_dict[res_id] = res_state
    return tmp_dict

def GetAllResState():
    import pdb
    #pdb.set_trace()
    res_state_dict = {}
    result = get_resource_state()
    while len(result) > 0 :
        line,result = get_line(result)
        if line.find('Group') != -1:
            result,tmp_dict = get_group(line,result)
            res_state_dict.update(tmp_dict)
        elif line.find('Clone') != -1:
            result,tmp_dict = get_clone(line,result)
            res_state_dict.update(tmp_dict)
        elif line.find('Master') != -1:
            result,tmp_dict = get_master(line,result)
            res_state_dict.update(tmp_dict)
        else:
            tmp_dict = get_primite(line)
            res_state_dict.update(tmp_dict)
    return res_state_dict

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
    return result[:-1]

def FindResState(res_state_dict , res_id):
    if not res_state_dict:
        res_state_dict = GetAllResState()
    return res_state_dict.get(res_id)



#########################################################
#print get_primite(sys.argv[1])
#exit(0)
#state_list =  GetAllResState()
#print state_list
#print FindResState(state_list,sys.argv[1])
