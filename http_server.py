#!/usr/bin/python3

"""HTTP SERVER.
Usage:
  http_server.py --src_port=<sp> [--dir=<dir>]
  http_server.py --version
  http_server.py (-h | --help)


Options:
  --src_port=<sp>  port on which http_server will run
  --dir=<dir>	   Directory in which the server runs.
  -h --help	   Print this help
  --version	   server version
"""

from docopt import docopt
import os
import http.server
import socketserver

if __name__ == 	'__main__':
	args = docopt(__doc__, version='HTTP SERVER 0.1')
	print(args)
	if args['--dir']:
		try:
			print('Moving to', args['--dir'])
			os.chdir(args['--dir'])
		except FileNotFoundError:
			print('--dir argument is not a valid path')
			exit()
	handler = http.server.SimpleHTTPRequestHandler
	sock = socketserver.TCPServer(('', int(args['--src_port'])), handler)
	sock.allow_reuse_address = True
	sock.serve_forever()	

