# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/server")))
import puma_pb2

client = client.CClient("172.24.8.108",50001)

request = puma_pb2.AddLunReq()
ip = request.ip
ip.ip = '172.16.9.110'
ip.nic = 'eth0'
tgt = request.tgt
lu = request.lu
lu.path = '/dev/vgh/lv00'
stub = client.stub()
stub.add_lun(None,request,None)
response = client.get_response()
print str(response)


#request = puma_pb2.AddCluResourceReq()
#'''
#add lvm
#'''
#request.resName = 'mylvm'
#request.resType = 'ocf:heartbeat:LVM'
#opt = request.resOpt.add()
#opt.key =  'volgrpname'
#opt.value = 'vgr0'
#
#stub.add_cluster_resource(None,request,None)
#response = client.get_response()
#print str(response)
#
#
#request = puma_pb2.AddCluResourceReq()
#'''
#add target 
#'''
#request.resName = 'target2'
#request.resType = 'ocf:heartbeat:iSCSITarget'
#opt = request.resOpt.add()
#opt.key =  'implementation'
#opt.value = 'lio-t'
#opt = request.resOpt.add()
#opt.key =  'iqn'
#opt.value = 'iqn.2015-12.localhost.com.cn'
#opt = request.resOpt.add()
#opt.key =  'tid'
#opt.value = '2'
#
#stub.add_cluster_resource(None,request,None)
#response = client.get_response()
#print str(response)
#
#
#request = puma_pb2.AddCluResourceReq()
#'''
#add logicalunit
#'''
#request.resName = 'myUnit2'
#request.resType = 'ocf:heartbeat:iSCSILogicalUnit'
#opt = request.resOpt.add()
#opt.key =  'implementation'
#opt.value = 'lio-t'
#opt = request.resOpt.add()
#opt.key =  'lun'
#opt.value = '2'
#opt = request.resOpt.add()
#opt.key =  'path'
#opt.value = '/dev/sdd2'
#opt = request.resOpt.add()
#opt.key =  'target_iqn'
#opt.value = 'iqn.2015-12.localhost.com.cn'
#
#stub.add_cluster_resource(None,request,None)
#response = client.get_response()
#print str(response)
