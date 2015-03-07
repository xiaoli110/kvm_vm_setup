#/usr/bin/env python


import os
import sys
import string
import commands
import time
#status, output = commands.getstatusoutput('ls -l')
mycwd=os.getcwd()
modcwd=mycwd+'/virtmod'
sys.path.append(modcwd)
modcwd=mycwd+'/virtclass'
sys.path.append(modcwd)
import colpt

def chang_md5_file(filename):
    c=filename
    a="/datapool/"+filename
    b=c.split(".")
    d=b[0]
    f = open(a)
    readtext = f.read( )
    f.close( )
    var_md5 = readtext.split()
    f = open(a,"w")
    f.write(var_md5[0]+"  /datapool/"+d+"\n")
    f.close

def getTemp(filename,url):
    a=filename
    md5_file=a+".md5"
    b=url
    dlcmd="wget "+b+a+" -O /datapool/"+a+" -c "
    dlcmdmd5="wget "+b+a+".md5 -O /datapool/"+a+".md5 -c "
    #print dlcmd
    colpt.ptred("vm images not exists,Will download it ,Please wait a moment")
    #sys.exit(1)
    #p=os.popen(dlcmd).read()
    #status, output = commands.getstatusoutput(dlcmd)
    #statusmd5, outputmd5 = commands.getstatusoutput(dlcmdmd5)
    os.popen(dlcmd)
    os.popen(dlcmdmd5)
    colpt.ptgreen("**********************************************")
    i=1
    chang_md5_file(md5_file)
    #print str(status)+" is  wget status !"
    #while (status != 0):
    #    status, output = commands.getstatusoutput(dlcmd)
    #    print str(status)+" is  wget  status ! and times is "+str(i)
    #    i=i+1
    #    if (i > 5):
    #        print "vm images download failed"
    #        return 10
    #        break
    return 0
    #end
def urlTest(url):
    urlTestCmd="wget -c "+url+"ratetest -O /datapool/ratetest"
    rmTestFile="rm -f /datapool/ratetest*"
    a=time.time()
    os.popen(urlTestCmd)
    os.popen(rmTestFile)
    b=time.time()
    c=b-a
    return c
def geturl(url1,url2):
    c1=urlTest(url1)
    c2=urlTest(url2)
    if ( c2 < c1):
        return url2
    else:
        return url1
    #end
def checkTempFile(filename,url1,url2):
    a=filename
    colpt.ptgreen("check vm images "+a)
    checkmd5="md5sum -c /datapool/"+a+".md5"
    #print checkmd5
    if os.path.isfile("/datapool/"+a):
        colpt.ptgreen("vm images "+a+" exists ok!")
        return 0
    else:
        colpt.ptyellow("vm images not exists ,Will download "+a)
        vmgeturl=geturl(url1,url2)
        b=getTemp(a,vmgeturl)
        if (b != 0):
            colpt.ptred("Download errors Please check !")
            return 11
        j=1
        statusCheckMd5, outputCheckMd5 = commands.getstatusoutput(checkmd5)
        print str(statusCheckMd5)+"  md5 status is!"
        print "outputCheckMd5 is "+outputCheckMd5
        if (string.find(outputCheckMd5,"OK")>0):
            statusCheckMd5=0
        else:
            statusCheckMd5=1
        while (statusCheckMd5 != 0):
            os.system("rm /datapool/"+a+" -f")
            os.system("rm /datapool/"+a+"md5 -f")
            getTemp(a)
            statusCheckMd5, outputCheckMd5 = commands.getstatusoutput(checkmd5)
            j=j+1
            print str(statusCheckMd5)+"  md5 status is!"
            if (j > 6):
                print "images sync filed"
                return 12
        colpt.ptgreen("Temp is ok!")
        return 0
#end
