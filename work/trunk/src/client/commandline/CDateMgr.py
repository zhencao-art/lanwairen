# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *
import sys , os ,commands ,socket
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../server")))
import puma_pb2

class CDateMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['date']
        self.view = CViewMgr() 

    def cli_timeinfo(self,params={}):
        req = puma_pb2.TimezoneReq()
        self.srv.stub.get_current_time(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        time = str(response.time.year) + '-' + str(response.time.mon) + '-' + str(response.time.day) + ' ' + str(response.time.hour) + ':' + str(response.time.min) + ':' + str(response.time.sec)
        tmp_dict = {}
        tmp_dict['time'] = time
        return self.view.info_view(tmp_dict)

    def cli_tzinfo(self,params={}):
        req = puma_pb2.TimezoneReq()
        self.srv.stub.get_current_tz(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        tmp_dict = {}
        tmp_dict['timezone'] = response.tz[0].tz
        return self.view.info_view(tmp_dict)

    def cli_tzlist(self,params={}):
        req = puma_pb2.TimezoneReq()
        self.srv.stub.list_timezone(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        rtn = []
        for timezone in response.tz:
            tmp_dict = {}
            tmp_dict['time'] = timezone.tz
            rtn.append(tmp_dict)
        return self.view.list_view(rtn)

    def cli_timeset(self,params = {}):
        if not params.has_key('time') or not params.has_key('date'):
            raise Exception('please input entire datetime options')
        date = params.get('date').split('-')
        time = params.get('time').split(':')
        req = puma_pb2.SetTimeReq()
        req.time.year = int(date[0])
        req.time.mon = int(date[1])
        req.time.day = int(date[2])
        req.time.hour = int(time[0])
        req.time.min = int(time[1])
        req.time.sec = int(time[2])
        req.time.wday = 0
        self.srv.stub.set_time(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg

    def cli_tzset(self,params = {}):
        if not params.has_key('timezone'):
            raise Exception('please input the timezone')
        req = puma_pb2.SetTimezoneReq()
        req.tz.tz = params.get('timezone')
        self.srv.stub.set_timezone(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return response.ret.msg
        
    def cli_ntpinfo(self,params = {}):
        req = puma_pb2.NtpGetConfReq()
        self.srv.stub.cluster_ntp_get_conf(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        if response.status:
            return 'ntp serevr running'
        else:
            return 'ntp server not running'
        return response

    def cli_ntpset(self,params = {}):
        if not params.has_key('timezone'):
            raise Exception('miss timezone')
        if not params.has_key('cluster_node'):
            raise Exception('miss host node')
        if not params.has_key('url'):
            raise Exception('miss pulic url')
        req = puma_pb2.NtpSetupReq()
        req.timezone = params.get('timezone')
        req.node_ip = params.get('cluster_node')
        req.public_url = params.get('url')
        self.srv.stub.cluster_ntp_setup(None,req,None)
        response = self.srv.client.get_response()
        if response.ret.retcode != 0:
            raise Exception(response.ret.msg)
        return 'setup ntp server success'

