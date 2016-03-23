# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/server")))
import puma_pb2

client = client.CClient("127.0.0.1",50001)

request = puma_pb2.StonithIPMIReq()
st1 = request.attr.add()
st1.host = 'node1'
st1.ip = '172.16.9.20'
st1.username = 's1'
st1.passwd = '123'
st1.id = 'fencing_ipmi_node1'
st2 = request.attr.add()
st2.host = 'node3'
st2.ip = '172.16.9.19'
st2.username = 's2'
st2.passwd = '456'
st2.id = 'fencing_ipmi_node3'
stub = client.stub()
stub.disable_stonith_ipmi(None,request,None)
response = client.get_response()
print str(response)

