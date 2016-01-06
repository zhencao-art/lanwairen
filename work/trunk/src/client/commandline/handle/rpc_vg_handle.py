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
        ret['name'] = vg.vg_name
        if vg.HasField('vg_total_size'):
            ret['size'] = str(vg.vg_free_size) + 'G'
        if vg.HasField('vg_free_size'):
            ret['free_size'] = str(vg.vg_free_size) + 'G'
        if vg.HasField('online'):
            if vg.online:
                ret['online'] = 'Yes'
            else:
                ret['online'] = 'No'
        flag = False
        pvs = ""
        for pv in vg.vg_md_pvs:
            pvs = pvs + pv.pv_name + " "
            flag = True
        if flag:
            ret['vg_pvs'] = pvs
        return ret

    #private
    def format_info_view(self,vg):
        ret = []
        ret.append({'key':'name','value':vg.vg_name})
        if vg.HasField('vg_total_size'):
            ret.append({'key':'size','value':str(vg.vg_free_size) + 'G'})
        if vg.HasField('vg_free_size'):
            ret.append({'key':'free_size','value':str(vg.vg_free_size) + 'G'})
        if vg.HasField('online'):
            if vg.online:
                ret.append({'key':'online','value':'Yes'})
            else:
                ret.append({'key':'online','value':'No'})
        #pvs
        flag = False
        pvs = ''
        for pv in vg.vg_md_pvs:
            flag = True
            pvs = pvs + pv.pv_name + " "
        if flag:
            ret.append({"key":"pvs",'value':pvs})
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
        keys = ['name','size','free_size','online']
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
