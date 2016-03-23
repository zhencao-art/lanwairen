# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../")))
import client

from rpc_auth_handle import *
from rpc_raid_handle import *
from rpc_lv_handle   import *
from rpc_vg_handle   import *
from rpc_disk_handle import *

from rpc_resource_handle import *
from rpc_pcs_handle import *
from rpc_constraint_handle import *
from rpc_stonith_handle import *

class CRpcFactory:
    def __init__(self,srv):
        ip = srv['ip']
        port = srv['port']
        self.client = client.CClient(ip,port)
        self.client.set_remote_call_timeout_max(20000)
        self.stub = self.client.stub()
        self.handle_set = {}
    
    def create_auth_handle(self):
        handle_name = 'auth'
        if self.handle_set.has_key(handle_name):
            return self.handle_set[handle_name]
        else:
            handle = CRpcAuthHandle(self.client,self.stub)
            self.handle_set[handle_name] = handle
            return handle

    def create_raid_handle(self):
        handle_name = 'raid'
        if self.handle_set.has_key(handle_name):
            return self.handle_set[handle_name]
        else:
            handle = CRpcRaidHandle(self.client,self.stub)
            self.handle_set[handle_name] = handle
            return handle

    def create_lv_handle(self):
        handle_name = 'lv'
        if self.handle_set.has_key(handle_name):
            return self.handle_set[handle_name]
        else:
            handle = CRpcLVHandle(self.client,self.stub)
            self.handle_set[handle_name] = handle
            return handle

    def create_vg_handle(self):
        handle_name = 'vg'
        if self.handle_set.has_key(handle_name):
            return self.handle_set[handle_name]
        else:
            handle = CRpcVGHandle(self.client,self.stub)
            self.handle_set[handle_name] = handle
            return handle

    def create_disk_handle(self):
        handle_name = 'disk'
        if self.handle_set.has_key(handle_name):
            return self.handle_set[handle_name]
        else:
            handle = CRpcDiskHandle(self.client,self.stub)
            self.handle_set[handle_name] = handle
            return handle
    
    def create_resource_handle(self):
        if self.handle_set.has_key('resource'):
            return self.handle_set.get('resource')
        else:
            resHandle = CRpcResourceHandle(self.client,self.stub)
            self.handle_set['resource'] = resHandle
            return resHandle
    
    def create_pcs_handle(self):
        if self.handle_set.has_key('pcs'):
            return self.handle_set.get('pcs')
        else:
            resHandle = CRpcPcsHandle(self.client,self.stub)
            self.handle_set['pcs'] = resHandle
            return resHandle

    def create_constraint_handle(self):
        if self.handle_set.has_key('constraint'):
            return self.handle_set.get('constraint')
        else:
            resHandle = CRpcConstraintHandle(self.client,self.stub)
            self.handle_set['constraint'] = resHandle
            return resHandle

    def create_stonith_handle(self):
        if self.handle_set.has_key('stonith'):
            return self.handle_set.get('stonith')
        else:
            resHandle = CRpcStonithHandle(self.client,self.stub)
            self.handle_set['stonith'] = resHandle
            return resHandle
