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

global vmarray, vminfo
global vminicouter

syncTemp.checkTempFile("win2008ent64chs")

