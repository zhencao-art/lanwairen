# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../time/ntp-conf")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../time")))
import ntp,puma_pb2 ,CDateTime

def ntp_client_setup(timezone,url):
    ##timezone setup
    CDateTime.SetTz(timezone)
    ntp.ntp_client_set(url)
    ntp.ntp_restart()
    ntp.ntp_enable()

def ntp_server_setup(timezone,public_url):
    ##timezone setup
    CDateTime.SetTz(timezone)

    ntp.ntp_server_set(public_url)
    ntp.ntp_restart()
    ntp.ntp_enable()

def ntp_check_server_conf():
    conf = ntp.ntp_cur_conf()

    if conf.has_key('restrict'):
        pass
    else:
        return (False,"")

    return (True,conf['server'])

def ntp_status():
    if ntp.ntp_status() != 0:
        return False
    else:
        return True

def remote_ntp_check_server_conf(rpc_client,rpc_stub):
    request = puma_pb2.NtpGetConfReq()

    rpc_stub.ntp_get_conf(None,request,None)
    response = rpc_client.get_response()

    if response.ret.retcode != 0:
        raise Exception("Remote RPC CALL ntp_get_conf failed,%s" % response.ret.msg)

    return response

def remote_ntp_client_setup(rpc_client,rpc_stub,timezone,url):
    request = puma_pb2.NtpClientSetupReq()

    request.timezone = timezone
    request.url = url

    rpc_stub.ntp_client_setup(None,request,None)
    response = rpc_client.get_response()

    if response.ret.retcode != 0:
        raise Exception("Remote RPC CALL ntp_client_setup failed,%s" % response.ret.msg)

def remote_ntp_server_setup(rpc_client,rpc_stub,timezone,public_url):
    request = puma_pb2.NtpServerSetupReq()
    request.timezone = timezone
    request.public_url = public_url

    rpc_stub.ntp_server_setup(None,request,None)
    response = rpc_client.get_response()

    if response.ret.retcode != 0:
        raise Exception("Remote RPC CALL ntp_server_setup failed,%s" % response.ret.msg)
