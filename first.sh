#!/bin/bash
#write by xiaoli
#version 2015 02 15

# get script path
selfpath=$(cd "$(dirname "$0")"; pwd) 
echo $selfpath
cd $selfpath

# install guestfish libvirt
yum install libguest* -y
yum install libvirt* -y

# setup el6 Base and winsupport
hostos=`uname -r |grep el6`
if [[ $? -eq 0   ]];then
yum groupinstall Base
echo "host os is CentOS 6, install winsupport"
rpm -ivh $selfpath/virtscript/libguestfs-winsupport-1.0-7.el6.x86_64.rpm
fi


#setup el7 Base and winsupport
hostos=`uname -r |grep el7`
if [[ $? -eq 0   ]];then
yum group install Base
echo "host os is CentOS 7, install lib-virtinst lib-virtcli winsupport"
\cp -r -f $selfpath/virtmod/virtinst /usr/lib/python2.7/site-packages/ 
\cp -r -f $selfpath/virtmod/virtcli /usr/lib/python2.7/site-packages/ 
rpm -ivh $selfpath/virtscript/libguestfs-winsupport-7.0-2.el7.x86_64.rpm
fi
