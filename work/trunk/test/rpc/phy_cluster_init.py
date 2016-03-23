# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/server")))
import puma_pb2

client = client.CClient("172.16.9.108",50001)

request = puma_pb2.ClusterInitReq()
node = request.cNode.add()
node.hostname = 'node1'
node.ip = '172.16.9.108'
node.port = '50001'
node.passwd = 'root123'
node = request.cNode.add()
node.hostname = 'node3'
node.ip = '172.16.9.109'
node.port = '50001'
node.passwd = 'root123'
request.cPasswd = 'hacluster'
request.clusterName = 'pamk1o1'
request.flag = 2
request.cNodelist = 'node1 node3'
client.stub().init_cluster(None,request,None)

response = client.get_response()

print str(response)
