#
#   init python lib moudle
#
###############yum##########################
rpm -ivh http://mirrors.ustc.edu.cn/fedora/epel//epel-release-latest-7.noarch.rpm
yum -y install gcc gcc-c++ wget

###############protobuf#######################
yum install python-devel openssl-devel protobuf-python cmake boost-devel protobuf-devel -y 

cd /tmp && wget http://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm get-pip.py && cd -
cd RCFProto-src-1.0.0.3 && rm -rf make && mkdir make && cd make && cmake -G "Unix Makefiles" .. && make
cd RCFProto-src-1.0.0.3/python/src && python setup.py install


####################lvm2py####################
wget 'https://pypi.python.org/packages/source/l/lvm2py/lvm2py-1.0.tar.gz'
tar xf lvm2py-1.0.tar.gz
cd lvm2py-1.0
python setup.py install


