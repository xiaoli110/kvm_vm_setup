#!/bin/bash
#version 2012 05 18
#version 2015 02 14 add suport for CentOS7
#write by xiaoli
#set hostname and nic ip
#get all if and mac and counter

################function set nic info############
set_nic_ip(){
nic_name=$1
nic_ip=$2
nic_netmask=$3
nic_name_file="/etc/sysconfig/network-scripts/ifcfg-"$nic_name
nic_name_file_bak="/etc/sysconfig/network-scripts/ifcfg-"$nic_name".bak"
if [ -z "$nic_name" ];then
    echo "no nic name give!"
    exit 5
else
    echo " nic name check ok   "
fi
echo "nic_name is" $nic_name
echo "nic_ip is" $nic_ip
echo "nic_netmask is " $nic_netmask
echo "nic file name is " $nic_name_file
if [ -f "$nic_name_file" ];then
    echo "nic file exist! backup it"
    rm $nic_name_file_bak -f
    mv $nic_name_file $nic_name_file_bak
else
   echo " nic file not exist create it   "
fi
touch $nic_name_file
echo "DEVICE="$nic_name >>$nic_name_file
echo "BOOTPROTO=none" >>$nic_name_file
echo "ONBOOT=yes" >>$nic_name_file
echo "TYPE=Ethernet" >>$nic_name_file
echo "IPADDR="$nic_ip >>$nic_name_file
echo "NETMASK="$nic_netmask >>$nic_name_file
/sbin/ifdown $nic_name
/sbin/ifup $nic_name
echo "++++++++++++++++++++++++++++++++++++++++++++++++"
cat $nic_name_file
echo "++++++++++++++++++++++++++++++++++++++++++++++++"
}
##############################################


#************************get variable*********
mac1=$5
mac2=$8
uname -r |grep el7
if [[ $? -eq 0   ]];then
    #typeset -i get_nic1_mac
    #get_nic1_mac="${mac1}"
    get_nic1_mac=$(echo $mac1 | tr '[A-Z]' '[a-z]') 
    get_nic2_mac=$(echo $mac2 | tr '[A-Z]' '[a-z]') 
else
    get_nic1_mac="${mac1}"
    get_nic2_mac="${mac2}"
fi
get_host_name=$1
get_gateway=$2
get_nic1_ip=$3
get_nic1_netmask=$4
#get_nic1_mac=$5
get_nic2_ip=$6
get_nic2_netmask=$7
#get_nic2_mac=$8
echo "test" >>/root/setmac.txt
#************************get variable*********

##############set hostname#####################
echo "host name is "$get_host_name
if [ -z "$get_host_name" ];then
    echo "please give host name!"
    echo "variable order by hostname gateway nic1 ip nic1 netmask nic1 mac nic2 ip nic2 netmask nic2 mac"
    exit 6
else
    sed -i 's/.*HOSTNAME.*/HOSTNAME\="'$get_host_name'"/g' /etc/sysconfig/network 
    hostnamectl set-hostname $get_host_name
    echo "host name set OK!"
fi
################################################

##############set gateway#####################
echo "gate way  is"$get_gateway
if [ -z "$get_gateway" ];then
    echo "please give gateway!"
    echo "variable order by hostname gateway nic1 ip nic1 netmask nic1 mac nic2 ip nic2 netmask nic2 mac"
    exit 7
else
    if [ `cat /etc/sysconfig/network |grep GATEWAY |wc -l`  -eq 1  ];then
        sed -i 's/.*GATEWAY.*/GATEWAY\="'$get_gateway'"/g' /etc/sysconfig/network 
    else
        echo "GATEWAY="$get_gateway >> /etc/sysconfig/network
    fi
    echo "gate way set OK!"
fi
echo "-----------------------------------------------"
cat /etc/sysconfig/network
echo "-----------------------------------------------"
################################################

temp001=`/sbin/ifconfig -a |grep Link`

if [[ $? -eq 0   ]];then
    allif=`/sbin/ifconfig -a |grep Link |awk '{print $1}'|grep -vE "lo|inet6|sit0"`
    allmac=`/sbin/ifconfig -a |grep Link |awk '{print $5}'|grep -vE "lo|inet6|sit0"`
    ifcounter=`/sbin/ifconfig -a |grep Link|grep -vE "lo|inet6|sit0" |wc -l`
else
   if [[ $? -eq 1  ]];then
    allif=`/sbin/ifconfig -a |grep mtu |awk -F :  '{print $1}'|grep -vE "lo|inet6|sit0"`
    allmac=`/sbin/ifconfig -a |grep ether |awk '{print $2}'|grep -vE "lo|inet6|sit0"`
    ifcounter=`/sbin/ifconfig -a |grep mtu|grep -vE "lo|inet6|sit0" |wc -l`
fi
fi
echo "ifname is " $allif
echo "mac add is " $allmac
echo "ifcounter is " $ifcounter

#push if and mac to array
x=1
while [ $x -le $ifcounter ];
      
      do
      #STR_TEMP=`printf "%s%s" "$STR_TEMP" "$1"`
      ifname[$x]=`echo $allif|awk '{print $'$x'}'`
      ifmac[$x]=`echo $allmac|awk '{print $'$x'}'`
      echo "x" $x
      echo "ifname" ${ifname[$x]}
      echo "ifmac" ${ifmac[$x]}
      if [ "${ifmac[$x]}" = "$get_nic1_mac"    ];then
          set_nic_ip ${ifname[$x]} $get_nic1_ip $get_nic2_netmask
      else
         echo "not nic1"
      fi
      if [ "${ifmac[$x]}" = "$get_nic2_mac"    ];then
          set_nic_ip ${ifname[$x]} $get_nic2_ip $get_nic2_netmask
      else
         echo "not nic2"
      fi
      x=`expr $x + 1`
done
#b[0]=`echo $a |awk  '{print $1}'`
#b[1]=`echo $a |awk  '{print $2}'`
#echo ${b[0]}
#echo ${b[1]}
#-----------------disable rc.local-----------------------
sed -i '/^sh\ \/bin\/setipbymac/s/^/#/' /etc/rc.local
sed -i '/^sh\ \/bin\/setipbymac/s/^/#/' /etc/rc.d/rc.local
sed -i 's/\(127.*\)/\1 "'$get_host_name'"/' /etc/hosts
sed -i 's/"/\ /g' /etc/hosts
reboot
