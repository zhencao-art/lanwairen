# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import cmd, socket
from params import *
from cmd_option import *
from deltavsoft.rcfproto import *
from optparse import OptionParser
from CPcsMgr import CPcsMgr
from CResMgr import CResMgr
from CStnMgr import CStnMgr
from CConsMgr import CConsMgr
from CIpMgr import CIpMgr
from CLunMgr import CLunMgr
from CDateMgr import CDateMgr
from cmd_disk_mgr import CCmdDiskMgr
from cmd_lv_mgr import CCmdLVMgr
from cmd_vg_mgr import CCmdVGMgr
from cmd_raid_mgr import CCmdRaidMgr

from handle.rpc_factory import *

class CliOptionParser(OptionParser):
    def __init__(self, usage=""):
        OptionParser.__init__(self, usage)
        self.ret_code = 0
        self.ret_mess = ""

    def error(self, err_mgs):
        raise Exception(err_mgs)

    def exit(self):
        pass

class CLI(cmd.Cmd, object):
    def __init__(self,factory):
        cmd.Cmd.__init__(self,'TAB')
        self.prompt = PRODUCT_NAME+'> '
        self.intro  = IntroString
        self.factory= factory
        self._hist = [] # history
        self.role = None
        self.platform = None
        self.ip = "127.0.0.1"

    def post_init(self):
        self.cluster = CPcsMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.resource = CResMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.stonith = CStnMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        #self.constraint = CConsMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.ip = CIpMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.lun = CLunMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.date = CDateMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        
        self.disk = CCmdDiskMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.lv = CCmdLVMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.vg = CCmdVGMgr(self.factory, params={'role':self.role, 'platform':self.platform})
        self.raid = CCmdRaidMgr(self.factory, params={'role':self.role, 'platform':self.platform})

        # 载入历史动作
        self._hist = load_hist()

        # 根据当前机器类型，动态修改支持的操作
        cmd_list = []
        for cmd_name, cmd_items in cmd_option.items():
            for cmd_item in cmd_items.values():
                if self.platform in cmd_item['platform'] and self.role in cmd_item['role']:
                    cmd_list.append(cmd_name)
                    break;

        def create_do_cmd(cmd):
            def do_cmd(self, args):
                print self.action(cmd, args)
            return do_cmd
        
        def create_complete_cmd(cmd):
            def complete_cmd(self, text, line, begin_idx, end_idx):
                return self.op_complete(text,line)
            return complete_cmd

        for cmd in cmd_option.keys():
            if cmd in cmd_list:
                setattr(self.__class__, 'do_'+cmd, create_do_cmd(cmd))
                setattr(self.__class__, 'complete_'+cmd, create_complete_cmd(cmd))
            else:
                if hasattr(self.__class__, 'do_'+cmd):
                    delattr(self.__class__, 'do_'+cmd)
                    delattr(self.__class__, 'complete__'+cmd)

    def parse_cfg(self, opt={}, arg=""):
        params = {}
        dest_list = {}
        key = ""
    
        a=arg.strip().split()
        if (len(a) == 1 and a[0] in ['-h', '--help']) or (len(a) == 0):
            out  = []
            out += ["Options:"]
            find = 0
            for k, v in opt.items():
                if not v.has_key("role") or not self.role in v["role"]:
                    continue
                if not v.has_key("platform") or not self.platform in v["platform"]:
                    continue
                out += ["  %-8s: %s" % (k, v['help'])]
                find = find + 1
            if find == 0:
                return (7,"","")
            return (8, "\n".join(out), '')
    
        if not opt.has_key(a[0]):
            return (1, 'unsupport option', '')
    
        cmd = a[0]
        sub_opt = opt[cmd]
        if not sub_opt.has_key("role") or not self.role in sub_opt["role"]:
            return (1, 'unsupport option', '')
    
        if not sub_opt.has_key("platform") or not self.platform in sub_opt["platform"]:
            return (1, 'unsupport option', '')
        
        parser = CliOptionParser("")
    
        for item in sub_opt['opts']:
            if len(item['opt']) == 2:
                if item["platform"] == "all" or item["platform"] == self.platform:
                    if item.has_key('action'):
                        parser.add_option("-"+item['opt'][0], "--"+item['opt'][1], action=item['action'], metavar=item['metavar'], \
                                dest=item['dest'], help=item['help'])
                    else:
                        parser.add_option("-"+item['opt'][0], "--"+item['opt'][1], metavar=item['metavar'], dest=item['dest'], help=item['help'])
                    if item.has_key('cfun') and item['cfun'] != "": 
                        dest_list[item['dest']]= item['cfun']
                    else:
                        dest_list[item['dest']]= ""
            elif  len(item['opt']) == 0:
                key = item['dest']
        try:
            (options, args) = parser.parse_args(a[1:])
        except Exception as e:
            return (1, str(e), '')
    
        if parser.ret_code:
            return (1, 'parse arrgs', '')
    
        if "-h" in a[1:] or "--help" in a[1:]:
            out = []
            for item in sub_opt['opts']:
                if len(item['opt']) == 0:
                    out += ['  %s\t\t%s' % (item['metavar'], item['help'])] 
            if len(sub_opt['example']) != 0:
                out += ["Examples:"]
            for line in sub_opt['example']["all"]:
                out += ["  %s" % line]
            ##if sub_opt['example'].has_key(self.platform):
            ##    for line in sub_opt['example'][self.platform]:
            ##        out += ["  %s" % line]
            return (9, "\n".join(out), '')
    
        if key != "" and len(args) != 1:
            return (1, 'miss object name', '')
    
        if key != "" and len(args) == 0:
            return (1, 'miss option', '')
    
        if key == "" and len(dest_list.keys()) == 0 and len(args) != 0:
            return (1, "Excess parameters", "")
    
        for d, cfun in dest_list.items():
            if getattr(options, d) != None:
                value = getattr(options, d)
                if cfun != "":
                    value = getattr(ChkParams(), "chk_"+cfun)(value)
                    if not value: return (1, "params --%s's value illegal." % d, '')
                params[d] = value
    
        if key != "":
            params[key] = args[0]
    
        return (0, cmd, params)
    
    def get_complet(self,dict):
        list = []
        for key in dict.keys():
            if self.role in dict[key]["role"] and self.platform in dict[key]["platform"]:
                list = list + [key]
        return list
    
    def op_complete(self,text,line):
        args=line.split()
        if line.endswith(' ') : 
            args+=['']
        ret = []
        opt = getattr(self,args[0]).opt
        list = self.get_complet(opt)
        if text == "":
             ret = list
        else:
             for i in list:
                if i.startswith(text):
                    ret = ret+[i]
        return ret
        
    def preloop(self):
        cmd.Cmd.preloop(self)
        self._locals  = {}
        self._globals = {}

    def postloop(self):
        cmd.Cmd.postloop(self)
        self.do_save()

    # 命令预处理，去除掉不接受的字符
    def precmd(self, line):
        l=line.strip()
        if l not in ['']:
            self._hist += [l]
        if not re.match(r'^[\w /?<>!*%#=;:,.+_-]*$',line):
            print "Error: command contains invalid characters"
            return ''
        return line

    def postcmd(self, stop, line):
        return stop

    def emptyline(self):
        pass

    def default(self, line):
        a=line.strip().split()
        c=safepeek(a)
        print '\033[1;31m'+'Command Error : '+c+' is not a valid CLI command !'+"\033[0m"

    def action(self, type, args):
        try:
            obj = getattr(self, type)
            (e, cmd, params) = self.parse_cfg(obj.opt, args)
            if e == 7:
                return '\033[1;31m'+'Command Error : '+type+' is not a valid CLI command !'+"\033[0m"
            if e == 8:
                return cmd
            if e == 9:
                return cmd
            if e:
                return '\033[1;31mCommand Error : %s\033[0m' % cmd

            for opt in obj.opt[cmd]['opts']:
                if len(opt['opt']) == 2 and opt['opt'][1] == "noconfirm":
                    if not params.has_key('noconfirm') or params['noconfirm'] != True:
                        result = confirm(opt['info'])
                        if result in ['n', '']:
                            return "Canceled!"

            ret =  getattr(obj, "cli_"+cmd)(params)
            return ret
        except Exception as e:
            out  = "\033[1;31m"
            out += str(e)
            out += "\033[0m"
            return out
            # out  = "\033[1;31m"
            # out += "=======================================================================\n"
            # out += "* If you see this tip, it means that an unexpected error occurred !!! *\n"
            # out += "* Please contact your supplier for help.                              *\n"
            # out += "======================================================================="
            # out += "\033[0m"
            # logger.run.error("An unexpected error occurred : %s", e)
            # return out
    
    def do_hist(self, arg=''):
        if len(self._hist) > 0:
            print '\n'.join([' %d %s' % (i+1, line) for i, line in enumerate(self._hist)])

    def do_quit(self, arg=''):
        save_hist(self._hist)
        print 'Bye..'
        sys.exit(0)

    def do_help(self, arg=''):
        status = None
        out = []
        out += ['help']
        out += [' '*12+' : Show this information.']
        for cmd, sub_cmd in cmd_option.items():
            for sub_cmd_name, sub_cmd_param in sub_cmd.items():
                if not sub_cmd_param.has_key("role") or not self.role in sub_cmd_param["role"]:
                    continue
                if not sub_cmd_param.has_key("platform") or not self.platform in sub_cmd_param["platform"]:
                    continue
                if cmd != status:
                    out += ['%s' % cmd]
                    status = cmd
                out += [' '*4+'%-8s : %-10s' % (sub_cmd_name, sub_cmd_param['help'])]
        print "\n".join(out)

    do_q    = do_quit
    do_exit = do_quit

def main():
    factory = CRpcFactory({'ip':'127.0.0.1','port':50008})

    cli = CLI(factory)
    cli.role = "puma"
    cli.platform = "all"
    cli.post_init()

    try:
        factory.create_auth_handle().auth('admin','admin')
    except:
        print  "Server connection error: Please check Server status"
        sys.exit(1)

    if len(sys.argv) > 1 :
        cli.onecmd(' '.join(sys.argv[1:]))
    else:
        try:
            cli.cmdloop()
        except KeyboardInterrupt:
            print "Stopped.."
            cli.do_quit('')
        except socket.error, e:
            print "Server connection error: %s" % str(e)
            sys.exit(1)

if __name__ == '__main__':
    main()
