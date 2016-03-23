# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
import puma_pb2

class CClient:
    def __init__(self,server_ip,server_port):
        init()
        self.channel = RcfProtoChannel(TcpEndpoint(server_ip,server_port))

    def set_async_remote_call(self):
        self.channel.SetAsynchronousRpcMode(True)

    def set_connect_timeout_max(self,timeout):
        self.channel.SetConnectTimeoutMs(timeout*1000)

    def set_remote_call_timeout_max(self,timeout):
        self.channel.SetRemoteCallTimeoutMs(timeout*1000)

    def get_response(self):
        return self.channel.GetResponse()

    def stub(self):
        self.stub = puma_pb2.RpcService_Stub(self.channel)

        return self.stub
