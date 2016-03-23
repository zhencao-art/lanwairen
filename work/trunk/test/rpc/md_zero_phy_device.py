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

request = puma_pb2.MdZeroPhyDeviceReq()

request.md_phy_devices.add().dev_name = "/dev/sdd"
request.md_phy_devices.add().dev_name = "/dev/sde"

print str(request)
client.stub().zero_md_phy_device(None,request,None)

response = client.get_response()

print str(response)
