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

request = puma_pb2.NtpSetupReq()

request.timezone = "Asia/Shanghai"
request.node_ip = '172.24.8.96'
request.public_url = "202.120.2.101"

print str(request)
client.stub().cluster_ntp_setup(None,request,None)

response = client.get_response()

print str(response)
