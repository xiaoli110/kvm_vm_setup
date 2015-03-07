#!/usr/sbin/env python

import getopt
import sys

opts,args=getopt.getopt(sys.argv[1:],"d:h",["start","stop","restart","debug","help"])
print opts
if opts==[]:
    print "oooo"
print args
for o,a in opts:
        if o=="--start":
            print "statrt..."+a
        elif o=="--stop":
            print "stop..."+a
        elif o=="restart":
            print "stop...start..."+a
        elif o in ("-d","--debug"):
            print "debug..."+a
        elif o in("-h","--help"):
            print "usage()..."+a
        else:
            print "ttt"
            assert False,"unhandled option"
