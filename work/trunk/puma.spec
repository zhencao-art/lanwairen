Name:       puma
Version:    1.0.0
Release:    1%{?dist}
Summary:    Phegda Puma
Vendor:     Phegda Technologies
Packager:   Zhen Cao <zhen_cao@pbdata.com.cn>

Group:      Storage
License:    ASL 2.0
URL:        http://www.phegda.com/
Source:     puma.tar.gz
BuildRoot:  %{_tmppath}/puma-buildroot-%{%{__id_u}-n}

Provides:   puma

BuildRequires: make
Requires:   mdadm lvm2 targetcli
Requires:   pacemaker corosync
Requires:   protobuf

%description
Phegda Puma

%prep
%setup -c

%build
make

%pre

%install
%{__install} -d %{buildroot}/opt/puma
%{__install} -d %{buildroot}/opt/puma/conf
%{__install} -p -m 0644 conf/puma.conf %{buildroot}/opt/puma/conf
%{__install} -d %{buildroot}/opt/puma/ocf
%{__install} -d %{buildroot}/opt/puma/ocf/heartbeat
%{__install} -p -m 0755 ocf/hearbeat/* %{buildroot}/opt/puma/ocf/heartbeat
%{__install} -d %{buildroot}/usr/lib/systemd/system
%{__install} -p -m 0644 systemd/puma.service %{buildroot}/usr/lib/systemd/system
%{__install} -p -m 0644 systemd/puma-watchdog.service %{buildroot}/usr/lib/systemd/system
%{__install} -p -m 0644 systemd/puma-watchdog.timer %{buildroot}/usr/lib/systemd/system

%{__install} -p -m 0755 puma-watchdog %{buildroot}/opt/puma
%{__install} -p -m 0755 puma-init.sh %{buildroot}/opt/puma

##client
%{__install} -p -m 0755 pumacli %{buildroot}/opt/puma
%{__install} -d %{buildroot}/opt/puma/src/client
%{__install} -p -m 0644 src/client/*.py %{buildroot}/opt/puma/src/client
%{__install} -d %{buildroot}/opt/puma/src/client/commandline
%{__install} -p -m 0644 src/client/commandline/*.py %{buildroot}/opt/puma/src/client/commandline
%{__install} -d %{buildroot}/opt/puma/src/client/commandline/handle
%{__install} -p -m 0644 src/client/commandline/handle/*.py %{buildroot}/opt/puma/src/client/commandline/handle
%{__install} -d %{buildroot}/opt/puma/src/client/commandline/view
%{__install} -p -m 0644 src/client/commandline/view/*.py %{buildroot}/opt/puma/src/client/commandline/view

%{__install} -p -m 0755 server %{buildroot}/opt/puma
%{__install} -d %{buildroot}/opt/puma/src/cluster
%{__install} -p -m 0644 src/cluster/*.py %{buildroot}/opt/puma/src/cluster
%{__install} -d %{buildroot}/opt/puma/src/cluster/clustermgr
%{__install} -p -m 0644 src/cluster/clustermgr/*.py %{buildroot}/opt/puma/src/cluster/clustermgr
%{__install} -d %{buildroot}/opt/puma/src/cluster/common
%{__install} -p -m 0644 src/cluster/common/*.py %{buildroot}/opt/puma/src/cluster/common
%{__install} -d %{buildroot}/opt/puma/src/cluster/constraint
%{__install} -p -m 0644 src/cluster/constraint/*.py %{buildroot}/opt/puma/src/cluster/constraint
%{__install} -d %{buildroot}/opt/puma/src/cluster/resource
%{__install} -p -m 0644 src/cluster/resource/*.py %{buildroot}/opt/puma/src/cluster/resource
%{__install} -d %{buildroot}/opt/puma/src/cluster/stonith
%{__install} -p -m 0644 src/cluster/stonith/*.py %{buildroot}/opt/puma/src/cluster/stonith
%{__install} -d %{buildroot}/opt/puma/src/db
%{__install} -p -m 0644 src/db/*.py      %{buildroot}/opt/puma/src/db
%{__install} -d %{buildroot}/opt/puma/src/nic
%{__install} -p -m 0644 src/nic/*.py      %{buildroot}/opt/puma/src/nic
%{__install} -d %{buildroot}/opt/puma/src/ip
%{__install} -p -m 0644 src/ip/*.py      %{buildroot}/opt/puma/src/ip
%{__install} -d %{buildroot}/opt/puma/src/mid
%{__install} -p -m 0644 src/mid/*.py     %{buildroot}/opt/puma/src/mid
%{__install} -d %{buildroot}/opt/puma/src/server
%{__install} -p -m 0644 src/server/*.py   %{buildroot}/opt/puma/src/server
%{__install} -d %{buildroot}/opt/puma/src/storage
%{__install} -p -m 0755 src/storage/sas2ircu %{buildroot}/opt/puma/src/storage
%{__install} -p -m 0644 src/storage/*.py %{buildroot}/opt/puma/src/storage
%{__install} -d %{buildroot}/opt/puma/src/time
%{__install} -p -m 0644 src/time/*.py %{buildroot}/opt/puma/src/time
%{__install} -d %{buildroot}/opt/puma/src/time/ntp-conf
%{__install} -p -m 0644 src/time/ntp-conf/*.py %{buildroot}/opt/puma/src/time/ntp-conf
%{__install} -d %{buildroot}/opt/puma/src/util
%{__install} -p -m 0644 src/util/*.py %{buildroot}/opt/puma/src/util

%post
mkdir -p /var/lib/puma
#backup resource.d
cp /usr/lib/ocf/resource.d/heartbeat/iSCSILogicalUnit /usr/lib/ocf/resource.d/heartbeat/iSCSILogicalUnit.bak >/dev/null 2>&1
cp /usr/lib/ocf/resource.d/heartbeat/iSCSITarget /usr/lib/ocf/resource.d/heartbeat/iSCSITarget.bak >/dev/null 2>&1
cp -f /opt/puma/ocf/heartbeat/* /usr/lib/ocf/resource.d/heartbeat
#add pumacli into /usr/sbin
ln -s -f /opt/puma/pumacli /usr/sbin/pumacli
#start
systemctl start puma.service > /dev/null 2>&1
systemctl start puma-watchdog.timer > /dev/null 2>&1
systemctl enable puma.service > /dev/null 2>&1
systemctl enable puma-watchdog.timer > /dev/null 2>&1

%preun
systemctl disable puma.service > /dev/null 2>&1
systemctl disable puma-watchdog.timer > /dev/null 2>&1
systemctl stop puma-watchdog.timer > /dev/null 2>&1
systemctl stop puma > /dev/null 2>&1

%postun
#rm -rf /var/lib/puma

rm -rf /opt/puma >/dev/null 2>&1
rm -f /usr/lib/ocf/resource.d/heartbeat/md_raid >/dev/null 2>&1
rm -f /usr/lib/ocf/resource.d/heartbeat/dnt_lv >/dev/null 2>&1
rm -f /usr/lib/ocf/resource.d/heartbeat/iSCSILogicalUnit >/dev/null 2>&1

#recovery the old setting
cp /usr/lib/ocf/resource.d/heartbeat/iSCSILogicalUnit.bak /usr/lib/ocf/resource.d/heartbeat/iSCSILogicalUnit >/dev/null 2>&1
rm -f /usr/lib/ocf/resource.d/heartbeat/iSCSITarget >/dev/null 2>&1
cp /usr/lib/ocf/resource.d/heartbeat/iSCSITarget.bak /usr/lib/ocf/resource.d/heartbeat/iSCSITarget >/dev/null 2>&1

#rm /usr/sbin/pumacli
rm -rf /usr/sbin/pumacli

%clean
[ "${RPM_BUILD_ROOT}" != "/" -a -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%dir /opt/puma
%dir /opt/puma/conf
%dir /opt/puma/src
%dir /opt/puma/src/client
%dir /opt/puma/src/client/commandline
%dir /opt/puma/src/client/commandline/handle
%dir /opt/puma/src/client/commandline/view
%dir /opt/puma/src/cluster
%dir /opt/puma/src/cluster/clustermgr
%dir /opt/puma/src/cluster/common
%dir /opt/puma/src/cluster/constraint
%dir /opt/puma/src/cluster/resource
%dir /opt/puma/src/cluster/stonith
%dir /opt/puma/src/db
%dir /opt/puma/src/ip
%dir /opt/puma/src/nic
%dir /opt/puma/src/mid
%dir /opt/puma/src/server
%dir /opt/puma/src/storage
%dir /opt/puma/src/time
%dir /opt/puma/src/time/ntp-conf
%dir /opt/puma/src/util

%config(noreplace) /opt/puma/conf/puma.conf

/opt/puma/ocf/heartbeat/dnt_lv
/opt/puma/ocf/heartbeat/iSCSILogicalUnit
/opt/puma/ocf/heartbeat/iSCSITarget
/opt/puma/ocf/heartbeat/md_raid
/usr/lib/systemd/system/puma.service
/usr/lib/systemd/system/puma-watchdog.service
/usr/lib/systemd/system/puma-watchdog.timer

/opt/puma/pumacli
/opt/puma/puma-watchdog
/opt/puma/puma-init.sh
/opt/puma/conf/puma.conf
/opt/puma/server
/opt/puma/src/client/*.py
/opt/puma/src/client/*.pyc
/opt/puma/src/client/*.pyo
/opt/puma/src/client/commandline/*.py
/opt/puma/src/client/commandline/*.pyc
/opt/puma/src/client/commandline/*.pyo
/opt/puma/src/client/commandline/handle/*.py
/opt/puma/src/client/commandline/handle/*.pyc
/opt/puma/src/client/commandline/handle/*.pyo
/opt/puma/src/client/commandline/view/*.py
/opt/puma/src/client/commandline/view/*.pyc
/opt/puma/src/client/commandline/view/*.pyo
/opt/puma/src/cluster/*.py
/opt/puma/src/cluster/*.pyc
/opt/puma/src/cluster/*.pyo
/opt/puma/src/cluster/clustermgr/*py
/opt/puma/src/cluster/clustermgr/*pyc
/opt/puma/src/cluster/clustermgr/*pyo

/opt/puma/src/cluster/common/*py
/opt/puma/src/cluster/common/*pyc
/opt/puma/src/cluster/common/*pyo
/opt/puma/src/cluster/constraint/*py
/opt/puma/src/cluster/constraint/*pyc
/opt/puma/src/cluster/constraint/*pyo
/opt/puma/src/cluster/resource/*py
/opt/puma/src/cluster/resource/*pyc
/opt/puma/src/cluster/resource/*pyo
/opt/puma/src/cluster/stonith/*py
/opt/puma/src/cluster/stonith/*pyc
/opt/puma/src/cluster/stonith/*pyo
/opt/puma/src/db/*py
/opt/puma/src/db/*pyc
/opt/puma/src/db/*pyo
/opt/puma/src/nic/*py
/opt/puma/src/nic/*pyc
/opt/puma/src/nic/*pyo
/opt/puma/src/ip/*py
/opt/puma/src/ip/*pyc
/opt/puma/src/ip/*pyo
/opt/puma/src/mid/*py
/opt/puma/src/mid/*pyc
/opt/puma/src/mid/*pyo
/opt/puma/src/server/*py
/opt/puma/src/server/*pyc
/opt/puma/src/server/*pyo
/opt/puma/src/storage/*py
/opt/puma/src/storage/sas2ircu
/opt/puma/src/storage/*pyc
/opt/puma/src/storage/*pyo
/opt/puma/src/time/*py
/opt/puma/src/time/*pyc
/opt/puma/src/time/*pyo
/opt/puma/src/time/ntp-conf/*py
/opt/puma/src/time/ntp-conf/*pyc
/opt/puma/src/time/ntp-conf/*pyo
/opt/puma/src/util/*py
/opt/puma/src/util/*pyc
/opt/puma/src/util/*pyo

%changelog
* Thu Mar 3 2016 zhen_cao<zhen_cao@pbdata.com.cn> 1.0.0.1
 add soft link /usr/sbin/pumacli puma-init.sh
