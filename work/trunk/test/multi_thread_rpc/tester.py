import threading

from deltavsoft.rcfproto import *
import os,sys

sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/client")))
import client
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../src/server")))
import puma_pb2

def thread_callback_fun_0():
    client_l = client.CClient("127.0.0.1",50005)
    request = puma_pb2.LvmVGScanPVReq()
    request.vg_name = "test_vgs"
    client_l.stub().scan_pv_lvm_vg(None,request,None)
    response = client_l.get_response()
    print threading.current_thread().name + " ---> " + str(response)

def thread_callback_fun_1():
    client_l = client.CClient("127.0.0.1",50005)
    request = puma_pb2.LvmVGScanLVReq()
    request.vg_name = "test_vgs"
    client_l.stub().scan_lv_lvm_vg(None,request,None)
    response = client_l.get_response()
    print threading.current_thread().name + " ---> " + str(response)


thread_list = []

for i in range(1,5):
    if i%2 == 0:
        thread_callback_fun = thread_callback_fun_0
    else:
        thread_callback_fun = thread_callback_fun_1

    thread_list.append(threading.Thread(target = thread_callback_fun,name="thread_" + str(i)))

for i in range(0,4):
    thread_list[i].start()

for i in range(0,4):
    thread_list[i].join()
