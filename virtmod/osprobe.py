import platform
import string
def virt_os_probe():
    tmp_virt_os=platform.uname()
    virt_os=tmp_virt_os[2]
    #print virt_os
    #print string.find(virt_os,"3.10")
    if (string.find(virt_os,"3.10")>=0):
    	hostos="c7"
    elif(string.find(virt_os,"2.6.32")>=0):
        hostos="c6"
    elif(string.find(virt_os,"2.6.18")>=0):
        hostos="c5"
    else:
        hostos="unknow"
    return hostos
#print virt_os_probe()
