# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import logging
from deltavsoft.rcfproto import *

import sys,os,commands,socket,thread,subprocess
sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../cluster")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
import globalvar
sys.path.append(os.path.abspath(os.path.join(__file__,"../../mid")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../mon")))
import block_mgr,construct_destruct,database
import n_blockmgr
import md_event
import db_sync
sys.path.append(os.path.abspath(os.path.join(__file__,"../../db")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../storage")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../time")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../time/ntp-conf")))
import n_raidmgr,n_lvmmgr,CConfigMgr,CIPMgr,ntp ,CDateTime,ntp_setup,n_phydisk
from clustermgr import CClusterMgr
import CResourceFactory
import puma_pb2
import threading

class CServiceImpl(puma_pb2.RpcService):
    def __init__(self):
        self.cluster_commit_lock = thread.allocate_lock()
        #self.g_lvm_lock = threading.Lock()
        CIPMgr.InitIfcfg()

    #private
    def get_peer_ip(self):
        #return "172.16.9.241"
        #nodelist = CResourceFactory.GetNode()
        nodelist = CIPMgr.get_corosync_node()
        iplist = CIPMgr.GetIp(False)
        ipl = []
        for ip in iplist:
            if CIPMgr.IsIp(nodelist[0]):
                ipl.append(ip.get('ip'))
            else:
                ipl.append(ip.get('host'))
        for node in nodelist:
            if node not in ipl:
                return node
        raise Exception('can not get peer ip')

    def get_used_ip(self,controller,request,done):
        try:
            response = puma_pb2.GetIpRes()
            cmd = 'ip addr'
            (rtn,out,err) = self.Exec_cmd(cmd)
            if rtn!=0 :
                raise Exception(err)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'get local ip info success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = out
        done(response)
        return True

    #private
    def create_rpc_client_handle(self):
        try:
            peer_ip = CIPMgr.get_peer_ip()
            logging.debug(peer_ip)
            client_handle = client.CClient(peer_ip,globalvar.listen_port)
        except Exception,e:
            logging.error("Can not get the ip of the remote node, %s" % str(e))
            raise Exception("Can not get the ip of the remote node")

        return client_handle

    #private
    def create_self_rpc_client_handle(self):
        return client.CClient('127.0.0.1',globalvar.listen_port)

    #private
    def create_db_handle(self):
        client_handle = self.create_rpc_client_handle()
        return CConfigMgr.CConfigMgr(client_handle,globalvar.db_path,True)

    def create_db_local_handle(self):
        return CConfigMgr.CConfigMgr(None,globalvar.db_path,True)

    def db_file_sync(self,controller,request,done):
        response = puma_pb2.DBFileSyncRes()
        db_sync.db_sync_request(request.content)
        response.ret.retcode = 0
        done(response)

    
    def init_phy_disk(self,controller,request,done):
        response = puma_pb2.ListPhyDiskClusterRes()
        (ret,msg) = n_blockmgr.block_disk_init(request.dev_name)

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            response.ret.retcode = ret
            response.ret.msg = msg
            logging.error("CServiceImpl::init_phy_disk error %s" % msg)
        else:
            logging.info("CServiceImpl::init_phy_disk ok")
            response.ret.retcode = 0
        done(response)

    """
    """
    def cluster_list_phy_disk(self,controller,request,done):
        response = puma_pb2.ListPhyDiskClusterRes()

        (ret,phydisk_objs) = n_blockmgr.block_disk_list()

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            response.ret.retcode = ret
            msg = phy_disk_objs
            response.ret.msg = msg
            logging.error("CServiceImpl::cluster_list_phy_disk error %s" % msg)
            done(response)
            return
        if phydisk_objs:
            for obj in phydisk_objs:
                m_disk_obj = response.disks.add()
                m_disk_obj.online = obj.online
                m_disk_obj.inited = obj.inited
                if obj.user:
                    m_disk_obj.dev_used = True
                    m_disk_obj.dev_user = obj.user
                else:
                    m_disk_obj.dev_used = False
                if obj.info:
                    m_disk_obj.dev_name  = obj.info.name
                    m_disk_obj.dev_size  = obj.info.size
                    m_disk_obj.dev_wwn   = obj.info.wwn
                    m_disk_obj.dev_slot  = obj.info.slot
                    m_disk_obj.protocol  = obj.info.protocol
                    m_disk_obj.rotational = obj.info.rotational
                else:
                    m_disk_obj.dev_size  = obj.config.size
                    m_disk_obj.dev_wwn   = obj.config.name
                    m_disk_obj.dev_slot  = obj.config.slot
                    m_disk_obj.protocol  = obj.config.protocol
                    m_disk_obj.rotational = obj.config.rotational

        logging.info("CServiceImpl::cluster_list_phy_disk")
        response.ret.retcode = 0
        done(response)

    def get_backboard_info(self,controller,request,done):
        response = puma_pb2.GetBackBoardInfoRes()
        ##FIX ME
        response.backboard_info.slot_num = 24;

        logging.info("CServiceImpl::get_backboard_info")
        response.ret.retcode = 0
        done(response)

    """
        create raid device
    """
    def create_md_device(self,controller,request,done):
        response = puma_pb2.MdCreateRes()
        #check if the request is vailed
        if request.md_level != 1:
            if not request.HasField("md_chunk"):
                logging.error("CServiceImpl::create_md_device,\
                        request is not vaild")
                response.ret.retcode = -1
                response.ret.msg = "request missing md_chunk field"
                done(response)
                return
        res_handle = CClusterMgr.CClusterMgr()
        md_phy_devices = []
        for x in request.md_phy_devices:
            md_phy_devices.append(x.dev.dev_name)
        (ret,msg) = n_blockmgr.block_create_raid(res_handle,request.md_name,request.md_level,md_phy_devices,request.md_chunk)

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            response.ret.retcode = ret
            response.ret.msg = msg
            logging.error("CServiceImpl::create_md_device {0} error {1}".format(request.md_name,msg))
        else:
            logging.info("CServiceImpl::create_md_device %s success" % request.md_name)
            response.ret.retcode = 0
        done(response)

    """
        remove raid device
    """
    def remove_md_device(self,controller,request,done):
        response = puma_pb2.MdRemoveRes()
        res_handle = CClusterMgr.CClusterMgr()

        (ret,msg) = n_blockmgr.block_remove_raid(res_handle,request.md_name)
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            response.ret.msg = msg
            response.ret.retcode = ret
            logging.error("CServiceImpl::remove_md_device {0} error {1}".format(request.md_name,msg))
        else:
            logging.info("CServiceImpl::remove_md_device %s" % request.md_name)
            response.ret.retcode = 0
        done(response)

    """
    def assemble_md_device(self,controller,request,done):
        response = puma_pb2.MdAssembleRes()
        try:
            md_phy_devices = []
            for x in request.md_phy_devices:
                md_phy_devices.append(x.dev_name)

            if request.HasField("md_name"):
                self.raid_mgr.assemble_md(request.md_name,md_phy_devices)
            else:
                self.raid_mgr.assemble_scan()
        except Exception,e:
            logging.error("CServiceImpl::assemble_md_device,%s" % str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return
        
        logging.info("CServiceImpl::assemble_md_device")
        response.ret.retcode = 0
        done(response)
    """

    """
        scan all the raid devices of the localhost
    """
    def scan_md_device(self,controller,request,done):
        response = puma_pb2.MdScanRes()
        (ret,msg) = n_blockmgr.block_list_raid()
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::scan_md_device failed %s" % msg)
            response.ret.msg = msg
            response.ret.retcode = ret
        else:
            if msg:
                for i in msg:
                    msg_md_device = response.md_devices.add()
                    msg_md_device.dev_name = '/dev/' + i.config.name
                    msg_md_device.online = i.online
                    if i.user:
                        msg_md_device.dev_used = True
                        msg_md_device.dev_user = i.user
                    else:
                        msg_md_device.dev_used = False
                    msg_md_device.dev_size = i.config.size
                    msg_md_device.dev_level = i.config.level
                    msg_md_device.dev_chunk = i.config.chunk
                    for phy_device in i.config.disks:
                        msg_phy_devices = msg_md_device.dev_phy_devices.add()
                        msg_phy_devices.dev.dev_name = phy_device
                    
        logging.info("CServiceImpl::scan_md_device ok")
        response.ret.retcode = 0
        done(response)

    """
        md event report
    """
    def mdmon_event_report(self,controller,request,done):
        response = puma_pb2.MdMonEventReportRes()
        logging.info('Get Md Event {0}-{1}'.format(request.event_target,request.event_msg))
        #### md event deal
        md_event.md_event_dispatch(request.event_target,request.event_msg)

        response.ret.retcode = 0
        done(response)

    """
        step 1: move all the relate resource
        step 2: stop the md
    """
    def md_rebuild_start_pre(self,controller,request,done):
        response = puma_pb2.MdRebuildStartPreRes()

        (ret,msg) = md_event.md_rebuild_start_pre(request.md_name,request.relate_lvs)
        if ret != md_event.MdEventError.SUCCESS:
            response.ret.msg = msg
            response.ret.retcode = ret
            logging.error("CServiceImpl::md_rebuild_start_pre {0} error {1}".format(request.md_name,msg))
        else:
            logging.info("CServiceImpl::md_rebuild_start_pre %s" % request.md_name)
            response.ret.retcode = 0
        done(response)

    """
        step 1: Assmble the md
        step 2: vgs and lvs
        step 3: pcs resource cleanup(rebalance all resource)
    """
    def md_rebuild_finished(self,controller,request,done):
        response = puma_pb2.MdRebuildFinishedRes()
        (ret,msg) = md_event.md_rebuild_finished(request.md_name)
        if ret != md_event.MdEventError.SUCCESS:
            response.ret.msg = msg
            response.ret.retcode = ret
            logging.error("CServiceImpl::md_rebuild_finished {0} error {1}".format(request.md_name,msg))
        else:
            logging.info("CServiceImpl::md_rebuild_finished %s" % request.md_name)
            response.ret.retcode = 0
        done(response)

    """
        scan all the physical device used by the md device
    """
    def md_phy_device_scan(self,controller,request,done):
        response = puma_pb2.MdPhyDeviceScanRes()
        try:
            ##NOW NOT SUPPORT
            ##ADD CODE HERE
            pass
        except Exception,e:
            logging.error("CServiceImpl::md_phy_device_scan %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::md_phy_device_scan")
        response.ret.retcode = 0
        done(response)

    """
        del the physical device used by the md_device
    """
    def md_phy_device_del(self,controller,request,done):
        response = puma_pb2.MdPhyDeviceDelRes()
        try:
            ##NOW NOT SUPPORT
            ##ADD CODE HERE
            request = puma_pb2.MdPhyDeviceDelReq()
        except Exception,e:
            logging.error("CServiceImpl::md_phy_device_del %s" % str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::md_phy_device_del")
        response.ret.retcode = 0
        done(response)

    """
        create volume group
    """
    def create_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGCreateRes()
        
        pv_devices = []
        for device in request.vg_pvs:
            pv_devices.append(device.pv_name)
        (ret,msg) = n_blockmgr.block_create_vg(request.vg_name,pv_devices)

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::create_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        logging.info("CServiceImpl::create_lvm_vg %s" % request.vg_name)
        response.ret.retcode = 0
        done(response)

    """
        remove volume group
    """
    def remove_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGRemoveRes()

        (ret,msg) = n_blockmgr.block_remove_vg(request.vg_name)
        
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::remove_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return
        #try:
        #    db_handle = self.create_db_handle()
        #    if request.crashing:
        #        block_mgr.vg_remove_crashing(db_handle,request.vg_name)
        #    else:
        #        block_mgr.vg_remove(db_handle,request.vg_name)

        #except Exception,e:
        #    logging.error("CServiceImpl::remove_lvm_vg %s" % str(e))
        #    response.ret.retcode = -1;
        #    response.ret.msg = str(e)
        #    done(response)
        #    return

        logging.info("CServiceImpl::remove_lvm_vg %s" % request.vg_name)
        response.ret.retcode = 0
        done(response)

    """
        scan volume group
        if the request specify cluster,it will return the shared vgs,
        otherwise localhost vgs
    """
    def scan_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGScanRes()
        (ret,vg_objs) = n_blockmgr.block_list_vg()

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::remove_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = str(e)
            done(response)
            return

        if not vg_objs:
            logging.info("CServiceImpl::scan_lvm_vg ok,but is's none")
            response.ret.retcode = 0
            done(response)
            return

        for vg in vg_objs:
            m_vg = response.vgs.add()

            m_vg.online = vg.online
            m_vg.vg_name = vg.config.name
            m_vg.vg_total_size = vg.config.size

            for pv in vg.config.raids:
                m_pv = m_vg.vg_md_pvs.add()
                m_pv.pv_name = '/dev/' + pv
            if vg.online:
                m_vg.vg_free_size = vg.info.free_size()

        logging.info("CServiceImpl::scan_lvm_vg ok")
        response.ret.retcode = 0
        logging.info(str(response))
        done(response)

    """
        find volume group
        if the request specify cluster,it will return the shared vgs,
        otherwise localhost vgs
    """
    def find_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGFindRes()
        (ret,vg_obj) = n_blockmgr.block_info_vg(request.vg_name)
    
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            msg = vg_obj
            logging.error("CServiceImpl::find_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        m_vg = response.vg
        m_vg.online = vg_obj.online
        m_vg.vg_name = vg_obj.config.name
        (ret,pv_objs) = n_blockmgr.block_pv_list()
        (ret,lv_objs) = n_blockmgr.block_lv_list()

        if vg_obj.online:
            self.fill_vg_info(m_vg,vg_obj.info)
            (ret,pvs) = n_blockmgr.block_list_vg_pv(vg_obj.config.name,pv_objs)
            self.fill_vg_pv_info(m_vg,pvs)
            
            (ret,lvs) = n_blockmgr.block_list_vg_pv(vg_obj.config.name,lv_objs)
            self.fill_vg_lv_info(m_vg,lvs)
        logging.info("CServiceImpl::find_lvm_vg ok")
        response.ret.retcode = 0
        done(response)

    """
        add physical volume to volume group specified
    """
    def add_pv_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGAddPVRes()

        vg_pvs = []
        for i in request.vg_pvs:
            vg_pvs.append(i.pv_name)
        (ret,msg) = n_blockmgr.block_extend_vg(request.vg_name,vg_pvs)

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::add_pv_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return
        ### add constraint betwween vg and raid-resource
        CClusterMgr.CClusterMgr().SetCons(request.vg_name)

        logging.info("CServiceImpl::add_pv_lvm_vg")
        response.ret.retcode = 0
        done(response)

    """
        del physical volume form volume group
        if request specify crashing flag,it will erase lvm metadata from
        physical volume
    """
    def del_pv_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGDelPVRes()

        vg_pvs = []
        for i in request.vg_pvs:
            vg_pvs.append(i.pv_name)
        (ret,msg) = n_blockmgr.block_reduce_vg(request.vg_name,vg_pvs)

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::del_pv_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return
        ### add constraint betwween vg and raid-resource
        CClusterMgr.CClusterMgr().SetCons(request.vg_name)

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::del_pv_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        logging.info("CServiceImpl::del_pv_lvm_vg")
        response.ret.retcode = 0
        done(response)

    """
        scan the physcial volume of the volume group
    """
    def scan_pv_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGScanPVRes()

        try:
            db_handle = self.create_db_handle()
            """
                Now not use
            """

        except Exception,e:
            logging.error("CServiceImpl::scan_pv_lvm_vg %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::scan_pv_lvm_vg")
        response.ret.retcode = 0
        done(response)

    """
        create a logical volume in the specific volume group
    """
    def create_lv_lvm_vg(self,controller,request,done):
        logging.info("create_lv_lvm_vg")
        response = puma_pb2.LvmVGCreateLVRes()

        res_handle = CClusterMgr.CClusterMgr()
        if request.lv_type == "linear":
            pass
        else:
            msg = "lv type: %s is not supported now"
            logging.error(msg)
            response.ret.retcode = -1
            response.ret.msg = msg
            done(response)
            return

        (ret,msg) = n_blockmgr.block_create_lv(res_handle,request.vg_name,request.lv_name,request.lv_size,request.size_unit)
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::create_lv_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        logging.info("CServiceImpl::create_lv_lvm_vg {0}/{1}".format(request.vg_name,request.lv_name))
        response.ret.retcode = 0
        done(response)

    """
        extend the lv
    """
    def extend_lv_lvm(self,controller,request,done):
        response = puma_pb2.LvmExtendLVRes()
        (ret,msg) = n_blockmgr.block_extend_lv(request.vg_name,request.lv_name,request.lv_size,request.size_unit)
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::extend_lv_lvm %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        logging.info("CServiceImpl::extend_lv_lvm {0}/{1}".format(request.vg_name,request.lv_name))
        response.ret.retcode = 0
        done(response)

    """
        reduce the lv
    """
    def reduce_lv_lvm(self,controller,request,done):
        response = puma_pb2.LvmReduceLVRes()

        (ret,msg) = n_blockmgr.block_reduce_lv(request.vg_name,request.lv_name,request.lv_size,request.size_unit)
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::reduce_lv_lvm %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        logging.info("CServiceImpl::reduce_lv_lvm {0}/{1}".format(request.vg_name,request.lv_name))
        response.ret.retcode = 0
        done(response)

    """
        remove a logical volume form the specific volume group
    """
    def remove_lv_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGRemoveLVRes()
        res_handle = CClusterMgr.CClusterMgr()
        (ret,msg) = n_blockmgr.block_remove_lv(res_handle,request.vg_name,request.lv_name)
        if ret != n_blockmgr.BlockOpError.SUCCESS:
            logging.error("CServiceImpl::remove_lv_lvm_vg %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return

        logging.info("CServiceImpl::remove_lv_lvm_vg {0}/{1}".format(request.vg_name,request.lv_name))
        response.ret.retcode = 0
        done(response)

    """
        scan all logical volumes of the volume group
    """
    def scan_lv_lvm_vg(self,controller,request,done):
        response = puma_pb2.LvmVGScanLVRes()
        try:
            lvs = lvm.scan_lv(request.vg_name)
            for lv in lvs:
                msg_lv = response.lvs.add()
                msg_lv.lv_name = lv.name
                msg_lv.vg_name = request.vg_name
                msg_lv.lv_uuid = lv.uuid
                msg_lv.lv_size = lv.size("GiB")

        except Exception,e:
            logging.error("CServiceImpl::scan_lv_lvm_vg %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::scan_lv_lvm_vg %s" % request.vg_name)
        response.ret.retcode = 0
        done(response)

    """
        scan all the logical volumes created of the system
    """
    def scan_lv_lvm(self,controller,request,done):
        response = puma_pb2.LvmScanLVRes()
        (ret,lv_objs) = n_blockmgr.block_list_lv()

        if ret != n_blockmgr.BlockOpError.SUCCESS:
            msg = lv_objs
            logging.error("CServiceImpl::scan_lv_lvm %s" % msg)
            response.ret.retcode = ret
            response.ret.msg = msg
            done(response)
            return
        if lv_objs:
            for i in lv_objs:
                m_lv = response.lvs.add()
                m_lv.online  = i.online
                m_lv.lv_name = i.config.name
                m_lv.vg_name = i.config.vg_name
                m_lv.lv_size = i.config.size
                if i.user:
                    m_lv.lv_used = True
                    m_lv.lv_user = i.user
                else:
                    m_lv.lv_used = False
        logging.info("CServiceImpl::scan_lv_lvm ok")
        response.ret.retcode = 0
        logging.debug(str(response))
        done(response)

    def mdadm_config_set(self,controller,request,done):
        response = puma_pb2.MdadmConfigSetRes()
        try:
            n_raidmgr.mdadm_config_set(request.home_host,request.device)
        except Exception,e:
            logging.error("CServiceImpl::mdadm_config_set %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::mdadm_config_set")
        response.ret.retcode = 0
        done(response)

    def Exec_cmd(self,args):
        try:
            cmd = args.split()
            proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            stdout,stderr = proc.communicate()
            ret = proc.returncode
            return ret,stdout,stderr
        except Exception as e:
            raise e

    """
        check locahost name
        @param hostname,the hostname will be checked
        @return if hostname is localhost,true
    """
    #private
    def JudgeHost(self,hostname):
        try:
            hostname += '/'
            #(rtn,out) = commands.getstatusoutput('ip addr |grep ' + hostname)
            rtn,out,err = self.Exec_cmd('ip addr')
            if rtn!=0 :
                return False
            if hostname in out:
                return True
            return False
        except Exception as e:
            raise e
    #private
    def JudgeIP(self,iplist):
        def get_bin(ip):
            result = ''
            numlist = ip.split('.')
            for num in numlist:
                bip = bin(int(num))
                bip = bip.replace('0b','')
                i = 8 - len(bip)
                while(i>0):
                    bip = '0' + bip
                    i -= 1
                result += bip
            return result
        def get_mask(ip):
            ipf = ip + '/'
            (rtn,out,err) = self.Exec_cmd('ip addr')
            if ipf not in out:
                cli = client.CClient(str(ip),globalvar.listen_port)
                req = puma_pb2.GetIpReq()
                cli.stub().get_used_ip(None,req,None)
                res = cli.get_response()
                if res.ret.retcode != 0:
                    raise Exception(res.ret.msg)
                out = res.ret.msg
            begin = out.find(ipf)
            if begin == -1:
                raise Exception('ip[%s] not exist')
            begin = begin + len(ipf)
            end = out.find(' ',begin)
            return out[begin:end]
        def transform(mask):
            mask_d = int(mask)
            count = 0;ret = ''
            while(count < 4):
                if mask_d >= 8:
                    ret += str(255)
                elif mask_d > 0:
                    v =0;n = 8;m= mask_d
                    while(m>0):
                        v += 2**(n-m)
                        m -= 1
                    ret += str(v)
                else:
                    ret += str(0)
                if count !=3:
                    ret += '.'
                count +=1
                mask_d -= 8
            return ret
        result = []
        for ip in iplist:
            d = {}
            #bip = get_bin(ip)
            nmask = get_mask(ip)
            d['mask'] = nmask
            d['net_mask'] = transform(nmask)
            d['bip'] = ip
            result.append(d)
        n1 = result[0]; n2 = result[1]
        if n1.get('mask') != n2.get('mask'):
           raise Exception('ip[%s] has different netmask'%' '.join(iplist))
        from IPy import IP
        sub1 = IP(n1.get('bip')).make_net(n1.get('net_mask'))
        sub2 = IP(n2.get('bip')).make_net(n2.get('net_mask'))
        if sub1 != sub2:
            raise Exception('heartbeat address[%s] not in one subnet'%' '.join(iplist))

    def start_coro_and_pamk(self,controller,request,done):
        try:
            nodelist = request.cNodelist.split(' ')
            response = puma_pb2.ClusterInitRes()
            cluster = CClusterMgr.CClusterMgr(True)
            rtn = cluster.InitService()
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'start corosync and pacemaker service success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def passwd_cluster(self,controller,request,done):
        try:
            nodelist = request.cNodelist.split(' ')
            response = puma_pb2.ClusterInitRes()
            cluster = CClusterMgr.CClusterMgr(True)
            rtn = cluster.Passwd(nodelist,request.cPasswd,request.clusterName)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'set cluster passwd success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def auth_cluster(self,controller,request,done):
        try:
            nodelist = request.cNodelist.split(' ')
            response = puma_pb2.ClusterInitRes()
            cluster = CClusterMgr.CClusterMgr(True)
            rtn = cluster.Auth(nodelist,request.cPasswd,request.clusterName)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'auth cluster success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def setup_cluster(self,controller,request,done):
        try:
            nodelist = request.cNodelist.split(' ')
            response = puma_pb2.ClusterInitRes()
            cluster = CClusterMgr.CClusterMgr(True)
            rtn = cluster.Setup(nodelist,request.cPasswd,request.clusterName)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'setup cluster success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def init_cluster(self,controller,request,done):
        try:
            cluster = CClusterMgr.CClusterMgr(True)
            nodelist = request.cNodelist.split(' ')
            for node in request.cNode:
                if self.JudgeHost(node.ip) == True:
                    local = node.ip
                else:
                    remote = node.ip
            iplist = [local,remote]
            CIPMgr.JudgeSubnet2(local,None,remote,None)
            #self.JudgeIP(iplist)
            cli = client.CClient(str(remote),globalvar.listen_port)
            stub = cli.stub()
            rtn = cluster.Passwd(nodelist,request.cPasswd,request.clusterName)
            if not rtn:
                raise Exception('passwd set failed')
            logging.info('set cluster passwd success')
            stub.passwd_cluster(None,request,None)
            response = cli.get_response()
            if response.ret.retcode != 0:
                raise Exception(response.ret.msg)

            rtn = cluster.Auth(nodelist,request.cPasswd,request.clusterName)
            if not rtn:
                raise Exception('auth cluster failed')
            logging.info('auth cluster success')
            stub.auth_cluster(None,request,None)
            response = cli.get_response()
            if response.ret.retcode != 0:
                raise Exception(response.ret.msg)
                    
            rtn = cluster.Setup(nodelist,request.cPasswd,request.clusterName)
            if not rtn:
                raise Exception('setup cluster failed')
            cluster.Start()
            cluster.InitPropety()
            block_mgr.cluster_mdadm_config_set(cli,stub,request.clusterName)
            logging.info('setup cluster  success')
        except Exception as e:
            logging.error(str(e))
            response = puma_pb2.ClusterInitRes()
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'init cluster success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True
    
    def add_heartbeat_ip(self,controller,request,done):
        try:
            response = puma_pb2.SetIpRes()
            ip = request.ipOpt
            hb_ip = ip.ip
            mask = None
            if ip.HasField('cidr_netmask'):
                mask = ip.cidr_netmask
            CIPMgr.SetIP(hb_ip,'heartbeat',mask,None)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'ip manage success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def add_ip(self,controller,request,done):
        try:
            response = puma_pb2.SetIpRes()
            if request.node != 'local' and request.node != '' and not CIPMgr.CheckIp(request.node):
                cli = client.CClient(str(request.node),globalvar.listen_port)
                stub = cli.stub()
                request.node = 'local'
                stub.add_ip(None,request,None)
                resp = cli.get_response()
                done(resp)
                return True
            opt = {}
            ip = request.ipOpt
            opt['ip'] = ip.ip
            if ip.HasField('nic'):
                opt['nic'] = ip.nic
            if ip.HasField('cidr_netmask'):
                opt['cidr_netmask'] = ip.cidr_netmask
            if ip.HasField('gate_way'):
                opt['gate_way'] = ip.gate_way
            CIPMgr.SetIP(opt.get('ip'),opt.get('nic'),opt.get('cidr_netmask'),opt.get('gate_way'))
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'ip manage success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def delete_ip(self,controller,request,done):
        try:
            response = puma_pb2.SetIpRes()
            if request.node != 'local' and request.node != '' and not CIPMgr.CheckIp(request.node):
                cli = client.CClient(str(request.node),globalvar.listen_port)
                stub = cli.stub()
                request.node = 'local'
                stub.delete_ip(None,request,None)
                resp = cli.get_response()
                done(resp)
                return True
            opt = {}
            ip = request.ipOpt
            opt['ip'] = ip.ip
            if ip.HasField('nic'):
                opt['nic'] = ip.nic
            if ip.HasField('cidr_netmask'):
                opt['cidr_netmask'] = ip.cidr_netmask
            CIPMgr.DeleteIp(opt.get('ip'),opt.get('nic'))
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'ip manage success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)
        return True

    def get_nic_private(self,controller,request,done):
        response = puma_pb2.GetIpRes()
        try:
            rtn = CIPMgr.GetNicWithHost()
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'get nic success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = str(rtn)
        done(response)
        return True

    def get_nic(self,controller,request,done):
        def get_nic_by_node(node):
            cli = client.CClient(str(node),globalvar.listen_port)
            stub = cli.stub()
            req = puma_pb2.GetIpReq()
            stub.get_nic_private(None,req,None)
            resp = cli.get_response()
            if resp.ret.retcode != 0:
                raise Exception(resp.ret.msg)
            return eval(resp.ret.msg)

        response = puma_pb2.GetIpRes()
        try:
            if not request.HasField('node'):
                remote = CIPMgr.get_peer_ip()
                local_ip_list = CIPMgr.GetNicWithHost()
                remote_ip_list = get_nic_by_node(remote)
                rtn = local_ip_list + remote_ip_list
            elif request.node != 'local' and request.node != '' and not CIPMgr.CheckIp(request.node):
                rtn = get_nic_by_node(request.node)
            else:
                rtn = CIPMgr.GetNicWithHost()
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'get nic success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = str(rtn)
        done(response)
        return True

    def get_ip_private(self,controller,request,done):
        response = puma_pb2.GetIpRes()
        try:
            rtn = CIPMgr.GetIp(request.is_detail)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'get ip success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = str(rtn)
        done(response)
        return True

    def get_ip(self,controller,request,done):
        def get_ip_by_node(node, flag = False):
            logging.debug('ip:%s,port:%d' %(node,globalvar.listen_port))
            cli = client.CClient(str(node),globalvar.listen_port)
            stub = cli.stub()
            req = puma_pb2.GetIpReq()
            req.is_detail = flag
            stub.get_ip_private(None,req,None)
            resp = cli.get_response()
            if resp.ret.retcode != 0:
                raise Exception(resp.ret.msg)
            return eval(resp.ret.msg)

        response = puma_pb2.GetIpRes()
        try:
            detail_flag = True 
            if request.HasField('is_detail'):
                detail_flag = request.is_detail
            logging.debug('start')
            if not request.HasField('node'):
                remote = CIPMgr.get_peer_ip()
                local_ip_list = CIPMgr.GetIp(detail_flag)
                remote_ip_list = get_ip_by_node(remote,detail_flag)
                rtn = local_ip_list + remote_ip_list
            elif request.node != 'local' and request.node != '' and not CIPMgr.CheckIp(request.node):
                rtn = get_ip_by_node(request.node,detail_flag)
            else:
                rtn = CIPMgr.GetIp(detail_flag)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return False
        msg = 'get ip success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = str(rtn)
        done(response)
        logging.debug('end')
        return True

    def start_cluster(self,controller,request,done):
        response = puma_pb2.ClusterStartRes()
        try:
            node = request.node
            cluster = CClusterMgr.CClusterMgr(True)
            rtn = cluster.Start(node)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return
        msg = 'cluster start success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)

    def stop_cluster(self,controller,request,done):
        response = puma_pb2.ClusterStopRes()
        try:
            node = request.node
            cluster = CClusterMgr.CClusterMgr()
            rtn = cluster.Stop(node)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return
        msg = 'cluster stop success'
        logging.info(msg)
        response.ret.retcode = 0
        response.ret.msg = msg
        done(response)

    def set_property_cluster(self,controller,request,done):
        response = puma_pb2.ClusterPropertyRes()
        try:
            opt = []
            for op in request.opt:
                tem = []
                tem.append(op.pName)
                tem.append(op.pValue)
                opt.append(tem)

            cluster = CClusterMgr.CClusterMgr()
            rtn = cluster.SetProperty(opt,request.code)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return
        msg = 'cluster set property success'
        logging.info(msg)
        response.ret.retcode = 0
        if request.code in 'all default':
            response.ret.msg = str(rtn)
        else:
            response.ret.msg = msg
        done(response)

    def syn_xml(self,controller,request,done):
        try:
            response = puma_pb2.XmlSynRes()
            cfg = CConfigMgr.CConfigMgr(None,globalvar.db_path,True)
            if request.HasField('xml'):
                local_xml = CConfigMgr.GetXml(globalvar.db_path)
                if not CConfigMgr.Compare(local_xml,request.xml):
                    raise Exception('xml on two nodes are different')
            for action in request.action :
                nodename = action.nodename
                if action.nodepath == '':
                    nodepath = None
                else:
                    nodepath = action.nodepath.split(':')
                attr = {}
                for a in action.attr:
                    attr[a.key] = a.value
                #pdb.set_trace()
                if action.action == 'AddNode':
                    cfg.AddNoded(nodepath,nodename,attr,True)
                elif action.action == 'AddKey' :
                    cfg.AddKey(nodepath,attr)
                elif action.action == 'UpdateNode' :
                    cfg.UpdateNoded(nodepath,nodename,attr)
                elif action.action == 'UpdateKey' :
                    for k in attr:
                        key = k
                        value = attr[k]
                    cfg.UpdateKey(nodepath,key,value)
                elif action.action == 'DeleteNode' :
                    cfg.DeleteNoded(nodepath,nodename)
                elif action.action == 'DeleteKey' :
                    cfg.DeleteKey(nodepath,nodename)
            cfg.Commit(True)
        except Exception as e:
            logging.error(str(e))
            response.ret.retcode = -1
            response.ret.msg = str(e)
            done(response)
            return
        
        logging.info('xml sync success')
        response.ret.retcode = 0
        response.ret.msg = str('xml sync success')
        done(response)
        return

    def add_cluster_resource(self,controller,request,done):
        try:
            resp = puma_pb2.AddCluResourceRes()
            resopt = {}
            resgrp = {}
            name = request.resName
            resType = request.resType
            for op in request.resOpt:
                resopt[op.key]=op.value
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.AddResource(name,resType,resopt)
            del mgr
        except Exception as e:
            logging.error('add resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        logging.info('add resource['+name+'] success')
        resp.ret.retcode = 0
        resp.ret.msg = str('add resource['+name+'] success')
        done(resp)
        return

    def add_lun(self,controller,request,done):
        try:
            resp = puma_pb2.AddCluResourceRes()
            resopt = {}
            resgrp = {}
            ip = request.ip
            lu = request.lu
            resopt['ip'] = ip.ip
            if ip.HasField('nic'):
                resopt['nic'] = ip.nic
            if ip.HasField('cidr_netmask'):
                resopt['cidr_netmask'] = ip.cidr_netmask
            resopt['path'] = lu.path
            if lu.HasField('lun'):
                resopt['lun'] = lu.lun
            if lu.HasField('target_iqn'):
                import re
                regx = '^iqn\.\d{4}-\d{2}\.\S*:\w'
                if not re.search(regx,lu.target_iqn):
                    raise Exception('you input target-iqn[%s] is invaild' % lu.target_iqn)
                resopt['target_iqn'] = lu.target_iqn
            tmp_str = '"'
            for acess in lu.allowed_initiators:
                import re
                regx = '^iqn\.\d{4}-\d{2}\.\S*:\w'
                if not re.search(regx,acess.iqn):
                    raise Exception('you input target-iqn[%s] is invaild' % acess.iqn)
                tmp_str += acess.iqn + ';' + acess.acess + ' '
            if tmp_str != '"':
                tmp_str += '"'
                resopt['allowed_initiators'] = tmp_str 
            if request.HasField('tgt'):
                tgt = request.tgt
                if tgt.HasField('additional_parameters'):
                    resopt['additional_parameters'] = tgt.additional_parameters
                if tgt.HasField('allowed_initiators'):
                    resopt['allowed_initiators'] = tgt.allowed_initiators
            
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.SetResource(resopt)
            del mgr
        except Exception as e:
            logging.error('add resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = 'add lun success'
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def delete_lun(self,controller,request,done):
        try:
            resp = puma_pb2.DeleteResourceRes()
            mgr = CClusterMgr.CClusterMgr()
            resopt = {}
            if request.HasField('ip'):
                resopt['ip'] = request.ip
            if request.HasField('device_path'):
                resopt['path'] = request.device_path
            if len(resopt) == 0:
                raise Exception('please specify which lun you want to delete')
            rtn = mgr.DeleteResource(resopt)
            del mgr
        except Exception as e:
            logging.error('delete resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('delete resource success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def update_lun(self,controller,request,done):
        try:
            resp = puma_pb2.AddCluResourceRes()
            resopt = {}
            ip = request.ip
            lu = request.lu
            resopt['ip'] = ip.ip
            if ip.HasField('nic'):
                resopt['nic'] = ip.nic
            if ip.HasField('cidr_netmask'):
                resopt['cidr_netmask'] = ip.cidr_netmask
            resopt['path'] = lu.path
            if lu.HasField('lun'):
                resopt['lun'] = lu.lun
            if lu.HasField('target_iqn'):
                resopt['target_iqn'] = lu.target_iqn
            tmp_str = '"'
            for acess in lu.allowed_initiators:
                if acess.iqn == '':
                    tmp_str = ''
                    break
                import re
                regx = '^iqn\.\d{4}-\d{2}\.\S*:\w'
                if not re.search(regx,acess.iqn):
                    raise Exception('you input target-iqn[%s] is invaild' % acess.iqn)
                tmp_str += acess.iqn + ';' + acess.acess + ' '
            if tmp_str != '"':
                if tmp_str != '':
                    tmp_str += '"'
                resopt['allowed_initiators'] = tmp_str 
            if request.HasField('tgt'):
                tgt = request.tgt
                if tgt.HasField('additional_parameters'):
                    resopt['additional_parameters'] = tgt.additional_parameters
            
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.UpdateLun(resopt)
            del mgr
        except Exception as e:
            logging.error('update resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = 'lun update success'
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def get_lun(self,controller,request,done):
        try:
            logging.debug('start')
            resp = puma_pb2.GetResourceRes()
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.GetLunInfo()
            del mgr
        except Exception as e:
            logging.error('get lun failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str(rtn)
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg.replace('"',''))
        done(resp)
        logging.debug('end')
        return

    def check_lun(self,controller,request,done):
        try:
            resp = puma_pb2.AddCluResourceRes()
            mgr = CClusterMgr.CClusterMgr()
            resopt = {}
            if request.HasField('ip'):
                resopt['ip'] = request.ip
            if request.HasField('device_path'):
                resopt['path'] = request.device_path
            if len(resopt) == 0:
                raise Exception('please specify which lun you want to delete')
            rtn,out = mgr.CheckLun(resopt)
            del mgr
            if not rtn:
                raise Exception(out)
        except Exception as e:
            logging.error('check lun failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('check lun success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def delete_cluster_resource(self,controller,request,done):
        try:
            resp = puma_pb2.DeleteResourceRes()
            mgr = CClusterMgr.CClusterMgr()
            if request.HasField('resName'):
                resName = request.resName
                rtn = mgr.DeleteResourced(resName)
            else:
                resopt = {}
                for op in request.resOpt:
                    resopt[op.key]=op.value
                rtn = mgr.DeleteResource(resopt)
            del mgr
        except Exception as e:
            logging.error('delete resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('delete resource success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def update_cluster_resource(self,controller,request,done):
        try:
            resp = puma_pb2.UpdateResourceRes()
            resopt = {}
            name = request.resName
            for op in request.resOpt:
                resopt[op.key]=op.value
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.UpdateResource(name,resopt)
            del mgr
        except Exception as e:
            logging.error('update resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('update resource['+name+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def get_cluster_state(self,controller,request,done):
        try:
            resp = puma_pb2.GetResourceRes()
            mgr = CClusterMgr.CClusterMgr()
            detail_flag = False
            if request.HasField('detail_flag'):
                detail_flag = request.detail_flag
            rtn = mgr.GetClusterState(detail_flag)
            del mgr
        except Exception as e:
            logging.error('get cluster failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str(rtn)
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def get_cluster_resource(self,controller,request,done):
        logging.debug('start get resource list')
        try:
            resp = puma_pb2.GetResourceRes()
            name = request.resName
            isType = request.isType
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.GetResState(name,isType)
            del mgr
        except Exception as e:
            logging.error('get resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str(rtn)
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return
    
    def cleanup_cluster_resource(self,controller,request,done):
        try:
            resp = puma_pb2.CleanupRes()
            if request.HasField('resName'):
                name = request.resName
            else:
                name = ''
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.Cleanup(name)
            del mgr
        except Exception as e:
            logging.error('disable resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def stop_cluster_resource(self,controller,request,done):
        try:
            resp = puma_pb2.StopResourceRes()
            name = request.resName
            mgr = CClusterMgr.CClusterMgr()
            if request.isStop:
                rtn = mgr.DisableResource(name)
            else:
                rtn = mgr.EnableResource(name)
            del mgr
        except Exception as e:
            logging.error('disable resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def group_cluster(self,controller,request,done):
        try:
            resp = puma_pb2.GroupRes()
            resopt = []
            name = request.grpName
            action = request.action
            member = request.grpMember
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.Group(action,name,member)
            del mgr
        except Exception as e:
            logging.error(action+' group['+name+']failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str(action+' group['+name+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def debug_start(self,controller,request,done):
        try:
            resp = puma_pb2.DebugStartRes()
            name = request.resName
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.DebugStart(name)
            del mgr
        except Exception as e:
            logging.error('debug-start resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('debug resource success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def move_cluster_resource(self,controller,request,done):
        try:
            resp = puma_pb2.MoveResourceRes()
            name = request.resName
            node = request.cluNode
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.Move(name,node)
            del mgr
        except Exception as e:
            logging.error('move resource failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('move resource success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def add_cluster_cons(self,controller,request,done):
        try:
            resp = puma_pb2.AddConstraintRes()
            consopt = {}
            consType = request.consType
            for op in request.consOpt:
                consopt[op.key] = op.value
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.AddConstraint(consType,consopt)
            del mgr
        except Exception as e:
            logging.error('add constraint failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('add constraint['+consType+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return
    
    def delete_cluster_cons(self,controller,request,done):
        try:
            resp = puma_pb2.DeleteConstraintRes()
            resName = request.resName
            if request.HasField('isId'):
                flag = request.isId
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.DeleteConstraint(resName,flag)
            del mgr
        except Exception as e:
            logging.error('delete constraint failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('delete constraint['+resName+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def get_cluster_cons(self,controller,request,done):
        try:
            resp = puma_pb2.GetConstraintRes()
            resName = request.resName
            flag = request.isId
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.GetConsState(resName,flag)
            del mgr
        except Exception as e:
            logging.error('get constraint failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str(rtn)
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def add_cluster_stonith(self,controller,request,done):
        try:
            resp = puma_pb2.AddStonithRes()
            stopt = []
            stname = request.stName
            sttype = request.stType
            for op in request.stOpt:
                oplist = []
                oplist.append(op.key)
                oplist.append(op.value)
                stopt.append(oplist)
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.AddStonith(stname,sttype,stopt)
            del mgr
        except Exception as e:
            logging.error('add stonith failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('add stonith['+stname+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def delete_cluster_stonith(self,controller,request,done):
        try:
            resp = puma_pb2.DeleteStonithRes()
            stname = request.stName
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.DeleteStonith(stname)
            del mgr
        except Exception as e:
            logging.error('delete stonith failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('delete stonith['+stname+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def update_cluster_stonith(self,controller,request,done):
        try:
            resp = puma_pb2.UpdateStonithRes()
            stopt = []
            stname = request.stName
            for op in request.stOpt:
                oplist = []
                oplist.append(op.key)
                oplist.append(op.value)
                stopt.append(oplist)
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.UpdateStonith(stname,stopt)
            del mgr
        except Exception as e:
            logging.error('update stonith failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('update stonith['+stname+'] success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return
    def get_cluster_stonith(self,controller,request,done):
        try:
            resp = puma_pb2.GetStonithRes()
            stname = request.stName
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.GetStState(stname)
            del mgr
        except Exception as e:
            logging.error('get stonith failed,error reason: '+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str(rtn)
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def commit_cluster(self,controller,request,done):
        try:
            self.cluster_commit_lock.acquire()
            resp = puma_pb2.CommitRes()
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.Commit()
        except Exception as e:
            logging.error('cluster commit failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            self.cluster_commit_lock.release()
            return
        msg = str('cluster commit success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        self.cluster_commit_lock.release()
        return

    def rollback_cluster(self,controller,request,done):
        try:
            resp = puma_pb2.RollBackRes()
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.RollBack()
        except Exception as e:
            logging.error('cluster rollback failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('cluster rollback success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def setpoint_cluster(self,controller,request,done):
        try:
            resp = puma_pb2.SetPointRes()
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.SetPoint()
        except Exception as e:
            logging.error('cluster setpoint failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('cluster setpoint success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def set_clone_cluster(self,controller,request,done):
        try:
            resp = puma_pb2.ResourceMgrRes()
            mgr = CClusterMgr.CClusterMgr()
            act = request.action
            resname = request.resName
            opt = []
            for op in request.resOpt:
                tmp = []
                tmp.append(op.key)
                tmp.append(op.value)
                opt.append(tmp)

            rtn = mgr.SetClone(act,resname,opt)
        except Exception as e:
            logging.error('set ['+resname+'] clone failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set ['+resname+'] clone success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def set_master_cluster(self,controller,request,done):
        try:
            resp = puma_pb2.ResourceMgrRes()
            mgr = CClusterMgr.CClusterMgr()
            act = request.action
            resname = request.resName
            mastername = request.masterName
            opt = []
            for op in request.resOpt:
                tmp = []
                tmp.append(op.key)
                tmp.append(op.value)
                opt.append(tmp)

            rtn = mgr.SetMaster(act,mastername,resname,opt)
        except Exception as e:
            logging.error('set ['+resname+'] master failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set ['+resname+'] master success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def set_manage_cluster(self,controller,request,done):
        try:
            resp = puma_pb2.ResourceMgrRes()
            mgr = CClusterMgr.CClusterMgr()
            act = request.action
            resname = request.resName
            opt = []
            for op in request.resOpt:
                tmp = []
                tmp.append(op.key)
                tmp.append(op.value)
                opt.append(tmp)

            rtn = mgr.SetManage(act,resname)
        except Exception as e:
            logging.error('set ['+resname+'] manage failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set ['+resname+'] manage success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def enable_stonith_ipmi(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            mgr = CClusterMgr.CClusterMgr()
            opt = []
            for op in request.attr:
                tmp = {}
                tmp['host'] = op.host
                tmp['username'] = op.username
                tmp['passwd'] = op.passwd
                tmp['ip'] = op.ip
                if op.HasField('id'):
                    tmp['id'] = op.id
                opt.append(tmp)

            rtn = mgr.EnableIpmi(opt)
        except Exception as e:
            logging.error('set ipmi failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set ipmi success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def disable_stonith_ipmi(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            mgr = CClusterMgr.CClusterMgr()
            opt = []
            for op in request.attr:
                tmp = {}
                tmp['host'] = op.host
                tmp['username'] = op.username
                tmp['passwd'] = op.passwd
                tmp['ip'] = op.ip
                if op.HasField('id'):
                    tmp['id'] = op.id
                opt.append(tmp)

            rtn = mgr.DisableIpmi(opt)
        except Exception as e:
            logging.error('disable ipmi failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('disable ipmi success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def update_stonith_ipmi(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            mgr = CClusterMgr.CClusterMgr()
            opt = []
            for op in request.attr:
                tmp = {}
                tmp['host'] = op.host
                tmp['username'] = op.username
                tmp['passwd'] = op.passwd
                tmp['ip'] = op.ip
                if op.HasField('id'):
                    tmp['id'] = op.id
                else:
                    raise Exception('please specify the ipmi stonith-id when you try to update the stonith')
                opt.append(tmp)

            rtn = mgr.UpdateIpmi(opt)
        except Exception as e:
            logging.error('update ipmi failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('update ipmi success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(msg)
        done(resp)
        return

    def get_stonith_ipmi(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            mgr = CClusterMgr.CClusterMgr()
            rtn = mgr.GetIPMI()
        except Exception as e:
            logging.error('get ipmi failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('get ipmi success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(rtn)
        done(resp)
        return

    def set_cluster_name(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            mgr = CClusterMgr.CClusterMgr()
            cluster_name = request.cluster_name
            rtn = mgr.SetClusterName(cluster_name)
        except Exception as e:
            logging.error('set cluster name failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set cluster name success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def get_cluster_name(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            rtn = CIPMgr.GetClusterName()
        except Exception as e:
            logging.error('get cluster name failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('get cluster name success,result:%s' % str(rtn))
        logging.info(resp)
        resp.ret.retcode = 0
        resp.ret.msg = str(rtn)
        done(resp)
        return

    def set_heartbeat(self,controller,request,done):
        def set_hb_dict(hb):
            hb_dict = {}
            hb_dict['hb_ip'] = hb.hb
            hb_dict['host'] = hb.host
            hb_dict['nic'] = hb.nic
            if hb.HasField('cidr_netmask'):
                hb_dict['mask'] = hb.cidr_netmask
            return hb_dict

        try:
            resp = puma_pb2.StonithIPMIRes()
            hb1 = request.hb1
            hb2 = request.hb2
            hblist = []
            hblist.append(set_hb_dict(hb1))
            hblist.append(set_hb_dict(hb2))
            mgr = CClusterMgr.CClusterMgr(True)
            passwd = None
            if request.HasField('passwd'):
                passwd = request.passwd
            rtn = mgr.SetHeartb(hblist,passwd)
        except Exception as e:
            logging.error('set heartbeat failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set heartbeat success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def syn_file(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            rtn = CConfigMgr.SetXmlByString(request.file_name,request.file_cont)
        except Exception as e:
            logging.error('syn file failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('syn file:%s success' % request.file_name)
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return
    
    def ntp_add_url(self,controller,request,done):
        response = puma_pb2.NtpAddUrlRes()
        try:
            ntp.ntp_add(request.url)
            logging.info("ntp: add url %s" % request.url)
            ntp.ntp_restart()
        except Exception,e:
            logging.error("CServiceImpl::ntp_add_url %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::ntp_add_url")
        response.ret.retcode = 0
        done(response)

    def ntp_del_url(self,controller,request,done):
        response = puma_pb2.NtpDelUrlRes()
        try:
            ntp.ntp_del(request.url)
            logging.info("ntp: del url %s" % request.url)
            ntp.ntp_restart()
        except Exception,e:
            logging.error("CServiceImpl::ntp_del_url %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::ntp_del_url")
        response.ret.retcode = 0
        done(response)
    
    def ntp_client_setup(self,controller,request,done):
        response = puma_pb2.NtpClientSetupRes()
        try:
            ntp_setup.ntp_client_setup(request.timezone,request.url)
        except Exception,e:
            logging.error("CServiceImpl::ntp_client_setup %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::ntp_client_setup")
        response.ret.retcode = 0
        done(response)

    def ntp_server_setup(self,controller,request,done):
        response = puma_pb2.NtpServerSetupRes()
        try:
            ntp_setup.ntp_server_setup(request.timezone,request.public_url)
        except Exception,e:
            logging.error("CServiceImpl::ntp_server_setup %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::ntp_server_setup")
        response.ret.retcode = 0
        done(response)

    ##private
    def ntp_add_url_remote(self,rpc_client,request):
        rpc_client.stub().ntp_add_url(None,request,None)
        response = rpc_client.get_response()
        if response.ret.retcode != 0:
            raise Exception("Remote rpc Call ntp_add_url:{0} failed {1}".format(request.url,response.ret.msg))

    ##private
    def ntp_del_url_remote(self,rpc_client,request):
        rpc_client.stub().ntp_del_url(None,request,None)
        response = rpc_client.get_response()
        if response.ret.retcode != 0:
            raise Exception("Remote rpc Call ntp_del_url:{0} failed {1}".format(request.url,response.ret.msg))

    def cluster_ntp_add_url(self,controller,request,done):
        response = puma_pb2.NtpAddUrlRes()
        try:
            rpc_client = self.create_rpc_client_handle()
            self.ntp_add_url_remote(rpc_client,request)
            logging.info("ntp: remove add success")
            ntp.ntp_add(request.url)
            logging.info("ntp: add url %s" % request.url)
            ntp.ntp_restart()
        except Exception,e:
            logging.error("CServiceImpl::cluster_ntp_add_url %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::cluster_ntp_add_url")
        response.ret.retcode = 0
        done(response)

    def cluster_ntp_del_url(self,controller,request,done):
        response = puma_pb2.NtpDelUrlRes()
        try:
            rpc_client = self.create_rpc_client_handle()
            self.ntp_add_url_remote(rpc_client,request)
            logging.info("ntp: remove del success")
            ntp.ntp_del(request.url)
            logging.info("ntp: del url %s" % request.url)
            ntp.ntp_restart()
        except Exception,e:
            logging.error("CServiceImpl::cluster_ntp_del_url %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::cluster_ntp_del_url")
        response.ret.retcode = 0
        done(response)

    """
    """
    def cluster_ntp_setup(self,controller,request,done):
        response = puma_pb2.NtpSetupRes()
        try:
            rpc_client = self.create_rpc_client_handle()
            rpc_stub = rpc_client.stub()

            if request.node_ip in CIPMgr.get_corosync_node():
                ##
                if CIPMgr.CheckIp(request.node_ip):
                    ##local
                    ntp_setup.ntp_server_setup(request.timezone,request.public_url)
                    logging.debug("ntp_server_setup")
                    ntp_setup.remote_ntp_client_setup(rpc_client,rpc_stub,\
                            request.timezone,request.node_ip)
                    logging.debug("remote_ntp_client_setup")
                else:
                    ##remote
                    ntp_setup.remote_ntp_server_setup(rpc_client,rpc_stub,request.timezone,request.public_url)
                    logging.debug("remote_ntp_server_setup")
                    ntp_setup.ntp_client_setup(request.timezone,request.node_ip)
                    logging.debug("ntp_client_setup")
            else:
                logging.error("node_ip is not cluster ip")
                raise Exception("node ip must be the one of the cluster node's heartbeat ip")
        except Exception,e:
            logging.error("CServiceImpl::cluster_ntp_setup %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::cluster_ntp_setup")
        response.ret.retcode = 0
        done(response)

    def ntp_get_conf(self,controller,request,done):
        response = puma_pb2.NtpGetConfRes()
        try:
            rpc_client = self.create_rpc_client_handle()
            (flag,url) = ntp_setup.ntp_check_server_conf()

            if flag != True:
                logging.error("local host is not ntp server")
                raise Exception("local host is not ntp server")

            response.host_name = CIPMgr.GetHostname()
            response.status = ntp_setup.ntp_status()
            response.url = url

        except Exception,e:
            logging.error("CServiceImpl::cluster_ntp_get_conf %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::cluster_ntp_get_conf")
        response.ret.retcode = 0
        done(response)

    def cluster_ntp_get_conf(self,controller,request,done):
        response = puma_pb2.NtpGetConfRes()
        try:
            ## step one,get server conf from local host
            (flag,url) = ntp_setup.ntp_check_server_conf()

            if flag != True:
                logging.debug("local host is not ntp server,will get\
                        server conf from remote node")
                rpc_client = self.create_rpc_client_handle()
                rpc_stub = rpc_client.stub()
                response = ntp_setup.remote_ntp_check_server_conf(rpc_client,rpc_stub)
            else:
                response.host_name = CIPMgr.GetHostname()
                response.status = ntp_setup.ntp_status()
                response.url = url

        except Exception,e:
            logging.error("CServiceImpl::cluster_ntp_get_conf %s" % str(e))
            response.ret.retcode = -1;
            response.ret.msg = str(e)
            done(response)
            return

        logging.info("CServiceImpl::cluster_ntp_get_conf")
        response.ret.retcode = 0
        done(response)

    def list_timezone(self,controller,request,done):
        try:
            resp = puma_pb2.TimezoneRes()
            tz_list = CDateTime.ListTimezone()
            for tz in tz_list:
                tz_obj = resp.tz.add()
                tz_obj.tz = tz

        except Exception as e:
            logging.error('list timezone failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('list timezone success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def get_current_tz(self,controller,request,done):
        try:
            resp = puma_pb2.TimezoneRes()
            tz = CDateTime.CurrentTz()
            tz_obj = resp.tz.add()
            tz_obj.tz = tz
        except Exception as e:
            logging.error('get timezone failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('get timezone success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def get_current_time(self,controller,request,done):
        try:
            resp = puma_pb2.TimeRes()
            t = CDateTime.CurrentTime()
            resp.time.year = t.tm_year
            resp.time.mon = t.tm_mon
            resp.time.day = t.tm_mday
            resp.time.hour = t.tm_hour
            resp.time.min = t.tm_min
            resp.time.sec = t.tm_sec
            resp.time.wday = t.tm_wday+1
        except Exception as e:
            logging.error('get current time failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('get current time success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def set_time(self,controller,request,done):
        try:
            if not request.HasField('local'):
                request.local = True
                peer_ip = CIPMgr.get_peer_ip()
                cli = client.CClient(str(peer_ip),globalvar.listen_port)
                stub = cli.stub()
                stub.set_time(None,request,None)
                resp = cli.get_response()
                if resp.ret.retcode != 0:
                    raise Exception(resp.ret.msg)

            resp = puma_pb2.StonithIPMIRes()
            time = '"'
            time += str(request.time.year) + '-' 
            time += str(request.time.mon) + '-' 
            time += str(request.time.day) + ' ' 
            time += str(request.time.hour) + ':' 
            time += str(request.time.min) + ':' 
            time += str(request.time.sec) + '"'
            t = CDateTime.SetTime(time)
        except Exception as e:
            logging.error('set time failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set time success')
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def set_timezone(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            if not request.HasField('local'):
                request.local = True
                peer_ip = CIPMgr.get_peer_ip()
                cli = client.CClient(str(peer_ip),globalvar.listen_port)
                stub = cli.stub()
                stub.set_timezone(None,request,None)
                resp = cli.get_response()
                if resp.ret.retcode != 0:
                    raise Exception(resp.ret.msg)
            t = CDateTime.SetTz(request.tz.tz)
        except Exception as e:
            logging.error('set timezone failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('set timezone success' )
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = msg
        done(resp)
        return

    def get_nic_byip(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            rtn = CIPMgr.GetNicIp(request.ip)
        except Exception as e:
            logging.error('get nic by ip failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('get nic by ip success' )
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(rtn)
        done(resp)
        return

    def get_nic_info(self,controller,request,done):
        try:
            resp = puma_pb2.StonithIPMIRes()
            rtn = CIPMgr.GetNicInfo(request.node)
        except Exception as e:
            logging.error('get nic by ip failed,reason:'+str(e))
            resp.ret.retcode = -1
            resp.ret.msg = str(e)
            done(resp)
            return
        msg = str('get nic by ip success' )
        logging.info(msg)
        resp.ret.retcode = 0
        resp.ret.msg = str(rtn)
        done(resp)
        return

