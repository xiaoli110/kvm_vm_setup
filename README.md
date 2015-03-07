kvm_vm_setup
============
KVM 虚拟机自动部署脚本，可以自动化的完成kvm虚拟机的部署，包括ip注入。

主要功能如下：

1 全自动的完成虚拟机生成、主机名、ip地址配置；
2 支持Windows系统、RHEL6/RHEL7、CentOS6/CentOS7、RHEL6/RHEL7衍生系统、Ubuntu系统的部署，其它系统未做测试；

使用前提条件：

1 Windows、Linux系统按照帮助文档要求制作镜像；
2 宿主机上，镜像、虚拟机的存储路径为/datapool；
3 如果要使用lvm，vg的名字必须是vmvg。



