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

request = puma_pb2.AddLunReq()
request.ip.ip = '172.16.9.20'
request.lu.path = '/dev/vgh/grp02'
acess = request.lu.allowed_initiators.add()
acess.iqn = 'iqn.2016-02.hcw.com.cn:123'
acess.acess = 'ro'
stub = client.stub()
stub.update_lun(None,request,None)
response = client.get_response()
print str(response)

