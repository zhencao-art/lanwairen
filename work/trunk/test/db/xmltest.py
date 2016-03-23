#!/usr/bin/env python


import os,sys,commands
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/db")))

import CConfigMgr , client

cfg = CConfigMgr.CConfigMgr('just.conf',True)

node = ['raids']
import pdb
#pdb.set_trace()
try:
    try:
        e = cfg.GetNode(node)
        e = cfg.GetNode(['lvms'])
    except Exception as e:
        cfg.AddNode(None,'raids')
        cfg.AddNode(None,'lvms')
    node = ['raids']
    cfg.AddNode(node,'raid',{'raid-name':'/dev/md1','raid-devices':'/dev/sdc'})
    print node
    rtn = cfg.AddNode(node,'raid',{'raid-name':'/dev/md2','raid-devices':'/dev/sdc'})
    print node
    cfg.AddNode(['lvms'],'lvm',{'lvm-name':'lv1'})
except Exception as e:
    print str(e)
    exit() 

cli = client.CClient('172.16.9.108',50001)

cfg.Commit(cli)
