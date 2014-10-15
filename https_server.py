#!/usr/bin/python3
import http.server 
import ssl
import sys

if len(sys.argv) > 1:
	PORT = int(sys.argv[1])
else:
	PORT = 443

if len(sys.argv) > 2:
	FILE = sys.argv[2]
else:
	FILE = 'privcert.pem'


httpd = http.server.HTTPServer(('0.0.0.0', PORT), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile=FILE, keyfile=FILE, server_side=True)
httpd.serve_forever()
