#!/usr/bin/python
#2012 05 09
#vm class

import os
import sys
import string
mycwd=os.getcwd()
modcwd=mycwd+'/virtmod'
sys.path.append(modcwd)
modcwd=mycwd+'/virtclass'
sys.path.append(modcwd)
import colpt
import syncTemp
import osprobe

#colpt.ptred("tttt")

class vm():
    def __init__(self):
        import virtinst.util
        MAC1=virtinst.util.randomMAC("qemu")
        MAC2=virtinst.util.randomMAC("qemu")
        self.name=""
        self.temp=""
        self.cpu="2"
        self.mem="2097152"
        self.disk1_size=""
        self.disk2_size=""
        self.vda=self.name+".qcow2.vda"
        self.vdb=self.name+".qcow2.vdb"
        self.out_type="e1000"
        self.out_bridge=""
        self.outip=""
        self.outmask=""
        self.outgw=""
        self.out_mac=MAC1
        self.in_type="e1000"
        self.in_bridge=""
        self.inip=""
        self.inmask=""
        self.ingw="none"
        self.in_mac=MAC2
        self.vnc_port=""
        self.vgname="none"
        self.os="none"
    def  vmstatus(self):
        a=os.popen('virsh list --all')
        colpt.ptgreen(a.read())
        #print a.read()
    def vm_name_check(self):
        if self.name=="":
           colpt.ptred("Please give vm name") 
           #sys.exit()
           return "1"
        else:
           colpt.ptgreen("name check pass")
    def vm_temp_check(self):
        if self.temp=="":
           colpt.ptred("Please give vm template") 
           #sys.exit()
           return "1"
        else:
           colpt.ptgreen("template check pass")
    def vm_disk1_size_check(self):
        if self.disk1_size=="":
           colpt.ptred("Please give vm disk1 size") 
           #sys.exit()
           return "1"
        else:
           colpt.ptgreen("disk1 size check pass")
    def vm_os_check(self):
        print "check vm os ......"
        checkos="virt-inspector  /datapool/"+self.temp
        a=os.popen(checkos)
        c=a.read()
        b=c[0:1024]
        colpt.ptgreen("virt-inspector Running:")
        colpt.ptgreen(b[0:100])
        if (string.find(b,"2003")>0):
            self.os="2003"
        elif(string.find(b,"2008")>0):
            self.os="2008"
        elif(string.find(b,"2012")>0):
            self.os="2008"
        elif(string.find(b,"centos")>=0):
            self.os="linux"
        else:
            #check whether os is Ubuntu    
            deepcheckos="virt-inspector  /datapool/"+self.temp
            t=os.popen(deepcheckos)
            r=t.read()
            print r[0:100]
            if (string.find(r,"ubuntu")>0):
                self.os="ubuntu"
            else:
                print "os is unknow"
        print "os is "+self.os
    def define_vda_vdb(self):
        if (self.vgname=="none"):
            self.vda="/datapool/"+self.name+".vda"
            self.vdb="/datapool/"+self.name+".vdb"
        elif (self.vgname=="cp"):
            self.vda="/datapool/"+self.name+".vda"
            self.vdb="/datapool/"+self.name+".vdb"
        else:
            self.vda="/dev/"+self.vgname+"/"+self.name+"-vda"
            self.vdb="/dev/"+self.vgname+"/"+self.name+"-vdb"
        colpt.ptgreen(self.vda)
        colpt.ptgreen(self.vdb)
    def vm_lvm_disk1(self):
        vgname=self.vgname
        checkos=self.os
        create_lvm_vda="lvcreate -L "+self.disk1_size+" -n "+self.name+"-vda "+self.vgname
        print create_lvm_vda
        c=os.popen(create_lvm_vda)
        d=c.read()
        print d
        if (checkos=="2003"):
            vm_disk1_resize="virt-resize --expand /dev/vda1 /datapool/"+self.temp+" "+self.vda
        elif(checkos=="2008"):
            vm_disk1_resize="virt-resize --expand /dev/vda1 /datapool/"+self.temp+" "+self.vda
        elif(checkos=="linux"):
            colpt.ptred("Linux disk expand only test image by centos5.6 ")
            #virt-resize --lvexpand /dev/vmvg/root centos56x64_10G_vda.qcow2 centostest.vda
            vm_disk1_resize="virt-resize --expand /dev/vda2 --lvexpand /dev/vmvg/root /datapool/"+self.temp+" "+self.vda
        else:
            vm_disk1_resize="ls /datapool"
            print "RRRR"
        print vm_disk1_resize
        #os.popen(vmdisk1)
        os.system(vm_disk1_resize)
    def vm_lvm_disk2(self):
        mycwd=os.getcwd()
        w2k3vdbvirtpath=mycwd+"/virtvdb/win2k3.vdb"
        w2k3vdbdatapath="/datapool/win2k3.vdb"
        copyw2k3vdb="\cp -f "+w2k3vdbvirtpath+" /datapool/"
        w2k8vdbvirtpath=mycwd+"/virtvdb/win2k8.vdb"
        w2k8vdbdatapath=mycwd+"/datapool/win2k8.vdb"
        copyw2k8vdb="\cp -f "+w2k8vdbvirtpath+" /datapool/"
        if os.path.isfile(w2k3vdbdatapath):
            pass
        else:
            os.popen(copyw2k3vdb)
        if os.path.isfile(w2k8vdbdatapath):
            pass
        else:
            os.popen(copyw2k8vdb)
        checkos=self.os
        create_lvm_vdb="lvcreate -L "+self.disk2_size+" -n "+self.name+"-vdb "+self.vgname
        print create_lvm_vdb
        c=os.popen(create_lvm_vdb)
        d=c.read()
        print d
        if (checkos=="2003"):
            vm_disk2_resize="virt-resize --expand /dev/vda1 /datapool/"+self.temp+" "+self.vdb
        elif (checkos=="2008"):
            vm_disk2_resize="virt-resize --expand /dev/vda1 /datapool/"+self.temp+" "+self.vdb
        elif (checkos=="linux"):
            colpt.ptred("Linux disk expand only test image by centos5.6 ")
            #virt-resize --lvexpand /dev/vmvg/root centos56x64_10G_vda.qcow2 centostest.vda
            vm_disk2_resize="virt-resize --expand /dev/vda2 --lvexpand /dev/vmvg/root /datapool/"+self.temp+" "+self.vdb
        else:
            vmiprun="ls /datapool"
            print "RRRR"
        print vm_disk2_resize
        os.system(vm_disk2_resize)
    def vm_resize_disk1(self):
        checkos=self.os
        vmdisk1="qemu-img create  -f qcow2 "+self.vda+" "+self.disk1_size
        if (checkos=="2003"):
            vm_disk1_resize="virt-resize --expand /dev/vda1 /datapool/"+self.temp+" "+self.vda
        elif (checkos=="2008"):
            vm_disk1_resize="virt-resize --expand /dev/vda1 /datapool/"+self.temp+" "+self.vda
        elif (checkos=="linux"):
            colpt.ptred("Linux disk expand only test image by centos5.6 ")
            #virt-resize --lvexpand /dev/vmvg/root centos56x64_10G_vda.qcow2 centostest.vda
            vm_disk1_resize="virt-resize --expand /dev/vda2 --lvexpand /dev/vmvg/root /datapool/"+self.temp+" "+self.vda
        elif (checkos=="ubuntu"):
            colpt.ptred("Linux disk expand only test image by ubuntu ")
            #virt-resize --lvexpand /dev/vmvg/root centos56x64_10G_vda.qcow2 centostest.vda
            vm_disk1_resize="virt-resize --expand /dev/sda2 --lvexpand /dev/vmvg/root /datapool/"+self.temp+" "+self.vda        
	else:
            vmiprun="ls /datapool"
            print "RRRR"
        print vmdisk1
        #vm_disk1_resize="virt-resize --lveexpand /dev/vda1 /datapool/"+self.temp+" /datapool/"+self.vda
        print vm_disk1_resize
        os.popen(vmdisk1)
        os.system(vm_disk1_resize)
    def vm_resize_disk2(self):
        mycwd=os.getcwd()
        w2k3vdbvirtpath=mycwd+"/virtvdb/win2k3.vdb"
        w2k3vdbdatapath="/datapool/win2k3.vdb"
        copyw2k3vdb="\cp -f "+w2k3vdbvirtpath+" /datapool/"
        w2k8vdbvirtpath=mycwd+"/virtvdb/win2k8.vdb"
        w2k8vdbdatapath=mycwd+"/datapool/win2k8.vdb"
        copyw2k8vdb="\cp -f "+w2k8vdbvirtpath+" /datapool/"
        if os.path.isfile(w2k3vdbdatapath):
            pass
        else:
            os.popen(copyw2k3vdb)
        if os.path.isfile(w2k8vdbdatapath):
            pass
        else:
            os.popen(copyw2k8vdb)
        checkos=self.os
        vmdisk2="qemu-img create  -f qcow2 "+self.vdb+" "+self.disk2_size
        #vm_disk1_resize="virt-resize --expand /dev/vda1 "+size+" "+self.disk1_size
        os.popen(vmdisk2)
        if (checkos=="2003"):
            vm_disk2_resize="virt-resize --expand /dev/vda1 /datapool/win2k3.vdb "+self.vdb
        elif (checkos=="2008"):
            vm_disk2_resize="virt-resize --expand /dev/vda1 /datapool/win2k8.vdb "+self.vdb
        elif (checkos=="linux"):
            colpt.ptred("Linux disk expand only test image by centos5.6 ")
            #virt-resize --lvexpand /dev/vmvg/root centos56x64_10G_vda.qcow2 centostest.vda
            #vm_disk2_resize="virt-resize --expand /dev/vda2 --lvexpand /dev/vmvg/root /datapool/"+self.temp+" /datapool/"+self.vda
            vm_disk2_resize=""" echo "linux not expand disk2" """
	elif (checkos=="ubuntu"):
            colpt.ptred("Linux disk expand only test image by ubuntu ")
            #virt-resize --lvexpand /dev/vmvg/root centos56x64_10G_vda.qcow2 centostest.vda
            #vm_disk2_resize="virt-resize --expand /dev/vda2 --lvexpand /dev/vmvg/root /datapool/"+self.temp+" /datapool/"+self.vda
            vm_disk2_resize=""" echo "linux not expand disk2" """       
	else:
            vmiprun="ls /datapool"
            print "RRRR"
        #vm_disk1_resize="virt-resize --lveexpand /dev/vda1 /datapool/"+self.temp+" /datapool/"+self.vda
        print vm_disk2_resize
        os.system(vm_disk2_resize)
        #os.popen(vm_disk2_resize)
    def vm_cp_disk1(self):
        checkos=self.os
        vmdisk1="qemu-img create  -f qcow2 "+self.vda+" "+self.disk1_size
        vm_disk1_cp="cp /datapool/"+self.temp+" "+self.vda
        print vmdisk1
        #vm_disk1_resize="virt-resize --lveexpand /dev/vda1 /datapool/"+self.temp+" /datapool/"+self.vda
        print vm_disk1_cp
        #os.popen(vmdisk1)
        os.system(vm_disk1_cp)
    def vm_nicinfo_create(self):
        nic_file=mycwd+"/virttmp/nicinfo.ini"
        f=open(nic_file, "w")
        f.write("ipsetup:0\n")
        f.write("ip:"+self.outip+"\n")
        f.write("mask:"+self.outmask+"\n")
        f.write("gw:"+self.outgw+"\n")
        f.write("mac:"+self.out_mac+"\n")
        f.write("ip:"+self.inip+"\n")
        f.write("mask:"+self.inmask+"\n")
        f.write("gw:"+self.ingw+"\n")
        f.write("mac:"+self.in_mac+"\n")
        f.close()
        nic_file2dos="unix2dos "+nic_file
        os.system(nic_file2dos)
    def vm_nicinfo_copy_in(self):
        checkos=self.os
        if (checkos=="2003"):
            nic_file=mycwd+"/virttmp/nicinfo.ini"
            vmiprun="virt-copy-in -a "+self.vda+" "+nic_file+" /WINDOWS"
        elif (checkos=="2008"):
            nic_file=mycwd+"/virttmp/nicinfo.ini"
            vmiprun="virt-copy-in -a "+self.vda+" "+nic_file+" /Windows"
        elif (checkos=="linux"):
            colpt.ptred("Linux system ip config only test image by centos5.6 ")
            tmp_setipbymac=mycwd+"/virtscript/setipbymac.sh"
            tmp_rc_local_out="virt-copy-out -a "+self.vda+" /etc/rc.d/rc.local "+mycwd+"/virttmp/"
            tmp_rc_local_in="virt-copy-in -a "+self.vda+"  "+mycwd+"/virttmp/rc.local /etc/rc.d/"
            tmp_rc_local_in_setipscript="virt-copy-in -a "+self.vda+" "+mycwd+"/virtscript/setipbymac.sh /bin/"
            tmp_setip_cmd="setipbymac.sh "+self.name+" "+self.outgw+" "+self.outip+" "+self.outmask+" "+self.out_mac.upper()+\
            " "+self.inip+" "+self.inmask+" "+self.in_mac.upper()
            tmp_setip_echo="echo sh /bin/"+tmp_setip_cmd+" >>"+mycwd+"/virttmp/rc.local"
            tmp_chmod_rc_local="chmod 711 "+mycwd+"/virttmp/rc.local"
            print "show copy out "+tmp_rc_local_out
            print "show copy in "+tmp_rc_local_in
            print "show setip echo "+tmp_setip_echo
            print "show copy in setipscript "+tmp_rc_local_in_setipscript

            print tmp_setip_cmd
            os.system(tmp_rc_local_out)  
            os.system(tmp_setip_echo)  
            os.system(tmp_chmod_rc_local)  
            os.system(tmp_rc_local_in)
            os.system(tmp_rc_local_in_setipscript)
            vmiprun="echo 'linux ^_^'"
        elif (checkos=="ubuntu"):
            colpt.ptred("Linux system ip config only test image by ubuntu1104*64 ")
            tmp_setipbymac=mycwd+"/virtscript/setipbymac.sh"
            tmp_rc_local_out="virt-copy-out -a "+self.vda+" /etc/rc.local "+mycwd+"/virttmp/"
            tmp_rc_local_in="virt-copy-in -a "+self.vda+"  "+mycwd+"/virttmp/rc.local /etc/"
            tmp_rc_local_in_setipscript="virt-copy-in -a "+self.vda+" "+mycwd+"/virtscript/setipbymac-ubuntu.sh /bin/"
            tmp_setip_cmd="setipbymac-ubuntu.sh "+self.name+" "+self.outgw+" "+self.outip+" "+self.outmask+" "+self.out_mac.upper()+\
            " "+self.inip+" "+self.inmask+" "+self.in_mac.upper()
	    tmp_start_rc_local="sed -i \'s/#!\/bin\/sh -e/#!\/bin\/sh/g\' "+mycwd+"/virttmp/rc.local"
            tmp_del_exit_rc_local="sed -i /exit/d "+mycwd+"/virttmp/rc.local"
            tmp_setip_echo="echo /bin/bash /bin/"+tmp_setip_cmd+" >>"+mycwd+"/virttmp/rc.local"
            tmp_chmod_rc_local="chmod 711 "+mycwd+"/virttmp/rc.local"
            print "show copy out "+tmp_rc_local_out
            print "show copy in "+tmp_rc_local_in
            print "show setip echo "+tmp_setip_echo
            print "show copy in setipscript "+tmp_rc_local_in_setipscript

            print tmp_setip_cmd
            os.system(tmp_rc_local_out)  
            os.system(tmp_start_rc_local)
	    os.system(tmp_del_exit_rc_local)
            os.system(tmp_setip_echo)  
            os.system(tmp_chmod_rc_local)  
            os.system(tmp_rc_local_in)
            os.system(tmp_rc_local_in_setipscript)
            vmiprun="echo 'ubuntu ^_^'"
        else:
            vmiprun="ls /datapool"
            print "RRRR"
        c=os.popen(vmiprun)
        d=c.read()
        print c

    def vm_xmlfile_create(self):
        tmp_xml=mycwd+"/virtxml/win03.xml"
        f=open(tmp_xml,"r")
        vmfile="/datapool/"+self.name+".xml"
        if os.path.isfile(vmfile):
            print vmfile," file exists skip this vm create!"
            #continue
            a="xml file is exist skip!"
            colpt.ptred(a)
            return "1"
        f2=open(vmfile,"w")
        for line in f:
            if ((line.find("vmname"))>0):
                line=string.replace(line,"vmname",self.name)
            elif (line.find("vmmem")>=0):
                line=string.replace(line,"vmmem",self.mem)
            elif (line.find("vmcpu")>=0):
                line=string.replace(line,"vmcpu",self.cpu)
            elif (line.find("vmvda")>=0):
                line=string.replace(line,"vmvda",self.vda)
            elif (line.find("vmvdb")>=0):
                line=string.replace(line,"vmvdb",self.vdb)
            elif (line.find("vmbr1type")>=0):
                line=string.replace(line,"vmbr1type",self.out_type)
            elif (line.find("vmbr2type")>=0):
                line=string.replace(line,"vmbr2type",self.in_type)
            elif (line.find("vmbr1")>=0):
                line=string.replace(line,"vmbr1",self.out_bridge)
            elif (line.find("mac1")>=0):
                line=string.replace(line,"mac1",self.out_mac)
            elif (line.find("vmbr2")>=0):
                line=string.replace(line,"vmbr2",self.in_bridge)
            elif (line.find("mac2")>=0):
                line=string.replace(line,"mac2",self.in_mac)
            elif (line.find("vncport")>=0):
                line=string.replace(line,"vncport",self.vnc_port)
            f2.write(line)
        f.close()
        f2.close()
        
    def vm_xmlfile_exist(self):
        vmfile="/datapool/"+self.name+".xml"
        vmvda=self.vda
        vmvdb=self.vdb
        if os.path.isfile(vmfile):
            #print vmfile," xml file exists skip this vm create!"
            #continue
            a="xml file"+vmfile+" is exist skip!"
            colpt.ptred(a)
            return "1"
        elif os.path.isfile(vmvda):
            a="vda file"+vmvda+" is exist skip!"
            colpt.ptred(a)
            return "1"
        elif os.path.isfile(vmvdb):
            a="vdb file"+vmvdb+" is exist skip!"
            colpt.ptred(a)
            return "1"
        else:
            lvscan="lvs"
            a=os.popen(lvscan)
            b=a.read()
            if (b.find(self.name)>=0):
                c="Lvm "+self.name+" exist!"
                colpt.ptred(c)
                return "1"
            else:
                print "+_+"
    def vm_host_exist(self):
        name_run="virsh list --all"
        a=self.name
        b=os.popen(name_run).read()
        print a
        print b
        print str(string.find(b,a))
        if (string.find(b,a)>=0):
            return "1"
    def vm_xmlfile_create2(self):
        vmfile="/datapool/"+self.name+".xml"
        tmp_cpu_capabilities="virsh capabilities |grep pentium3"
        tmp_cpu_info=os.popen(tmp_cpu_capabilities).read()
        print tmp_cpu_info
        if (string.find(tmp_cpu_info,"pentium3")>=0):
            if (self.vgname=="none" or self.vgname=="cp"):
                tmp_xml2=" virt-install --name="+self.name+" --vcpus="+self.cpu+" --cpu host-passthrough --ram="+self.mem+" --disk path="+self.vda+\
                ",bus=virtio,cache=writethrough,format=qcow2,io=native"+\
                " --disk path="+self.vdb+\
                ",bus=virtio,cache=writethrough,format=qcow2,io=native"+\
                " --network bridge="+self.out_bridge+",model="+self.out_type+",mac="+self.out_mac+" --network bridge="+self.in_bridge+\
                ",model="+self.in_type+",mac="+self.in_mac+" --vnc --vncport="+self.vnc_port+" --import --hvm --virt-type kvm  "+\
                " --print-xml>"+vmfile
            else:
                tmp_xml2=" virt-install --name="+self.name+" --vcpus="+self.cpu+" --cpu host-passthrough --ram="+self.mem+" --disk path="+self.vda+\
                ",bus=virtio,cache=writethrough,format=raw,io=native"+\
                " --disk path="+self.vdb+\
                ",bus=virtio,cache=writethrough,format=raw,io=native"+\
                " --network bridge="+self.out_bridge+",model="+self.out_type+",mac="+self.out_mac+" --network bridge="+self.in_bridge+\
                ",model="+self.in_type+",mac="+self.in_mac+" --vnc --vncport="+self.vnc_port+" --import --hvm --virt-type kvm  "+\
                " --print-xml>"+vmfile
        else:
            if (self.vgname=="none" or self.vgname=="cp"):
                tmp_xml2=" virt-install --name="+self.name+" --vcpus="+self.cpu+" --cpu host-passthrough --ram="+self.mem+" --disk path="+self.vda+\
                ",bus=virtio,cache=writethrough,format=qcow2,io=native"+\
                " --disk path="+self.vdb+\
                ",bus=virtio,cache=writethrough,format=qcow2,io=native"+\
                " --network bridge="+self.out_bridge+",model="+self.out_type+",mac="+self.out_mac+" --network bridge="+self.in_bridge+\
                ",model="+self.in_type+",mac="+self.in_mac+" --vnc --vncport="+self.vnc_port+" --import --hvm --virt-type kvm  "+\
                " --print-xml>"+vmfile
            else:
                tmp_xml2=" virt-install --name="+self.name+" --vcpus="+self.cpu+" --cpu host-passthrough --ram="+self.mem+" --disk path="+self.vda+\
                ",bus=virtio,cache=writethrough,format=raw,io=native"+\
                " --disk path="+self.vdb+\
                ",bus=virtio,cache=writethrough,format=raw,io=native"+\
                " --network bridge="+self.out_bridge+",model="+self.out_type+",mac="+self.out_mac+" --network bridge="+self.in_bridge+\
                ",model="+self.in_type+",mac="+self.in_mac+" --vnc --vncport="+self.vnc_port+" --import --hvm --virt-type kvm "+\
                " --print-xml>"+vmfile
        colpt.ptyellow(tmp_xml2)
        createxml_temp=os.popen(tmp_xml2)
        createxml_temp_read=createxml_temp.read()
        colpt.ptgreen(createxml_temp_read)
        xmlfilelist=[]
        f3=open(vmfile,"r")
        for line in f3:
            if ((line.find("clock"))>0):
                line="<clock offset='localtime'/>"
            if ((line.find("input"))>0):
                line="<input type='tablet' bus='usb'/>\n<input type='mouse' bus='ps2'/>"
                #f2.write(line)
            xmlfilelist.append(line)
        f3.close()
        f4=open(vmfile,"w")
        for line in xmlfilelist:
            f4.write(line)
        f4.close()
    def vm_define(self):
        vmfile="/datapool/"+self.name+".xml"
        vm_define="virsh define "+vmfile
        if os.system(vm_define)==0:
            pass
        else:
           return "1"
    def vm_run(self):
        vm_run="virsh start "+self.name
        os.system(vm_run)
    def vm_autostart(self):
        vm_autostart="virsh autostart "+self.name
        os.system(vm_autostart)
    def vm_define_run_autostart():
        vm_define()
        vm_run()
        vm_autostart()
#end
