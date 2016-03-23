# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

def host_mounted():
    try:
        mounts_file = open("/proc/mounts")
        mount_lines = mounts_file.readlines();
    finally:
        mounts_file.close()

    return mount_lines

def boot_dev():
    ss = host_mounted()
    for s in ss:
        x =s.split(' ')
        if x[1] == '/boot':
            return x[0]
