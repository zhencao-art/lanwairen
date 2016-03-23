# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/server")))
import puma_pb2

client = client.CClient("172.16.9.108",50001)

request = puma_pb2.AddStonithReq()
request.stName = 'myfence'
request.stType = 'fence_scsi'
opt = request.stOpt.add()
opt.key =  'devices'
opt.value = '/dev/sdd'

client.stub().add_cluster_stonith(None,request,None)

response = client.get_response()

print str(response)
