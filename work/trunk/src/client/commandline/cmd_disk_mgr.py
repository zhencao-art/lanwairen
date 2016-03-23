# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *

class CCmdDiskMgr:
    def __init__(self,factory,params = {}):
        self.handle = factory.create_disk_handle()

        self.opt = cmd_option['disk']
        self.view = CViewMgr()
    
    def cli_list(self,params = {}):
        (result,keys) = self.handle.list(params)
        return self.view.list_view(result,key_list = keys)
    def cli_init(self,params = {}):
        if not params.has_key('name'):
            raise Exception("Missing option name")
        self.handle.init(params)
        return "Success"
