# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import disk_handle

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../")))
import puma_pb2,params

class CRpcDiskHandle(disk_handle.CDiskHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    #private
    def protobuf_to_dict(self,disk):
        ret = {}
        ret["name"] = disk.dev_name
        ret["size"] = params.sectors2txt(disk.dev_size)

        if disk.rotational == 1:
            ret['type'] = 'HDD'
        else:
            ret['type'] = 'SSD'

        if disk.HasField("dev_wwn"):
            ret["wwn"] = disk.dev_wwn

        if disk.HasField("protocol"):
            ret['protocol'] = disk.protocol

        if disk.HasField("dev_used"):
            if disk.dev_used:
                ret["used"] = "Yes"
            else:
                ret["used"] = "No"

        if disk.HasField("dev_user"):
            ret['user'] = disk.dev_user

        if disk.HasField("dev_slot"):
            ret['slot'] = disk.dev_slot

        if disk.HasField("inited"):
            if disk.inited:
                ret['inited'] = 'Yes'
            else:
                ret['inited'] = 'No'

        if disk.HasField('online'):
            if disk.online:
                ret['online'] = 'Yes'
            else:
                ret['online'] = 'No'

        return ret

    def list(self,params = {}):
        keys = ['name','size','type','protocol','used','user','slot','inited','online','wwn']
        if params.has_key('ip'):
            raise Exception("This is not supported now")
        request = puma_pb2.ListPhyDiskClusterReq()
        self.stub.cluster_list_phy_disk(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)

        ret = []
        for disk in response.disks:
            ret.append(self.protobuf_to_dict(disk))
        return (ret,keys)

    def info(self,params = {}):
        pass

    def init(self,params = {}):
        request = puma_pb2.InitPhyDiskReq()
        request.dev_name = params['name']
        self.stub.init_phy_disk(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
        
