# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from deltavsoft.rcfproto import *

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/server")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../../src/mid")))
import puma_pb2 , block_mgr

client = client.CClient("172.24.8.109",50001)
stub = client.stub()
block_mgr.cluster_mdadm_config_set(client,stub,'pacemaker22')

