Name:freebird
Version:1.0.0
Release:	1%{?dist}
Summary:Hit or Fuck Great Wall

Group:Freedom
License:GPL
URL:www.freedom.org
Source0:freebird.tar.gz
BuildRoot:%{_tmppath}/%{name}-%{version}-%{release}-root

%description
free bird

%prep
%setup -c -n %{name}-%{version}

%build


%install
%{__install} -d %{buildroot}/usr/bin
%{__install} -d %{buildroot}/etc
%{__install} -d %{buildroot}/usr/lib/systemd/system

%{__install} -p -m 0755 freebird.py %{buildroot}/usr/bin
%{__install} -p -m 0644 freebird.conf %{buildroot}/etc/freebird.conf
%{__install} -p -m 0644 freebird.service %{buildroot}/usr/lib/systemd/system
%{__install} -p -m 0644 freebird.timer %{buildroot}/usr/lib/systemd/system

%clean
rm -rf %{buildroot}


%files
/usr/bin/freebird.py
/etc/freebird.conf
/usr/lib/systemd/system/freebird.service
/usr/lib/systemd/system/freebird.timer

%changelog

