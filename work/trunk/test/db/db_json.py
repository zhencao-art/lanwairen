import sys,os
sys.path.append(os.path.abspath(os.path.join(__file__,'../../../src/db')))

from configuredb import *

def test_disk():
    json_obj = db_file_load()

    if json_obj == None:
        print "load file error"
        return
    
    raid_config = RaidConfig('md0',['wwn-1','wwn-2'])
    if db_raid_check('md0',json_obj):
        print "md0 is exists in db"
        print '---------add md0----------------'
    else:
        db_raid_add(raid_config,json_obj) 
        for i in db_raid_list(json_obj):
            print i.jsons()
        for i in db_disk_list(json_obj):
            print i.jsons()
        print '---------add md0----------------'

    raid_config = RaidConfig('md1',['wwn-3','wwn-4'])
    if db_raid_check('md1',json_obj):
        print "md1 is exists in db"
        print '--------add md1-----------------'
    else:
        db_raid_add(raid_config,json_obj) 
        for i in db_raid_list(json_obj):
            print i.jsons()
        for i in db_disk_list(json_obj):
            print i.jsons()
        print '--------add md1-----------------'

    if not db_raid_check('md1',json_obj):
        print 'md1 is not found in db'
    else:
        db_raid_del('md1',json_obj)
        for i in db_raid_list(json_obj):
            print i.jsons()
        for i in db_disk_list(json_obj):
            print i.jsons()
        print '---------del md1----------------'

    if not db_raid_check('md2',json_obj):
        print 'md1 is not found in db'
        print '---------del md2----------------'
    else:
        db_raid_del('md2',json_obj)
        for i in db_raid_list(json_obj):
            print i.jsons()
        for i in db_disk_list(json_obj):
            print i.jsons()
        print '---------del md2----------------'

    raid_config = RaidConfig('md0',['wwn-1','wwn-2'])
    if db_raid_check('md0',json_obj):
        print "md0 is exists in db"
        print '--------add md0-----------------'
    else:
        db_raid_add(raid_config,json_obj) 
        for i in db_raid_list(json_obj):
            print i.jsons()
        for i in db_disk_list(json_obj):
            print i.jsons()
        print '--------add md0-----------------'

    vg_config = VgConfig('grp00',['md0','md1'])
    if db_vg_check('grp00',json_obj):
        print "grp00 is exists in db"
        print '--------add vg00-----------------'
    else:
        db_vg_add(vg_config,json_obj)
        for i in db_vg_list(json_obj):
            print i.jsons()
        print '--------add vg00-----------------'

   # if not db_vg_check('grp00',json_obj):
   #     print "grp00 is not found in db"
   #     print '--------del vg00-----------------'
   # else:
   #     db_vg_del('grp00',json_obj)
   #     for i in db_vg_list(json_obj):
   #         print i.jsons()
   #     print '--------del vg00-----------------'
    
    for i in db_disk_name_used(json_obj):
        print i
    for i in db_raid_name_used(json_obj):
        print i

    db_file_store(json_obj)

def run_test():
    test_disk()

if __name__ == '__main__':
    run_test()
