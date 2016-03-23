# uft-8 unicode
#tabstop=4 shiftwidth=4 softtabstop=4


import logging,commands
import sys,os
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../')
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/../../ip')
#from common import CMessageSSH
import CIPMgr

class CClusterInit(object):
    def __init__(self):
        self._NodeList=None
    def StartService(self):
        try:
            rtn = self.CheckState('systemctl status pcsd')
            if rtn != True :
                self.Action('systemctl enable pcsd')
                self.Action('systemctl start pcsd')
        except Exception as e:
            raise e
        return True
    
    def StartPandC(self):
        self.Action('systemctl start corosync')
        self.Action('systemctl start pacemaker')

    def StartCandP(self):
        try:
            rtn = self.CheckState('systemctl status corosync')
            if rtn != True :
                self.Action('systemctl enable corosync')
                #self.Action('systemctl start corosync')
            rtn = self.CheckState('systemctl status pacemaker')
            if rtn != True :
                self.Action('systemctl enable pacemaker')
                #self.Action('systemctl start pacemaker')
        except Exception as e:
            raise e
        return True

    def Authrication(self,nodeList = None,passwd = None):
        hostname = ""
        try:
            rtn = self.StartService()
            #rtn = self.CheckState('pcs status')
            if None == passwd :
                passwd = 'hacluster'
            cmd = 'echo ' + passwd + '| passwd --stdin hacluster'
            #if rtn != True :
            self.Action(cmd)
            #else:
             #   raise Exception('cluster has already start')
        except Exception as e:
            raise e 
        return True
    def Auth1(self,nodeList,passwd):
        hostname = ""
        for node in nodeList:
            hostname += node + ' '
        #rtn = self.CheckState('pcs status')
        #if rtn == True :
        #    return True
        if None == passwd :
            passwd = 'hacluster'
        self.Action('pcs cluster auth '+ hostname +' -u hacluster -p '+passwd+' --force',120)
        rtn = self.StartCandP()

    def Setup(self,nodeList,clusterName,passwd):
        hostname = ""
        for node in nodeList:
            hostname += node + ' '
        cmd = 'pcs cluster setup --force --name ' +clusterName + ' ' + hostname
        cmd += ' --wait_for_all=1 --last_man_standing=1 --last_man_standing_window=50'
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd,30)
        if rtn!=0 :
            raise Exception(out)
        logging.debug('commands['+cmd +'] do success')
        return True

    def SetProperty(self,proOpt,code,isForce = False):
        rtn = self.CheckState('pcs status')
        if rtn!=True :
            raise Exception('cluster not start,cannot set properties')

        cmd = 'pcs property '
        import pdb
        if code == 'set':
            cmd += 'set '
            for op in proOpt:
                cmd += ' ' +op[0] + '=' + op[1]
        elif code == 'unset':
            cmd += 'unset ' 
            for op in proOpt:
                cmd += op[0]+op[1]
        else:
            raise Exception('cannot set property,reason: bad action code ='+code)
        if isForce:
            cmd += ' --force'
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0:
            raise Exception(out)
    
    def SetResDefaults(self,opt_dict):
        cmd = 'pcs resource defaults '
        for k in opt_dict:
            cmd += k + '=' + opt_dict.get(k) + ' '
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        while out or err:
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
            import time
            time.sleep(1)
        if rtn!=0:
            raise Exception(out)


    def GetProperty(self,code):
        rtn = self.CheckState('pcs status')
        if rtn!=True :
            raise Exception('cluster not start,cannot get properties')
        cmd = 'pcs property '
        if code != '':
            cmd += '--' + code
        (rtn,out,err) = CIPMgr.Exec_cmd(cmd)
        if rtn!=0:
            raise Exception(out)
        out = out.replace('Cluster Properties:\n','')
        plist = out.split('\n')
        result = []
        for p in plist:
            if p == '':
                continue
            tmp = {}
            tmp['value'] = p.split(':')[1]
            tmp['key'] = p.split(':')[0]
            result.append(tmp)
        return result
        
    def Start(self,nodeList):
        try:
            str = ""
            if nodeList== None or nodeList=='':
                str = 'pcs cluster start --all'
            else:
                str = 'pcs cluster start ' + nodeList
            (rtn,out,err) = CIPMgr.Exec_cmd(str,30)
            if rtn!= 0 :
                raise Exception(out)
            logging.debug('commands['+str+'] do success')
            return True
        except :
            raise

    def Stop(self,nodeList):
        str = ''
        if nodeList== None or nodeList=='':
             str = 'pcs cluster stop --all'
        else:
            str = 'pcs cluster stop ' + nodeList
        (rtn,out,err) = CIPMgr.Exec_cmd(str,30)
        if rtn!= 0 :
            raise Exception(out)
        logging.debug('commands['+str+'] do success')
        return True

    def CheckState(self,cmd):
        try:
            if cmd != None :
                (rtn,out) = commands.getstatusoutput(cmd)
                if rtn!=0:
                    return False
            else:
                raise Exception(repr('CheckState() :bad cmd input'))
            return True
        except Exception as e:
            raise 

    def Action(self,cmd,timeout = 10):
        try:
            (rtn,out,err) = CIPMgr.Exec_cmd(cmd,timeout)
            if rtn!=0:
                raise Exception(out)
            logging.debug('do command['+cmd+'] success')
            return rtn
        except Exception as e:
            raise e



