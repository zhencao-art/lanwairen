#!/usr/bin/python
''' function:manage the interface configuration 
    (1)read the configuration from file and create a dict to store the configuraion
    (2)update the dictionary
    (3)write the disctionary to the configuation.
'''
import re
from  collections import OrderedDict 
import os
import sys  # to support command line arguments.

def check_mac(mac):
    pattern = r"^([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}$"
    if re.match(pattern, mac):
        print "%s is a vaild MAC address" % mac
        return True
    else :
        print "%s is not a vaild MAC address" % mac
        return False


def check_ip_or_mask(value):
    addr = value.split(".")
    segs = [ int(i) for i in addr ]
    for ip in segs:
        if ip < 0 or ip > 255:
            return False
    return True
    
def check_ip(addr):
    pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$" 
    if re.match(pattern, addr):
        print "%s is a good IP address." % addr
        return True
    else :
        print "%s is not a valid address." % addr
        return False

def ip2int(addr):
    ''' convert dot-separated address into 32-bit integer '''
    ips = [ int(i) for i in addr.split(".") ]
    
    if len(ips) < 4 :
        return None 
    #print ips[0], ips[1], ips[2], ips[3]
    return (((((ips[0] << 8) | ips[1]) << 8) | ips[2]) << 8) | ips[3]

def  int2ip(ui32):
    ''' convert 32-bi integer to dot-separated address.'''
    for n in range(4):
        if n == 0:
            ip = str(ui32 & 0xff) 
        else:
            ip = str(ui32 & 0xff) +"." + str(ip)
        ui32 = ui32 >> 8
    return ip

def network(addr, prefix):
    ''' given dot-separated address and prefix, compute the nework address '''
    ip = ip2int( addr)
    mask= 0xffffffff << (32 - prefix)
    return (ip & mask)

def network_str(addr, prefix):
    return int2ip( network(addr, prefix) )
    
def mask2perfix(mask) :
    if not check_ip(mask) :
        return None 
    prefix = 0
    netmask = 0xffffffff ^ ip2int(mask)
    while netmask :
        if netmask & 0x1:
            prefix += 1
        netmask = netmask >> 1
    return (32 - prefix) 

def network2(addr, mask):
    ip = ip2int(addr)
    mk = ip2int(mask)
    return int2ip(ip & mk)

    
class nic_if:
    ''' an instance of nic_if stands for an IP address.
    an interface may be configured several IP addresses statically.
    '''
    def __init__(self):
        self.ip = "192.168.6.1"
        self.prefix = 24
        self.index = 0 
        
        self.gateway = ""     # no gateway is set by default.
        return None 

    def set_ip(self, ip, idx = 0) :
        ''' ip is dot-separated decimal data, e.g 172.16.9.24'''
        if not check_ip_or_mask( ip):
            raise ValueError("IP must be dot-separated decimal.")
        self.ip = ip
        self.index = idx 
        # print self.ip, self.prefix, self.index
    
    def set_prefix(self, prefix):
        if prefix < 0 or prefix > 32:
            raise ValueError("Prefix must be an int between [0,32]")
        self.prefix = prefix
        
    def gateway_match_ip(self, gateway):
        if not check_ip_or_mask(gateway):
            raise ValueError
        # print self.prefix 
        return network(gateway, self.prefix) == network(self.ip, self.prefix)
        
    def set_gateway(self, gateway):
        if not check_ip_or_mask(gateway):
            return False
        if not self.gateway_match_ip(gateway):
            return False
        self.gateway = gateway
        return True 
        

def test_nic_if():
    nic = nic_if()
    try:
        nic.set_ip("172.16.9.239", 0)
    except ValueError as e:
        print e 
        return 
    nic.set_prefix(24)
    if nic.gateway_match_ip("172.16.8.254"):
        print "OK"
    else:
        print "gateway is not matched with IP."
    
    if nic.set_gateway("172.16.9.254"):
        print "Set gateway is OK"

class iface_conf_manager:
    ''' each interface has its own configuration file.'''
    def __init__(self):
        self.interfaces = []
        self.keyval = OrderedDict()
        # an interface is statically configured by default.
        self.BOOTPROTO = "static" 

    def lookup_by_ip(self, ip):
        for inf in self.interfaces:
            if ip2int(inf.ip) == ip2int(ip) :
                return inf
        return None 

    def lookup_by_index(self, index):
        for inf in self.interfaces :
            if inf.index == index :
                return inf 
        return None 

    def set_nic_ip(self, index,ip):
        ''' create an instance of nic_if with the ip address
            gotten from configuration file.
        '''
        flag = False
        for inf in self.interfaces:
            if ip2int(inf.ip) == ip2int(ip) :
                flag = True
                break;
        if not flag:
            inf = nic_if()
            inf.set_ip(ip, index)
            self.interfaces.append(inf)

    def set_nic_gateway(self, gateway):
        for inf in self.interfaces:
            if inf.gateway_match_ip(gateway):
                inf.set_gateway(gateway)
                return True
        return False
    
    def set_nic_prefix(self, index, prefix):
        flag = False
        for inf in self.interfaces :
            if inf.index == index :
                inf.prefix = prefix 
                flag = True 
                break;
        if not flag :
            inf = nic_if()
            inf.index = index
            inf.set_prefix(prefix)
            self.nic_interfaces.append(inf)
    
    def add_nic_ip(self, ip,prefix):
        if not check_ip_or_mask(ip) :
            raise ValueError
        # check if the IP address has been set
        # if not set, then get the next index for the IP address.
        index = 0
        for inf in self.interfaces:
            if index < inf.index:
                index = inf.index 
            if ip2int(inf.ip) == ip2int(ip) :
                return None 
        index = index + 1
        print "index = %d" % index
        nic = nic_if()
        nic.set_ip(ip, index)
        nic.set_prefix(prefix) 
        self.interfaces.append(nic)

    def update_nic_ip(self, old, new, prefix):
        if not  check_ip_or_mask(new) : 
            return False
        if not check_ip_or_mask(old) :
            return False

        for inf in self.interfaces :
            if ip2int(inf.ip) == ip2int(old) :
                inf.ip = new
                inf.prefix = prefix
                break;
        return True

    def del_nic_ip(self, ip):
        index = 0
        flag = False
        
        for inf in self.interfaces:
            if ip2int(inf.ip) == ip2int(ip) :
                index = inf.index
                self.interfaces.remove(inf)
                flag = True
                break;
        if flag:
            for inf in self.interfaces:
                if inf.index > index:
                    inf.index = inf.index -1

    def output(self):
        for inf in self.interfaces:
            print "index %d, ip %s, prefix %d" % ( inf.index, inf.ip, inf.prefix)
            if inf.gateway :
                print "gateweay %s" % inf.gateway 
            
    def init_ips(self) :
        if self.keyval["BOOTPROTO"]:
            self.BOOTPROTO = self.keyval["BOOTPROTO"]
        else:
            raise ValueError
        # if the interface is configured with DHCP,
        # then no static address will be configured.
        if self.BOOTPROTO == "DHCP" :
            return None
        print self.BOOTPROTO
        # keyval is instance of OrderedDict.
        for key in self.keyval.keys():
            m = re.search(r'(?<=IPADDR)\d',key)
            if m: 
                #print "addr", m.group(0), "=", keyval[key]
                self.set_nic_ip( int(m.group(0)),self.keyval[key] )

            m = re.search(r'(?<=PREFIX)\d', key)
            if m: 
                #print "prefix", m.group(0), "=", keyval[key]
                self.set_nic_prefix( int(m.group(0)),int(self.keyval[key]) )        
            m = re.search(r'(?<=GATEWAY)\d', key)
            if m:
                #print "gateway", m.group(0), "=", keyval[key]
                self.set_nic_gateway( self.keyval[key] )

        self.output()

    def update_addr(self):
        ''' intfs is an instance of nic_interfaces, 
        keyval is an instance of OrderedDict
        '''
        # delete all the IPADDR, PREFIX and GATEWAY from keyval OrderedDict.
        for key in self.keyval.keys():
            m = re.search(r'(?<=IPADDR)\d',key)
            if m: 
                del self.keyval[key]
            m = re.search(r'(?<=PREFIX)\d', key)
            if m: 
                del self.keyval[key]
            m = re.search(r'(?<=GATEWAY)\d', key)
            if m:
                del self.keyval[key]

        for inf in self.interfaces: 
            ip = "IPADDR" + str(inf.index)
            prefix = "PREFIX" + str(inf.index)
            self.keyval[ip] = inf.ip;
            self.keyval[prefix] = inf.prefix 
            if inf.gateway :
                gateway = "GATEWAY" + str(inf.index)
                self.keyval[gateway] = inf.gateway 

    def parse_conf_file(self, filename):
        ''' convert the configuration file to a  ordered dict'''
        f = open(filename,"r")
        for line in f:
            # the comment line is ignored.
            m = re.match(r'^#', line) 
            if m :
                continue
            # print line
            # spaces or tab at the begining is/are stripped.
            line = line.strip() 
            # there is at most one parameter in a line.
            m = re.match(r'(\w+(?:\(\d+\))?)\s*=\s*(.*?)(?=(!|$|\w+(\(\d+\))?\s*=))', line)
            if m :
                vals = m.group(2)
                # strip double quote at the begining and trailing of the value.
                self.keyval[ m.group(1) ] = vals.strip('"') 
        f.close()
        self.init_ips()
        # check the configurations
        for key in self.keyval.keys():
            value = self.keyval[key]
            print "%s=%s" % (key, value)  
    
        
    def update_conf(self, path, *filename):
        self.update_addr()
        import tempfile
        (fd, self.tempfile) = tempfile.mkstemp('', '/tmp/')

        new_conf = path + "ifcfg-"+ dev + "-"+str(os.getpid())
        
        print self.tempfile 
        f2 = open(self.tempfile, "w+")
        for key in self.keyval.keys():
                value = self.keyval[key]
                print "%s=%s" % (key, value) 
                line = str(key) +"=" + str(value) +"\n"
                f2.write(line)
        os.rename(self.tempfile, new_conf)
        # os.rename(self.tempfile, filename)
        f2.close()
        

 
if __name__ == '__main__':
     # examples.
    '''
    mask = "255.255.255.192"
    value = "172.16.9.239"
    
    print ip2int("172.16.9.239")  
    print int2ip(2886732272)
    print "network = ",network("172.16.9.239", 26)
    print "network = ", network2("172.16.9.239", "255.255.255.192")
    '''

    test_nic_if()

    if len(sys.argv)  < 2:
        print "Usage : %s dev-name." % sys.argv[0]
        sys.exit(1)
    path = "/home/"
    dev = sys.argv[1]
    filename = path + "ifcfg-" + dev

    intfs = iface_conf_manager()
    intfs.parse_conf_file(filename)
    
    intfs.init_ips()
    print "\n"
    intfs.add_nic_ip("192.168.6.168", 24)
    intfs.add_nic_ip("172.16.8.148",24)
    intfs.update_nic_ip("172.22.5.251", "172.22.5.168", 16)
    intfs.output()
    print " After updating IP address \n"
    intfs.update_addr()
    for key in intfs.keyval.keys():
            value = intfs.keyval[key]
            print "%s=%s" % (key, value)  
    
    intfs.update_conf(path)
    check_ip("192.168.6.168")
    check_ip("239.255.255.293")
    check_mac("00:0c:29:3e:95:ff")
    prefix = mask2perfix("255.255.192.0")
    print "prefix is %d" % prefix
