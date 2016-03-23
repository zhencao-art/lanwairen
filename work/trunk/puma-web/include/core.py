# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import sys
import logging
import ConfigParser
from deltavsoft.rcfproto import *
from json import *
import importlib
import puma_pb2
from puma_pb2 import _RPCSERVICE

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S', filename='/var/log/data_script.log')
# logging.info("service name: %s" %  _RPCSERVICE.name)

class DataCore:
    def __init__(self):
        pass

    def set_obj_param(self,obj,param,ins=None):
        if ins:
            request=ins
        else:
            modu = importlib.import_module("puma_pb2")
            request_class = getattr(modu,obj.name)
            request = request_class()
        #label --- 1:optional 2:required 3:repeat
        #type  --- 11:Object 9:String  4\5\13:int 8:bool
        for field in obj.fields:
            # logging.info("field: %s" % field.name)
            # logging.info("type: %s" % field.type)
            # logging.info("label: %s" % field.label)
            if field.label==3: #list
                for field_child in obj.fields_by_name:
                  #  print obj.fields_by_name[field_child].message_type
                    if field_child==field.name:  #option is object
                        child_obj = obj.fields_by_name[field_child].message_type
                        for child in param[field.name]:
                            child_ins = getattr(request, field.name).add()
                            self.set_obj_param(child_obj,param[field.name][child],child_ins)
            elif field.label==2: #required
                if param.has_key(field.name):
                    if field.type==11:  #if object
                        child_ins = getattr(request, field.name)
                        self.set_obj_param(field.message_type,param[field.name],child_ins)
                    else:
                        key_value = int(param[field.name]) if field.type==13 or field.type==5 or field.type==4 else param[field.name]
                        setattr(request,field.name,key_value)
                else:
                    logging.warning("%s required" % field.name)
                    dataCore.exit_msg(1003)
            else:  #optional
                if param.has_key(field.name):
                    if field.type==11:
                        child_ins = getattr(request, field.name)
                        self.set_obj_param(field.message_type,param[field.name],child_ins)
                    else:
                        key_value = int(param[field.name]) if field.type==13 or field.type==5 or field.type==4 else param[field.name]
                        setattr(request,field.name,key_value)
        return request
        
    def create_obj(self,param):
        request = None;
        for m in  _RPCSERVICE.methods:
            if m.name==param["method"]:
                obj = m.input_type
                #m.input_type.name  --request class name
                request = self.set_obj_param(obj,param["param"])
                break;
        return request

    def request(self,method,request,server_ip,server_port):
        init()
        channel = RcfProtoChannel(TcpEndpoint(server_ip,server_port))
        channel.SetConnectTimeoutMs(3000)
        channel.SetRemoteCallTimeoutMs(50000)
        stub = puma_pb2.RpcService_Stub(channel)
        getattr(stub,method)(None,request,None)
        return channel.GetResponse()

    def parse_response(self,response):
        res = {}
        for k in response._fields:
            child = response._fields[k];
            res[k.name] = self.parse_child(child)
        return res
        
    def parse_child(self,child):
        if isinstance(child,google.protobuf.internal.containers.RepeatedCompositeFieldContainer):
            child_list = []
            for idx in child:
                child_list.append(self.parse_child(idx))
            return child_list
        elif hasattr(child,'__module__') and child.__module__=="puma_pb2":  #if object
            child_field_json = {}
            for child_field in child._fields:
                child_field_json[child_field.name] = self.parse_child(child._fields[child_field]);
            return child_field_json
        else:
            return child
        
    def parse_data(self,response):
        res = {}
        for k in response._fields:
            if isinstance(response._fields[k],google.protobuf.internal.containers.RepeatedCompositeFieldContainer):
                res[k.name] = self.parse_data_repeat(response._fields[k])
            else:
                child_json = {}
                for child in response._fields[k]._fields:
                    child_obj = response._fields[k]._fields[child];
                    child_json[child.name] = self.parse_data_object(child,child_obj);
                res[k.name] = child_json
        return res
        
    def parse_data_repeat(self,response):
        child_list = []
        for idx in response:
            child_json = {}
            for child in idx._fields:
                if isinstance(idx._fields[child],google.protobuf.internal.containers.RepeatedCompositeFieldContainer):
                    child_json[child.name] = self.parse_data_repeat(idx._fields[child])
                else:
                    child_obj = idx._fields[child];
                    child_json[child.name] = self.parse_data_object(child,child_obj);
            child_list.append(child_json)
        return child_list
        
    def parse_data_object(self,child,child_obj):
        child_json = {}
        if child.type==11:  #if object
            child_field_json = {}
            for child_field in child_obj._fields:
                child_field_json[child_field.name] = child_obj._fields[child_field];
            return child_field_json
        else:
            return child_obj
    
    def parse_param(self,param):
        return JSONDecoder().decode(param);

    def exit_msg(self,error_code):
        print "{\"ret\":{\"retcode\":",error_code,"}}"
        exit(error_code)
    
    def load_config(self,path):
        cf = ConfigParser.ConfigParser()
        cf.read(path)
        res = {}
        if cf.has_option("service","ip"):
            res["server_ip"] = cf.get("service", "ip");
        if cf.has_option("service","port"):
            res["server_port"] = int(cf.get("service", "port"));
        return res
        
if __name__ == '__main__':
    dataCore = DataCore();
    if len(sys.argv)<2:
        logging.warning("argv error: %s" % str(sys.argv))
        dataCore.exit_msg(1001)
    # logging.info("argv[1] param: %s" % sys.argv[1])
    try:
        param = dataCore.parse_param(sys.argv[1])
        # logging.info("param type: %s" % type(param))
    except ValueError,e:
        logging.warning("argv parse error: %s" % str(e))
        dataCore.exit_msg(1002)
    logging.info("command param: %s" % str(param))
    conf = dataCore.load_config("/usr/share/puma-web/include/puma-core.ini");
    if not conf.has_key("server_ip") or not conf.has_key("server_port"):
        logging.warning("server ip and port is required in file '/usr/share/puma/include/puma-core.ini'")
        dataCore.exit_msg(1006)
    #param = {"method":"list_phy_disk","param":{"node_ip":"1.1.1.2"}}
    #param = {"method":"create_md_device","param":{"md_name":"test_md_name","md_level":4,"md_chunk":512,"md_phy_devices":[{"dev_name":"test_devname"},{"dev_name":"test222_devname"}]}}
    logging.info("call Service: %s" % param["method"])
    request = dataCore.create_obj(param)
    logging.info('-----request info------')
    logging.info(str(request))
    if request is None:
        logging.info("not exist Service %s" % param["method"])
        dataCore.exit_msg(1007)
    try:
        response = dataCore.request(param["method"],request,conf["server_ip"],conf["server_port"])
    except Exception,e:
        logging.warning("request data error: %s" % str(e))
        dataCore.exit_msg(1004)
    logging.info('-------response info------')
    logging.info(str(response))
    try:
         # parse_res = JSONEncoder().encode(dataCore.parse_data(response))
         parse_res = JSONEncoder().encode(dataCore.parse_response(response))
    except Exception,e:
        logging.warning("parse respose error: %s" % str(e))
        dataCore.exit_msg(1005)
    logging.info('------parse response----------')
    logging.info(parse_res)
    print parse_res