#!/usr/bin/env python
# Basic HTTP Server Example - Chapter 16 - simplehttp.py

from BaseHTTPServer import HTTPServer 
from SimpleHTTPServer import SimpleHTTPRequestHandler

serveraddr=('',10501)
srvr = HTTPServer(serveraddr,SimpleHTTPRequestHandler)
srvr.serve_forever()
