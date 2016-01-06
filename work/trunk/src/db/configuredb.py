# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import json

database_file = '/var/lib/puma/puma.json'

class DiskConfig:
    def __init__(self,name = None,size = None,slot = None,rotational = None,protocol = None,backup = None):
        self.name     = name
        self.size     = size
        self.slot     = slot
        self.rotational= rotational
        self.protocol = protocol
        self.backup   = backup

    @staticmethod
    def create(jsons):
        return DiskConfig(jsons['name'],jsons['size'],jsons['slot'],jsons['rotational'],jsons['protocol'],jsons['backup'])

    def jsons(self):
        ret = {}
        ret['name']     = self.name
        ret['size']     = self.size
        ret['slot']     = self.slot
        ret['rotational']= self.rotational
        ret['protocol'] = self.protocol
        ret['backup']   = self.backup
        return ret

class RaidConfig:
    def __init__(self,name = None,size = None,level = None,chunk = None,disks = None):
        self.name  = name
        self.size  = size
        self.level = level
        self.chunk = chunk
        self.disks = disks
    
    @staticmethod
    def create(jsons):
        return RaidConfig(jsons['name'],jsons['size'],jsons['level'],jsons['chunk'],jsons['disks'])

    def jsons(self):
        ret = {}
        ret['name']  = self.name
        ret['size']  = self.size
        ret['level'] = self.level
        ret['chunk'] = self.chunk
        ret['disks'] = self.disks
        return ret

class VgConfig:
    def __init__(self,name = None,size = None,raids = None):
        self.name  = name
        self.size  = size
        self.raids = raids

    @staticmethod
    def create(jsons):
        return VgConfig(jsons['name'],jsons['size'],jsons['raids'])

    def jsons(self):
        ret = {}
        ret['name']  = self.name
        ret['size']  = self.size 
        ret['raids'] = self.raids
        return ret

class LvConfig:
    def __init__(self,name = None,vg_name = None,size = None):
        self.name    = name
        self.vg_name = vg_name
        self.size    = name

    @staticmethod
    def create(jsons):
        return LvConfig(jsons['name'],jsons['vg_name'],jsons['size'])
    
    def jsons(self):
        ret = {}
        ret['name']    = self.name
        ret['vg_name'] = self.vg_name
        ret['size']    = self.name
        return ret

###########################################
#        db file API                      #
###########################################
def db_file_init():
    if not os.path.exists(os.path.abspath(os.path.join(__file__,database_file))):
       fp = open(database_file,'w')
       fp.write('{}')
       fp.close()


def db_file_load():
    json_obj = None
    try:
        fp = open(database_file,'r')
        json_obj = json.load(fp)
        fp.close()
    except:
        json_obj = None
    return json_obj

def db_file_store(json_obj):
    fp = open(database_file,'w')
    json_obj = json.dump(json_obj,fp,indent = 4)
    fp.close()

###########################################
#        db disk API                      #
###########################################
def db_disk_list(json_obj):
    if not json_obj:
        return None
    if not json_obj.has_key('disk_table'):
        return None
    disk_conf_objs = []
    for disk in json_obj['disk_table']:
        disk_conf_objs.append(DiskConfig.create(disk))
    return disk_conf_objs

def _db_disk_check(disk,disks):
    if not disks:
        return None
    for i in disks:
        if i.name == disk:
            return i
    return None

def db_disk_check(disk,json_obj):
    if not json_obj:
        return None
    return _db_disk_check(disk,db_disk_list(json_obj))

def db_disk_add(disk_config,json_obj):
    if not json_obj or not json_obj.has_key('disk_table'):
        value = []
        value.append(disk_config.jsons())
        json_obj['disk_table'] =  value
    else:
        json_obj['disk_table'].append(disk_config.jsons())

def db_disks_add(disk_configs,json_obj):
    if not json_obj or not json_obj.has_key('disk_table'):
        value = []
        for i in disk_configs:
            value.append(i.jsons())
        json_obj['disk_table'] =  value
    else:
        for i in disk_configs:
            json_obj['disk_table'].append(i.jsons())

def db_disk_del(disk,json_obj):
    if not json_obj or not json_obj.has_key('disk_table'):
        return
    else:
        for obj in json_obj['disk_table']:
            if obj['name'] == disk:
                json_obj['disk_table'].remove(obj)

def db_disk_stat_used(json_obj):
    raid_configs = db_raid_list(json_obj)
    if not raid_configs:
        return None
    stats = []
    for i in raid_configs:
        for j in i.disks:
            stats.append({j:i.name})
    return stats

def _db_disk_stat_find(stats,disk):
    if not stats:
        return None
    for i in stats:
        if i.has_key(disk):
            return i
    return None

def db_disk_stat_find(json_obj,raid):
    return _db_disk_stat_find(db_disk_stat_used(json_obj),disk)

###########################################
#        db backup disk API               #
###########################################
def db_backup_disk_list(json_obj):
    if not json_obj or not json_obj.has_key('backup_disk'):
        return None
    disk_objs = []
    for i in json_obj['backup_disk']:
        disk_objs.append(DiskConfig.create(i))
    return disk_objs

def _db_backup_disk_check(disk,disk_objs):
    if not disk_objs:
        return None
    for i in disk_objs:
        if i.name == disk:
            return i
    return None

def db_backup_disk_check(disk,json_obj):
    return _db_backup_disk_check(disk,db_backup_disk_list(json_obj))

def db_backup_disk_add(disk_config,json_obj):
    if not json_obj or not json_obj.has_key('backup_disk'):
        value = []
        value.append(disk_config.jsons())
        json_obj['backup_disk'] = value
    else:
        json_obj['backup_disk'].append(disk_config.jsons())

def db_backup_disks_add(disk_configs,json_obj):
    if not json_obj or not json_obj.has_key('backup_disk'):
        value = []
        for i in disk_configs:
            value.append(i.jsons())
        json_obj['backup_disk'] = value
    else:
        for i in disk_configs:
            json_obj['backup_disk'].append(i.jsons())

def db_backup_disk_del(disk,json_obj):
    if not json_obj or not json_obj.has_key('backup_disk'):
        return
    else:
        for i in json_obj['backup_disk']:
            if i['name'] == disk:
                json_obj['backup_disk'].remove(i)

###########################################
#        db raid API                      #
###########################################
def db_raid_list(json_obj):
    if not json_obj or not json_obj.has_key('raid_table'):
        return None
    raid_objs = []
    for i in json_obj['raid_table']:
        raid_objs.append(RaidConfig.create(i))
    return raid_objs

def _db_raid_check(raid,raids):
    if not raids:
        return None
    for i in raids:
        if i.name == raid:
            return i
    return None

def db_raid_check(raid,json_obj):
    if not json_obj:
        return None
    return _db_raid_check(raid,db_raid_list(json_obj))

def db_raid_add(raid_config,json_obj):
    if not json_obj or not json_obj.has_key('raid_table'):
        value = []
        value.append(raid_config.jsons())
        json_obj['raid_table'] = value
    else:
        json_obj['raid_table'].append(raid_config.jsons())

def db_raid_del(raid,json_obj):
    if not json_obj or not json_obj.has_key('raid_table'):
        return
    else:
        for obj in json_obj['raid_table']:
            if obj['name'] == raid:
                json_obj['raid_table'].remove(obj)

def db_raid_stat_used(json_obj):
    vg_configs = db_vg_list(json_obj)
    if not vg_configs:
        return None
    stats = []
    for i in vg_configs:
        for j in i.raids:
            stats.append({j:i.name})
    return stats

def _db_raid_stat_find(stats,raid):
    if not stats:
        return None
    for i in stats:
        if i.has_key(raid):
            return i
    return None

def db_raid_stat_find(json_obj,raid):
    return _db_raid_stat_find(db_raid_stat_used(json_obj),raid)

###########################################
#        db vg API                        #
###########################################
def db_vg_list(json_obj):
    if not json_obj or not json_obj.has_key('vg_table'):
        return None
    vg_objs = []
    for i in json_obj['vg_table']:
        vg_objs.append(VgConfig.create(i))
    return vg_objs

def _db_vg_check(vg,vgs):
    if not vgs:
        return None
    for i in vgs:
        if i.name == vg:
            return i
    return None

def db_vg_check(vg,json_obj):
    if not json_obj:
        return None
    return _db_vg_check(vg,db_vg_list(json_obj))

def db_vg_add(vg_config,json_obj):
    if not json_obj or not json_obj.has_key('vg_table'):
        value = []
        value.append(vg_config.jsons())
        json_obj['vg_table'] = value
    else:
        json_obj['vg_table'].append(vg_config.jsons())

def db_vg_del(vg,json_obj):
    if not json_obj or not json_obj.has_key('vg_table'):
        return
    else:
        for obj in json_obj['vg_table']:
            if obj['name'] == vg:
                json_obj['vg_table'].remove(obj)

def db_vg_add_pv(vg,pvs,json_obj):
    ret = -1
    if not json_obj or not json_obj.has_key('vg_table'):
        return -1
    else:
        for i in json_obj['vg_table']:
            if i['name'] == vg:
                for j in pvs:
                    i['raids'].append(j)
                ret = 0
    return ret

def db_vg_del_pv(vg_name,pvs,json_obj):
    ret = -1
    if not json_obj or not json_obj.has_key('vg_table'):
        return -1
    else:
        for i in json_obj['vg_table']:
            if i['name'] == vg_name:
                for j in pvs:
                    i['raids'].remove(j)
                ret = 0
    return ret

##init db
db_file_init()
