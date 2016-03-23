# vim: tabstop=4 shiftwidth=4 softtabstop=4
from view.view_mgr import *
from cmd_option import *

class CPcsMgr:
    def __init__(self, srv=None, params={}):
        self.srv  = srv
        self.opt  = cmd_option['cluster']
        self.view = CViewMgr() 

    def cli_setup(self,params={}):
        rtn = self.srv.create_pcs_handle().setup(params)
        return rtn

    def cli_start(self,params={}):
        if not params.get('cluster_node'):
            params['cluster_node'] = 'all'
        rtn = self.srv.create_pcs_handle().start(params)
        return rtn

    def cli_stop(self,params={}):
        if not params.get('cluster_node'):
            params['cluster_node'] = 'all'
        rtn = self.srv.create_pcs_handle().stop(params)
        return rtn

    def cli_property(self,params={}):
        if len(params)>1:
            raise Exception('you have input too much options')
        rtn = self.srv.create_pcs_handle().property(params)
        if params.has_key('all') or params.has_key('defualt') or len(params)==0:
            return self.view.list_view(eval(rtn))
        else:
            return rtn

    def cli_commit(self,params = {}):
        rtn = self.srv.create_pcs_handle().commit(params)
        return rtn

    def cli_rollback(self,params = {}):
        rtn = self.srv.create_pcs_handle().rollback(params)
        return rtn

    def cli_status(self,params = {}):
        rtn = self.srv.create_pcs_handle().status(params)
        return self.view.list_view(eval(rtn))

    def cli_heartbeat(self,params = {}):
        if len(params) < 2:
            raise Exception('you must specify two nodes to set the heartbeat at least')
        rtn = self.srv.create_pcs_handle().heartbeat(params)
        return rtn

    def cli_getname(self,params = {}):
        rtn = self.srv.create_pcs_handle().getname(params)
        tmp_dict = {}
        tmp_dict['cluster_name'] = rtn
        return self.view.info_view(tmp_dict)

    def cli_rename(self,params = {}):
        rtn = self.srv.create_pcs_handle().rename(params)
        return rtn

