# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from constraint_handle import *
import sys,os
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
import puma_pb2


class CRpcConstraintHandle(CConstraintHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    def create(self,params = {}):
        request = puma_pb2.AddConstraintReq()
        resType = params.get('type')
        resOpt =  params.get('option')
        if resOpt:
            optlist = resOpt.split(',')
        request.consType = resType
        for op in optlist:
            opt = request.consOpt.add()
            opt.key = op.split('=')[0]
            opt.value = op.split('=')[1]
        self.stub.add_cluster_cons(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def list(self,params = {}):
        return self.info(params)

    def info(self,params = {}):
        if params.get('name'):
            name = params.get('name')
            flag = False
        elif params.get('id'):
            name = params.get('id')
            flag = True
        else:
            flag = True
            name = 'all'
        request = puma_pb2.GetConstraintReq()
        request.resName = name
        request.isId = flag
        self.stub.get_cluster_cons(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def extend(self,params = {}):
        pass
    
    def reduce(self,params = {}):
        pass
    
    def remove(self,params = {}):
        if params.get('name'):
            name = params.get('name')
            flag = False
        if params.get('id'):
            name = params.get('id')
            flag = True
        request = puma_pb2.DeleteConstraintReq()
        request.resName = name
        request.isId = flag
        self.stub.delete_cluster_cons(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

