kvm_vm_setup
============
KVM 虚拟机自动部署脚本，可以自动化的完成kvm虚拟机的部署，包括ip注入。

主要功能如下：

1 全自动的完成虚拟机生成、主机名、ip地址配置；

2 支持Windows系统、RHEL6/RHEL7、CentOS6/CentOS7、RHEL6/RHEL7衍生系统、Ubuntu系统的部署，其它系统未做测试；

使用前提条件：

1 Windows、Linux系统按照帮助文档要求制作镜像:

Windows 镜像制作请参考Windows_img_make,Linux镜像制作请参考Linux_img_make；

2 宿主机上，镜像、虚拟机的存储路径为/datapool；

3 如果要使用lvm，vg的名字必须是vmvg；

4 宿主机系统只支持RHEL6/RHEL7、CentOS6/CentOS7、RHEL6/RHEL7衍生系统，本脚本通过调用Libvirt配置虚拟机，通过guestfish编辑虚拟机镜像，需要安装虚拟化组件、Libvirt组件、guestfish组件：

首先需要运行firsh.sh脚本，会自动判断操作系统，并安装组件，升级操作系统。

安装完成后重启系统，并启动libvirt服务。

service libvirtd restart


使用方法：

1 下载脚本源代码

git clone https://github.com/xiaoli110/kvm_vm_setup

2 编辑vm.csv文件，格式如下：

\#vmflag,template,name,disk1_size,disk2_size,mem_size,cpu_num,nic_type,nic1_bridge,nic2_bridge,vnc_port,outip,outmask,outgw,inip,inmask,ingw

\#vm template name must be ''win2003ent32chs' 'win2003ent64chs' 'win2008ent64chs' 'centos56x64' 'ubuntu1204X64'

\#keyword vmLvm means create lvm for vm,default vg is datavg

\#keyword vmCpOnly means not resize images , just cp imaiges,default vg is datavg

\#kerword url: means download vm images path,like 

\#url:http://172.16.1.100/

ftp:ftp://ftpuser1:password@ftp.myimages.com:10021/

ftp:ftp://ftpuser2:password@ftp.myimages2.com:10021/


此处如果指定url，会到url上去拉去虚拟机镜像，支持ftp方式，拉取方式为url加镜像名字，镜像名字为下面虚拟机配置文件中的镜像名字。

可以指定两个url，脚本会自动比较多个url的速度，需要在url里面放置一个200MB大小的名为“ratetest”的文件。

vm,win2003ent32chs,win2003-138,20G,20G,2048,2,e1000,br1,br1,5921,10.10.10.21,255.255.255.0,10.10.10.1,192.168.122.138,255.255.255.0,none

vmLvm,win2003ent32chs,virt1-lab-222,10G,10G,2048,2,e1000,br2,br2,59222,10.0.0.222,255.0.0.0,10.0.0.1,172.16.2.222,255.255.255.0,none

vm,win2003ent32chs,virt1-lab-29,10G,100G,2048,2,e1000,br1,br1,5929,10.0.0.29,255.0.0.0,10.0.0.1,172.16.2.29,255.255.255.0,none

vm,win2003ent64chs,virt1-lab-23,10G,100G,2048,2,e1000,br1,br1,5923,10.0.0.23,255.0.0.0,10.0.0.1,172.16.2.23,255.255.255.0,none

vm,win2008ent64chs,win2008-22,40G,20G,2048,2,e1000,br1,br1,5922,10.0.0.22,255.0.0.0,10.0.0.1,172.16.2.124,255.255.255.0,none

vm,win2008ent64chs,win2008-23,40G,20G,2048,2,e1000,br1,br1,5923,10.0.0.23,255.0.0.0,10.0.0.1,172.16.2.125,255.255.255.0,none

vmLvm,win2008ent64chs,virt1-lab-224,30G,10G,2048,2,e1000,br2,br2,59224,10.0.0.224,255.0.0.0,10.0.0.1,172.16.2.224,255.255.255.0,none

vm,centos56x64,centos5-121,20G,20G,1048,2,virtio,br1,br1,5923,10.10.10.23,255.255.255.0,10.10.10.1,192.168.122.121,255.255.255.0,none

vm,ubuntu1204X64,ubuntu-120,30G,10G,1048,2,virtio,br0,virbr0,59120,10.10.10.120,255.255.255.0,10.10.10.1,192.168.122.120,255.255.255.0,none

vmCpOnly,centos6564.qcow2,centos65-8,30G,20G,2048,2,virtio,br1,br1,59008,10.10.10.8,255.255.255.0,10.10.10.1,172.16.2.8,255.255.255.0,none

vm,centos6564.qcow2,centos65-9,30G,20G,2048,2,virtio,br1,br1,59009,10.10.10.9,255.255.255.0,10.10.10.1,172.16.2.9,255.255.255.0,none

vm,centos7.qcow2,centos7-189,120G,20G,4096,4,virtio,br0,br1,59189,10.20.102.189,255.255.255.0,10.20.102.1,172.16.2.189,255.255.255.0,none

vmCpOnly,centos7.qcow2,centos7-190,120G,20G,4096,4,virtio,br0,br1,59190,10.20.102.190,255.255.255.0,10.20.102.1,172.16.2.190,255.255.255.0,none

vm,win2012datacenter_chs,win2012-11,50G,20G,2048,2,e1000,br1,br1,5911,10.10.10.11,255.255.255.0,10.10.10.1,172.16.2.11,255.255.255.0,none

虚拟机生成配置文件信息如下：

第一个关键字意义如下：

vm 使用qcow2方式，并通过guestfish进行文件系统的扩展；

vmLvm 使用lvm方式；

vmCpOnly 使用qcow2方式，直接复制镜像。

第二个关键字为镜像名字，建议名字包含操作系统信息。

后面的配置关机字依次为虚拟机主机名，第一块磁盘大小，第二块磁盘大小，CPU、内存配置等信息。

注意：

1 如果使用vm关键字进行磁盘扩展，第一块磁盘必须大于镜像；

2 每个关键字必须有内容，第二块磁盘必须有，最小为1G；

3 ip地址合法性本脚本不作检查；

4 CentOS7的虚拟机只支持在CentOS7的宿主机上进行配置。

运行脚本

使用命令

python virtauto.py 就可以自动生成虚拟机。

virtauto.py 帮助信息如下：

kvm vm setup script

-h, --help print this

--vg,assige vg name,such as --vg=datavg,vg=vmVG

default vg name is 'datavg' if not assige

--config,assige config file name ,such as --config=vm.csv

config file must in same directory and must be csv

default config file name is 'vm.csv' if not assige

--url,give path to download vm images,such as --url=ftp://user1:pass@172.16.1.100/





