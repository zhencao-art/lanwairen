# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from pcs_handle import *
import sys , os ,commands ,socket
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../server")))
import puma_pb2

class CRpcPcsHandle(CPcsHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    def setup(self,params = {}):
        request = puma_pb2.ClusterInitReq()
        request.cPasswd = params.get('passwd')
        request.clusterName = params.get('cluster_name')
        iplist = params.get('cluster_node').split(',')
        
        request.cNodelist = ''
        for ip in iplist:
            node = request.cNode.add()
            node.ip = ip
            #node.hostname = socket.gethostbyaddr(ip)[0]
            #request.cNodelist += node.hostname + ' '
            node.hostname = ''
            request.cNodelist += ip + ' '
            node.port = '50001'
            node.passwd = 'root123'

        self.stub.init_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def stop(self,params = {}):
        request = puma_pb2.ClusterStopReq()
        node = params.get('cluster_node')
        if node == 'all':
            request.node = ''
        else:
            request.node = node.replace(',',' ')
        self.stub.stop_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def start(self,params = {}):
        request = puma_pb2.ClusterStartReq()
        node = params.get('cluster_node')
        if node == 'all':
            request.node = ''
        else:
            request.node = node.replace(',',' ')
        self.stub.start_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def property(self,params = {}):
        if params.has_key('set-option'):
            optlist = params.get('set-option').split(',')
            code = 'set'
        elif params.has_key('unset-option'):
            optlist = params.get('unset-option').split(',')
            code = 'unset'
        elif params.has_key('all'):
            optlist = []
            code = 'all'
        elif params.has_key('defualt'):
            optlist = []
            code = 'default'
        else:
            optlist = []
            code = ''

        request = puma_pb2.ClusterPropertyReq()
        request.code = code
        for op in optlist:
            opt = request.opt.add()
            if code == 'unset':
                opt.pName = op
                opt.pValue =' '
            else:
                opt.pName = op.split('=')[0]
                opt.pValue = op.split('=')[1]
        self.stub.set_property_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def commit(self,params = {}):
        request = puma_pb2.CommitReq()
        self.stub.commit_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def rollback(self,params = {}):
        request = puma_pb2.RollBackReq()
        self.stub.rollback_cluster(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
        
    def GetHostname(self,nodelist):
        result = ''
        if nodelist == 'all':
            return result
        elif ',' in nodelist:
            for node in nodelist.split(','):
                result += socket.gethostbyaddr(node)[0]+ ' '
        else:
            result = socket.gethostbyaddr(nodelist)[0]
        return result

    def status(self,params):
        request = puma_pb2.GetClusterReq()
        request.detail_flag = True
        self.stub.get_cluster_state(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def heartbeat(self,params = {}):
        request = puma_pb2.SetHeartbReq()
        request = self.set_hb_paramter(params,request)
        self.stub.set_heartbeat(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def getname(self,params = {}):
        request = puma_pb2.SetPointReq()
        self.stub.get_cluster_name(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def rename(self,params = {}):
        request = puma_pb2.SetClusterNameReq()
        if not params.has_key('name'):
            raise Exception('miss the cluster name,please specify a vaild cluster name')
        request.cluster_name = params.get('name')
        self.stub.set_cluster_name(None,request,None)
        response = self.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def set_hb_paramter(self,params,req):
        def get_hb_dict(opt_str):
            opt_list = opt_str.split(',')
            tmp_dict = {}
            for opt in opt_list:
                value = opt.split('=')
                if len(value) != 2:
                    raise Exception('bad input options[%s] please check the format' % opt)
                tmp_dict[value[0]] = value[1]
            if not tmp_dict.has_key('hb'):
                raise Exception('miss heartbeat')
            if not tmp_dict.has_key('host'):
                raise Exception('miss host')
            return tmp_dict
        node1_dict = get_hb_dict(params.get('hb1'))
        req.hb1.hb = node1_dict.get('hb')
        req.hb1.host = node1_dict.get('host')
        if node1_dict.has_key('cidr_netmask'):
            req.hb1.cidr_netmask = node1_dict.get('cidr_netmask')
        node2_dict = get_hb_dict(params.get('hb2'))
        req.hb2.hb = node2_dict.get('hb')
        req.hb2.host = node2_dict.get('host')
        if node2_dict.has_key('cidr_netmask'):
            req.hb2.cidr_netmask = node2_dict.get('cidr_netmask')
        if params.has_key('passwd'):
            req.passwd = params.get('passwd')
        return req
