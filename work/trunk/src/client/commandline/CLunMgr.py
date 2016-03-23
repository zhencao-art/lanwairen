# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *
import sys , os ,commands ,socket
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../server")))
import puma_pb2

class CLunMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['lun']
        self.view = CViewMgr() 

    def cli_add(self,params={}):
        req = puma_pb2.AddLunReq()
        req = self.set_lun_paramters(params,req)
        self.srv.stub.add_lun(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
    
    def set_lun_paramters(self,params,req):
        if not params.has_key('ip') or not params.has_key('path'):
            raise Exception('please input ip and path to specify a lun')
        ip = params.get('ip')
        path = params.get('path')
        resOpt =  params.get('options')
        opt_dict = {}
        if resOpt:
            optlist = resOpt.split(',')
            for op in optlist:
                value = op.split('=')
                if len(value) != 2:
                    raise Exception('option[%s] has invalid format' % resOpt)
                opt_dict[value[0]] = value[1]
        req.ip.ip = ip
        req.lu.path = path
        if opt_dict.has_key('nic'):
            req.ip.nic = opt_dict.get('nic')
        if opt_dict.has_key('cidr_netmask'):
            req.ip.cidr_netmask = opt_dict.get('cidr_netmask')
        if opt_dict.has_key('lun'):
            req.lu.lun = opt_dict.get('lun')
        if opt_dict.has_key('allowed_initiators'):
            req.lu.allowed_initiators = opt_dict.get('allowed_initiators')
        return req

    def cli_delete(self,params = {}):
        if not params.has_key('ip') and not params.has_key('path'):
            raise Exception('please input ip and path to specify a lun')
        request = puma_pb2.DeleteLunReq()
        if params.has_key('ip'):
            request.ip = params.get('ip')
        if params.has_key('path'):
            request.device_path = params.get('path')
        self.srv.stub.delete_lun(None,request,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cli_list(self,params = {}):
        req = puma_pb2.GetLunReq()
        self.srv.stub.get_lun(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return self.view.list_view(self.set_lun_list(response.ret.msg))

    def set_lun_list(self,msg):
        result = []
        lun_list = eval(msg)
        show_key_list = ['implementation' ,'lun_status','path','ip','group','target_iqn','lun']
        for lun in lun_list:
            tmp_dict = {}
            for k in lun:
                if k in show_key_list:
                    tmp_dict[k] = lun.get(k)
            if not tmp_dict.has_key('ip'):
                tmp_dict['ip'] = ''
            if not tmp_dict.has_key('path'):
                tmp_dict['path'] = ''
            if not tmp_dict.has_key('implementation'):
                tmp_dict['implementation'] = ''
            if not tmp_dict.has_key('lun'):
                tmp_dict['lun'] = ''
            if not tmp_dict.has_key('target_iqn'):
                tmp_dict['target_iqn'] = ''
            result.append(tmp_dict)
        return result
        
    def cli_update(self,params = {}):
        req = puma_pb2.AddLunReq()
        req = self.set_lun_paramters(params,req)
        self.srv.stub.update_lun(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cli_debug(self,params = {}):
        if not params.has_key('ip') or not params.has_key('path'):
            raise Exception('please input ip and path to specify a lun')
        request = puma_pb2.DeleteLunReq()
        request.ip = params.get('ip')
        request.device_path = params.get('path')
        self.srv.stub.check_lun(None,request,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg



