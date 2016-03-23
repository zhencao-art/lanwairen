# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *

class CCmdVGMgr:
    def __init__(self,factory,params = {}):
        self.handle = factory.create_vg_handle()

        self.opt = cmd_option['vg']
        self.view = CViewMgr()
    
    def cli_create(self,params = {}):
        if not params.has_key('vg_name'):
            raise Exception("Missing option name")
        if not params.has_key('phy_vol'):
            raise Exception("Missing option pv")
        pvs = params['phy_vol']
        if len(pvs.split(',')) < 1:
            raise Exception("phy_vol option is not vaild")
        self.handle.create(params)
        return "Success"

    def cli_list(self,params = {}):
        (result,keys) = self.handle.list(params)
        return self.view.list_view(result,key_list = keys)

    def cli_list_pv(self,params = {}):
        result = self.handle.list_pv(params)
        return self.view.list_view(result)

    def cli_info(self,params = {}):
        if not params.has_key('vg_name'):
            raise Exception("Missing option name")
        result = self.handle.info(params)
        return self.view.list_view(result)

    def cli_extend(self,params = {}):
        if not params.has_key('vg_name'):
            raise Exception("Missing option name")
        if not params.has_key('phy_vol'):
            raise Exception("Missing option pv")
        pvs = params['phy_vol']
        if len(pvs.split(',')) < 1:
            raise Exception("phy_vol option is not vaild")
        self.handle.extend(params)
        return "Success"

    def cli_reduce(self,params = {}):
        if not params.has_key('vg_name'):
            raise Exception("Missing option name")
        if not params.has_key('phy_vol'):
            raise Exception("Missing option pv")
        pvs = params['phy_vol']
        if len(pvs.split(',')) < 1:
            raise Exception("phy_vol option is not vaild")
        if params.has_key('rm_drast'):
            params['rm_drast'] = True
        else:
            params['rm_drast'] = False

        self.handle.reduce(params)
        return "Success"

    def cli_remove(self,params = {}):
        if not params.has_key('vg_name'):
            raise Exception("Missing option name")
        if params.has_key('rm_drast'):
            params['rm_drast'] = True
        else:
            params['rm_drast'] = False

        self.handle.remove(params)
        return "Success"
