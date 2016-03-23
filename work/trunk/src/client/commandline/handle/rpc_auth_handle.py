# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import auth_handle

class CRpcAuthHandle(auth_handle.CAuthHandle):
    def __init__(self,client,stub):
        self.client = client
        self.stub = stub

    def auth(self,user,passwd):
        pass
