# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/server")))
import puma_pb2

client = client.CClient("127.0.0.1",50000)

request = puma_pb2.MdCreateReq()

request.md_name = "/dev/md1"
request.md_level = 0
request.md_chunk = 16
phy_device = request.md_phy_devices.add()
phy_device.dev_name = "/dev/sdb"
phy_device = request.md_phy_devices.add()
phy_device.dev_name = "/dev/sdc"

print str(request)
client.stub().create_md_device(None,request,None)

response = client.get_response()

print str(response)
