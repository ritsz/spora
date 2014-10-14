#!/usr/bin/python3

################
## TODO
## 1> Add Scripts and Support for other servers
## 2> Option to create a new container and then
## 	2.1> Option to copy server script into rootfs
## 3> Add pcap start stop support
## 4> Add help string to all functions

"""SPORA SERVER.

Usage:
  server_script.py (-h | --help)
  server_script.py --name=<name> --type=<server> --src_port=<kn> --dest_port=<kn> [--pcap=<file>]
  server_script.py --name=<name> --type=<server> --src_port=<kn> --dest_port=<kn> [--pcap=<file>] [--debug=<True>] [--new]
  server_script.py --name=<name> --src_port=<kn> --dest_port=<kn> --del
  server_script.py --version

Options:
  -h --help     	Show this screen.
  --debug=<True>	Show debug messages 
  --version     	Show version.
  --name=<name>  	Name of server
  --type=<server>	Type of Server
  --src_port=<sp>	Local port for server
  --dest_port=<dp>	Port on which container is handling the server
  --pcap=<file>		Perform packet capture and save in <file>
"""


import lxc
import sys
import time
from docopt import docopt
import subprocess
import lxc_wrapper

BASE_CONTAINER = 'LXC_REMOTE'

class server_class :
	def __init__(self, _container, type_of_server, src_port, dst_port, 
							pcap_file = None):
		self.container 	=	_container
		self.name 	= 	_container.name
		self.srv_type 	= 	type_of_server
		self.pcap	= 	pcap_file
		self.ip_addr 	= 	_container.get_ips()[0]
		self.state	=	_container.running
		self.src_port  	=	src_port
		self.dest_port 	=	dst_port 
	
	#def network_stats(self):
		#subprocess. 
	


def add_iptable(INTF, SRC_PORT, DEST_IP, DEST_PORT) :
	ip_table_rule = "iptables -t nat -A PREROUTING -i " + INTF + " -p tcp --dport " + SRC_PORT + " -j DNAT --to " + DEST_IP + ":" + DEST_PORT
	print(ip_table_rule)
	try:
		subprocess.call(ip_table_rule.split(" "))
	except OSError:
		print('Not able to apply iptables rule. Try manually\n', ip_table_rule)


def del_iptable(INTF, SRC_PORT, DEST_IP, DEST_PORT) :
	ip_table_rule = "iptables -t nat -D PREROUTING -i " + INTF + " -p tcp --dport " + SRC_PORT + " -j DNAT --to " + DEST_IP + ":" + DEST_PORT
	print(ip_table_rule)
	try:
		subprocess.call(ip_table_rule.split(" "))
	except OSError:
		print('Not able to delete iptables rule. Try manually\n', ip_table_rule)
		



def server_main(CONTAINER_NAME, SERVER_TYPE, SRC_PORT, DST_PORT, DEBUG) :
	assert lxc.list_containers().count(BASE_CONTAINER)
	container = lxc_wrapper.lxc_main(CONTAINER_NAME, DEBUG) 
	time.sleep(5)
	ip_addr = container.get_ips()[0]
	
	if SERVER_TYPE == 'http' :
		lxc_wrapper.lxc_attach_process(container, "python3 -m http.server " + DST_PORT)
		add_iptable("eth0", SRC_PORT, ip_addr, DST_PORT)
		http_server = server_class(container, 'http', SRC_PORT, DST_PORT)




if __name__ == '__main__' :
	args = docopt(__doc__, version='SPORA SERVER 0.1')
	print(args)
	if args['--del'] ==False:
		server_main(args['--name'], args['--type'], args['--src_port'], args['--dest_port'], args['--debug'])
	else :
		del_iptable('eth0', args['--src_port'], lxc_wrapper.ip_from_name(args['--name']), args['--dest_port'])
		lxc_wrapper.lxc_kill(lxc.Container(args['--name']))
		
		if args['--pcap']:
			print('Pcap capturing')
		
