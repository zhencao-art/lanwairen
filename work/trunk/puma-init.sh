#!/usr/bin/sh

#firewalld
systemctl stop firewalld
systemctl disable firewalld

#selinux
setenforce 0
sed '7c SELINUX=permissive' /etc/selinux/config -i


#lvm2 metad
lvmconf --disable-cluster
sed 's/use_lvmetad = 1/use_lvmetad = 0/g' /etc/lvm/lvm.conf -i

systemctl stop lvm2-lvmetad.service
systemctl disable lvm2-lvmetad.service

systemctl stop lvm2-lvmetad.socket
systemctl disable lvm2-lvmetad.socket

#targetcli
targetcli /iscsi set global auto_add_default_portal=false
