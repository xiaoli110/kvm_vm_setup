#!/usr/bin/env python
#_*_encoding:UTF-8_*_
"""
..MySQL......
"""

import MySQLdb

connstring="host='localhost',user='root'"
try:
    #conn=MySQLdb.Connect(host='127.0.0.1',user='root')
    conn=MySQLdb.Connect(connstring)
except Exception ,e:
    print e
#break
