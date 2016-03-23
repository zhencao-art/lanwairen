# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import lvm2py
import os,sys,logging
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
import CIPMgr
import exception
##import blkid

"""
"""
def cleanup_lvm_lovk():
    cmd = "rm -f /var/run/lock/lvm/*"
    CIPMgr.Exec_cmd(cmd)

"""
"""
def create_linear_vol(vg_name,lv_name,lv_size,size_unit):
    #if not self.check_vg_exists(vg_name):
    #    raise exception.HandleError("vg %s is not found" % vg_name)
    #logging.debug("FOR DEBUG.....120")
    #try:
    #    vg = self.check_vg_exists(vg_name)
    #except:
    #    raise exception.HandleError("vg %s is not found" % vg_name)
    #logging.debug("FOR DEBUG.....124")

    #if self.check_lv_exists(vg_name,lv_name):
    #    raise exception.HandleError("{0} is exist in {1}".format(lv_name,vg_name))
    cleanup_lvm_lovk()
    logging.debug("create {0}/{1}".format(vg_name,lv_name))
    #vg.create_lv(lv_name,lv_size,size_unit)
    cmd = 'lvcreate -Z y -L ' + str(lv_size) + size_unit + ' -n ' + lv_name + ' ' + vg_name
    logging.info("Run command %s ing" % cmd)
    #(status,output) = commands.getstatusoutput(cmd)
    (status,output,error) = CIPMgr.Exec_cmd(cmd)
    logging.info("Run command %s ok" % cmd)
    if 0 != status:
        raise exception.CommitError("Run command {0} error,{1}".format(cmd,error))

"""
"""
def remove_lv(vg_name,lv_name):
    ##try:
    ##    vg = self.get_vg(vg_name,"w")
    ##except:
    ##    raise exception.HandleError("vg %s is not found" % vg_name)

    ##try:
    ##    lv = vg.get_lv(lv_name)
    ##except:
    ##    raise exception.handleError("lv %s is not found" % lv_name)

    #if not self.check_lv_exists(vg_name,lv_name):
    #   raise exception.HandleError("{0} is not found in {1}".format(lv_name,vg_name))
    ##vg.remove_lv(lv)
    logging.debug("remove {0}/{1}".format(vg_name,lv_name))
    #vg.create_lv(lv_name,lv_size,size_unit)
    cmd = 'lvremove -f ' + vg_name + '/' + lv_name
    logging.info("Run command %s ing" % cmd)
    (status,output,stderr) = CIPMgr.Exec_cmd(cmd)
    logging.info("Run command %s ok" % cmd)
    if 0 != status:
        raise exception.CommitError("Run command {0} error,{1}".format(cmd,stderr))

class CLVMEx(lvm2py.LVM):
    @staticmethod
    def lvm_util_installed(util):
        util_path = '/usr/sbin/' + util
        if os.path.exists(util_path):
            return True
        return False

    def pv_create(self,pv_name):
        if not os.path.exists(pv_name):
            raise exception.HandleError("%s is not found" % pv_name)
        if not CLVMEx.lvm_util_installed('pvcreate'):
            raise exception.HandleError("%s is not installed" % 'pvcreate')
        pv_cmd = 'pvcreate -ff -y ' + pv_name
        logging.debug("Run cmd %s" % pv_cmd)
        (status,output,stderr) = CIPMgr.Exec_cmd(pv_cmd)
        if status != 0:
            raise exception.CommitError("Run cmd {0} error,{1}".format(pv_cmd,stderr))

    def pvs_create(self,pv_names):
        for pv in pv_names:
            self.pv_create(pv)

    def pv_remove(self,pv_name):
        if not os.path.exists(pv_name):
            raise exception.HandleError("%s is not found" % pv_name)
        if not CLVMEx.lvm_util_installed('pvremove'):
            raise exception.HandleError("%s is not installed" % 'pvremove')

        pv_cmd = 'pvremove -ff -y ' + pv_name
        logging.debug("Run cmd %s" % pv_cmd)
        (status,output,stderr) = CIPMgr.Exec_cmd(pv_cmd)

        if status != 0:
            raise exception.Commit("pv_remove fialed %s" % stderr)

    def pvs_remove(self,pv_names):
        for pv in pv_names:
            self.pv_remove(pv)

    #private
    def check_vg_exists(self,vg_name):
        vgs = self.vgscan()
        for vg in vgs:
            if vg.name == vg_name:
                return True
        return False
    #private
    def check_lv_exists(self,vg_name,lv_name):
        try:
            vg = self.get_vg(vg_name)
            for lv in vg.lvscan():
                if lv.name == lv_name:
                    return True
            return False
        except:
            return False

    #overwirte
    def create_vg(self,name,devices):
        if self.check_vg_exists(name):
            raise exception.HandleError("vg %s already exists" % name)

        if not CLVMEx.lvm_util_installed('vgcreate'):
            raise exception.HandleError("vgcreate is not installed")

        ##pvcreate
        self.pvs_create(devices)

        vg_cmd = 'vgcreate -f ' + name + ' '
        for pv in devices:
            vg_cmd = vg_cmd + pv + ' '

        (status,output,stderr) = CIPMgr.Exec_cmd(vg_cmd)
        if status != 0:
            raise exception.CommitError('vgcreate failed %s' % stderr)

    def remove_vg_cover(self,vg_name):
        if not self.check_vg_exists(vg_name):
            raise exception.HandleError("vg %s is not found" % vg_name)

        if not CLVMEx.lvm_util_installed('vgremove'):
            raise exception.HandleError("vgremove is not installed")

        vgrm_cmd = 'vgremove ' + vg_name
        (status,output,stderr) = CIPMgr.Exec_cmd(vgrm_cmd)
        if status != 0:
            raise exception.CommitError('vgcreate failed %s' % stderr)

    def pv_scan_vg(self,vg_name):
        pvs = []
        vg = self.get_vg(vg_name,'r')
        
        for pv in vg.pvscan():
            pvs.append(pv.name)

        return pvs
    
    def remove_vg_crashing(self,vg_name):
        if not self.check_vg_exists(vg_name):
            raise exception.HandleError("vg %s is not found" % vg_name)

        if not CLVMEx.lvm_util_installed('vgremove'):
            raise exception.HandleError("vgremove is not installed")

        pvs = self.pv_scan_vg(vg_name)

        self.remove_vg_cover(vg_name)
        
        self.pvs_remove(pvs)

    """
    """
    def add_pv_for_vg(self,vg_name,pvs):
        if not os.path.exists('/usr/sbin/vgextend'):
            raise exception.HandleError("vgextend is not found")

        vg_extend = 'vgextend ' + vg_name + ' '

        for pv in pvs:
            vg_extend = vg_extend + pv + ' '
        logging.debug("Run command %s" % vg_extend)
        (status,output,stderr) = CIPMgr.Exec_cmd(vg_extend)
        if status != 0:
            raise exception.CommitError('vgextend failed %s' % stderr)

    """
    """
    def del_pv_for_vg_crashing(self,vg_name,pv_name):
        vg_reduce = 'vgreduce vg_name ' + pv_name

        (status,output,stderr) = CIPMgr.Exec_cmd(vg_reduce)

        if status != 0:
            raise exception.CommitError('pvremove failed %s' % stderr)

    """
    """
    def create_linear_vol(self,vg_name,lv_name,lv_size,size_unit):
        #if not self.check_vg_exists(vg_name):
        #    raise exception.HandleError("vg %s is not found" % vg_name)
        #logging.debug("FOR DEBUG.....120")
        #try:
        #    vg = self.check_vg_exists(vg_name)
        #except:
        #    raise exception.HandleError("vg %s is not found" % vg_name)
        #logging.debug("FOR DEBUG.....124")

        #if self.check_lv_exists(vg_name,lv_name):
        #    raise exception.HandleError("{0} is exist in {1}".format(lv_name,vg_name))
        logging.debug("create {0}/{1}".format(vg_name,lv_name))
        #vg.create_lv(lv_name,lv_size,size_unit)
        cmd = 'lvcreate -Z y -L ' + str(lv_size) + size_unit + ' -n ' + lv_name + ' ' + vg_name
        logging.info("Run command %s ing" % cmd)
        #(status,output) = commands.getstatusoutput(cmd)
        (status,output,error) = CIPMgr.Exec_cmd(cmd)
        logging.info("Run command %s ok" % cmd)
        if 0 != status:
            raise exception.CommitError("Run command {0} error,{1}".format(cmd,error))

    """
    """
    def remove_lv(self,vg_name,lv_name):
        ##try:
        ##    vg = self.get_vg(vg_name,"w")
        ##except:
        ##    raise exception.HandleError("vg %s is not found" % vg_name)

        ##try:
        ##    lv = vg.get_lv(lv_name)
        ##except:
        ##    raise exception.handleError("lv %s is not found" % lv_name)

        if not self.check_lv_exists(vg_name,lv_name):
            raise exception.HandleError("{0} is not found in {1}".format(lv_name,vg_name))
        ##vg.remove_lv(lv)
        logging.debug("remove {0}/{1}".format(vg_name,lv_name))
        #vg.create_lv(lv_name,lv_size,size_unit)
        cmd = 'lvremove -f ' + vg_name + '/' + lv_name
        logging.info("Run command %s ing" % cmd)
        (status,output,stderr) = CIPMgr.Exec_cmd(cmd)
        logging.info("Run command %s ok" % cmd)
        if 0 != status:
            raise exception.CommitError("Run command {0} error,{1}".format(cmd,stderr))

    """
    """
    def scan_lv(self,vg_name):
        if not self.check_vg_exists(vg_name):
            raise exception.HandleError("vg %s is not found" % vg_name)
        vg = self.get_vg(vg_name)
        return vg.lvscan()

    """
        private
        @param direct the direct of changing the lv,+,-
    """
    def change_lv(self,vg_name,lv_name,ex_size,unit,direct):
        if not os.path.exists('/usr/sbin/lvextend'):
            raise exception.HandleError("lvextend is not installed")
        if not os.path.exists('/dev/' + vg_name + '/' + lv_name):
            raise exception.HandleError('the logical volume {0}/{1} is not found'.format(vg_name,lv_name))

        extend_cmd = 'lvextend -f -L ' + direct + str(ex_size) + unit + ' ' + vg_name + '/' + lv_name
        (status,output,stderr) = CIPMgr.Exec_cmd(extend_cmd)
        if 0 != status:
            raise exception.CommitError('run cmd {1} error,{2}'.format(extend_cmd,stderr))

    """
    """
    def extend_lv(self,vg_name,lv_name,ex_size,unit = "M"):
        self.change_lv(vg_name,lv_name,ex_size,unit,'+')

    """
    """
    def reduce_lv(self,vg_name,lv_name,ex_size,unit = "M"):
        self.change_lv(vg_name,lv_name,ex_size,unit,'-')


#import pdb
#pdb.set_trace()
#lvm = CLVMEx()
#
#lvm.create_vg('kk',['/dev/sdd','/dev/sdc'])
#lvm.remove_vg_crashing('kk')
