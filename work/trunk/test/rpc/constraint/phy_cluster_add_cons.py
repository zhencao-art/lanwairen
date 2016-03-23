# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/server")))
import puma_pb2
if len(sys.argv) < 3:
    print 'please input constraint options'
    exit()
client = client.CClient("172.16.9.108",50001)

request = puma_pb2.AddConstraintReq()
request.consType = sys.argv[1]
index = 2
while(index<len(sys.argv)):
    opt = request.consOpt.add()
    opt.key = sys.argv[index]
    opt.value = sys.argv[index+1]
    index = index+2

client.stub().add_cluster_cons(None,request,None)

response = client.get_response()

print str(response)
