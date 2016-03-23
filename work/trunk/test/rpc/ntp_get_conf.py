# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/server")))
import puma_pb2

client = client.CClient("127.0.0.1",50005)

request = puma_pb2.NtpGetConfReq()

print str(request)
client.stub().cluster_ntp_get_conf(None,request,None)

response = client.get_response()

print str(response)
