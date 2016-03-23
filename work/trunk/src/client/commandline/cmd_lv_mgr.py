# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *

class CCmdLVMgr:
    def __init__(self,factory,params = {}):
        self.handle = factory.create_lv_handle()

        self.opt = cmd_option['lv']
        self.view = CViewMgr()
    
    def cli_create(self,params = {}):
        if not params.has_key('lv_name'):
            raise Exception("Missing option lv_name")
        if not params.has_key('vg_name'):
            raise Exception("Missing option vg_name")
        if not params.has_key('lv_size'):
            raise Exception("Missing option lv_size")
        self.handle.create(params)
        return "Success"

    def cli_list(self,params = {}):
        (result,keys) = self.handle.list(params)
        return self.view.list_view(result,key_list = keys)

    def cli_info(self,params = {}):
        if not params.has_key('lv_name'):
            raise Exception("Missing option lv_name")
        if not params.has_key('vg_name'):
            raise Exception("Missing option vg_name")
        (result,keys) = self.handle.info(params)
        return self.view.list_view(result,key_list = keys)

    def cli_extend(self,params = {}):
        if not params.has_key('lv_name'):
            raise Exception("Missing option lv_name")
        if not params.has_key('vg_name'):
            raise Exception("Missing option vg_name")
        if not params.has_key('lv_size'):
            raise Exception("Missing option lv_size")
        self.handle.extend(params)
        return "Success"

    def cli_reduce(self,params = {}):
        if not params.has_key('lv_name'):
            raise Exception("Missing option lv_name")
        if not params.has_key('vg_name'):
            raise Exception("Missing option vg_name")
        if not params.has_key('lv_size'):
            raise Exception("Missing option lv_size")
        self.handle.reduce(params)
        return "Success"

    def cli_remove(self,params = {}):
        if not params.has_key('lv_name'):
            raise Exception("Missing option lv_name")
        if not params.has_key('vg_name'):
            raise Exception("Missing option vg_name")
        self.handle.remove(params)
        return "Success"
