# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *
from service_impl import *

class CServer:
    def __init__(self,ip,port):
        init()
        self.server  = RcfProtoServer(TcpEndpoint(ip,port))
        self.server.BindService(CServiceImpl())

    def set_thread_pool(self,name,thread_max):
        thread_pool = ThreadPool(1,thread_max)
        thread_pool.SetThreadName(name)
        self.server.SetThreadPool(thread_pool)

    def start(self):
        self.server.Start()
