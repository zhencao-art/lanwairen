# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import CViewMgr
from cmd_option import *

class CCmdRaidMgr:
    def __init__(self,factory,params = {}):
        self.handle = factory.create_raid_handle()
        self.opt = cmd_option['raid']
        self.view = CViewMgr()

    def cli_create(self,params = {}):
        if not params.has_key('md_name'):
            raise Exception("Missing option name")
        if not params.has_key('md_level'):
            raise Exception("Missing option level")
        if not params.has_key('md_phys'):
            raise Exception("Missing option P")
        pds = params['md_phys']
        if len(pds.split(',')) < 1:
            raise Exception("option P is not vaild")

        if not '1' == params['md_level']:
            if not params.has_key('md_width'):
                raise Exception("Missing option width")
        self.handle.create(params)
        return "Success"

    def cli_list(self,params = {}):
        (result,keys) = self.handle.list(params)
        return self.view.list_view(result,key_list = keys)

    def cli_info(self,params = {}):
        if not params.has_key('md_name'):
            raise Exception("Missing option name")
        result = self.handle.info(params)
        return self.view.list_view(result)

    def cli_extend(self,params = {}):
        if not params.has_key('md_name'):
            raise Exception("Missing option name")
        if not params.has_key('md_phys'):
            raise Exception("Missing option P")
        pds = params['md_phys']
        if len(pds.split(',')) < 1:
            raise Exception("option P is not vaild")
        self.handle.extend(params)
        return "Success"

    def cli_reduce(self,params = {}):
        if not params.has_key('md_name'):
            raise Exception("Missing option name")
        if not params.has_key('md_phys'):
            raise Exception("Missing option P")
        pds = params['md_phys']
        if len(pds.split(',')) < 1:
            raise Exception("option P is not vaild")
        self.handle.extend(params)
        return "Success"

    def cli_remove(self,params = {}):
        if not params.has_key('md_name'):
            raise Exception("Missing option name")
        if params.has_key('rm_drast'):
            params['rm_drast'] = True
        else:
            params['rm_drast'] = False

        self.handle.remove(params)
        return "Success"
