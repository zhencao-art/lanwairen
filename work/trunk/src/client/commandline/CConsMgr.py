# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *
class CConsMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['constraint']
        self.view = CViewMgr()

    def cli_add(self,params={}):
        if not params.has_key('type') or not params.has_key('option'):
            raise Exception('bad param options')
        return self.srv.create_constraint_handle().create(params)

    def cli_delete(self,params={}):
        if not params.has_key('name') and not params.has_key('id'):
            raise Exception('bad param options')
        return self.srv.create_constraint_handle().remove(params)

    def cli_list(self,params={}):
        rtn = self.srv.create_constraint_handle().list(params)
        return self.view.list_view(eval(rtn))

    def cli_info(self,params={}):
        if not params.has_key('id') and not params.has_key('name'):
            raise Exception('bad param options')
        rtn = self.srv.create_constraint_handle().info(params)
        return self.view.list_view(eval(rtn))

