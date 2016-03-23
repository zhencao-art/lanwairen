# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from resource_handle import *
import sys , os ,commands 
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
import puma_pb2

class CRpcResourceHandle(CResourceHandle):
    def __init__(self,client,stub):
        self.stub = stub
        self.client = client

    def create(self,params = {}):
        resName = params.get('name')
        resType = params.get('type')
        resOpt =  params.get('option')
        if resOpt:
            optlist = resOpt.split(',')
        request = puma_pb2.AddCluResourceReq()
        opt_dict = {}
        for op in optlist:
            opt = request.resOpt.add()
            opt.key = op.split('=')[0]
            opt.value = op.split('=')[1]
            opt_dict[op.split('=')[0]] = op.split('=')[1]
        if not resName:
            req = puma_pb2.AddLunReq()
            req.ip.ip = opt_dict.get('ip')
            req.lu.path = opt_dict.get('path')
            if opt_dict.has_key('iqn'):
                req.tgt.iqn = opt_dict.get('iqn')
            self.stub.add_lun(None,req,None)
        else:
            request.resName = resName
            request.resType = resType
            self.stub.add_cluster_resource(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def list(self,params = {}):
        params['name'] = 'all'
        return self.info(params)
        return str([{'id':1,'name':'myi'},{'id':2,'name':'myio'},{'id':3,'name':'myiii'}])

    def info(self,params = {}):
        if params.has_key('name'):
            resName = params.get('name')
            flag = False
        else:
            resName = params.get('type')
            flag = True
        request = puma_pb2.GetResourceReq()
        request.resName = resName
        request.isType = flag
        self.stub.get_cluster_resource(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def master(self,params = {}):
        request = puma_pb2.ResourceMgrReq()
        request.resName = params.get('res_name')
        request.action = 'master'
        request.masterName = params.get('master_name')
        self.stub.set_master_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def clone(self,params = {}):
        request = puma_pb2.ResourceMgrReq()
        request.resName = params.get('name')
        if not params.has_key('unclone'):
            request.action = 'clone'
        else:
            request.action = 'unclone'
        self.stub.set_clone_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def remove(self,params = {}):
        resName = params.get('name')
        request = puma_pb2.DeleteResourceReq()
        if resName:
            request.resName = resName
        optlist = []
        resOpt =  params.get('option')
        if resOpt:
            optlist = resOpt.split(',')
        for op in optlist:
            opt = request.resOpt.add()
            opt.key = op.split('=')[0]
            opt.value = op.split('=')[1]
        self.stub.delete_cluster_resource(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def update(self,params = {}):
        resName = params.get('name')
        resOpt =  params.get('option')
        if resOpt:
            optlist = resOpt.split(',')
        request = puma_pb2.UpdateResourceReq()
        opt_dict = {}
        for op in optlist:
            opt = request.resOpt.add()
            opt.key = op.split('=')[0]
            opt.value = op.split('=')[1]
            opt_dict[op.split('=')[0]] = op.split('=')[1]
        if not resName  :
            #raise Exception('resource options error,please check your input or config')
            req_lun = puma_pb2.AddLunReq()
            req_lun.ip.ip = opt_dict.get('ip')
            req_lun.lu.path = opt_dict.get('path')
            if opt_dict.has_key('lun') :
                req_lun.lu.lun = opt_dict.get('lun')
            self.stub.update_lun(None,req_lun,None)
        else:
            request.resName = resName
            self.stub.update_cluster_resource(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def group(self,params = {}):
        if params.has_key('action'):
            act = 'add'
        else:
            act = 'remove'
        request = puma_pb2.GroupReq()
        request.action = act
        request.grpName = params.get('name')
        request.grpMember = params.get('option').replace(',',' ')
        self.stub.group_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg


    def move(self,params = {}):
        request = puma_pb2.MoveResourceReq()
        request.resName = params.get('name')
        request.cluNode = params.get('node')
        self.stub.move_cluster_resource(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def stop(self,params = {}):
        request = puma_pb2.StopResourceReq()
        request.resName = params.get('name')
        if params.get('action'):
            request.isStop = True
        else:
            request.isStop = False
        self.stub.stop_cluster_resource(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
        
    def debug(self,params = {}):
        param = params.get('name')
        if param.find('=') != -1:
            opt_dict = {}
            optlist = param.split(',')
            for opt in optlist:
                op =opt.split('=')
                opt_dict[op[0]] = op[1]
            req_lun = puma_pb2.AddLunReq()
            req_lun.ip.ip = opt_dict.get('ip')
            req_lun.lu.path = opt_dict.get('path')
            self.stub.check_lun(None,req_lun,None)
        else:
            request = puma_pb2.DebugStartReq()
            request.resName = params.get('name')
            self.stub.debug_start(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cleanup(self,params = {}):
        req = puma_pb2.CleanupReq()
        if params.has_key('name'):
            req.resName = params.get('name')
        self.stub.cleanup_cluster_resource(None,req,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
        
