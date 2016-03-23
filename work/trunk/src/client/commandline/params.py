# -*- coding: utf-8 -*
#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os, re

# Phoenix版本
PRODUCT_VERSION = '1.0.0'

# CLI INTRO
IntroString = "\n\
Welcome to Puma storage console!, Ver %s\n\
Type: \033[1;37mhelp\033[0m for list all cmd\n\
Type: \033[1;37m<cmd> -h\033[0m for list all action for one cmd\n\
Type: \033[1;37m<cmd> <action> -h\033[0m for get detail help \n" % PRODUCT_VERSION

# mds rpc 端口号
MDS_PORT = 20150

# 命令行前缀
PRODUCT_NAME = "Puma-Cli"

# 历史记录最大数量
MAX_OPT_HIST = 1000

opt_history = "/tmp/opt_history"

def safepeek(ls) :
    if len(ls)>0 : return ls[0]
    else : return ''

# 保存历史
def save_hist(hist=[]):
    count = MAX_OPT_HIST
    if len(hist) < MAX_OPT_HIST: count = len(hist)

    f = open(opt_history, 'w', 0)
    f.write("\n".join(hist[::-1][:count]))
    f.close()

# 载入历史
def load_hist():
    if os.path.exists(opt_history):
        f = open(opt_history)
        lines = f.read().strip()
        if lines=="":
            return []
        return lines.split('\n')[::-1] 
    return []


class ChkParams():
    def __init__(self):
        pass

    def chk_arg2value(self, value):
        # arg1=value1,arg2=value2
        kv={}
        item = value.split(',')
        for i in item:
            sp = i.split('=')
            if len(sp) != 2: return None
            if len(sp[0].strip()) == 0:return None
            if len(sp[1].strip()) == 0:return None
            kv[sp[0].strip()] = sp[1].strip()
        return kv

def confirm(txt):
    defans='y/n/yes/no'
    ans='x'
    while ans.lower() not in ['y','n','yes','no']:
        try:
            ans=raw_input('\033[1;37m%s [%s] ?\033[0m ' % (txt,defans))
        except (KeyboardInterrupt, EOFError):
            print
            return ''
        if ans.lower() not in ['y','n','yes','no']:
            print 'Please type y/n/yes/no as answer, try again'
    if ans.lower() in ['y','yes'] : return 'y'
    return 'n'

def is_ip(str):
    if re.search(r'^(\d{1,3}\.){3}\d{1,3}$', str) == None:
        return False

    items = str.split('.')
    if items[0] == '0':
        return False

    for item in items:
        if int(item)>255 or int(item)<0:
            return False
    return True

def is_port(str):
    if not str.isdigit():
        return False
    if int(str) > 65535:
        return False
    return True

SUPPORT_UNIT = ('b', 'k', 'm', 'g', 't', 'p', 'e', 'z', 'y')

""" 
磁盘大小取整, 例如将599转换为600，2998转换为3000
@param size     : 磁盘的原始大小
@param modulus  : 磁盘的取整系数, 默认1.01合适, 比如对于size=600,modulus=1.01, 则上下浮动大小为6
@param unit     : 取整的最小单元, 默认100合适
@return         : 转换后的大小
"""
def get_fix_disk_size(size=0, modulus=1.01, unit=10):
    if size == 0 or modulus < 1 or modulus > 2 or unit == 0:
        return 0

    size = int(size)
    base = 0

    if (size % unit) > (unit / 2):
        base = (size / unit + 1) * unit
    else:
        base = (size / unit) * unit

    min = int(base * (2 - modulus));
    max = int(base * modulus);

    if size <= max and size >= min:
        return base
    else:
        return size

def bytes2txt(by,unit = "k"):
    bits = 0

    if unit == 'k':
        bits = 10
    elif unit == 'm':
        bits = 20
    elif unit == 'g':
        bits = 30
    else:
        return None

    by = by >> bits

    return str(by) + unit

def sectors2txt(sectors, sector=512, per=1000, unit="g"):
    pos      = -1
    pos_curr = -1
    try:
        sectors = int(sectors)
        unit.strip().lower()
        if unit == "":
            unit = 'g'
        if unit != "":
            pos = SUPPORT_UNIT.index(unit)
    except:
        return None
    size = sectors*sector
    while True:
        pos_curr += 1
        if pos >= 0 and pos_curr == pos:
            break
        size /= 1.0*per
    size = 1.0*sectors*sector/(per**(pos_curr))
    size = get_fix_disk_size(size)

    return "%d%s" % (size, SUPPORT_UNIT[pos_curr].upper())

def txt2sectors(txt, sector=512, per=1000):
    try:
        unit = txt[-1].lower()
        num  = int(txt[:-1])
        pos  = SUPPORT_UNIT.index(unit)
    except :
        return None
    return num*(per**pos)/sector
