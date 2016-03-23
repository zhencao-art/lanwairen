# vim: tabstop=4 shiftwidth=4 softtabstop=4
import sys , os ,commands
#sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
from view.view_mgr import *
from cmd_option import *

class CResMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['resource']
        self.view = CViewMgr()

    def cli_add(self,params={}):
        if not params.has_key('option'):
            raise Exception('bad param options')
        return self.srv.create_resource_handle().create(params)

    def cli_update(self,params={}):
        if not params.has_key('option'):
            raise Exception('bad param options')
        return self.srv.create_resource_handle().update(params)

    def cli_delete(self,params={}):
        if not params.has_key('name') and  not params.has_key('option'):
            raise Exception('bad param options')
        return self.srv.create_resource_handle().remove(params)

    def cli_list(self,params={}):
        rtn = self.srv.create_resource_handle().list(params)
        return self.view.list_view(eval(rtn))

    def cli_info(self,params={}):
        if not params.has_key('name') and not params.has_key('type'):
            raise Exception('miss name param')
        rtn = self.srv.create_resource_handle().info(params)
        return self.view.list_view(eval(rtn))

    def cli_master(self,params={}):
        if not params.has_key('master_name') or not params.has_key('res_name'):
            raise Exception('miss name param')
        rtn = self.srv.create_resource_handle().master(params)
        return rtn

    def cli_clone(self,params={}):
        if not params.has_key('name'):
            raise Exception('miss name param')
        rtn = self.srv.create_resource_handle().clone(params)
        return rtn

    def cli_group(self,params = {}):
        if not params.has_key('name') or not params.has_key('option'):
            raise Exception('miss name param')
        rtn = self.srv.create_resource_handle().group(params)
        return rtn

    def cli_move(self,params = {}):
        if not params.has_key('name') or not params.has_key('node'):
            raise Exception('bad param options')
        rtn = self.srv.create_resource_handle().move(params)
        return rtn

    def cli_stop(self,params = {} ):
        if not params.has_key('name'):
            raise Exception('bad param options')
        rtn = self.srv.create_resource_handle().stop(params)
        return rtn

    def cli_debug(self,params = {} ):
        if not params.has_key('name'):
            raise Exception('bad param options')
        rtn = self.srv.create_resource_handle().debug(params)
        return rtn

    def cli_cleanup(self,params={}):
        rtn = self.srv.create_resource_handle().cleanup(params)
        return rtn
