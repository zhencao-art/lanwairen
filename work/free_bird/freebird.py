#!/usr/bin/python
import sys,os
import ConfigParser
import commands

CONF_PATH='/etc/freebird.conf'

##global var
global local_ip
local_ip = '127.0.0.1'

global local_port
local_port = 7070

global srv_user
srv_user = 'root'
global srv_ip
srv_ip = '127.0.0.1'

def conf_parser():
    global local_ip,local_port,srv_user,srv_ip

    config = ConfigParser.ConfigParser()
    
    try:
        config.read(CONF_PATH)
        local_ip = config.get('free_bird','local_ip')
        local_port = config.get('free_bird','local_port')
        srv_user = config.get('free_bird','srv_user')
        srv_ip = config.get('free_bird','srv_ip')
    except Exception as e:
        print 'Configfile Parser error'
        sys.exit(1)

def cur_status(proc_id):
    cmd = 'ps -elf | grep \'' + proc_id + '\'|grep -v grep'
    (status,output) = commands.getstatusoutput(cmd)
    if 0 == status:
        return True
    else:
        return False

def main(argv):
    conf_parser()
    proc = 'ssh -qTfnN -D ' + local_ip + ':' + local_port + ' ' + srv_user + '@' + srv_ip

    if not cur_status(srv_user + '@' + srv_ip):
        pid = os.fork()
        if pid == 0:
            (status,output) = commands.getstatusoutput(proc)
            if 0 != status:
                sys.exit(status)
            else:
                sys.exit(0)
        else:
            sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)
