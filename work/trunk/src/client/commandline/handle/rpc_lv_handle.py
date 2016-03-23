# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import lv_handle

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
import puma_pb2
import logging

class CRpcLVHandle(lv_handle.CLVHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub
    #private
    def gen_protobuf_to_dict(self,lv):
        ret = {}
        ret['lv_name'] = lv.lv_name
        ret['vg_name'] = lv.vg_name
        ret['lv_path'] = '/dev/' + lv.vg_name + '/' + lv.lv_name

        if lv.HasField('lv_uuid'):
            ret['lv_uuid'] = lv.lv_uuid
        if lv.HasField('lv_size'):
            ret['lv_size'] = str(lv.lv_size) + "G"
        if lv.HasField('lv_used'):
            if lv.lv_used:
                ret['lv_used'] = 'Yes'
            else:
                ret['lv_used'] = 'No'

        if lv.HasField('lv_cluster'):
            if lv.lv_cluster:
                ret['lv_cluster'] = 'Yes'
            else:
                ret['lv_cluster'] = 'No'
        return ret

    def create(self,params = {}):
        request = puma_pb2.LvmVGCreateLVReq()
        request.lv_name = params['lv_name']
        request.vg_name = params['vg_name']
        request.lv_size = int(params['lv_size'])

        self.stub.create_lv_lvm_vg(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
    
    def list(self,params = {}):
        ret = []
        keys = ['lv_path','lv_name','vg_name','lv_size','lv_used','lv_cluster']
        lv_request = puma_pb2.LvmScanLVReq()
        self.stub.scan_lv_lvm(None,lv_request,None)
        lv_response = self.client.get_response()
        if lv_response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)

        for lv in lv_response.lvs:
            ret.append(self.gen_protobuf_to_dict(lv))

        return (ret,keys)
        
    def info(self,params = {}):
        raise Exception("This is not supported now")
    
    def extend(self,params = {}):
        req = puma_pb2.LvmExtendLVReq()
        req.vg_name = params['vg_name']
        req.lv_name = params['lv_name']
        req.lv_size = params['lv_size']
        self.stub.extend_lv_lvm(None,request,None)
        res = self.client.get_response()
        if res.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
    
    def reduce(self,params = {}):
        req = puma_pb2.LvmReduceLVReq()
        req.vg_name = params['vg_name']
        req.lv_name = params['lv_name']
        req.lv_size = params['lv_size']
        self.stub.reduce_lv_lvm(None,request,None)
        res = self.client.get_response()
        if res.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
    
    def remove(self,params = {}):
        request = puma_pb2.LvmVGRemoveLVReq()
        request.vg_name = params['vg_name']
        request.lv_name = params['lv_name']

        self.stub.remove_lv_lvm_vg(None,request,None)
        response = self.client.get_response()
        
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
