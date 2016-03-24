# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
import puma_pb2

sys.path.append(os.path.abspath(os.path.join(__file__,"../../ip")))
from CIPMgr import get_peer_ip

sys.path.append(os.path.abspath(os.path.join(__file__,"../../db")))
import configuredb

sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
import client

sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
import globalvar

import threading,logging
from time import sleep

import json

def db_sync_request(content):
    json_obj = json.loads(content)
    configuredb.db_file_store(json_obj,True)
    logging.info('Save the updates of the db file')

##private
def db_file_sync_remote(json_obj):
    try:
        peer_ip = get_peer_ip()
        rpc_client = client.CClient(peer_ip,globalvar.listen_port)
    except Exception as e:
        msg = 'Get RPC Client Error %s' % str(e)
        logging.error(msg)
        return (-1,msg)
    rpc_stub = rpc_client.stub()

    content = json.dumps(json_obj)
    request = puma_pb2.DBFileSyncReq()
    request.content = content

    try:
        rpc_stub.db_file_sync(None,request,None)
    except Exception as e:
        msg = 'Sync db file error,%s' % str(e)
        return (-1,msg)
    response = rpc_client.get_response()
    if response.ret.retcode != 0:
        msg = 'Sync db file error,RPC Call error %s' % response.ret.msg
        return (-1,msg)
    return (0,None)

def sync_stop():
    g_sync_stop = True

def do_loop():
    configuredb.g_db_rw_lock.read_lock()
    db_handle = configuredb.db_file_load()
    if not configuredb.db_file_get_sync(db_handle):
        configuredb.g_db_rw_lock.read_unlock()
        (ret,msg) = db_file_sync_remote(db_handle)
        if ret != 0:
            logging.error('Sync thread sync to remote error,%s' % msg)
        else:
            logging.info('Sync thread sync to remote success')
            configuredb.g_db_rw_lock.write_lock()
            configuredb.db_file_set_sync()
            configuredb.g_db_rw_lock.write_unlock()

def sync_thread_main():
    logging.info('Sync db file thread stared')
    while not g_sync_stop:
        sleep(3)
        do_loop()
    logging.info('Sync db file thread stopped')

g_sync_stop   = False
