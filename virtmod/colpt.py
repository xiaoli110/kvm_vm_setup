#!/usr/bin/python
#"""print color mod,print red green yellow"""
#write by xiaoli
#version 1.0 2012 05 09
version='1.0'
def ptyellow(str):
    print  '\x1b[0;33m'+str+'\x1b[0m'
def ptred(str):
    print  '\x1b[0;31m'+str+'\x1b[0m'
def ptgreen(str):
    print  '\x1b[0;32m'+str+'\x1b[0m'
def ptyellow_no_enter(str):
    print  '\x1b[0;33m'+str+'\x1b[0m',
def ptred_no_enter(str):
    print  '\x1b[0;31m'+str+'\x1b[0m',
def ptgreen_no_enter(str):
    print  '\x1b[0;32m'+str+'\x1b[0m',
#ptyellow("testyellow")
#ptred("testred")
#ptgreen("testgreen")
