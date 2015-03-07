Linux 镜像制作方法

1	RHEL/CentOS镜像制作方法

首先进行系统的安装，安装过程就不详细介绍了，有以下几个注意点：

（1）关于镜像大小

根据我的经验，一般Linux系统盘20GB大小比较合适。

但也不是绝对的，要根据业务类型来决定，比如在生产环境中，根据业务需要，我有的Linux系统镜像模版为150GB大小。

（2）关于分区大小

 分区建议使用自定义方式安装，boot、swap、根分区我的配置经验如下：
 
1）boot分区大小配置

boot分区建议按照下表配置：

系统	      boot分区大小(MB)

RHEL/CentOS 5系列	100

RHEL/CentOS 6系列	200

RHEL/CentOS 7系列	500

2）swap分区配置

swap一般和内存大小一致，或者安装的时候不创建swap分区，安装完成后使用文件的格式：

swap文件分区操作方法：

① 创建swap
# fallocate -l 512M /swapfile

② 启用swap

# chmod 600 /swapfile

# mkswap –f /swapfile

# swapon /swapfile

③ 验证swap是否生效，大小是否符合预期

# swapon -s

# free -m

④ 修改fstab ，使swap开机自动挂载

添加以下内容：

/swapfile            none                 swap       defaults              0 0

3）关于根分区大小和业务数据存储

建议剩余空间全部留给跟分区，业务数据存储另外挂载一块磁盘，根据业务需求配置大小。

（3）系统升级，这步很重要, 升级系统可以提升虚拟化的转换效率，使用较新的Virtio驱动，命令如下：

# yum update –y

（4）删除旧的内核

为了节约空间，删除旧的内核，并修改启动菜单不用的内核。

（5）安装基础组件和开发组件

基础组件Base和开发组件一般系统都需要使用，建议安装。

（6）yum配置

建议搭建内部yum源，好处如下：

更新速度快；

省带宽；

可以将自己制作的rpm包放入yum源中。

如果有自定义的yum源，在模版镜像中添加自建的yum源配置。

（7）配置NTP

可以配置外网的NTP地址，也可以自己搭建NTP服务，以外网NTP为例：

将/etc/ntp.conf中的ntp服务器更换为亚洲的ntp源：

# vim /etc/ntp.conf

server 0.centos.pool.ntp.org

server 1.centos.pool.ntp.org

server 2.centos.pool.ntp.org

修改为：

server 0.asia.pool.ntp.org

server 1.asia.pool.ntp.org

server 2.asia.pool.ntp.org

开启NTP服务、配置NTP服务开机运行：

# service ntpd start

# chkconfig ntpd on 

（8）关闭SELinux

SELinux和许多程序都有冲突，一般在生产环境建议关闭。

方法为修改/etc/selinux/config将SELINUX=enforcing修改为SELINUX=disabled。

2	Ubuntu、Debian虚拟机配置注意点

Ubuntu、Debian的虚拟机安装配置和CentOS类似，这里只介绍下需要注意的地方：

因为Ubuntu系统的升级比较激进，尽量选择长支持的版本和长支持的内核，

我在生产环境中碰到多次Ubuntu系统使用较新内核，系统崩溃的问题。

用手工分区，不要使用lvm方式，笔者碰到过多次使用lvm方式，重启系统的时候文件系统检查不通过的情况。

进行严格的性能和稳定性测试。
