# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../../ip")))
import CIPMgr,logging

NTP_CONF_PATH = '/etc/ntp.conf'

NTP_SERVER_CONF_CONTENT = "driftfile /var/lib/ntp/drift\n\
restrict default nomodify notrap\n\
restrict 127.0.0.1\n\
restrict ::1\n\
includefile /etc/ntp/crypto/pw\n\
keys /etc/ntp/keys\n\
disable monitor"

def Run_cmd(cmd):
    logging.debug("Run cmd %s" % cmd)
    (s,o,err) = CIPMgr.Exec_cmd2(cmd)
    return (s,o,err)

def check_ntp_installed():
    pass

def ntp_cur_conf():
    fd = open(NTP_CONF_PATH)
    conf =fd.read()
    fd.close()

    ret = {}

    for item in conf.strip().split('\n'):
        kv = item.strip().split()
        try:
            ret[kv[0]] = kv[1]
        except:
            continue

    return ret

def ntp_server_set(url):
    content = NTP_SERVER_CONF_CONTENT + '\nserver ' + url + ' iburst'
    cmd = "echo -e \"" + content + "\" > " + NTP_CONF_PATH
    Run_cmd(cmd)

"""
    write only url into ntp.conf
"""
def ntp_client_set(url):
    content = 'server ' + url
    cmd = "echo -e \"" + content + "\" > " + NTP_CONF_PATH
    Run_cmd(cmd)

def ntp_start():
    cmd = 'systemctl start ntpd'
    Run_cmd(cmd)

def ntp_stop():
    cmd = 'systemctl stop ntpd'
    Run_cmd(cmd)

def ntp_restart():
    cmd = 'systemctl restart ntpd'
    Run_cmd(cmd)

def ntp_status():
    cmd = 'systemctl status ntpd'
    (status,output,stderr) = Run_cmd(cmd)
    return status

def ntp_enable():
    cmd = 'systemctl enable ntpd'
    Run_cmd(cmd)

def ntp_disable():
    cmd = 'systemctl disable ntpd'
    Run_cmd(cmd)

def ntp_stop():
    cmd = 'systemctl stop ntpd'
    Run_cmd(cmd)
