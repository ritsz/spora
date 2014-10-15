#!/usr/bin/python3

################
## TODO
## 2> Add pcap start stop support
## 3> Edit config and cgroup values via commandline
## 4> Add help string to all functions

"""SPORA SERVER.

Usage:
  server_script.py (-h | --help)
  server_script.py --name=<name> [--base=base] [--template=tp] --type=<server> --intf=<intf> [--src_port=<kn>] [--dest_port=<kn>] [--args <args>...] [--pcap=<file>]
  server_script.py --name=<name> [--base=base] [--template=<tp>] --type=<server> --intf=<intf> [--src_port=<kn>] [--dest_port=<kn>] [--args <args>...] [--pcap=<file>] [--debug ] [--new]
  server_script.py --name=<name> [--type=<server>] --src_port=<kn> --intf=<intf> --dest_port=<kn> --del
  server_script.py --name=<name> --copy_from=<path> --copy_to=<path>
  server_script.py --name=<name> --cmd=<command> [--wait]
  server_script.py --name=<name> --shell
  server_script.py --version

Options:
  -h --help             Show this screen.
  --debug               Show debug messages  
  --version             Show version.
  --name=<name>         Name of server
  --base=base           Base container which is to be cloned
  --template=tp         Template to use for container [default: sshd]
  --type=<server>       Type of Server
  --intf=<intf>         Interface to start the server on.
  --src_port=<sp>       Local port for server
  --dest_port=<dp>      Port on which container is handling the server 
  --pcap=<file>         Perform packet capture and save in <file>
  --copy_from==<path>   Copy file from path 
  --copy_to==<path>	Copy file to path 
  --cmd=<command>	Command to attach to the server container
  --wait                Wait for command to finish [default: False]
  --args <args>...	Repeated arguments required as configs in case of some servers
"""


import lxc
import sys
import time
from docopt import docopt
import subprocess
import lxc_wrapper

BASE_CONTAINER = 'LXC_HTTP'

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
		



def server_main(CONTAINER_NAME, TEMPLATE, SERVER_TYPE, INTF, SRC_PORT, DST_PORT, DEBUG, NEW) :
	if NEW == False:
		assert lxc.list_containers().count(BASE_CONTAINER), "The " + BASE_CONTAINER + " doesn't exist" 
		print(BASE_CONTAINER + ' is present')		

	container = lxc_wrapper.lxc_main(CONTAINER_NAME, BASE_CONTAINER, TEMPLATE, NEW, DEBUG)
	time.sleep(5)
	ip_addr = container.get_ips()[0]
	
	if SERVER_TYPE == 'http' :
		if NEW:
			copy_file(container, 'http_server.py', '.')
		http_cmd = "./http_server.py --src_port="+DST_PORT
		lxc_wrapper.lxc_attach_process(container, http_cmd)
		add_iptable(INTF, SRC_PORT, ip_addr, DST_PORT)
		http_server = server_class(container, 'http', SRC_PORT, DST_PORT)

	if SERVER_TYPE == 'ftp':
		if NEW:
			copy_file(container, 'ftp_server.py', '.')
		ftp_cmd = "./ftp_server.py --src_port=" + DST_PORT
		lxc_wrapper.lxc_attach_process(container, ftp_cmd)
		add_iptable(INTF, SRC_PORT, ip_addr, DST_PORT)
		ftp_server = server_class(container, 'ftp', SRC_PORT, DST_PORT)
		
		

def copy_file(__container, FROM, TO):
	rootfs_path = __container.get_config_path() + '/' + __container.name + '/rootfs/'
	copy_to = rootfs_path + TO
	copy_command = 'cp -vR ' + FROM + ' ' + copy_to
	print(copy_command)
	subprocess.call(copy_command.split(' '))




if __name__ == '__main__' :
	args = docopt(__doc__, version='SPORA SERVER 0.1')
	print(args)
	
	if args['--base']:
		BASE_CONTAINER = args['--base']
	
	if args['--name']:
		__container = lxc.Container(args['--name'])
	
	
	if args['--shell']:
		lxc_wrapper.lxc_attach_shell(__container)
		exit()
	
	if args['--cmd']:
		lxc_wrapper.lxc_attach_process_name(__container.name, args['--cmd'], args['--wait'])
		exit()
	
	
	if args['--del'] ==False:
		if (args['--copy_from'] != None) and (args['--copy_to'] != None):
			assert args['--copy_from'] != '', 'Provide correct paths'
			copy_file(__container, args['--copy_from'], args['--copy_to'])
			exit()
		
		server_main(args['--name'], args['--template'], args['--type'], args['--intf'], args['--src_port'], args['--dest_port'], args['--debug'], args['--new'])
	
	else :
		del_iptable(args['--intf'], args['--src_port'], lxc_wrapper.ip_from_name(args['--name']), args['--dest_port'])
		lxc_wrapper.lxc_kill(__container)
		
		if args['--pcap']:
			print('Pcap capturing')
		
