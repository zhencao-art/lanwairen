# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys,logging,re
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
import CIPMgr
import exception,toolbox

class LvmPV:
    def __init__(self):
        self.name = None
        self.vg_name = None
        self.size_sectors = None
        self.inter_num = None
        self.status = None
        self.not_alloc = None
        self.lv_num = None
        self.extent_kb = None
        self.total_extents = None
        self.free_extents = None
        self.alloc_extents= None
        self.uuid = None

    def dev_size(self,unit = "GiB"):
        return toolbox.Sectors2Gib(self.size_sectors)

    def size(self,unit = "GiB"):
        return (self.extent_kb * self.total_extents)\
                >> (toolbox.unit2bits(unit) - 10)

    def free(self,unit = "GiB"):
        return (self.extent_kb * self.free_extents)\
                >> (toolbox.unit2bits(unit) - 10)

    def format(self,out = {}):
        out["name"]          = self.name
        out["vg_name"]       = self.vg_name
        out["size_sectors"]  = self.size_sectors
        out["inter_num"]     = self.inter_num
        out["status"]        = self.status
        out["not_alloc"]     = self.not_alloc
        out["lv_num"]        = self.lv_num
        out["extent_kb"]     = self.extent_kb
        out["total_extents"] = self.total_extents
        out["free_extents"]  = self.free_extents
        out["alloc_extents"] = self.alloc_extents
        out["uuid"]          = self.uuid
        

class LvmVG:
    def __init__(self):
        self.name             = None
        self.access           = None
        self.status           = None
        self.inter_num        = None
        self.max_lv_num       = None
        self.cur_lv_num       = None
        self.opened_lv_num    = None
        self.max_lv_size      = None
        self.max_pv_num       = None
        self.cur_pv_num       = None
        self.actual_pv_num    = None
        self.size_kb          = None
        self.phy_extent_size  = None
        self.total_extent_num = None
        self.alloc_extent_num = None
        self.free_extent_num  = None
        self.uuid             = None

    def free_size(self,unit = "GiB"):
        return (self.phy_extent_size * self.free_extent_num)\
                >> (toolbox.unit2bits(unit) - 10)

    def total_size(self,unit = "GiB"):
        return (self.phy_extent_size * self.total_extent_num)\
                >> (toolbox.unit2bits(unit) - 10)

    def extent_size(self,unit = "KiB"):
        return self.phy_extent_size

    def extent_count(self):
        return self.total_extent_num

    def free_extent_count(self):
        return self.free_extent_num

    def format(self,out = {}):
        out["name"]             = self.name
        out["access"]           = self.access
        out["status"]           = self.status
        out["inter_num"]        = self.inter_num
        out["max_lv_num"]       = self.max_lv_num
        out["cur_lv_num"]       = self.cur_lv_num
        out["opened_lv_num"]    = self.opened_lv_num
        out["max_lv_size"]      = self.max_lv_size
        out["max_pv_num"]       = self.max_pv_num
        out["cur_pv_num"]       = self.cur_pv_num
        out["actual_pv_num"]    = self.actual_pv_num
        out["size_kb"]          = self.size_kb
        out["phy_extent_size"]  = self.phy_extent_size
        out["total_extent_num"] = self.total_extent_num
        out["alloc_extent_num"] = self.alloc_extent_num
        out["free_extent_num"]  = self.free_extent_num
        out["uuid"]             = self.uuid


class LvmLV:
    def __init__(self):
        self.name            = None
        self.vg_name         = None
        self.access          = None
        self.status          = None
        self.inter_num       = None
        self.opened_lv_num   = None
        self.size_sectors    = None
        self.cur_extent_num  = None
        self.alloc_extent_num= None
        self.alloc_policy    = None
        self.read_ah_sectors = None
        self.major           = None
        self.minor           = None

    def size(self,unit = "GiB"):
        return toolbox.Sectors2Gib(self.size_sectors)

    def format(self,out = {}):
        out["name"]            = self.name
        out["vg_name"]         = self.vg_name
        out["access"]          = self.access
        out["status"]          = self.status
        out["inter_num"]       = self.inter_num
        out["opened_lv_num"]   = self.opened_lv_num
        out["size_sectors"]    = self.size_sectors
        out["cur_extent_num"]  = self.cur_extent_num
        out["alloc_extent_num"]= self.alloc_extent_num
        out["alloc_policy"]    = self.alloc_policy
        out["read_ah_sectors"] = self.read_ah_sectors
        out["major"]           = self.major
        out["minor"]           = self.minor


def Run_cmd(cmd):
    logging.debug("Run command %s" % cmd)
    (status,output,stderr) = CIPMgr.Exec_cmd(cmd)
    logging.info("Run command %s ok" % cmd)
    if status != 0:
        logging.error('Run commands {0} error,{1}'.format(cmd,stderr));
        raise exception.CommitError('Run commands {0} error,{1}'.format(cmd,stderr))

    return (status,output,stderr)

##############################
#          API               #
##############################
"""
"""
def pv_display(pv_name):
    cmd = "pvdisplay -c " + pv_name
    
    (status,output,stderr) = Run_cmd(cmd)

    pv_obj = LvmPV()

    #parse output for pvdisplay
    lines = output.strip().split('\n')
    content_index = 0

    if len(lines) != 1:
        logging.debug("pv:%s is a new physical volume" % pv_name)
        content_index = 1

    content = lines[content_index]
    logging.debug("its content is %s" % content)

    cols = content.strip().split(":")
    #fill all fileds of the pv
    pv_obj.name            = cols[0]
    pv_obj.vg_name         = cols[1]
    pv_obj.size_sectors    = int(cols[2])
    pv_obj.inter_num       = int(cols[3])
    pv_obj.status          = int(cols[4])
    pv_obj.not_alloc       = int(cols[5])
    pv_obj.lv_num          = int(cols[6])
    pv_obj.extent_kb       = int(cols[7])
    pv_obj.total_extents   = int(cols[8])
    pv_obj.free_extents    = int(cols[9])
    pv_obj.alloc_extents   = int(cols[10])
    pv_obj.uuid            = cols[11]

    return pv_obj

"""
    get the list of the pv name
"""
def pv_name_list():
    cmd = "pvs"

    (status,output,stderr) = Run_cmd(cmd)

    lines = output.strip().split("\n")
    if len(lines) <= 1:
        logging.debug("pvs,its content is empty")

    pv_names = []
    for item in range(1,len(lines)):
        pv_names.append(lines[item].strip().split()[0])

    return pv_names

def check_pv_exists(pv_name):
    return pv in pv_name_list()

"""
    get the list of the pv-obj
"""
def pv_list(filter_ = []):
    pvs = []

    for name in pv_name_list():
        if name in filter_:
            continue
        pvs.append(pv_display(name))

    return pvs

"""
    create pv
"""
def pv_create(pv_name):
    cmd = 'pvcreate -ff -y ' + pv_name
    Run_cmd(cmd)

def pvs_create(pv_names):
    for pv in pv_names:
        pv_create(pv)

def pv_remove(pv_name):
    cmd = 'pvremove -ff -y ' + pv_name
    Run_cmd(cmd)

def pvs_remove(pv_names):
    for pv in pv_names:
        pv_remove(pv)

"""
"""
def vg_display(vg_name):
    cmd = "vgdisplay -c " + vg_name

    (status,output,stderr) = Run_cmd(cmd)

    content = output
    #parser content
    vg_obj = LvmVG()

    cols = content.strip().split(":")
    ##file all fileds of the vg_obj

    vg_obj.name             = cols[0]
    vg_obj.access           = cols[1]
    vg_obj.status           = int(cols[2])
    vg_obj.inter_num        = int(cols[3])
    vg_obj.max_lv_num       = int(cols[4])
    vg_obj.cur_lv_num       = int(cols[5])
    vg_obj.opened_lv_num    = int(cols[6])
    vg_obj.max_lv_size      = int(cols[7])
    vg_obj.max_pv_num       = int(cols[8])
    vg_obj.cur_pv_num       = int(cols[9])
    vg_obj.actual_pv_num    = int(cols[10])
    vg_obj.size_kb          = int(cols[11])
    vg_obj.phy_extent_size  = int(cols[12])
    vg_obj.total_extent_num = int(cols[13])
    vg_obj.alloc_extent_num = int(cols[14])
    vg_obj.free_extent_num  = int(cols[15])
    vg_obj.uuid             = cols[16]

    return vg_obj

"""
"""
def vg_name_list():
    cmd = "vgs"

    (status,output,stderr) = Run_cmd(cmd)

    lines = output.strip().split("\n")
    if len(lines) <= 1:
        logging.debug("pvs,its content is empty")

    #parser output
    vg_names = []
    for item in range(1,len(lines)):
        vg_names.append(lines[item].strip().split()[0])

    return vg_names

"""
"""
def check_vg_exists(vg_name):
    return vg_name in vg_name_list()

"""
"""
def vg_list(filter_ = []):
    vgs = []

    for name in vg_name_list():
        if name in filter_:
            continue
        vgs.append(vg_display(name))

    return vgs

def vg_pv_name_list(vg_name):
    cmd = "vgdisplay -v " + vg_name
    
    (status,output,stderr) = Run_cmd(cmd)
    
    content = output
    lines = content.split('\n')
    
    pv_names = []

    for line in lines:
        if line.find('PV Name') >= 0:
            ##parser pv
            pv_names.append(re.findall(r'\w*/dev/\w*',line)[0])

    return pv_names

def n_vg_pv_list(vg_name):
    pv_objs = []

    for pv in vg_pv_name_list(vg_name):
        pv_objs.append(pv_display(pv))

    return pv_objs

def vg_pv_list(vg_name,pv_objs):
    ret = []
    for obj in pv_objs:
        if obj.vg_name and obj.vg_name == vg_name:
            ret.append(obj)
    return ret

def vg_lv_name_list(vg_name):
    cmd = "vgdisplay -v " + vg_name
    
    (status,output,stderr) = Run_cmd(cmd)
    
    content = output
    lines = content.split('\n')
    
    lv_names = []
    for line in lines:
        if line.find('LV Path') >= 0:
            ##parser pv
            lv_names.append(re.findall(r'\w*/dev/\w*/\w*',line)[0].split('/')[3])

    return lv_names

def vg_remove_check(vg_name):
    if len(vg_lv_name_list(vg_name)) > 0:
        return False
    else:
        return True


def vg_lv_gname_list(vg_name):
    ret = []

    for lv in vg_lv_name_list(vg_name):
        ret.append('/dev/' + vg_name + '/' + lv)

    return ret

def vg_lv_list(vg_name,lv_objs):
    ret = []
    for obj in lv_objs:
        if obj.vg_name and obj.vg_name == vg_name:
            ret.append(obj)
    return ret

def n_vg_lv_list(vg_name):
    lv_objs = []
    for lv in vg_lv_name_list(vg_name):
        lv_objs.append(lv_display(vg_name + '/' + lv))
    return lv_objs

"""
"""
def vg_create(name,devices):
    ##create pv
    pvs_create(devices)

    cmd = 'vgcreate -f ' + name
    sub_cmd = ""

    for pv in devices:
        sub_cmd = sub_cmd + ' ' + pv

    cmd = cmd + sub_cmd

    (status,output,stderr) = Run_cmd(cmd)

def vg_remove_cover(vg_name):
    cmd = 'vgremove -f ' + vg_name

    (status,output,stderr) = Run_cmd(cmd)

def vg_remove_crashing(vg_name):
    pvs = vg_pv_name_list(vg_name)
    
    vg_remove_cover(vg_name)

    pvs_remove(pvs)

"""
"""
def vg_add_pv(vg_name,pvs):
    cmd = 'vgextend ' + vg_name

    sub_cmd = ""
    for pv in pvs:
        sub_cmd = sub_cmd + ' ' + pv
    
    cmd = cmd + sub_cmd

    Run_cmd(cmd)

"""
"""
def vg_del_pv_crashing(vg_name,pv_names):
    cmd = 'vgreduce ' + vg_name

    sub_cmd = ""
    for pv in pv_names:
        sub_cmd = sub_cmd + ' ' + pv

    cmd = cmd + sub_cmd

    Run_cmd(cmd)

"""
    @param local_lv_path vg_name/lv_name
    @return LvmLV
"""
def lv_display(local_lv_path):
    cmd = 'lvdisplay -c ' + local_lv_path
    (status,output,stderr) = Run_cmd(cmd)
    
    lv_obj = LvmLV()
    content = output
    #parser content
    cols = content.strip().split(":")
    lv_obj.name            = cols[0].split('/')[3]
    lv_obj.vg_name         = cols[1]
    lv_obj.access          = cols[2]
    lv_obj.status          = int(cols[3])
    lv_obj.inter_num       = int(cols[4])
    lv_obj.opened_lv_num   = int(cols[5])
    lv_obj.size_sectors    = int(cols[6])
    lv_obj.cur_extent_num  = int(cols[7])
    lv_obj.alloc_extent_num= int(cols[8])
    lv_obj.alloc_policy    = int(cols[9])
    lv_obj.read_ah_sectors = int(cols[10])
    lv_obj.major           = int(cols[11])
    lv_obj.minor           = int(cols[12])

    return lv_obj

"""
"""
def lv_local_path_list():
    cmd = 'lvs'
    (status,output,stderr) = Run_cmd(cmd)
    lines = output.strip().split('\n')

    if len(lines) <= 1:
        logging.debug("lvs,its content is empty")

    lv_local_paths = []
    for item in range(1,len(lines)):
        temp = lines[item].strip().split()
        lv_local_paths.append(temp[1] + '/' + temp[0])

    return lv_local_paths

"""
"""
def check_lv_exists(lv_name,vg_name):
    return (vg_name + "/" + lv_name) in lv_local_path_list() 

"""
"""
def lv_list(filter_ = []):
    lvs = []

    for local_path in lv_local_path_list():
        if local_path in filter_:
            continue
        lvs.append(lv_display(local_path))

    return lvs

def lv_list_for_pv(pv_name):
    ret = []
    lv_names = None
    vg_name = None

    try:
        pv_obj = pv_display(pv_name)
    except:
        return None

    if pv_obj.vg_name:
        vg_name = pv_obj.vg_name
    else:
        return None

    try:
        lv_names = vg_lv_name_list(vg_name)
        for i in lv_names:
            ret.append('/dev/' + vg_name + '/' + i)
    except:
        return None

    return ret

def lv_activate(lv_path):
    cmd = 'lvchange -ay ' + lv_path
    Run_cmd(cmd)

def lv_deactivate(lv_path):
    cmd = 'lvchange -an ' + lv_path
    Run_cmd(cmd)

"""
"""
def lv_linear_create(vg_name,lv_name,lv_size,size_unit):
    cmd = 'lvcreate -Z y -L ' + str(lv_size) + size_unit + ' -n ' + lv_name + ' ' + vg_name
    Run_cmd(cmd)

"""
"""
def lv_remove(vg_name,lv_name):
    cmd = 'lvremove -f ' + vg_name + '/' + lv_name
    Run_cmd(cmd)

"""
    private
    @param direct the direct of changing the lv,+,-
"""
def lv_change(vg_name,lv_name,ex_size,unit,direct):
    cmd = 'lvextend -f -L ' + direct + str(ex_size) + unit + ' ' + vg_name + '/' + lv_name
    Run_cmd(cmd)

"""
"""
def lv_extend(vg_name,lv_name,ex_size,unit = "M"):
    lv_change(vg_name,lv_name,ex_size,unit,'+')

"""
"""
def lv_reduce(vg_name,lv_name,ex_size,unit = "M"):
    lv_change(vg_name,lv_name,ex_size,unit,'-')
