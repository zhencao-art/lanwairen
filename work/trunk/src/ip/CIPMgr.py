#auth  huchuanwen
#func  manage ip

import sys, os ,logging , ConfigParser, re , subprocess
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../cluster/resource')
sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../server")))
import client,CCoroFile 
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
sys.path.append(os.path.abspath(os.path.join(__file__,"../../nic")))
import globalvar,puma_pb2, CResourceMgr,  CResourceFactory
from nic import *
sys.path.append('')

dfile = '/etc/sysconfig/network-scripts/'
#dfile = './'

def Exec_cmd(args,timeout = 10):
    try:
       # cmdlist = args.split('|')
       # out = None
       # proc = None
       # for cmd1 in cmdlist:
       #     cmd = cmd1.split()
       #     if not out:
       #         proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
       #     else:
       #         proc = subprocess.Popen(cmd,stdin=out,stdout=subprocess.PIPE)
       #     out = proc.stdout
       #     if proc.returncode!= 0:
       #         stdout,stderr = proc.communicate()
       #         raise Exception(stderr)

        cmd = args
        proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        wait_time = 0.0005
        import time
        deadline = time.time() + timeout
        while time.time() < deadline and proc.poll()== None:
            time.sleep(wait_time)
        if proc.poll() == None:
            proc.terminate()
            raise Exception('do command[%s] timeout' % args)
        stdout,stderr = proc.communicate()
        ret = proc.returncode
        if ret != 0:
            raise Exception(stdout+stderr)
        return ret,stdout,stderr
    except Exception as e:
        raise e

def Exec_cmd2(args,timeout = 10):
    try:
        cmd = args
        proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        wait_time = 0.0005
        import time
        deadline = time.time() + timeout
        while time.time() < deadline and proc.poll()== None:
            time.sleep(wait_time)
        if proc.poll() == None:
            proc.terminate()
            raise Exception('do command[%s] timeout' % args)
        stdout,stderr = proc.communicate()
        ret = proc.returncode
        return ret,stdout,stderr
    except Exception as e:
        raise e

def InitIfcfg():
    def replace_item(fc,item,new):
        regx = item + '\S*'
        proc = re.compile(regx)
        rst_list = proc.findall(fc)
        rpl = item + '=' + new
        if not rst_list:
            fc += '\n' + rpl
        else:
            fc = fc.replace(rst_list[0],rpl)
        return fc

    try:
        nic_list = GetNic()
        for nic in nic_list:
            filename = dfile + 'ifcfg-' + nic
            f = File(filename)
            fc = f.GetFile()
            fc = replace_item(fc,'BOOTPROTO','static')
            fc = replace_item(fc,'ONBOOT','yes')
            f.Write(fc)
    except Exception as e:
        logging.info('init ifcfg file failed,please check your net config file mannally')

def SetIP(ip,nic,mask, gateway=None):
    if nic and nic == 'heartbeat':
        nic = GetHeartBeatNic()
    SetIPByFile(ip,nic,mask, gateway)

def SetIPByFile(ip,nic,mask, gateway):
    if not nic:
        niclist = GetNic()
        nic = niclist[0]
    if not mask:
        mask = '24'
    if CheckIp(ip):
        raise Exception('ip[%s] exist already'%ip)
    #mask_d = Format(mask)
    try:
        Exec_cmd('ip addr add '+ip+'/'+mask+' dev '+nic)
        if gateway:
            SetGateWay(gateway,ip,nic,mask)
        WriteIp(ip,nic,mask,gateway)
    except Exception as e:
        Exec_cmd('systemctl restart network')
        raise e

def SetGateWay(gateway,ip,nic,mask):
    if not gateway:
        return
    CheckGwSecurity(gateway,ip,nic,mask) 
    rtn,out,err = Exec_cmd('ip route')
    check_result = CheckGateWay(out,gateway)
    if check_result == 0:
        return
    elif check_result == 1:
        item = 'default via'
        begin = out.find(item)
        while begin != -1 :
            end = out.find('\n')
            cmd = 'ip route del ' + out[begin:end]
            Exec_cmd(cmd)
            begin = out.find(item,end+1)
        cmd = 'ip route add default via ' + gateway + ' dev ' + nic + ' proto static metric 1024'
        Exec_cmd(cmd)
    else:
        cmd = 'ip route add default via ' + gateway + ' dev ' + nic + ' proto static metric 1024'
        Exec_cmd(cmd)

def CheckGwSecurity(gateway,ip,nic,mask):
    if '/' in gateway:
        mask_gw = gateway.split('/')[1]
    else:
        mask_gw = mask
    sub1 = network(ip,int(mask))
    sub2 = network(gateway,int(mask_gw))
    if sub1 != sub2:
        raise Exception('you input ip[%s] and gateway[%s] are not in one subnet' % (ip,gateway) )
    hblist = get_corosync_node()
    rtn,out,err = Exec_cmd('ip addr show ' + nic)
    for hb in hblist:
        if hb+'/' in out:
            raise Exception('nic[%s] is heartbeat nic,cannot set gateway' % nic)

def CheckGateWay(out,gateway):
    if gateway in out:
        return 0
    regx = 'default via'
    proc = re.compile(regx)
    result = proc.findall(out)
    if len(result) > 0:
        return 1
    return -1

def GetNicWithHost():
    niclist = GetNic()
    result = []
    host = GetHostname()
    for nic in niclist:
        tmp = {}
        tmp['nic'] = nic
        tmp['host'] = host
        result.append(tmp)
    return result

def GetNic(ip = None):
    cmd = 'ip token'
    (rtn,out,err) = Exec_cmd(cmd)
    prex = ':: dev '
    begin = out.find(prex)
    token = []
    while(begin != -1):
        begin += len(prex)
        end = out.find('\n',begin)
        token.append(out[begin:end].strip())
        begin = out.find(prex,end+1)
    return token

def CheckIp(ip):
    if ip.count('.')!= 3:
        raise Exception('please input a vaild ip address,you input['+ip+']')
    iplist = ip.split('.')
    for i in iplist:
        if not i.isalnum() or int(i)<0 or int(i)>255:
            raise Exception('please input a vaild ip address,you input['+ip+']')
    rtn,out,err = Exec_cmd('ip addr')
    if ip+'/' in out:
        return True
    return False

def IsIp(ip):
    if ip.count('.')!= 3:
        return False
    iplist = ip.split('.')
    for i in iplist:
        if not i.isalnum() or int(i)<0 or int(i)>255:
            return False
    return True

def numTo(mask):
    pass

def Format(mask):
    mask_d = int(mask)
    count = 0;ret = ''
    while(count < 4):
        if mask_d >= 8:
            ret += str(255)
        elif mask_d > 0:
            v =0;n = 8;m= mask_d
            while(m>0):
                v += 2**(n-m)
                m -= 1
            ret += str(v)
        else:
            ret += str(0)
        if count !=3:
            ret += '.'
        count +=1
        mask_d -= 8
    return ret

def GetMask(ip):
    ipf = ip + '/'
    (rtn,out,err) = Exec_cmd('ip addr')
    begin = out.find(ipf)
    if begin == -1:
        raise Exception('ip[%s] not exist')
    begin = begin + len(ipf)
    end = out.find(' ',begin)
    return out[begin:end]

def get_num(fc):
    item = 'IPADDR'
    ref = '\S*'+item+'\S*'
    regx = re.compile(ref)
    iplist = regx.findall(fc)
    if iplist:
        s = iplist[len(iplist)-1]
        begin = s.find(item) + len(item)
        end = s.find('=',begin)
        num = int(s[begin:end])+1
    else:
        num = 0
    return num

def WriteIp(ip,nic,mask,gateway):
    def replace(s,old,new):
        old += '='
        begin = s.find(old)
        if begin == -1:
            return s
        else:
            begin += len(old)
        end = s.find('\n',begin)
        s = s.replace(s[begin:end],new)
        return s

    def write_item(item,fc,flag,value,num):
        if flag:
            fc = replace(fc,'NAME',nic)
            fc = replace(fc,'UUID','')
            
            for it in iplist:
                fc = fc.replace(it+'\n','')
            fc += item+'0='+value+'\n'
            return fc
        fc += item + str(num) + '=' + value+'\n'
        return fc
    

    global dfile
    filename = dfile + 'ifcfg-'+nic
    flag = False
    if not os.path.exists(filename):
        niclist = GetNic()
        cmd = 'cp ' + dfile + 'ifcfg-'+niclist[0] + ' ' + filename
        (rtn,out,err) = Exec_cmd(cmd)
        flag = True
    f = File(filename)
    fc = f.GetFile()
    num = get_num(fc)
    fc = write_item('IPADDR',fc,flag,ip,num)
    fc = write_item('PREFIX',fc,flag,mask,num)
    if gateway:
        fc = WriteGateway(fc,gateway)
    f.Write(fc)

def WriteGateway(fc,gateway):
    item = 'GATEWAY0'
    begin = fc.find(item)
    if begin == -1 :
        fc += '\n' + item + '=' + gateway
    else:
        #begin += len(item) + 1
        end = fc.find('\n',begin)
        #logging.debug(fc[begin:end])
        fc = fc.replace(fc[begin:end],item+'='+gateway)
    return fc
    
def DeleteIp(ip,nic):
    DeleteIpByFile(ip,nic)

def DeleteIpByFile(ip,nic):
    def get_num(fc,ip):
        end = fc.find(ip)
        if end == -1:
            raise Exception('ip[%s] do not exist in config file' % ip)
        item = 'IPADDR'
        begin = fc[:end].rfind(item)
        fc = fc[begin:end]
        t_end = fc.find('=')
        t_begin = fc.find(item) + len(item)
        return fc[t_begin:t_end]

    def delete_item(fc,item,num):
        begin = fc.find(item+num)
        end = fc.find('\n',begin)
        if end != -1:
            end +=1
        else:
            end = len(fc)
        fc = fc.replace(fc[begin:end],'')
        return fc

    status = CheckIpState(ip,nic)
    if status != 'free':
        raise Exception('ip[%s] is %s address' % (ip,status))
    filename = dfile + 'ifcfg-' + nic
    if not os.path.exists(filename):
        raise Exception('nic[%s] do not exist '%nic)
    f = File(filename)
    fc = f.GetFile()
    rtn,out,err = Exec_cmd('ip addr show '+nic)
    if ip not in out:
        raise Exception('ip[%s] do not exist'%ip)
    if ip+'/' in out and ip in fc:
        num = get_num(fc,ip)
        fc = delete_item(fc,'IPADDR' , num)
        if 'PREFIX'+num in fc:
            fc = delete_item(fc,'PREFIX' , num)
        if 'NETMASK'+num in fc:
            fc = delete_item(fc,'NETMASK' , num)
        fc = sort_num(fc,int(num))
        f.Write(fc)
    Exec_cmd('ip addr del ' + ip + ' dev ' + nic)
    #Exec_cmd('ifdown ' + nic)
    #Exec_cmd('ifup ' + nic)

def replace_item(fc,old,new):
    begin = fc.find(old)
    if begin == -1:
        return fc
    fc = fc.replace(old,new,1)
    return fc

def sort_num(fc,num):
    max_num = get_num(fc) - 1
    while num < max_num :
        item = 'IPADDR'
        new = item + str(num)
        old = item + str(num+1)
        fc = replace_item(fc,old,new)
        item = 'PREFIX'
        new = item + str(num)
        old = item + str(num+1)
        fc = replace_item(fc,old,new)
        num += 1
    return fc

def GetIp(check_flag = True):
    return  GetIpByCmd(check_flag)

def GetIpByFile(ip):
    def get_item(fc,item):
        ref = '\S*'+item+'=\S*'
        regx = re.compile(ref)
        iplist = regx.findall(fc)
        if len(iplist) > 1:
            raise Exception('item[%s] should be unique'%item)
        if len(iplist) == 0:
            return 'None'
        begin = iplist[0].find('=') + 1
        rtn = iplist[0][begin:]
        if rtn.startswith('"') and rtn.endswith('"'):
            rtn = eval(rtn)
        return rtn

    def get_ip(fc,nic,ip1):
        ref = '\S*IPADDR\S*'
        regx = re.compile(ref)
        iplist = regx.findall(fc)
        count = 0
        for ip in iplist:
            opt = {}
            opt['nic'] = nic
            item = 'IPADDR' + str(count)
            opt['ip'] = get_item(fc,item)
            if opt.get('ip') != ip1:
                count += 1
                continue
            item = 'PREFIX' + str(count)
            opt['cidr_netmask'] = get_item(fc,item)
            return opt
        return None
    niclist = GetNic()
    for nic in niclist:
        filename = dfile + 'ifcfg-'+nic
        f = File(filename)
        fc = f.GetFile()
        ip_dict = get_ip(fc,nic,ip)
        if ip_dict:
            return ip_dict
    return None

def SetIPByCmd(ip,nic,mask):
    pass

#@rtn  ---  free,heartbeat,float_ip,lun
def CheckIpState(ip,nic,ip_res_list = None,tgtlist = None):
    #check heartbeat
    hb_list = get_corosync_node()
    if ip in hb_list:
        return 'heartbeat'
    #check float ip
    if ip_res_list != None:
        for ip_res in ip_res_list:
            if ip_res.get('ip') == ip:
                for tgt in tgtlist:
                    if tgt.get('portals') and tgt.get('portals').split(':')[0] == ip:
                        return 'lun'
                return 'float_ip'
        return 'free'
    else:
        CResourceFactory.SetCfg()
        rtn = CResourceFactory.CheckIpRes(ip)
    return rtn 

def GetHostname():
    rtn,out,err = Exec_cmd('uname -n')
    return out[:-1]

def GetIpByCmd(check_flag = True):
    hostname = GetHostname()
    niclist = GetNic()
    result = []
    if check_flag:
        cfg = CResourceFactory.SetCfg()
        ip_res_list = CResourceMgr.GetResByType(cfg,'IPaddr2',False)
        tgtlist = CResourceMgr.GetResByType(cfg,'iSCSITarget',False)
    for nic in niclist:
        rtn,out,err = Exec_cmd('ip addr show '+nic)
        ref = 'inet\s\S*'
        regx = re.compile(ref)
        iplist = regx.findall(out)
        for ip in iplist:
            begin = ip.find(' ') + 1
            s = ip[begin:]
            tmp = {}
            tmp['ip'] = s.split('/')[0]
            if check_flag:
                tmp['status'] = CheckIpState(tmp['ip'],nic,ip_res_list,tgtlist)
            tmp['mask'] = s.split('/')[1]
            tmp['nic'] = nic
            tmp['host'] = hostname
            tmp['gateway'] = GetGateway(nic)
            result.append(tmp)
    return result

def GetGateway(nic):
    filename = dfile + 'ifcfg-'+nic
    f = File(filename)
    fc = f.GetFile()
    item = 'GATEWAY0'
    begin = fc.find(item)
    if begin == -1 :
        return '' 
    else:
        begin += len(item) + 1
        end = fc.find('\n',begin)
        rtn = fc[begin:end].strip()
        if rtn.startswith('"') and rtn.endswith('"'):
            rtn = eval(rtn)
        return rtn

def get_corosync_node():
    filename = '/etc/corosync/corosync.conf'
    f = File(filename)
    fc = f.GetFile()
    rex = 'ring0_addr:\s\S*'
    regx = re.compile(rex)
    iplist = regx.findall(fc)
    result = []
    for ip in iplist:
        begin = ip.find(':') + 1
        result.append(ip[begin:].strip())
    return result

class File():
    def __init__(self,f_name):
        self._fname = f_name
        self._fcontent = ''

    def GetFile(self):
        f_handle = open(self._fname,'r')
        self._fcontent = f_handle.read()
        f_handle.close()
        return self._fcontent

    def Write(self,f_content):
        f_handle = open(self._fname,'w+')
        f_handle.write(f_content)
        f_handle.close()


def CheckIpForResource(ip,nic,mask):
    if ip.count('.')!= 3:
        raise Exception('please input a vaild ip address,you input['+ip+']')
    iplist = ip.split('.')
    for i in iplist:
        if not i.isalnum() or int(i)<0 or int(i)>255:
            raise Exception('please input a vaild ip address,you input['+ip+']')
    if JudgeExist(ip,nic,mask):
        raise Exception('ip address['+ip+'] has been used in cluster node')

def JudgeToken(local_ip,ip,nic):
    cmd = 'ip token'
    local_ip += '/'
    (rtn,out,err) = Exec_cmd(cmd)
    prex = ':: dev '
    begin = out.find(prex)
    token = []
    while(begin != -1):
        begin += len(prex)
        end = out.find('\n',begin)
        token.append(out[begin:end].strip())
        begin = out.find(prex,end+1)
    if not nic:
        nic = token[0]
    for t in token:
        cmd = 'ip addr show ' + t
        (rtn,out,err) = Exec_cmd(cmd)
        if local_ip in out:
            if nic == t:
                return False
            return True
    return False

def GetIpByNic(nic):
    rtn,out,err = Exec_cmd('ip addr show '+nic)
    ref = 'inet\s\S*'
    regx = re.compile(ref)
    iplist = regx.findall(out)
    result = []
    for ip in iplist:
        begin = ip.find(' ') + 1
        s = ip[begin:]
        tmp = {}
        result.append(s.split('/')[0])
    return result

def JudgeSubnet1(ip,nic,mask):
    if CheckIp(ip):
        raise Exception('ip[%s] has already exist' % ip)
    nic_list = GetNic()
    for nic1 in nic_list:
        if nic == nic1:
            continue
        ip_list = GetIpByNic(nic1)
        for ip1 in ip_list:
            JudgeSubnet(ip1,ip,mask)
    pass

def JudgeSubnet2(ip1,mask1,ip2,mask2):
    if not mask1:
        mask1 = 24
    if not mask2:
        mask2 = 24
    mask1_d = Format(mask1)
    mask2_d = Format(mask2)
    from IPy import IP
    sub1 = IP(ip1).make_net(mask1_d)
    sub2 = IP(ip2).make_net(mask2_d)
    if sub1 != sub2:
        raise Exception('heartbeat address[%s , %s]should be in one subnet'%(ip1,ip2))

def JudgeSubnet(local_ip,ip,mask):
    ips = ip.replace('/','')
    if not mask:
        mask = '24'
    local_mask = GetMask(local_ip)
    local_mask_d = Format(local_mask)
    mask_d = Format(mask)
    from IPy import IP
    sub1 = IP(local_ip).make_net(local_mask_d)
    sub2 = IP(ips).make_net(mask_d)
    if sub1 == sub2:
        raise Exception('heartbeat address and float_ip[%s , %s] should not be in one subnet'%(local_ip,ip))

def JudgeExist(ip,nic = None,mask = None):
    ip = ip + '/'
    cmd = 'ip addr'
    (rtn,out,err) = Exec_cmd(cmd)
    if ip in out:
        return True
    nodelist = get_corosync_node()
    for node in nodelist:
        if node+'/' not in out:
            peer_ip = node
        else:
            local_ip = node
    if not peer_ip:
        raise Exception('can not get peer ip')
    if not JudgeToken(local_ip,ip,nic):
        raise Exception('float_ip you specify cannot be the same net interface with heartbeat address')
    JudgeSubnet(local_ip,ip,mask)
    cli  = client.CClient(peer_ip,globalvar.listen_port)
    req = puma_pb2.GetIpReq()
    cli.stub().get_used_ip(None,req,None)
    resp = cli.get_response()
    if resp.ret.retcode != 0:
        raise Exception('get peer used ip failed:'+resp.ret.msdg)
    if ip in resp.ret.msg:
        return True
    return False

def GetClusterName():
    path = ['totem']
    key = 'cluster_name'
    rtn = CCoroFile.GetCoroValue(path,key)
    if len(rtn) != 1:
        raise Exception('bad cluster name[%s]' % str(rtn))
    return rtn[0]

def get_peer_ip():
    nodelist = get_corosync_node()
    for node in nodelist:
        if  not CheckIp(node):
            return node
    raise Exception('can not get peer ip')

def GetNicByIp(ip):
    if not CheckIp(ip):
        peer_ip = get_peer_ip()
        cli  = client.CClient(peer_ip,globalvar.listen_port)
        req = puma_pb2.GetNicByIpReq()
        req.ip = ip
        cli.stub().get_nic_byip(None,req,None)
        resp = cli.get_response()
        if resp.ret.retcode != 0:
            raise Exception('get peer used ip failed:'+resp.ret.msdg)
        return eval(resp.ret.msg)
    return GetNicIp(ip)

def GetNicIp(ip):
    niclist = GetNic()
    rtn_dict = {}
    for nic in niclist:
        rtn,out,err = Exec_cmd('ip addr show ' + nic)
        if ip+'/' in out:
            regx = ip+'/\S*'
            proc = re.compile(regx)
            result = proc.findall(out)
            rtn_dict['nic'] = nic
            rtn_dict['cidr_netmask'] = result[0].split('/')[1]
            break
    return rtn_dict

def GetNicInfo(node):
    #nodelist = get_corosync_node()
    result = []
    #for node in nodelist:
    #    logging.debug('start   --->' + node)
    #    if  not CheckIp(node):
    #        tmp = GetNicByIp(node)
    #        tmp['ip'] = node
    #        result.append(tmp)
    #    else:
    #        result.append(GetIpByFile(node))
    #logging.debug('end   --->' + node)
    niclist = GetNic()
    if  not CheckIp(node):
        tmp = GetNicByIp(node)
        tmp['ip'] = node.encode('utf-8')
        result.append(tmp)
    else:
        result.append(GetIpByFile(node))
    niclist.remove(result[0].get('nic'))
    for nic in niclist:
        tmp = {}
        tmp['nic'] = nic
        result.append(tmp)
    return result

def GetHeartBeatNic():
    pci_id = globalvar.heartbeat_nic_pci_id
    if not pci_id:
        raise Exception('please config heartbeat nic pci path')
    nic_list = GetNic()
    for nic in nic_list:
        cmd = 'udevadm info --query=path /sys/class/net/' + nic
        rtn,out,err = Exec_cmd(cmd)
        if pci_id in out or pci_id in err:
            return nic
    raise Exception('can not find nic for heartbeat,default pci_id[%s]' % pci_id)

def IsDcnode():
    cmd = 'pcs cluster status |grep "Current DC:"'
    rtn,out,err = Exec_cmd(cmd)
    hostname = GetHostname()
    if hostname in out:
        return True
    return False

#############################################
