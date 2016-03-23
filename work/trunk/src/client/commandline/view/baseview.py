# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import re
from params import sectors2txt

import sys, os, re
sys.path.append(os.path.abspath(os.path.join(__file__, '../../../../lib/rpc/phoenix')))
sys.path.append(os.path.abspath(os.path.join(__file__, '../../../../lib/rpc/mds')))

# 安全获取对象
def O(obj, key='', d=None):
    try:
        return obj[key]
    except:
        return d

# 安全获取字符串值
def S(obj, key='', d='NULL'):
    try:
        if key!='':
            return str(obj[key])
        else:
            return str(obj)
    except:
        return d

# 安全获取整型值
def I(obj, key='', d=-1):
    try:
        if key!='':
            return int(obj[key])
        else:
            return int(obj)
    except:
        return d

class BaseView:
    def __init__(self):
        pass

    # 使用空格填充指定长度的字符串
    def fix_len(self, str, width, sep=" "):
        size = self.get_none_format_strlen(str)
        if size > width:
            return str
        return str + sep*(width - size)

    # 输出表格
    def common_list(self, tbl_th=[], tbl_key=[], data=[], idx_key='name', sep=' ', formats={}, sort=True, count=False):
        # 将传入的数据，按指定的key排序
        line_sort = []
        for l in range(len(data)):
            line_sort.append((l, S(data[l], idx_key, '')))

        if sort: line_sort.sort(lambda x,y:cmp(x[1],y[1]))
    
        # 需要整行标红的行
        color_line = []
        # 获取每列的最大宽度
        size_sort = {}
        for i in range(len(tbl_th)):
            max = len(tbl_th[i])
            for l in range(len(data)):
                value = O(data[l],tbl_key[i])
                if value == None: value=""

                if tbl_key[i] in formats.keys():
                    value, cl = getattr(self, "format_"+formats[tbl_key[i]]['fun'])(value=value, params=formats[tbl_key[i]]['params'])
                    data[l][tbl_key[i]] = value
                    if cl == True:
                        color_line.append(l)
                value_len = self.get_none_format_strlen(str(value))
                if max < value_len:
                    max = value_len
            size_sort[i] = max
    
        line_out = []
        out = ""
    
        sep_c = '+'
        sep_h = '-'
        sep_v = '|'
    
        # 画横梁
        line_sep = sep_c
        for k,v in size_sort.items():
            line_sep += sep_h
            for v in range(v):
                line_sep += sep_h
            line_sep += sep_h + sep_c
        line_out.append(line_sep)
    
        # 输出表头
        for i in range(len(tbl_th)):
            out += sep_v + sep + self.fix_len(tbl_th[i], size_sort[i])  + sep
        out += sep_v
        line_out.append(out)
        line_out.append(line_sep)
    
        # 输出内容
        for item in line_sort:
            out = ""
            line = item[0]
            for i in range(len(tbl_th)):
                value = S(data[line], tbl_key[i], "")
                out += sep_v + sep +self.fix_len(value, size_sort[i])  + sep 
            out += sep_v
            if line in color_line:
                out = "\033[1;31m" + out + "\033[0m"
            line_out.append(out)
        line_out.append(line_sep)
        if count:
            line_out.append("[\033[1;37m"+str(len(line_sort))+"\033[0m]"+" rows in set")
    
        return "\n".join(line_out)

    # 字节单位转换
    def format_disk_size(self, value="", params={}):
        size = "%dG" % (int(value) >> 30)
        if not size: size = ""
        if params.has_key('cl') and params['cl'] == True:
            return size, False
        else:
            return size

    # 扇区单位转换
    def format_disk_size_sector(self, value="", params={}):
        size = sectors2txt(value)
        if not size: size = ""
        if params.has_key('cl') and params['cl'] == True:
            return size, False
        else:
            return size

    def format_asm_size(self, value="", params={}):
        if not value: value = ""
        if params.has_key('cl') and params['cl'] == True:
            return value+"MB", False
        else:
            return value 
    
    def format_asm_state(self, value="", params={}):
        if value not in ["CONNECTED","MOUNTED","ONLINE", "CACHED"]:
            if params.has_key('cl') and params['cl'] == True:
                return value, True
            else:
                return "\033[1;31m" + value + "\033[0m"
        else:
            if params.has_key('cl') and params['cl'] == True:
                return value, False
            else:
                return value

    def format_disk_state(self, value="", params={}):
        flag = True
        for v in value.split('/'):
            if v not in ['Online']:
                flag = False
                break

        if not flag:
            if params.has_key('cl') and params['cl'] == True:
                return value, True
            else:
                return "\033[1;31m" + value + "\033[0m"
        else:
            if params.has_key('cl') and params['cl'] == True:
                return value, False
            else:
                return value

    def format_node_discover_state(self, value="", params={}):
        if value not in ["ATTACHED", "UNSUPPORT"]:
            if params.has_key('cl'):
                if params['cl'] == True:
                    return "\033[1;31m" + value + "\033[0m", True
                else:
                    return "\033[1;31m" + value + "\033[0m", False
            else:
                return "\033[1;31m" + value + "\033[0m"
        else:
            if params.has_key('cl'):
                if params['cl'] == True:
                    return value, True
                else:
                    return value, False
            else:
                return value

    def format_lun_state(self, value="", params={}):
        if value not in ["Online"]:
            if params.has_key('cl') and params['cl'] == True:
                return value, True
            else:
                return "\033[1;31m" + value + "\033[0m"
        else:
            if params.has_key('cl') and params['cl'] == True:
                return value, False
            else:
                return value

    # 计算不带颜色控制信息的字符串长度
    def get_none_format_strlen(self, str):
        res = re.findall(r'(\033.+?m)', str)
        size = len(str)
        if res == None:
            return size
        for r in res: size -= len(r)
        return size

    def out_error(self, str):
        return "\033[1;31m" + str + "\033[0m"

    def out_success(self, str):
        return "\033[1;32m" + str + "\033[0m"

    def params_error(self, str):
        return "\033[1;31mParameter error : " + str + "\033[0m"

