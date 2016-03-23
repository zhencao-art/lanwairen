#!/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
import client,puma_pb2
import ConfigParser
import logging

RPC_SERVER_CONF = '/opt/puma/conf/puma.conf'
MON_LOG_FILE    = '/var/log/puma-mon.log'

LISTEN_IP       = '127.0.0.1'
LISTEN_PORT     = 50008

def logging_init():
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename=MON_LOG_FILE,filemode='a+')

"""
    get rpc server listenning port and ip
"""
def config_parser(config_file):
    config_fd = ConfigParser.ConfigParser()
    config_fd.read(config_file)

    try:
        port = config_fd.get('server','listen_port')
    except:
        logging.error('config_parser {0} error,rpc_server default port {1}'.format(config_file,50008))
        return
    LISTEN_PORT = port

def main(argv):
    logging_init()

    if len(argv) < 3:
        logging.info('argv: %s' % argv)
        return

    event_message = argv[1]
    event_target  = argv[2]
    event_opt     = None
    if len(argv) == 4:
        event_opt = argv[3]

    config_parser(RPC_SERVER_CONF)
    try:
        rpc_handle = client.CClient(LISTEN_IP,LISTEN_PORT)
        rpc_handle.set_async_remote_call()
        
        request = puma_pb2.MdMonEventReportReq()

        request.event_target = event_target
        request.event_msg    = event_message
        if event_opt:
            request.event_opt = event_opt

        rpc_handle.stub().mdmon_event_report(None,request,None)

        if event_opt:
            logging.info('Send Event ({0},{1},{2})'.format(event_target,event_message,event_opt))
        else:
            logging.info('Send Event ({0},{1})'.format(event_target,event_message))

    except Exception as e:
        logging.error('Report event error,RPC error %s' % str(e))

if __name__ == '__main__':
    main(sys.argv)
