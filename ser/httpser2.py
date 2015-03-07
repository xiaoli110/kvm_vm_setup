#!/usr/bin/env python
# Basic HTTP Server Example with Two Document  - Chapter 16
# basichttpdoc.py

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import time

starttime = time.time()
class RequestHandler(BaseHTTPRequestHandler):
    """Definition of the request handler."""
    def __writeheaders(self,doc):
        """Write te HTTP headers for the document. If there's no
        document, send a 404 error code; otherwise, send a 200 success code"""
        if doc is None:
            self.send_response(404)
        else:
            self.send_response(200)
        # Always server up HTML for now.
        self.send_header('Content-type','text/html')
        self.end_headers()

    def __getdoc(self,filename):
        """Handle a request for a document, returning one of two different 
        pages as appropriate."""
        global starttime
        if filename == '/':
            return """<html><head><title>Sample Page</title></head>
            <body>This is a sample page. You can also look at the
            <a href="stats.html">server statistics</a>.
            </body></html>
            """
        elif filename == '/stats.html':
            return """<html><head><title>Statistics</title></head>
            <body>This server has been running for %d seconds.
            </body></html>
            """ %int(time.time() - starttime)
        else:
            return None
    def do_HEAD(self):
        """Handle a request for headers only"""
        doc = self.__getdoc(self.path)
        self.__writeheaders(doc)
    def do_GET(self):
        """Handle a request for header and body"""
        doc = self.__getdoc(self.path)
        self.__writeheaders(doc)
        if doc is None:
            self.wfile.write("""<html><head><title>Not Found</title></head>
            <body>The requested document '%s' was not found.</body>
            </html>
            """ % self.path)
        else:
            self.wfile.write(doc)
#Create the object and serve requests
serveraddr = ('', 10501)
srvr = HTTPServer(serveraddr,RequestHandler)
srvr.serve_forever()
