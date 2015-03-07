Windows 虚拟机制作方法

目前在生产环境使用的Windows版本主要是Windows Server 2008 R2及Windows Server 2012 R2。

本文以Windows Server 2008 R为例说明Windows系统镜像的制作方法，Windows Server 2012 R2制作方法非常类似，就不介绍了。

本文也会简单介绍下Windows Server 2003镜像的制作注意点。

需要说明的是，最新一代服务器已经不提供对Windows Server 2003驱动的支持 ，但是虚拟化对Windows Server 2003支持的很好。

如果有老的业务需要使用Windows Server 2003，通过虚拟化提供支持也是很好的解决方案。


1. Windows虚拟机的安装

（1）准备操作系统ISO文件

建议使用正版Windows ISO镜像，强烈建议生产环境不要使用非正常渠道获得的Windows ISO文件。

（2）Windows虚拟机的配置

Windows虚拟机建议根据下表来配置：

	                CPU	内存大小（MB）	硬盘方式  磁盘大小（G）	网卡方式

Windows 2003 系列	2个	512	            IDE       50GB	        e1000

Windows 2008 系列	2个	2048	          IDE       100GB	        Virtio

Windows 2012系列	4个	2048	          IDE       100GB	        Virtio

生成镜像的命令是：

qemu-img create -f qcow2 sys.img -opreallocation=metadata 100G 

为了传输管理方便，虚拟机镜像格式建议使用qcow2格式，要加上opreallocation=metadata参数。

否则使用virt-install命令安装完成后虚拟机磁盘镜像会变为raw格式。

1）关于Windows虚拟机镜像大小

直接将镜像复制，不再进行磁盘和文件系统的扩展。

这样做虽然牺牲了灵活性，但好处是生成虚拟机的时候速度要快很多。

并且生成的虚拟机第二次重启的时候，没有文件系统长时间检查的问题。

目前国内公有云大部分也都是通过复制镜像的方式进行部署。

2）关于Windows系统网卡驱动的说明

2014年上半年以前，我生产环境Windows虚拟机系统网卡使用e1000的网卡。

因为使用Virtio的网卡，在Windows系统上一直有闪断的情况。

但是到2014年底，最新发布的Virtio网卡Windows系统驱动，经过我在生产环境的检验，已经工作的非常稳定。

所以我又开始在生产环境使用Virtio网卡。

3）关于Windows虚拟机系统的磁盘驱动

开始安装系统的时候，建议磁盘驱动使用IDE方式，这样方便安装。

系统安装之后，建议将驱动更换为Virtio，因为Virtio性能要好很多，具体的操作方法在后面介绍。

（3）安装虚拟机

安装虚机有很多种方法，比如使用Virt-Manager、virt-install这样的工具，也可以通过事先定义xml文件来安装虚拟机。

以使用virt-install命令为例安装虚拟机：

virt-install \

              --hvm \

              --name windows2008 \

              --ram 2048 \

              --file=/opt/sys.img  \

              --livecd \

              --cdrom /opt/windows/windows2008.iso \

              --vnc \

              --vncport=5910

具体安装过程就不详细介绍了，但是Windows Server 2008 R2安装时候的分区需要注意。

因为2008默认安装的时候会有一个100MB的隐藏分区，放一些系统引导文件，类似Linux系统的boot分区。

但是这个分区在调整分区和文件系统的时候经常容易误导，如果不希望有这个分区，可以手工分区，方法如下：

在光盘引导起来之后，按shift加F10键，会出现一个命令行界面，键入diskpart命令，进入Windows的命令行分区模式。

diskpart类似Linux下的partd命令。
 
输入list disk命令，可以看到当前的磁盘，输入select disk 0命令，选择第一块磁盘。
 
输入create partition primary命令，将所有磁盘空间划分为一个大的主分区，输入active命令，将这个分区激活。
 
diskpart命令的详细使用可以输入help命令，查看帮助。

分区完成输入exit退出命令行界面，然后开始Windows系统的安装。

到磁盘分区的步骤时，直接选择刚才手工的分区安装就可以。
 
虚拟机安装完成后，重要的就是如何配置虚拟机系统，下面介绍如何让制作的虚拟机符合自己的需求。

2. 配置虚拟机 模版

（1）安装Virtio驱动

KVM是使用硬件虚拟化辅助技术（如Intel VT-x、AMD-V）的虚拟化引擎，在CPU运行效率方面有硬件支持，效率是比较高的。

KVM在I/O虚拟化方面，传统的方式是使用QEMU纯软件的方式来模拟I/O设备，其效率并不高。

在KVM中，可以在虚拟机中使用半虚拟化驱动（Paravirtualized Drivers，PV Drivers）来提高I/O性能。

因此在虚拟机的磁盘、网络尽量应使用Virtio设备。

1）安装硬盘Virtio驱动

首先下载硬盘Virtio驱动，下载地址：

http://www.linux-kvm.org/page/WindowsGuestDrivers/Download_Drivers。

然后新增一块临时硬盘，并将其驱动更新为SCSI模式：

qemu-img create -f qcow2 tmp.img 1G

virsh attach-disk vm --source /kvm/tmp.img --target vdb --persistent

通过热插拔方式动态增加了一块硬盘后，会在资源管理器里提示发现新的硬盘。

此时，将下载好的virto 驱动挂载到虚拟机。
打开后会发现其包括多个文件夹，其中几个文件夹对应的系统是wnet为Windows 2003 Server，wlh为Windows Server 2008 。

按照目前使用的Windows系统，安装相应目录里的驱动就行了。

安装完成后，还需要更新虚拟机xml文件中有关系统盘的配置。

使用virsh edit vmname命令，进入虚拟机xml编辑模式，找到如下的行：

<source file='/kvm/sys.img'/>

<target dev='hda' bus='ide'/>

将其修改为：

<source file='/kvm/sys.img'/>

<target dev='vda' bus='virtio'/>

参照上面的配置修改其他硬盘的xml部分，改完后关闭虚拟机，并启动。在设备管理器会发现原硬盘项已变成SCSI 。 

2）安装网卡Virtio驱动

首先手动通过热插拔方式增加一块临时网卡：

virsh attach-interface vm --type bridge --source br1 --model virtio

在设备管理器中可以看到新加的网卡，然后为新的网卡安装Virtio驱动即可，方法同Virtio磁盘的一样。

新增网卡的xml配置如下：

<interface type='bridge'>

 <mac address='32:45:11:sf:5c:3d'/>

 <source bridge='br1'/>

 <target dev='vnet3'/>

 <model type='Virtio'/>

 <alias name='net2'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0'/>

</interface> 

在安装完网卡Virtio驱动后，参照上面的配置修改其他网卡的xml文件，重启虚机后，在设备管理器里会要求重新安装驱动，安装即可。

（2）取消登录任务配置及清除任务栏记录

Windows Server 2008 R2安装完成后，默认会启动初始任务配置及服务器管理器。

为了避免打扰用户，勾选两个界面的“登录时不显示此窗口”选项。 

为了让用户得到新建的虚拟机菜单栏没有残留的程序痕迹 ，建议删除菜单的历史程序启动记录。

操作方法为，鼠标右键单机开始菜单点，选择属性，会出现“任务栏和开始菜单属性”窗口。

点击“开始菜单”按钮，将“隐私”复选框的两个选项勾取消，然后点击“应用”按钮，再勾选两个选项，在应用一次。
 
（3）配置系统更新源

为了提高同一数据中心Windows系统补丁更新速度，节省带宽，可以统一配置所以Windows虚拟机到数据中心内部的更新源进行补丁更新。

1）配置更新策略
操作方法是，同时按Windows键和R键，在弹出的“运行”对话框中中输入gpedit.msc回车，然后会启动组策略编辑器。

在组策略编辑器中依次选择“计算机配置”、“管理模板”、“Windows组件”、“Windows Update”。

右边双击配置自动更新，选择“已启用”，配置自动更新选择“2-通知下载并通知安装”，还可以根据需要定义更新的时间。
 
2）配置更新源
还是上一步的Windows Update组策略，双击“指定intranet microsoft更新位置”。

如果选择“未配置”单选按钮，此时系统将通过连接微站点自动更新。

在生产环境中一般我都会搭建自动安装服务器（WSUS）来实现加快更新速度和节省带宽的目的：

 （4）配置性能计数器

在系统遇到性能问题时，可以通过性能计数器收集到的数据方便的找出瓶颈所在。

建议根据自己业务的需要，添加相应的性能计数器。

添加性能计数器的的操作方法是：

1）同时按win键加R键，在运行对话框中输入命令：“%windir%\system32\perfmon.msc /s”回车，打开“性能监视器”。

2）选择“数据收集器”中的“用户自定义”，点击鼠标右键选择新建，打开“创建新的数据收集器集”对话框。

选择“手动创建（高级）”选项。
 
然后点击“下一步”按钮，选择“创建数据日志”复选框中的“性能计数器”。
 
根据自己的需要，添加响应的计数器选项，建议CPU、磁盘、网络、内存这些基本性能选项都添加上。

然后可以根据自己的业务需要，再添加相应的性能计数器。
 
在下一步的“日志格式”选项中，选择“逗号分隔”的格式，即csv格式，这种格式方便脚本或者电子表格分析。
 
（5）添加snmp组件

很多监控工具都需要通过snmp协议来获取监控数据，建议安装snmp组件。

安装方法为，在控制面板中，选择“程序和功能”，在打开的窗口中，选择“打开或关闭Windows功能”。

然后在“功能”选项中选择“添加功能”按钮，在打开的对话框中选择snmp组件，然后按照提示安装就可以。

（6）计算机属性设置

1）视觉性能优化
在计算机上，单机鼠标右键，选择“属性”按钮，然后选择“高级系统设置”选项，在打开的窗口中选择“高级”选型。

在“视觉”复选框中，选择“设置”按钮，然后选择“调整为最佳性能”选项。

配置这一步的原因是因为服务器系统主要是提供服务，更注重性能。
 
2）配置数据保护
接上一步，选择“数据执行保护”选项，然后选择“仅为Windows程序和服务启动DEP”。

这一步的操作目的是因为有些程序和DEP有兼容问题，会造成程序不能运行。

DEP （Data Execution Prevention）数据执行保护，是一套软硬件技术。能够在内存上执行额外检查以帮助防止在系统上运行恶意代码。

3）打开远程桌面

连接Windows虚拟机的主要方式是通过远程桌面，所以需要打开远程桌面。

操作方法为：在计算机上，单机鼠标右键，选择“属性”按钮，然后选择“远程设置”选项。

选择“允许允许任意版本远程桌面的计算机连接”选项，这个选项主要是兼容性比较好。

使用Linux的rdesktop套件都可以连接Windows计算机。

（7）通过组策略配置计算机启动执行脚本

在初始化虚拟机的过程中，用户可能需要做一些初始化配置，比如用户程序和配置文件的个性化设置，介绍下自动配置ip的操作步骤如下：

定制脚本名称、配置文件路径规范。

在虚拟机生成的时候，通过virt-copy-in命令将程序、相关配置文件、脚本复制到虚拟机里面。

在组策略里面指定开机运行脚本，（如果是Linux系统则是通过rc.local指定开机运行脚本），脚本为"c:\windows\setnicip.vbs"。

将soft_script目录下的所以脚本拷贝到模版虚拟机的c:\windows下面。

虚拟机第一次启动执行脚本，完成ip配置。

（8）配置允许系统在未登录的情况下关闭

在宿主机维护的时候，因为虚拟化管理员往往没有虚拟机系统的密码，又希望系统在未登录的情况下能正常关机。

修改组策略Windows安全选项的“关机：允许系统在未登录的情况下关闭”可以实现这个目的。
 
（9）配置Windows防火墙
Windows Server 2008 R2的防火墙，默认全部禁止数据包进入，初始配置的时候，因为用户需要远程连接。

建议开启远程桌面，为了方便判断虚拟机的状态，建议开启ICMP。

操作方法如下：在控制面板中选择“Windows防火墙”，然后选择“高级设置”，在“入站规则”中，点击鼠标右键。

选择“新建规则”，选择“自定义”：
 
下一步选择“TCP”，在“本地端口”中，选择“特定端口”，输入端口号“3399”，然后按照提示完成操作就可以。

同样的，在新建一个规则，选择ICMP，协议选择ICMPv4，其他按照提示操作就可以：
 
（10）配置精确时钟和NTP服务器

虚拟机都有时间漂移的现象，Windows虚拟机需要配置精确时钟和NTP服务器。

1）精确时钟的配置方法

Windows Server 2003开启精确时钟设置方法为，修改c:\boot.ini ，再启动行最后增加/usepmtimer参数。

另外，有时候需要进入安全方式进行配置，为了Windows Server 2003方便进入安全方式，在c:\boot.ini增加一行以设置进入安全方式。

修改后的boot.ini如下：

[boot loader]

rem 启动菜单时间为5秒钟

timeout=5

default=multi(0)disk(0)rdisk(0)partition(1)\WINDOWS

[operating systems]

rem 正常启动菜单

multi(0)disk(0)rdisk(0)partition(1)\WINDOWS="Windows Server 2003, Enterprise" /noexecute=optout /fastdetect /usepmtimer

rem 安全方式启动菜单

multi(0)disk(0)rdisk(0)partition(1)\WINDOWS="Safe Mode" /safeboot:minimal /fastdetect /usepmtimer

Windows Server 2008 R2配置精确时钟的方法为，在命令行方式下运行以下命令：

C:\Windows\system32>bcdedit /set {default} USEPLATFORMCLOCK on

2）NTP服务器配置

在桌面右下角的时间上，点击鼠标，选择“更改时间和日期”，在“Internet时间”选项中，输入自己的NTP服务器地址。

（11）IE配置

1）IE浏览器主页设置为空白页面，IE浏览器删除历史记录。

2）关闭IE浏览器的增强安全配置。

操作方法为，在服务器管理器中选择配置“IE ESC”。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
 
将“管理员”和“用户”的IE增强的安全配置禁用。

（12）网络配置

为了安全起见，关闭Windows的网络共享和WINS解析，关闭网络配置中的IPV6、微软网络客户端、文件和打印机共享选秀。

禁用TCP/IP协议中的WINS。
 
16.1.2	Windows 虚拟机sysprep初始化封装

镜像制作中，一般安装好系统，并设定好所有标准化选项，之后应进行系统封装。

以便通过镜像部署的虚拟机在首次启动时自动更新SID、配置、主机名。

如果不更新SID，通过模板部署的所有虚拟机SID都一样，这些虚拟机如果要加入Windows域就会有问题。

所以为了保险起见，在制作镜像过程中，最好进行镜像的封装，下面介绍下Windows封装的方法。

提示：
SID是每个Windows系统的唯一标识符，根据我的生产环境的经验，如果Windows系统不加入域，不进行系统封装也可以正常稳定的运行。

但是这样克隆出来的虚拟机会出现主机名同名的问题，解决方法是通过初始化脚本实现主机名随机修改。

另外，Windows Server 2003也可以通过newsid这个工具进行修改。

Windows Server 2008 R2如果要修改SID必须使用微软的封装方法。

1.Windows Server 2003的封装

Windows Server 2003的封装方法如下：

（1）在Windows Server 2003系统安装光盘中找到SUPPORT目录下TOOLS文件夹，将DEPLOY.CAB内的所有文件解压到到C盘Sysprep文件夹。

（2）运行其中的sysprep.exe，在下一步的封装主界面中选“重新封装”。 

（3）大概10-20秒封装准备完成后，系统自动关机。

通过以上步骤后，就可以把此封装后的虚拟机转化为模板，之后就可以通过此模板部署虚拟机了。

以上封装好的系统，首次启动会有对话框要求用户提供必要设定信息，如：主机名、区域语言设定等。

对于批量部署虚拟机每台都手动输入非常不方便，为了解决这个问题，微软提供自动应答文件的方案，

以便封装好的系统首次启动自动运行应对文件，不需要用户手动输入信息，具体设定步骤如下：

在运行封装之前，首先点击运行sysprep文件夹下的setupmgr.exe，安装向导会指导一步步完成自动应答文件的生成，

过程很简单，就不详细介绍了。

全部输入完毕后，结束向导，会在sysprep目录下生成一个叫sysprep.inf的应答文件，

自动应答文件生成后，再运行sysprep.exe进行封装就可以了，通过镜像克隆的系统首次运行就可以自动完成配置。

2. Windows 2008 R2封装

Windows Server 2008的封装工具位于C:\Windows\System32\sysprep 下，不需要安装光盘。

双击运行其中的sysperp，选择“OOBE”和下面的“通用”，确定后开始封装，结束后会自动关机。

Windows Server 2008 R2也可以制作自动应答文件，需要在微软网站下载相关的工具，

配置方法请参考微软官网的相关文档，就不作详细介绍了。
