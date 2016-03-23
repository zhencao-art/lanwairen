# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *
import sys , os ,commands ,socket
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../server")))
import puma_pb2

class CIpMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['ip']
        self.view = CViewMgr() 

    def cli_add(self,params={}):
        if not params.has_key('ip') or not params.has_key('nic'):
            raise Exception('lose ip or nic options')
        req = puma_pb2.SetIpReq()
        if not params.has_key('cluster_node'):
            req.node = 'local'
        else:
            req.node = params.get('cluster_node')
        req.addFlag = True
        req.ipOpt.ip = params.get('ip')
        req.ipOpt.nic = params.get('nic')
        if params.has_key('cidr_netmask'):
            req.ipOpt.cidr_netmask = params.get('cidr_netmask')
        if params.has_key('gateway'):
            req.ipOpt.gate_way = params.get('gateway')
        self.srv.stub.add_ip(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cli_heartbeat(self,params={}):
        if not params.has_key('ip'):
            raise Exception('lose heartbeat address options')
        req = puma_pb2.SetIpReq()
        if not params.has_key('cluster_node'):
            req.node = 'local'
        req.ipOpt.ip = params.get('ip')
        if params.has_key('cidr_netmask'):
            req.ipOpt.cidr_netmask = params.get('cidr_netmask')
        self.srv.stub.add_heartbeat_ip(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cli_delete(self,params = {}):
        if not params.has_key('ip') or not params.has_key('nic'):
            raise Exception('lose ip or nic options')
        req = puma_pb2.SetIpReq()
        if not params.has_key('cluster_node'):
            req.node = 'local'
        else:
            req.node = params.get('cluster_node')
        req.addFlag = False
        req.ipOpt.ip = params.get('ip')
        req.ipOpt.nic = params.get('nic')
        if params.has_key('cidr_netmask'):
            req.ipOpt.cidr_netmask = params.get('cidr_netmask')
        self.srv.stub.delete_ip(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cli_list(self,params = {}):
        req = puma_pb2.GetIpReq()
        if not params.has_key('cluster_node'):
            pass
        else:
            req.node = params.get('cluster_node')
        self.srv.stub.get_ip(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return self.view.list_view(eval(response.ret.msg))
        
    def cli_nic(self,params = {}):
        req = puma_pb2.GetIpReq()
        if not params.has_key('cluster_node'):
            pass
        else:
            req.node = params.get('cluster_node')
        self.srv.stub.get_nic(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return self.view.list_view(eval(response.ret.msg))
