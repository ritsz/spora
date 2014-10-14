#!/usr/bin/python3

"""FTP SERVER 0.1
Usage:
  ftp_server.py [--user name] [--pwd pwd] [--dir home] [--port num]
  ftp_server.py (-h | --help)
  ftp_server.py --version

Options:
  --user name  Username for ftp [default: ritsz]
  --pwd pwd    Password for ftp user [default: 123]
  --port num   Port number to run ftp server [default: 21]
  --dir home   Home directoy of ftp user [default: /home]
  -h --help    Print this help page
"""


from docopt import docopt
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def ftp_main(USER, PASSWD, HOME, PORT):
	authorizer = DummyAuthorizer()
	authorizer.add_user(USER, PASSWD, HOME, perm="elradfmw")
	authorizer.add_anonymous(HOME)

	handler = FTPHandler
	handler.authorizer = authorizer

	server = FTPServer(("0.0.0.0", PORT), handler)
	server.serve_forever()

if __name__ == '__main__':
	args = docopt(__doc__, version = "FTP SERVER 0.1")
	print(args)
	ftp_main(args['--user'], args['--pwd'], args['--dir'], args['--port'])	
