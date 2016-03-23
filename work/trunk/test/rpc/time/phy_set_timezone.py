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

request = puma_pb2.SetTimezoneReq()
request.tz.tz = 'Asia/Chongqing'
stub = client.stub()
stub.set_timezone(None,request,None)
response = client.get_response()
print str(response)

