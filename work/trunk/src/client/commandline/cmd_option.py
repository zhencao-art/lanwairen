# -*- coding: utf-8 -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
cmd_option = { \
    'disk':{
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'Get the list of the cluster physical disk, if ip option is specified,list sepecified node disk',
            'opts':[
                {'opt':('i','ip'),'platform':'all','metavar':'<cluster host ip>','dest':'host_ip','help':'Specify the ip of the host,'},
            ],
            'example': {'all':[
                'disk list',
                'disk list -c false -i 172.16.9.162',
            ]},
        },
        'init':{
            'role':['puma'],
            'platform':['all'],
            'help':'Init the cluster physical disk',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<disk device name>','dest':'name','help':'Specify the name of the disk device,'},
            ],
            'example': {'all':[
                'disk init -n /dev/sda',
            ]},
        },
    },
    'vg': {
        'create':{
            'role':['puma'],
            'platform':['all'],
            'help':'Create volume group',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify volume group name'},
                {'opt':('p','pv'),'platform':'all','metavar':'<physical volume name>','dest':'phy_vol','help':'Specify physical volume'},
            ],
            'example': {'all':[
                'vg create -n grp00 -p /dev/sda',
                'vg create -n grp00 -p /dev/sda,/dev/sdb',
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'Get the list of the volume group',
            'opts':[
            ],
            'example': {'all':[
                'vg list',
            ]},
        },
        'info':{
            'role':['puma'],
            'platform':['all'],
            'help':'Get the information of the volume group',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify volume group name'},
            ],
            'example': {'all':[
                'vg info -n grp00',
            ]},
        },
        'extend':{
            'role':['puma'],
            'platform':['all'],
            'help':'Add physical volume into volume group',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify volume group name'},
                {'opt':('p','pv'),'platform':'all','metavar':'<physical volume name>','dest':'phy_vol','help':'Specify physical volume'},
            ],
            'example': {'all':[
                'vg extend -n grp00 -p /dev/sda',
                'vg extend -n grp00 -p /dev/sda,/dev/sdb',
            ]},
        },
        'reduce':{
            'role':['puma'],
            'platform':['all'],
            'help':'Del physical volume from volume group',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify volume group name'},
                {'opt':('p','pv'),'platform':'all','metavar':'<physical volume name>','dest':'phy_vol','help':'Specify physical volume'},
                {'opt':('d','drastically'),'platform':'all','action':'store_true','metavar':'<true | false>','dest':'rm_drast','help':'Specify the way of removing physical volume'},
            ],
            'example': {'all':[
                'vg reduce -n grp00 -p /dev/sda',
                'vg reduce -n grp00 -p /dev/sda,/dev/sdb',
            ]},
        },
        'remove':{
            'role':['puma'],
            'platform':['all'],
            'help':'Remove volume group',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify volume group name'},
            ],
            'example': {'all':[
                'vg remove -n grp00',
            ]},
        },
    },
    'lv':{
        'create':{
            'role':['puma'],
            'platform':['all'],
            'help':'Create a logical volume',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<logical volume name>','dest':'lv_name','help':'Specify the name of the logical volume'},
                {'opt':('g','group'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify the name of the volume group'},
                {'opt':('s','size'),'platform':'all','metavar':'<the size of the logical volume>','dest':'lv_size','help':'Specify the size of the logical volume,the unit is Gib'},
            ],
            'example': {'all':[
                'lv create -n lv00 -g grp00 -s 10',
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'Get a list of the logical volume',
            'opts':[
            ],
            'example': {'all':[
                'lv list',
            ]},
        },
#        'info':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'Get the information of the logical volume',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<logical volume name>','dest':'lv_name','help':'Specify the name of the logical volume'},
#                {'opt':('g','group'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify the name of the volume group'},
#            ],
#            'example': {'all':[
#                'lv info -n lv00 -g grp00',
#            ]},
#        },
#        'extend':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'Extend the logical volume',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<logical volume name>','dest':'lv_name','help':'Specify the name of the logical volume'},
#                {'opt':('g','group'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify the name of the volume group'},
#                {'opt':('s','size'),'platform':'all','metavar':'<the size of the logical volume>','dest':'lv_size','help':'Specify the size of the logical volume,the unit is Mib'},
#            ],
#            'example': {'all':[
#                'lv extend -n lv00 -g grp00 -s 100',
#            ]},
#        },
#        'reduce':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'Reduce the logical volume',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<logical volume name>','dest':'lv_name','help':'Specify the name of the logical volume'},
#                {'opt':('g','group'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify the name of the volume group'},
#                {'opt':('s','size'),'platform':'all','metavar':'<the size of the logical volume>','dest':'lv_size','help':'Specify the size of the logical volume,the unit is Mib'},
#            ],
#            'example': {'all':[
#                'lv reduce -n lv00 -g grp00 -s 100',
#            ]},
#        },
        'remove':{
            'role':['puma'],
            'platform':['all'],
            'help':'Remove the logical volume',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<logical volume name>','dest':'lv_name','help':'Specify the name of the logical volume'},
                {'opt':('g','group'),'platform':'all','metavar':'<volume group name>','dest':'vg_name','help':'Specify the name of the volume group'},
            ],
            'example': {'all':[
                'lv remove -n lv00 -g grp00',
            ]},
        },
    },
    'raid':{
        'create':{
            'role':['puma'],
            'platform':['all'],
            'help':'Create a soft-raid device',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<raid device\'s name>','dest':'md_name','help':'Specify the name of the soft-raid'},
                {'opt':('l','level'),'platform':'all','metavar':'<0 | 1 | 4 | 5 | 6 | 10>','dest':'md_level','help':'Specify the level of the soft-raid'},
                {'opt':('w','width'),'platform':'all','metavar':'<raid device stripe\'s width>','dest':'md_width','help':'Specify the width of the soft-raid\'s stripe,the unit is kib'},
                {'opt':('P','raid_phy'),'platform':'all','metavar':'<md\'s physical device name>','dest':'md_phys','help':'Specify the physical device of the soft-raid'},
            ],
            'example': {'all':[
                'raid create -n md0 -l 0 -w 4 -P /dev/sda,/dev/sdb,/dev/sdc',
                'raid create -n /dev/md0 -l 0 -w 4 -P /dev/sda,/dev/sdb,/dev/sdc',
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'Get a list of the soft-raid device',
            'opts':[
            ],
            'example': {'all':[
                'raid list',
            ]},
        },
        'info':{
            'role':['puma'],
            'platform':['all'],
            'help':'Get the information the soft-raid device',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<raid device\'s name>','dest':'md_name','help':'Specify the name of the soft-raid'},
            ],
            'example': {'all':[
                'raid info -n md0',
                'raid info -n /dev/md0',
            ]},
        },
#        'extend':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'Extend the soft-raid device',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<raid device\'s name>','dest':'md_name','help':'Specify the name of the soft-raid'},
#                {'opt':('P','raid_phy'),'platform':'all','metavar':'<md\'s physical device name>','dest':'md_phys','help':'Specify the physical device of the soft-raid'},
#            ],
#            'example': {'all':[
#                'raid extend -n /dev/md0 -P /dev/sda',
#            ]},
#        },
#        'reduce':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'Reduce the soft-raid device',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<raid device\'s name>','dest':'md_name','help':'Specify the name of the soft-raid'},
#                {'opt':('P','raid_phy'),'platform':'all','metavar':'<md\'s physical device name>','dest':'md_phys','help':'Specify the physical device of the soft-raid'},
#            ],
#            'example': {'all':[
#                'raid reduce -n /dev/md0 -P /dev/sda',
#            ]},
#        },
        'remove':{
            'role':['puma'],
            'platform':['all'],
            'help':'Remove a soft-raid device',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<raid device\'s name>','dest':'md_name','help':'Specify the name of the soft-raid'},
            ],
            'example': {'all':[
                'raid remove -n md0',
                'raid remove -n /dev/md0',
            ]},
        },
    },
    'cluster': {
        'setup':{
            'role':['puma'],
            'platform':['all'],
            'help':'setup cluster',
            'opts':[
                {'opt':('n','cluster_node'),'platform':'all','metavar':'<cluster name>','dest':'cluster_name','help':'Specify cluster name'},
                {'opt':('p','passwd'),'platform':'all','metavar':'<cluster authriocation passwd>','dest':'passwd','help':'Specify cluster passwd'},
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'cluster setup -n pcmk1 -p 123456 -N 172.16.9.107, 172.16.9.108'
            ]},
        },
        'start':{
            'role':['puma'],
            'platform':['all'],
            'help':'start cluster,if option -N is specified,then start the specified node,otherwise start all the node',
            'opts':[
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify to start cluster node ,must be ip address'},
            ],
            'example': {'all':[
                'cluster start [-N 172.16.9.107]'
            ]},
        },
        'stop':{
            'role':['puma'],
            'platform':['all'],
            'help':'stop the cluster,if option -N is specified,then stop the specified node,otherwise stop all the node',
            'opts':[
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify to stop cluster node  ,must be ip address'},
            ],
            'example': {'all':[
                'cluster stop [-N 172.16.9.107]'
            ]},
        },
        'property':{
            'role':['puma'],
            'platform':['all'],
            'help':'set cluster properties and list the cluster properties',
            'opts':[
                {'opt':('o','option'),'platform':'all','metavar':'<property options>','dest':'set-option','help':'set cluster options'},
                {'opt':('a','all'),'platform':'all','action':'store_true','metavar':'<>','dest':'all','help':'show all cluster options'},
                {'opt':('d','defualt'),'platform':'all','action':'store_true','metavar':'<>','dest':'defualt','help':'show defualt cluster options'},
                {'opt':('u','unset'),'platform':'all','metavar':'<cluster property name>','dest':'unset-option','help':'unset cluster options'},
            ],
            'example': {'all':[
                'cluster property -u stonith-enabled',
                'cluster property -o stonith-enabled=true,have-watchdog=false',
                'cluster property -a',
                'cluster property -d'
            ]},
        },
#        'commit':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'commit transaction',
#            'opts':[
#            ],
#            'example': {'all':[
#                'cluster commit'
#            ]},
#        },
#        'rollback':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'rollback transaction',
#            'opts':[
#            ],
#            'example': {'all':[
#                'cluster rollback'
#            ]},
#        },
        'status':{
            'role':['puma'],
            'platform':['all'],
            'help':'show cluster status',
            'opts':[
            ],
            'example': {'all':[
                'cluster status'
            ]},
        },
        'heartbeat':{
            'role':['puma'],
            'platform':['all'],
            'help':'set cluster heartbeat,consider carefully when you do this step',
            'opts':[
                {'opt':('l','local'),'platform':'all','metavar':'<hb options>','dest':'hb1','help':'specify local heartbeat options'},
                {'opt':('r','remote'),'platform':'all','metavar':'<hb options>','dest':'hb2','help':'specify remote heartbeat options'},
                {'opt':('p','passwd'),'platform':'all','metavar':'<passwd>','dest':'passwd','help':'specify the passwd to auth the cluster'},
            ],
            'example': {'all':[
                'cluster heartbeat -l hb=172.16.9.239,host=host239 -r hb=172.16.9.241,host=host241',
            ]},
        },
        'getname':{
            'role':['puma'],
            'platform':['all'],
            'help':'show cluster name',
            'opts':[
            ],
            'example': {'all':[
                'cluster getname'
            ]},
        },
        'rename':{
            'role':['puma'],
            'platform':['all'],
            'help':'rename cluster',
            'opts':[
                {'opt':('n','cluster name'),'platform':'all','metavar':'<cluster name>','dest':'name','help':'new cluster name'},
            ],
            'example': {'all':[
                'cluster rename -n puma1.0'
            ]},
        },
    },
    'resource': {
#        'add':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'add cluster resources,you need specify block-devices and float-ip,then create ip,target,unit and constraint for you',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<res_name>','dest':'name','help':'if this specify,add a resource only'},
#                {'opt':('t','type'),'platform':'all','metavar':'<res_type>','dest':'type','help':'resource type'},
#                {'opt':('o','option'),'platform':'all','metavar':'<ip and path>','dest':'option','help':'Specify resource optionsi,ip and path'},
#            ],
#            'example': {'all':[
#                'resource add -o ip=172.16.9.110,nic=eth0,path=/dev/sdb',
#                'resource add -n myip1 -t ocf:hearbeat:IPaddr2 -o ip=172.16.9.110',
#            ]},
#        },
#        'delete':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'delete cluster resource',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
#                {'opt':('o','option'),'platform':'all','metavar':'<resource options>','dest':'option','help':'Specify resource options'},
#            ],
#            'example': {'all':[
#                'resource delete -n myip1',
#                'resource delete -o ip=172.16.9.110'
#            ]},
#        },
#        'update':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'update cluster resource',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
#                {'opt':('o','option'),'platform':'all','metavar':'<resource options>','dest':'option','help':'Specify resource options'},
#            ],
#            'example': {'all':[
#                'resource update -n myip1 -o ip=172.16.9.111'
#            ]},
#        },
        'info':{
            'role':['puma'],
            'platform':['all'],
            'help':'info a cluster resource',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
                {'opt':('t','type'),'platform':'all','metavar':'<resource type>','dest':'type','help':'Specify resource type'},
            ],
            'example': {'all':[
                'resource info -n myip1'
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'list cluster all the resource',
            'opts':[
            ],
            'example': {'all':[
                'resource list'
            ]},
        },
#        'master':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'create master resource',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<master name>','dest':'master_name','help':'Specify master name'},
#                {'opt':('r','rsc-name'),'platform':'all','metavar':'<resource name>','dest':'res_name','help':'Specify resource name'},
#                {'opt':('o','option'),'platform':'all','metavar':'<master options>','dest':'option','help':'Specify options'},
#            ],
#            'example': {'all':[
#                'resource master -n masterip -r myip1 -o max-clone-node=2'
#            ]},
#        },
#        'clone':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'clone a cluster resource',
#            'opts':[
#                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
#                {'opt':('o','option'),'platform':'all','metavar':'<clone options>','dest':'option','help':'Specify clone options'},
#                {'opt':('u','action'),'platform':'all','action':'store_true','metavar':'<add|remove>','dest':'unclone','help':'unclone'},
#            ],
#            'example': {'all':[
#                'resource clone -n myip1 -o max-clone-node=2' 
#            ]},
#        },
#        'group':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'manage cluster resource group',
#            'opts':[
#                {'opt':('a','action'),'platform':'all','action':'store_true','metavar':'<add|remove>','dest':'action','help':'add'},
#                {'opt':('n','name'),'platform':'all','metavar':'<group name>','dest':'name','help':'Specify group name'},
#                {'opt':('o','option'),'platform':'all','metavar':'<group member>','dest':'option','help':'Specify group member'},
#            ],
#            'example': {'all':[
#                'resource -a -n grp1 -o myip1 myip2',
#                'resource -n grp1 -o myip1'
#            ]},
#        },
        'move':{
            'role':['puma'],
            'platform':['all'],
            'help':'move the resource/group to specify node',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
                {'opt':('N','node'),'platform':'all','metavar':'<node name>','dest':'node','help':'Specify destination node'},
            ],
            'example': {'all':[
                'resource move -n myip1 -N node1' 
            ]},
        },
        'stop':{
            'role':['puma'],
            'platform':['all'],
            'help':'enable/disable the resource/group',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
                {'opt':('a','action'),'platform':'all','action':'store_true','metavar':'<enable/disable>','dest':'action','help':'disable'},
            ],
            'example': {'all':[
                'resource stop -a -n myip1' 
            ]},
        },
        'debug':{
            'role':['puma'],
            'platform':['all'],
            'help':'debug start the resource/stonith',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
            ],
            'example': {'all':[
                'resource debug -n myip1' 
            ]},
        },
        'cleanup':{
            'role':['puma'],
            'platform':['all'],
            'help':'cleanup the cluster resource state,if a resource is specified then cleanup it,otherwise cleanup all the resources',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
            ],
            'example': {'all':[
                'resource cleanup -n myip1' 
            ]},
        },
    },
#
#    'constraint': {
#        'add':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'add a constraint',
#            'opts':[
#                {'opt':('t','type'),'platform':'all','metavar':'<constraint type>','dest':'type','help':'Specify constraint type'},
#                {'opt':('o','option'),'platform':'all','metavar':'<constraint options>','dest':'option','help':'Specify constraint options'},
#            ],
#            'example': {'all':[
#                'constraint add -t location -o rsc=myip1,node=node1,score=80'
#            ]},
#        },
#        'delete':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'delete all constraints of the specified resource by -n or -I',
#            'opts':[
#                {'opt':('n','res-name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
#                {'opt':('I','cons-id'),'platform':'all','metavar':'<constraint id>','dest':'id','help':'Specify constraint id'},
#            ],
#            'example': {'all':[
#                'constraint delete -n myip1',
#                'constraint delete -I location-target2-node3-80'
#            ]},
#        },
#        'list':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'list all the constraint',
#            'opts':[
#            ],
#            'example': {'all':[
#                'constraint list'
#            ]},
#        },
#        'info':{
#            'role':['puma'],
#            'platform':['all'],
#            'help':'info the specified cluster constraints',
#            'opts':[
#                {'opt':('n','res-name'),'platform':'all','metavar':'<resource name>','dest':'name','help':'Specify resource name'},
#                {'opt':('I','cons-id'),'platform':'all','metavar':'<constraint id>','dest':'id','help':'Specify constraint id'},
#            ],
#            'example': {'all':[
#                'constraint info -n myip1',
#                'constraint info -I location-target2-node3-80'
#            ]},
#        },
#    },
    'stonith': {
       # 'add':{
       #     'role':['puma'],
       #     'platform':['all'],
       #     'help':'add a cluster stonith',
       #     'opts':[
       #         {'opt':('t','type'),'platform':'all','metavar':'<stonith type>','dest':'type','help':'Specify stonith type'},
       #         {'opt':('n','name'),'platform':'all','metavar':'<stonith name>','dest':'name','help':'Specify stonith name'},
       #         {'opt':('o','option'),'platform':'all','metavar':'<stonith options>','dest':'option','help':'Specify stonith options'},
       #     ],
       #     'example': {'all':[
       #         'stonith add -n myfence -t fece_scsi -o devices=/dev/sdc'
       #     ]},
       # },
       # 'delete':{
       #     'role':['puma'],
       #     'platform':['all'],
       #     'help':'delete cluster stonith',
       #     'opts':[
       #         {'opt':('n','name'),'platform':'all','metavar':'<stonith name>','dest':'name','help':'Specify stonith name'},
       #     ],
       #     'example': {'all':[
       #         'stonith delete -n myfence'
       #     ]},
       # },
       # 'update':{
       #     'role':['puma'],
       #     'platform':['all'],
       #     'help':'update cluster stonith',
       #     'opts':[
       #         {'opt':('n','name'),'platform':'all','metavar':'<stonith name>','dest':'name','help':'Specify stonith name'},
       #         {'opt':('o','option'),'platform':'all','metavar':'<stonith options>','dest':'option','help':'Specify stonith options'},
       #     ],
       #     'example': {'all':[
       #         'stonith update -n myfence -o devices=/dev/sdd'
       #     ]},
       # },
        'enable':{
            'role':['puma'],
            'platform':['all'],
            'help':'add/enable cluster stonith',
            'opts':[
                {'opt':('f','first'),'platform':'all','metavar':'<stonith options>','dest':'stopt1','help':'stonith options'},
                {'opt':('s','second'),'platform':'all','metavar':'<stonith options>','dest':'stopt2','help':'stonith options'},
            ],
            'example': {'all':[
                'stonith enable -f host=239,ip=172.16.9.240,username=admin,passwd=admin -s host=241,ip=172.16.9.238,username=admin,passwd=admin',
                'stonith enable -f id=fencing-host239 -s id=fencing-host241'
            ]},
        },
        'disable':{
            'role':['puma'],
            'platform':['all'],
            'help':'disable a cluster stonith',
            'opts':[
                {'opt':('f','first'),'platform':'all','metavar':'<stonith options>','dest':'stopt1','help':'stonith options'},
                {'opt':('s','second'),'platform':'all','metavar':'<stonith options>','dest':'stopt2','help':'stonith options'},
            ],
            'example': {'all':[
                'stonith disable -f id=fencing-host239 -s id=fencing-host241'
            ]},
        },
        'update':{
            'role':['puma'],
            'platform':['all'],
            'help':'update a cluster stonith',
            'opts':[
                {'opt':('f','first'),'platform':'all','metavar':'<stonith options>','dest':'stopt1','help':'stonith options'},
                {'opt':('s','second'),'platform':'all','metavar':'<stonith options>','dest':'stopt2','help':'stonith options'},
            ],
            'example': {'all':[
                'stonith update -f host=239,ip=172.16.9.240,username=admin,passwd=admin,id=fencing-host239 -s host=241,ip=172.16.9.238,username=admin,passwd=admin,id=fencing-host241'
            ]},
        },
        'info':{
            'role':['puma'],
            'platform':['all'],
            'help':'info a cluster stonith',
            'opts':[
                {'opt':('n','name'),'platform':'all','metavar':'<stonith name>','dest':'name','help':'Specify stonith name'},
            ],
            'example': {'all':[
                'stonith info -n myfence'
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'list cluster all the stonith',
            'opts':[
            ],
            'example': {'all':[
                'stonith list'
            ]},
        },
    },
    'date': {
        'timeinfo':{
            'role':['puma'],
            'platform':['all'],
            'help':'info system datetime',
            'opts':[
            ],
            'example': {'all':[
                'date timeinfo'
            ]},
        },
        'timeset':{
            'role':['puma'],
            'platform':['all'],
            'help':'set system datetime',
            'opts':[
                {'opt':('d','date'),'platform':'all','metavar':'<date format>','dest':'date','help':'Specify new date like 2016-02-15'},
                {'opt':('t','time'),'platform':'all','metavar':'<time format>','dest':'time','help':'Specify new time like 16:20:45'},
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'date timeset -d 2016-02-15 -t 16:25:12'
            ]},
        },
        'tzinfo':{
            'role':['puma'],
            'platform':['all'],
            'help':'info system timezone',
            'opts':[
            ],
            'example': {'all':[
                'date tzinfo'
            ]},
        },
        'tzset':{
            'role':['puma'],
            'platform':['all'],
            'help':'set system timezone',
            'opts':[
                {'opt':('t','timezone'),'platform':'all','metavar':'<timezone>','dest':'timezone','help':'Specify timezone'},
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'date tzset -t Asia/Shanghai'
            ]},
        },
        'tzlist':{
            'role':['puma'],
            'platform':['all'],
            'help':'list all the timezone',
            'opts':[
            ],
            'example': {'all':[
                'date tzlist'
            ]},
        },
        'ntpinfo':{
            'role':['puma'],
            'platform':['all'],
            'help':'info the system ntp config',
            'opts':[
            ],
            'example': {'all':[
                'date ntpinfo'
            ]},
        },
        'ntpset':{
            'role':['puma'],
            'platform':['all'],
            'help':'set system ntp server ',
            'opts':[
                {'opt':('t','timezone'),'platform':'all','metavar':'<timezone>','dest':'timezone','help':'Specify timezone'},
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
                {'opt':('p','ntp_server_url'),'platform':'all','metavar':'<ntp server url>','dest':'url','help':'Specify ntp server url'},
            ],
            'example': {'all':[
                'date ntpset -t Asia/Chongqing -N 172.16.9.239 -p 202.120.2.101'
            ]},
        },
    },
    'lun': {
        'add':{
            'role':['puma'],
            'platform':['all'],
            'help':'add a target and lun group',
            'opts':[
                {'opt':('p','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('d','device'),'platform':'all','metavar':'<store device>','dest':'path','help':'Specify store device'},
                {'opt':('o','option'),'platform':'all','metavar':'< options>','dest':'option','help':'Specify lun options'},
            ],
            'example': {'all':[
                'lun add -p 172.16.9.10 -d /dev/grp01/lv01 -o lun=1,nic=eno1'
            ]},
        },
        'delete':{
            'role':['puma'],
            'platform':['all'],
            'help':'delete the lun',
            'opts':[
                {'opt':('p','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('d','device'),'platform':'all','metavar':'<store device>','dest':'path','help':'Specify store device'},
            ],
            'example': {'all':[
                'lun delete -p 172.16.9.10 -d /dev/grp01/lv01',
                'lun delete -p 172.16.9.10',
                'lun delete -d /dev/grp01/lv01'
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'list all the lun',
            'opts':[
            ],
            'example': {'all':[
                'lun list'
            ]},
        },
        'update':{
            'role':['puma'],
            'platform':['all'],
            'help':'update the lun property',
            'opts':[
                {'opt':('p','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('d','device'),'platform':'all','metavar':'<store device>','dest':'path','help':'Specify store device'},
                {'opt':('o','lun options'),'platform':'all','metavar':'<lun options>','dest':'options','help':'Specify lun options,currently support(nic,cidr_netmask,lun,allowed_initiators) only'},
            ],
            'example': {'all':[
                'lun update -p 172.16.9.10 -d /dev/grp01/lv01 -o nic=eth0 cidr_netmask=24'
            ]},
        },
        'debug':{
            'role':['puma'],
            'platform':['all'],
            'help':'debug  target and lun group',
            'opts':[
                {'opt':('p','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('d','device'),'platform':'all','metavar':'<store device>','dest':'path','help':'Specify store device'},
            ],
            'example': {'all':[
                'lun debug -p 172.16.9.10 -d /dev/grp01/lv01'
            ]},
        },
    },
    'ip': {
        'heartbeat':{
            'role':['puma'],
            'platform':['all'],
            'help':'add a heartbeat address',
            'opts':[
                {'opt':('i','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('m','mask'),'platform':'all','metavar':'<cidr netmask>','dest':'cidr_netmask','help':'Specify net mask,default 24'},
            ],
            'example': {'all':[
                'ip heartbeat -i 172.16.9.101'
            ]},
        },
        'add':{
            'role':['puma'],
            'platform':['all'],
            'help':'add a ip',
            'opts':[
                {'opt':('i','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('g','gateway'),'platform':'all','metavar':'<gateway address>','dest':'gateway','help':'Specify gateway address'},
                {'opt':('n','nic'),'platform':'all','metavar':'<nic>','dest':'nic','help':'Specify net interface'},
                {'opt':('m','mask'),'platform':'all','metavar':'<cidr netmask>','dest':'cidr_netmask','help':'Specify net mask'},
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'ip add -i 172.16.9.101 -n eth0 -m 24 -g 172.16.9.254'
            ]},
        },
        'delete':{
            'role':['puma'],
            'platform':['all'],
            'help':'delete ip',
            'opts':[
                {'opt':('i','ip'),'platform':'all','metavar':'<ip address>','dest':'ip','help':'Specify ip address'},
                {'opt':('n','nic'),'platform':'all','metavar':'<nic>','dest':'nic','help':'Specify net interface'},
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'ip delete -i 172.16.9.101 -n eth0'
            ]},
        },
        'list':{
            'role':['puma'],
            'platform':['all'],
            'help':'list localhost ip which config in the file ifcfg-*',
            'opts':[
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'ip list'
            ]},
        },
        'nic':{
            'role':['puma'],
            'platform':['all'],
            'help':'list all the nic-interface',
            'opts':[
                {'opt':('N','cluster_node'),'platform':'all','metavar':'<cluster node>','dest':'cluster_node','help':'Specify cluster nodes'},
            ],
            'example': {'all':[
                'ip nic [-N 172.24.8.96]'
            ]},
        },
    },
}
