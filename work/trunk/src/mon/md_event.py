#!/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import logging

class MdEventError:
    SUCCESS         = 0

class MdEventEnum:
    NEWARRAY        = 'NewArray'
    STOPARRAY       = 'DeviceDisappeared'
    DEGRADED        = 'DegradedArray'
    REBUILDSTARTED  = 'RebuildStarted'
    REBUILDFINISHED = 'RebuildFinished'
    SPAREACTIVE     = 'SpareActive'
    FAILURE         = 'Fail'

"""
    md_name: /dev/md0
    md_relate_lvs: ['/dev/grp00/lv00','/dev/grp00/lv01']
    steps:
        step 1: move all the relate resource
        step 2: stop the md
"""
def md_rebuild_start_pre(md_name,md_relate_lvs):
    pass

"""
    md_name: /dev/md0
    steps:
        step 1: Assmble the md
        step 2: vgs and lvs
        step 3: pcs resource cleanup(rebalance all resource)
"""
def md_rebuild_finished(md_name):
    pass

############################
#        LOcal             #
############################
def new(target):
    pass

def stop(target):
    pass

def degraded(target):
    pass

"""
    when creating or manage -a
"""
def rebuild_stared(target):
    pass

def rebuild_finished(target):
    pass

def spare_active(target):
    pass

"""
    when disk missing
"""
def failure(target):
    pass

def md_event_dispatch(target,event):
    if event == MdEventEnum.NEWARRAY:
        new(target)
    elif event == MdEventEnum.STOPARRAY:
        stop(target)
    elif event == MdEventEnum.DEGRADED:
        degraded(target)
    elif event == MdEventEnum.REBUILDSTARTED:
        rebuild_stared(target)
    elif event == MdEventEnum.REBUILDFINISHED:
        rebuild_finished(target)
    elif event == MdEventEnum.SPAREACTIVE:
        spare_active(target)
    elif event == MdEventEnum.FAILURE:
        failure(target)
    else:
        logging.error('Get Unkonw Event %s,will be discard' % event)
