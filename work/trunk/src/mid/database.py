# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__,"../../db")))
import CConfigMgr
sys.path.append(os.path.abspath(os.path.join(__file__,"../../util")))
import exception
sys.path.append(os.path.abspath(os.path.join(__file__,"../../client")))
import client

"""
"""
def check_dev_is_md(db_handle,dev_name):
    try:
        db_handle.GetNode(['block-devices','raid','raids',dev_name])
        return True
    except:
        return False

"""
    check if the device is used by checking if the device is in db
"""
def device_is_used(db_handle,dev_name):
    try:
        db_handle.GetNode(['block-devices','raid','phy-devices',dev_name])
        return (True,"block-devices/raid/phy-devices/%s" % dev_name)
    except:
        try:
            db_handle.GetNode(['block-devices','lvm','pvs',dev_name])
            return (True,"block-devices/lvm/pvs/%s" % dev_name)
        except:
            return (False,None)

"""
"""
def database_md_create(db_handle,md_name,phy_devices):
    raid_path = ["block-devices",'raid','raids',md_name]
    flag = False

    try:
        db_handle.GetNode(raid_path)
        flag = True
    except Exception,e:
        db_handle.AddNode(raid_path)
        for dev in phy_devices:
            (used,path) = device_is_used(db_handle,dev)
            if used:
                raise exception.ExistsInDB("device {0} is used,{1}".format(dev,path))
            db_handle.AddNode(["block-devices","raid","raids",md_name,dev])
            try:
                db_handle.GetNode(["block-devices","raid","phy-devices",dev])
            except:
                db_handle.AddNode(["block-devices","raid","phy-devices",dev])
    if flag:
        raise exception.ExistsInDB("md %s is exists in db" % md_name)
    db_handle.Commit()

"""
"""
def database_md_device_phys(db_handle,md_name):
    raid_path = ["block-devices",'raid','raids',md_name]
    flag = False
    ret = []

    try:
        node = db_handle.GetNode(raid_path)
        for wwn in node[0].getchildren():
            ret.append(wwn.tag)
    except Exception,e:
        raise exception.ExistsInDB("md %s is not exists in db" % md_name)

    return ret

"""
    check if the md-device is in db
"""
def database_md_in_db(db_handle,md_name):
    path = ['block-devices','raid','raids',md_name]
    try:
        db_handle.GetNode(path)
        return True
    except:
        return False

"""
"""
def database_md_remove(db_handle,md_name):
    raid_entry_path = ["block-devices","raid","raids",md_name]
    try:
        db_handle.DeleteNode(raid_entry_path)
    except Exception,e:
        raise exception.NotFoundInDB("%s is not found in db" % md_name)
    db_handle.Commit()

"""
"""
def database_md_remove_crashing(db_handle,md_name):
    raid_entry_path = ["block-devices","raid","raids",md_name]

    try:
        dev_list = db_handle.GetNode(raid_entry_path)[0].getchildren()
        for dev in dev_list:
            dev_path = ["block-devices","raid","phy-devices",dev.tag]
            try:
                db_handle.DeleteNode(dev_path)
            except:
                pass
    except Exception,e:
        raise exception.NotFoundInDB("%s is not found in db" % md_name)

    try:
        db_handle.DeleteNode(raid_entry_path)
    except Exception,e:
        raise exception.NotFoundInDB("%s is not found in db" % md_name)
    db_handle.Commit()

"""
"""
def database_md_phy_zero(db_handle,device):
    dev_path = ["block-devices","raid","phy-devices",device]
    try:
        db_handle.DeleteNode(dev_path)
    except:
        raise exception.NotFoundInDB("%s is not found in db" % device)
    
    db_handle.Commit()

"""
"""
def database_md_phy_unzero(db_handle,device):
    dev_path = ["block-devices","raid","phy-devices",device]
    try:
        db_handle.AddNode(dev_path)
    except:
        pass
    
    db_handle.Commit()

"""
    add vg item to database
    @param db_handle database operation handle
    @param name vg name
    @param pvs physical volume
"""
def database_vg_create(db_handle,name,pvs):
    vg_path = ['block-devices','lvm','vgs',name]
    flag = False
    try:
        db_handle.GetNode(vg_path)
        flag = True
    except:
        db_handle.AddNode(vg_path)
      #  db_handle.Commit()
        for pv in pvs:
            (used,path) = device_is_used(db_handle,pv)
            if used:
                raise exception.ExistsInDB("device {0} is used,{1}".format(pv,path))
            db_handle.AddNode(['block-devices','lvm','vgs',name,pv])
            try:
                db_handle.GetNode(['block-devices','lvm','pvs',pv])
            except:
                db_handle.AddNode(['block-devices','lvm','pvs',pv])
    if flag:
        raise exception.ExistsInDB("vg %s is existsed in db" % name)

    db_handle.Commit()

"""
    check if the vg is in db
"""
def database_vg_in_db(db_handle,vg_name):
    path = ['block-devices','lvm','vgs',vg_name]
    try:
        db_handle.GetNode(path)
        return True
    except:
        return False

"""
"""
def database_vg_list(db_handle):
    path = ['block-devices','lvm','vgs']
    ret = []
    try:
        vg_node = db_handle.GetNode(path)
        for tag in vg_node[0].getchildren():
            ret.append(tag.tag)
        return ret
    except:
        return None

"""
"""
def database_vg_remove(db_handle,name):
    vg_path = ['block-devices','lvm','vgs',name]
    try:
        db_handle.DeleteNode(vg_path)
    except:
        raise exception.NotFoundInDB("%s is not found in db" % md_name)
    db_handle.Commit()

"""
"""
def database_vg_remove_crashing(db_handle,name):
    vg_path = ['block-devices','lvm','vgs',name]
    try:
        pvs = db_handle.GetNode(vg_path)[0].getchildren()
        for pv in pvs:
            try:
                db_handle.DeleteNode(['block-devices','lvm','pvs',pv.tag])
            except:
                pass
        db_handle.DeleteNode(vg_path)
    except:
        raise exception.NotFoundInDB("%s is not found in db" % name)

    db_handle.Commit()

"""
    add physical volume
    @param db_handle databse operation handle
    @param device physical device
"""
def database_vg_add_pv(db_handle,vg_name,device):
    try:
        db_handle.GetNode(['block-devices','lvm','vgs',vg_name])
    except:
        raise exception.NotFoundInDB("vg %s is not found in db" % vg_name)
    (used,path) = device_is_used(db_handle,device)
    if used:
        raise exception.ExistsInDB("device {0} is used,{1}".format(device,path))
    
    db_handle.AddNode(['block-devices','lvm','vgs',vg_name,device])
    db_handle.AddNode(['block-devices','lvm','pvs',device])

    db_handle.Commit()

"""
    delete pv from vg
    @param db_handle database operation handle
    @param vg_name volume
"""
def database_vg_del_pv(db_handle,vg_name,device):
    try:
        db_handle.GetNode(['block-devices','lvm','vgs',vg_name])
    except:
        raise exception.NotFoundInDB("vg %s is not found in db" % vg_name)

    db_handle.DeleteNode(['block-devices','lvm','vgs',vg_name,device])
    db_handle.Commit()

"""
    delete pv from vg drastically
    in other word,delete pv from /block-devices/lvm/pvs/
"""
def database_vg_del_pv_crashing(db_handle,vg_name,device):
    try:
        db_handle.GetNode(['block-devices','lvm','vgs',vg_name])
    except:
        raise exception.NotFoundInDB("vg %s is not found in db" % vg_name)

    db_handle.DeleteNode(['block-devices','lvm','vgs',vg_name,device])
    try:
        db_handle.DeleteNode(['block-devices','lvm','pvs',device])
    except:
        pass
    db_handle.Commit()

"""
"""
def database_pv_add(db_handle,pv_name):
    flag = False
    try:
        db_handle.GetNode(['block-devices','lvm','pvs',pv_name])
        flag = True
    except:
        db_handle.AddNode(['block-devices','lvm','pvs',pv_name])
    if flag:
        raise exception.ExistsInDB("block-devices/lvm/pvs/%s exists" % pv_name)

    db_handle.Commit()

"""
"""
def database_pv_del(db_handle,pv_name):
    try:
        db_handle.GetNode(['block-devices','lvm','pvs',pv_name])
        db_handle.DeleteNode(['block-devices','lvm','pvs',pv_name])
    except:
        raise exception.NotFoundInDB("block-devices/lvm/pvs/%s is not found" % pv_name)

    db_handle.Commit()

"""
    create drbd
    @param db_handle databse operation handle
"""
def database_drbd_create(db_handle):
    pass
