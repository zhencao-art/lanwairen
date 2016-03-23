# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import CViewMgr
from cmd_option import *

class CStnMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['stonith']
        self.view = CViewMgr() 

    def cli_add(self,params={}):
        if not params.has_key('type') or not params.has_key('name') or not params.has_key('option'):
            raise Exception('bad param options')
        return self.srv.create_stonith_handle().create(params)

    def cli_update(self,params={}):
        return self.srv.create_stonith_handle().update(params)
        

    def cli_delete(self,params={}):
        if not params.has_key('name'): 
            raise Exception('bad param options')
        return self.srv.create_stonith_handle().delete(params)

    def cli_list(self,params={}):
        rtn = self.srv.create_stonith_handle().list(params)
        return self.view.list_view(eval(rtn),count=True)

    def cli_info(self,params={}):
        if not params.has_key('name'): 
            raise Exception('bad param options')
        rtn = self.srv.create_stonith_handle().info(params)
        return self.view.list_view(eval(rtn))

    def cli_enable(self,params={}):
        if  len(params) != 2:
            raise Exception('you must imput two stonith options at least')
        rtn = self.srv.create_stonith_handle().enable(params)
        return rtn

    def cli_disable(self,params={}):
        if  len(params) != 2:
            raise Exception('you must imput two stonith options at least')
        rtn = self.srv.create_stonith_handle().disable(params)
        return rtn

