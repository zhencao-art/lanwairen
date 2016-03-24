# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import raid_handle

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../")))
import puma_pb2,params

class CRpcRaidHandle(raid_handle.CRaidHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    #private
    def gen_protobuf_to_dict(self,md):
        ret = {}
        ret['name'] = md.dev_name
        if md.HasField('dev_size'):
            ret['size'] = params.sectors2txt(md.dev_size)
        if md.HasField('dev_level'):
            ret['level'] = md.dev_level
        if md.HasField('dev_chunk'):
            ret['chunk'] = params.bytes2txt(md.dev_chunk)
        if md.HasField('dev_used'):
            if md.dev_used:
                ret['used'] = "Yes"
                ret['user'] = md.dev_user
            else:
                ret['used'] = "No"
        if md.HasField('online'):
            if md.online:
                ret['online'] = 'Yes'
            else:
                ret['online'] = 'No'

        flag = False
        phys = ""
        for phy in md.dev_phy_devices:
            phys = phys + phy.dev.dev_name + " "
            flag = True
        if flag:
            ret['phy_devices'] = phys

        return ret
        
    def create(self,params = {}):
        request = puma_pb2.MdCreateReq()

        if params['md_name'].startswith('/dev/'):
            request.md_name = params['md_name'].split('/')[2]
        else:
            request.md_name = params['md_name']

        request.md_level = int(params['md_level'])
        if params.has_key('md_width'):
            request.md_chunk = int(params['md_width'])
        for dev in params['md_phys'].split(','):
            request.md_phy_devices.add().dev.dev_name = dev

        self.stub.create_md_device(None,request,None)
        response = self.client.get_response()

        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)

    def list(self,params = {}):
        keys = ['name','size','level','chunk','used','user','online']
        request = puma_pb2.MdScanReq()

        self.stub.scan_md_device(None,request,None)
        response = self.client.get_response()
        
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s",response.ret.msg)
        ret = []
        for md in response.md_devices:
            ret.append(self.gen_protobuf_to_dict(md))
        return (ret,keys)

    ##private
    def format_info_view(self,md):
        def phy_devices_md(md):
            ret = ""
            begin = True
            for i in md.dev_phy_devices:
                if begin:
                    ret = ret + i.dev.dev_name
                else:
                    ret = ret + ',' + i.dev.dev_name
            return ret

        ret = []
        ret.append({'key':'name','value':md.dev_name})
        if md.HasField('dev_size'):
            ret.append({'key':'size','value':params.sectors2txt(md.dev_size)})
        if md.HasField('dev_level'):
            ret.append({'key':'level','value':md.dev_level})
        if md.HasField('dev_chunk'):
            ret.append({'key':'chunk','value':params.bytes2txt(md.dev_chunk)})
        if md.HasField('dev_used'):
            if md.dev_used:
                ret.append({'key':'used','value':'Yes'})
                ret.append({'key':'user','value':md.dev_user})
            else:
                ret.append({'key':'used','value':'No'})
        if md.HasField('online'):
            if md.online:
                ret.append({'key':'online','value':'Yes'})
            else:
                ret.append({'key':'online','value':'No'})

        phy_devices = phy_devices_md(md)
        ret.append({'key':'phy_devices','value':phy_devices})
        
        return ret

    def info(self,params = {}):
        request = puma_pb2.MdScanReq()

        self.stub.scan_md_device(None,request,None)
        response = self.client.get_response()
        
        md_dev = None
        md_name = None

        if params['md_name'].startswith('/dev/'):
            md_name = params['md_name'].split('/')[2]
        else:
            md_name = params['md_name']

        for md in response.md_devices:
            if  md.dev_name == '/dev/' + md_name:
                md_dev = md

        if md_dev:
            ret = self.format_info_view(md_dev)
        else:
            raise Exception("%s is not found" % params['md_name'])

        return ret
    
    def extend(self,params = {}):
        raise Exception("This is not supported now")
    
    def reduce(self,params = {}):
        raise Exception("This is not supported now")
    
    def remove(self,params = {}):
        request = puma_pb2.MdRemoveReq()

        if params['md_name'].startswith('/dev/'):
            request.md_name = params['md_name'].split('/')[2]
        else:
            request.md_name = params['md_name']

        if params.has_key('rm_drast'):
            if params['rm_drast'] == True:
                request.rm_crashing = True
            else:
                #request.rm_crashing = False
                request.rm_crashing = True

        self.stub.remove_md_device(None,request,None)
        response = self.client.get_response()
        
        if response.ret.retcode != 0:
            raise Exception("RPC call error,%s" % response.ret.msg)
