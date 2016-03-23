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

request = puma_pb2.SetTimeReq()
request.time.year = 2016
request.time.mon = 1
request.time.day = 29
request.time.hour = 17
request.time.min = 1
request.time.sec = 1
request.time.wday = 5
stub = client.stub()
stub.set_time(None,request,None)
response = client.get_response()
print str(response)

