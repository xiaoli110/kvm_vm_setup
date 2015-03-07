#!/bin/bash
#version 2012 10 11
#write by yangjunjun
#set hostname and nic ip
#get all if and mac and counter

#function create network config file
if_one(){
interface_name=$1
nic1_ip=$2
nic1_netmask=$3
nic1_gateway=$4
interface_file=$5
#interface 1
echo "# The primary network interface">>$interface_file
echo "auto "$interface_name>>$interface_file
echo "iface $interface_name inet static">>$interface_file
echo "        address "$nic1_ip>>$interface_file
echo "        netmask "$nic1_netmask>>$interface_file
echo "        gateway "$nic1_gateway>>$interface_file
echo "        dns-nameservers 8.8.8.8">>$interface_file
}
if_two(){
interface1_name=$1
nic1_ip=$2
nic1_netmask=$3
nic1_gateway=$4
interface_file=$5
interface2_name=$6
nic2_ip=$7
nic2_netmask=$8

#interface 1
echo "# The primary network interface">>$interface_file
echo "auto "$interface1_name>>$interface_file
echo "iface $interface1_name inet static">>$interface_file
echo "        address "$nic1_ip>>$interface_file
echo "        netmask "$nic1_netmask>>$interface_file
echo "        gateway "$nic1_gateway>>$interface_file
echo "        dns-nameservers 8.8.8.8">>$interface_file

#interface 2
echo "# The secondary network interface">>$interface_file
echo "auto "$interface2_name>>$interface_file
echo "iface ${ifname[1]} inet static">>$interface_file
echo "        address "$nic2_ip>>$interface_file
echo "        netmask "$nic2_netmask>>$interface_file

}

#************************get variable*********
get_host_name=$1
get_gateway=$2
get_nic1_ip=$3
get_nic1_netmask=$4
get_nic1_mac=$5
get_nic2_ip=$6
get_nic2_netmask=$7
get_nic2_mac=$8
#************************get variable*********

###################set interface##########################

#backup interface configure file
nic_name_file="/etc/network/interfaces"
nic_name_file_bak="/etc/network/interfaces.bak"

if [ -f "$nic_name_file" ];then
    echo "nic file exist! backup it"
    rm $nic_name_file_bak -f
    mv $nic_name_file $nic_name_file_bak
else
   echo " nic file not exist create it   "
fi
touch $nic_name_file

#set commem

echo "# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface">>$nic_name_file
echo "auto lo">>$nic_name_file
echo "iface lo inet loopback">>$nic_name_file


##############set hostname#####################
echo "host name is "$get_host_name
if [ -z "$get_host_name" ];then
    echo "please give host name!"
    echo "variable order by hostname gateway nic1 ip nic1 netmask nic1 mac nic2 ip nic2 netmask nic2 mac"
    exit 6
else
    echo $get_host_name > /etc/hostname 
    echo "host name set OK!"
fi
################################################

#######################get interface name###################
ifname=(`/sbin/ifconfig -a |grep Link |awk '{print $1}'|grep -vE "lo|inet6|sit0"`)
ifcounter=`/sbin/ifconfig -a |grep Link|grep -vE "lo|inet6|sit0" |wc -l`
echo This VM have $ifcounter interfaces
###########################################################


######################set network config file #######
#push if and mac to array
if [ $ifcounter == 1 ];then
	echo "This VM have one network"
	if_one ${ifname[0]} $get_nic1_ip $get_nic1_netmask $get_gateway $nic_name_file
elif [ $ifcounter == 2 ];then
	echo "This VM have two network"
	if_two ${ifname[0]} $get_nic1_ip $get_nic1_netmask $get_gateway $nic_name_file ${ifname[1]} $get_nic2_ip $get_nic2_netmask
else
	echo "this VM don't have network interface"
	exit 0
fi


###############function set nic info############
/etc/init.d/networking stop
/etc/init.d/networking start

echo "++++++++++++++++++++++++++++++++++++++++++++++++"
cat $nic_name_file
echo "++++++++++++++++++++++++++++++++++++++++++++++++"
##############################################
#-----------------disable rc.local-----------------------
sed -i '/^\/bin\/bash\ \/bin\/setipbymac-ubuntu/s/^/#/' /etc/rc.local
sed -i 's/\(127.*\)/\1 "'$get_host_name'" /' /etc/hosts
sed -i 's/"/\ /g' /etc/hosts
reboot
