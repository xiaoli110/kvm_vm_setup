#!/usr/bin/env python
#scritp read , config virt1.0 xml files then run vm
#write by xiaoli
#version 1.0 2012 04 23
#version 1.1 2012 05 11
#version 1.2 2012 06 27 add format windows disk D
#version 1.3 2012 07 15 add lvm support for vm,default vg is vmVG
#version 1.5 2012 08 15 support multi download source
#version 1.6 2012 10 11 support install ubuntu system 
#version 1.7 2012 12 26 check disk alignment ,fix md5 check 
#version 1.8 2013 03 04 support windows 2012 virt-machine create update by xiaoli
#version 2.0 2014 08 01 support copy only for create vm images
#version 3.0 2015 02 05 support host and vm is CentOS7,support cpu mode is host by xiaoli
#1 thinking search xml file keyworks then replace it
#2 create disk vda vdb 
#3 run virsh commond to start vm

import os
import sys
import string
mycwd=os.getcwd()
modcwd=mycwd+'/virtmod'
sys.path.append(modcwd)
modcwd=mycwd+'/virtclass'
sys.path.append(modcwd)
import colpt
import classvm
import syncTemp
import getopt

global vmarray, vminfo
global vminicouter
global vg
global vmurl1,vmurl2,urlcount
vmarray=range(255) #record valid vm info into array vmarray
vminfo=range(255)  #record vm info
vminicouter=0      #record vm num
vg="vmVG"          #defaulf vg name
vg="datavg"
vmurl1="ftp://virtftp:1qa2ws3ed4rF@211.147.0.120:38602/"
vmurl2="ftp://virtftp:1qa2ws3ed4rF@116.211.20.200:38602/"
urlcount=0

def getopts():
    helpinfo="""
    -h, --help print this
    --vg,assige vg name,such as --vg=datavg,vg=vmVG
        default vg name is 'datavg' if not assige
    --config,assige config file name ,such as --config=vm.csv
        config file must in same directory and must be csv
        default config file name is 'vm.csv' if not assige
    --url,give path to download vm images,such as --url=ftp://user1:pass@172.16.1.100/
    """
    global vg
    opts,args=getopt.getopt(sys.argv[1:],"hc:",["vg=","config=","help","url="])
    if opts==[]:
        colpt.ptgreen(helpinfo)
        colpt.ptgreen("Will run in default!")
    for o,a in opts:
        if o in ("-h","--help"):
            colpt.ptgreen(helpinfo)
            sys.exit(12)
        elif o=="--vg":
            vg=a
            b="vg name is "+a
            colpt.ptgreen(b)
        elif o=="--config":
            pass
        elif o=="--url":
            vmurl=a
            b="url is "+a
            colpt.ptgreen(b)
        else:
            print "wrong argument ,pleale check again"
            sys.exit(11)
            assert False,"unhand option"
def checkinifile():
    """check config file exist!"""
    global vmarray, vminfo
    global vminicouter
    colpt.ptgreen_no_enter("check config file")
    if os.path.isfile("vm.csv"):
        colpt.ptgreen("..................config file exists ok!")
    else:
        colpt.ptred("config file not exists,please check!!!")
        sys.exit(1)
def readinifile():
    """read config file and find valid value,assign value to vm array"""
    global vmarray, vminfo
    global vminicouter,vmurl1,vmurl2,urlcount
    f=open("vm.csv","r")
    i=0
    for line in f:
        #print line.strip()
        line=line.strip()
        if (line.find("vm")==0):
            vmarray[i]=line
            i=i+1
            vminicouter=i
        if (line.find("url:")==0):
            temurl=line.split(":",1)
            if (urlcount==0):
                vmurl1=temurl[1]
                urlcount=1
            elif (urlcount==1):
                vmurl2=temurl[1]
                urlcount=2
            else:
                print "url more count error!"
    f.close()
def vm_ct():
    """ split vm info and assign to vm object;
    and create vm inst """
    global vmarray, vminfo
    global vminicouter
    global vg
    global vmurl
    j=0
    vminfo=range(vminicouter)
    print "vm config info is:"
    while j < vminicouter:
         #print vmarray[j],j
         #vminfo[j]=vmarray[j].split
         a=vmarray[j]
         vminfo=string.split(a,",")
         colpt.ptred("vm "+str(j)+" info")
         colpt.ptyellow(str(vminfo))
         vmtmp=classvm.vm()
         ifvg=vminfo[0]
         if (ifvg.find("Lvm")>0):
             vmtmp.vgname="vg"
         elif (ifvg.find("CpOnly")>0):
             vmtmp.vgname="cp"
         else:
             vmtmp.vgname="none"
         vmtmp.temp=vminfo[1]
         c=syncTemp.checkTempFile(vmtmp.temp,vmurl1,vmurl2)
         print str(c)+" is check vm iamges error status"
         if (c != 0 ):
             colpt.ptred(" vm images errors Please check!!!")
             sys.exit(5)
         colpt.ptgreen(" vm images check is ok!")
         vmtmp.name=vminfo[2]
         vmtmp.define_vda_vdb()
         vmtmp.disk1_size=vminfo[3]
         vmtmp.disk2_size=vminfo[4]
         vmtmp.mem=vminfo[5]
         vmtmp.cpu=vminfo[6]
         vmtmp.out_type=vminfo[7]
         vmtmp.out_bridge=vminfo[8]
         vmtmp.in_bridge=vminfo[9]
         vmtmp.vnc_port=vminfo[10]
         vmtmp.outip=vminfo[11]
         vmtmp.outmask=vminfo[12]
         vmtmp.outgw=vminfo[13]
         vmtmp.in_type=vminfo[7]
         vmtmp.inip=vminfo[14]
         vmtmp.inmask=vminfo[15]
         vmtmp.ingw=vminfo[16]
         if vmtmp.vm_xmlfile_exist()=="1":
            colpt.ptred("xml or vda vdb file exist skip vm create!")
         elif vmtmp.vm_host_exist()=="1":
            colpt.ptred("vm allready exist skip vm create!")
         else:
            vmtmp.vm_os_check()
            if (vmtmp.vgname=="none"):
                vmtmp.vm_resize_disk1()
                vmtmp.vm_resize_disk2()
            elif (vmtmp.vgname=="cp"):
                vmtmp.vm_cp_disk1()
                vmtmp.vm_resize_disk2()
            elif (vmtmp.vgname=="vg"):
                vmtmp.vm_lvm_disk1()
                vmtmp.vm_lvm_disk2()
            vmtmp.vm_xmlfile_create2()
            vmtmp.vm_nicinfo_create()
            vmtmp.vm_nicinfo_copy_in()
            if vmtmp.vm_define()=="1":
                colpt.ptred("define failed skip vm create!")
            else:
                vmtmp.vm_run()
                vmtmp.vm_autostart()
         j=j+1
getopts()
checkinifile()
readinifile()
vm_ct()
colpt.ptgreen("Done")
