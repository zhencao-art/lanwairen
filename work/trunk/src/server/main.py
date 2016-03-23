# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import sys
import getopt
import logging
import ConfigParser
import signal
import time

sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
import globalvar

from server import *
#golbal var
VERSION = "Puma 1.0.0.0.1"

def usage():
    print "Puma Usage:"
    print "-h,--help: print help message."
    print "-v,--version: print version."
    print "-f,--foregroud: foregroud executive"

def print_version():
    print VERSION

def load_config(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    configs = {}

    try:
        log_level = config.get("server","log_level")
        if log_level:
            configs.setdefault("log_level",log_level)
    except:
        pass

    try:
        log_file_path = config.get("server","log_file_path")
        if log_file_path:
            configs.setdefault("log_file_path",log_file_path)
    except:
        pass
    
    try:
        listen_ip = config.get("server","listen_ip")
        if listen_ip:
            configs.setdefault("listen_ip",listen_ip)
    except:
        pass
    
    try:
        listen_port = config.get("server","listen_port")
        if listen_port:
            configs.setdefault("listen_port",listen_port)
    except:
        pass

    try:
        thread_pool_max = config.get("server","thread_pool_max")
        if thread_pool_max:
            configs.setdefault("thread_pool_max",thread_pool_max)
    except:
        pass

    try:
        pid_file = config.get("server","heartbeat_nic_pci_id")
        if pid_file:
            configs.setdefault("heartbeat_nic_pci_id",pid_file)
    except:
        pass

    try:
        pid_file = config.get("server","pid_file")
        if pid_file:
            configs.setdefault("pid_file",pid_file)
    except:
        pass

    return configs

def deamon(pid_file):
    try:
        if os.fork() > 0:
            sys.exit(9)
    except OSError,e:
        print str(e)
        sys.exit(1)
    os.setsid()
    os.chdir("/")
    os.umask(0)
    try:
        if os.fork() > 0:
            sys.exit(0)
    except OSError,e:
        print str(e)
        sys.exit(1)
    
    pid_object = open(pid_file,"w")
    pid = os.getpid()
    pid_object.write(str(pid))
    pid_object.close()


def signal_handle(sig,frame):
    if sig == signal.SIGINT:
        sys.exit(0)

def init_signal():
    signal.signal(signal.SIGINT,signal_handle)

def main():
    foregroud = False

    log_level = logging.DEBUG
    log_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    log_datefmt = '%a, %d %b %Y %H:%M:%S'
    log_file_path = "/var/log/puma.log"

    server_pid_file = "/var/run/puma.pid"
    server_config_file_path = "/opt/puma/conf/puma.conf"
    server_listen_ip = "0.0.0.0"
    server_listen_port = "50000"
    server_thread_pool_max = 10

    try:
        opts,args = getopt.getopt(sys.argv[1:],"c:hvf",["config=","help","version","foreground"])
    except getopt.GetoptError,err:
        print str(err)
        usage()
        sys.exit(1)

    for o,a in opts:
        if o in ('-h','--help'):
            usage()
            sys.exit(1)
        elif o in ('-v','--version'):
            print_version()
            sys.exit(0)
        elif o in ('-f','--foreground'):
            foregroud = True
        elif o in ('-c','--config'):
            server_config_file_path = a
        else:
            print "unkonw options"
            sys.exit(2)
    
    for config in load_config(server_config_file_path).items():
        if config[0] == "log_level":
            if config[1] == "debug":
                log_level = logging.DEBUG
            elif config[1] == "warning":
                log_level = logging.WARNING
            elif config[1] == "info":
                log_level = logging.INFO
            elif config[1] == "ERROR":
                log_level = logging.ERROR
            else:
                print "config file log_level %s is unkonw" % config[1]
        elif config[0] == "log_file_path":
            #check if direct is exist
            log_file_path = config[1]
        elif config[0] == "listen_ip":
            server_listen_ip = config[1]
        elif config[0] == "listen_port":
            server_listen_port = config[1]
        elif config[0] == "thread_pool_max":
            server_thread_pool_max = int(config[1])
        elif config[0] == "pid_file":
            server_pid_file = config[1]

    if not foregroud:
        deamon(server_pid_file)

    init_signal()

    if foregroud:
        logging.basicConfig(level=log_level,format=log_format,stream=sys.stderr,filemode='a+')
    else:
        logging.basicConfig(level=log_level,format=log_format,datefmt=log_datefmt,filename=log_file_path,filemode='a+')
    ##init globalvar
    globalvar.listen_port = int(server_listen_port)
    globalvar.heartbeat_nic_pci_id = load_config(server_config_file_path).get('heartbeat_nic_pci_id')
    ##end of init globalevar

    ##start rpc server
    rpc_server = CServer(server_listen_ip,int(server_listen_port))
    rpc_server.set_thread_pool("puma rpc server",server_thread_pool_max)
    rpc_server.start()

    logging.info("log-level {0} log_file_path {1} listen_ip {2} listen_port {3} thread_pool {4}".format(log_level,log_file_path,server_listen_ip,server_listen_port,server_thread_pool_max))

    #entry main loop
    while True:
        time.sleep(1000)

if __name__ == "__main__":
    main()
