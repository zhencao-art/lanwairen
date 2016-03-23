# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from stonith_handle import CStonithHandle
import sys , os ,commands ,socket
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
import puma_pb2

class CRpcStonithHandle(CStonithHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    def create(self,params = {}):
        request = puma_pb2.AddStonithReq()
        request.stName = params.get('name')
        request.stType = params.get('type')
        oplist = params.get('option').split(',')
        for op in oplist:
            opt = request.stOpt.add()
            opt.key = op.split('=')[0] 
            opt.value = op.split('=')[1]
        self.stub.add_cluster_stonith(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def list(self,params = {}):
        params['name'] = 'all'
        return self.info(params)

    def info(self,params = {}):
        request = puma_pb2.GetStonithReq()
        request.stName = params.get('name')
        self.stub.get_cluster_stonith(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def extend(self,params = {}):
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def reduce(self,params = {}):
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def remove(self,params = {}):
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def update(self,params = {}):
        request = puma_pb2.StonithIPMIReq()
        request = self.init_stonith_paramter(params,request,True)
        self.stub.update_stonith_ipmi(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def delete(self,params = {}):
        request = puma_pb2.DeleteStonithReq()
        request.stName = params.get('name')
        self.stub.delete_cluster_stonith(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def enable(self,params = {}):
        request = puma_pb2.StonithIPMIReq()
        request = self.init_stonith_paramter(params,request)
        self.stub.enable_stonith_ipmi(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def disable(self,params = {}):
        request = puma_pb2.StonithIPMIReq()
        request = self.init_stonith_paramter(params,request)
        self.stub.disable_stonith_ipmi(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def init_stonith_paramter(self,params,req ,update_flag = False):
        def get_dict(opt_str):
            opt_list = opt_str.split(',')
            tmp_dict = {}
            for opt in opt_list:
                value = opt.split('=')
                if len(value) != 2:
                    raise Exception('bad input options[%s] please check the format' % opt)
                tmp_dict[value[0]] = value[1]
            if not tmp_dict.has_key('id') and len(tmp_dict) !=4:
                raise Exception('there need host,ip,username and passwd to add a ipmi stonith')
            if not tmp_dict.has_key('id') and update_flag:
                raise Exception('please specify the stonith id,you can get it by command "stonith list"')
            if len(tmp_dict) == 0:
                raise Exception('you input nothing')
            return tmp_dict
        for key in params:
            stAttr = req.attr.add()
            st_dict = get_dict(params.get(key))
            if st_dict.has_key('host'):
                stAttr.host = st_dict.get('host')
            else:
                stAttr.host = ''
            if st_dict.has_key('ip'):
                stAttr.ip = st_dict.get('ip')
            else:
                stAttr.ip = ''
            if st_dict.has_key('username'):
                stAttr.username = st_dict.get('username')
            else:
                stAttr.username = ''
            if st_dict.has_key('passwd'):
                stAttr.passwd = st_dict.get('passwd')
            else:
                stAttr.passwd = ''
            if st_dict.has_key('id'):
                stAttr.id = st_dict.get('id')
        return req 
