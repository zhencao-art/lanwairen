# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import vg_handle

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
import puma_pb2

class CRpcVGHandle(vg_handle.CVGHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    #priavate
    def gen_protobuf_to_dict(self,vg):
        ret = {}
        ret['vg_name'] = vg.vg_name
        if vg.HasField('vg_uuid'):
            ret['vg_uuid'] = vg.vg_uuid
        if vg.HasField('vg_free_size'):
            ret['vg_free_size'] = str(vg.vg_free_size) + 'G'
        if vg.HasField('vg_extent_size'):
            ret['vg_extent_size'] = str(vg.vg_extent_size >> 10) + 'K'
        if vg.HasField('vg_extent_count'):
            ret['vg_extent_count'] = vg.vg_extent_count
        if vg.HasField('vg_free_extent_count'):
            ret['vg_free_extent_count'] = vg.vg_free_extent_count

        flag = False
        pvs = ""
        for pv in vg.vg_pvs:
            pvs = pvs + pv.pv_name + " "
            flag = True
        if flag:
            ret['vg_pvs'] = pvs

        flag = False
        lvs = ""
        for lv in vg.vg_lvs:
            lvs = lvs + lv.lv_name + " "
            flag = True
        if flag:
            ret['vg_lvs'] = lvs

        return ret

    #private
    def format_info_view(self,vg):
        ret = []
        ret.append({'key':'vg_name','value':vg.vg_name})
        if vg.HasField('vg_uuid'):
            ret.append({'key':'vg_uuid','value':vg.vg_uuid})
        if vg.HasField('vg_free_size'):
            ret.append({'key':'vg_free_size','value':str(vg.vg_free_size) + 'G'})
        if vg.HasField('vg_extent_size'):
            ret.append({'key':'vg_extent_size','value':str(vg.vg_extent_size>>10) + 'K'})
        if vg.HasField('vg_extent_count'):
            ret.append({'key':'vg_extent_count','value':vg.vg_extent_count})
        if vg.HasField('vg_free_extent_count'):
            ret.append({'key':'vg_free_extent_count','value':vg.vg_free_extent_count})
        #pvs
        flag = False
        pvs = ''
        for pv in vg.vg_pvs:
            flag = True
            pvs = pvs + pv.pv_name + " "
        if flag:
            ret.append({"key":"pvs",'value':pvs})
        #lvs
        flag = False
        lvs = ''
        for lv in vg.vg_lvs:
            flag = True
            lvs = lvs + lv.lv_name + " "
        if flag:
            ret.append({"key":"lvs",'value':lvs})

        return ret

    def create(self,params = {}):
        request = puma_pb2.LvmVGCreateReq()
        request.vg_name = params['vg_name']
        pvs = params['phy_vol']
        for pv in pvs.split(','):
            request.vg_pvs.add().pv_name = pv

        self.stub.create_lvm_vg(None,request,None)
        response = self.client.get_response()

        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
    
    def list(self,params = {}):
        keys = ['vg_name','vg_free_size','vg_extent_size','vg_uuid','vg_extent_count','vg_free_extent_count']
        request = puma_pb2.LvmVGScanReq()
        request.vg = True
        ##only vg_name
        self.stub.scan_lvm_vg(None,request,None)
        response = self.client.get_response()
        
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)

        ret = []
        for vg in response.vgs:
            ret.append(self.gen_protobuf_to_dict(vg))

        return (ret,keys)

    def list_pv(self,params = {}):
        pass

    def info(self,params = {}):
        request = puma_pb2.LvmVGFindReq()
        request.vg_name = params['vg_name']
        request.pv = True
        request.lv = True

        self.stub.find_lvm_vg(None,request,None)
        response = self.client.get_response()
        
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)

        return self.format_info_view(response.vg)
    
    def extend(self,params = {}):
        request = puma_pb2.LvmVGAddPVReq()
        request.vg_name = params['vg_name']
        pvs = params['phy_vol']
        for pv in pvs.split(','):
            request.vg_pvs.add().pv_name = pv
        self.stub.add_pv_lvm_vg(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
    
    def reduce(self,params = {}):
        request = puma_pb2.LvmVGDelPVReq()
        request.vg_name = params['vg_name']
        pvs = params['phy_vol']
        for pv in pvs.split(','):
            request.vg_pvs.add().pv_name = pv
        if params.has_key('rm_drast'):
            if params['rm_drast'] == True:
                request.crashing = True
            else:
                #request.crashing = False
                request.crashing = True

        self.stub.del_pv_lvm_vg(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
    
    def remove(self,params = {}):
        request = puma_pb2.LvmVGRemoveReq()
        request.vg_name = params['vg_name']
        if params.has_key('rm_drast'):
            if params['rm_drast'] == True:
                request.crashing = True
            else:
                #request.crashing = False
                request.crashing = True
        self.stub.remove_lvm_vg(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
