#!/usr/bin/python3

import lxc
import sys
import time
import subprocess
import lxc_wrapper

BASE_CONTAINER = 'LXC_REMOTE'


class server_class :
	def __init__(self, _container, type_of_server, src_port, dst_port, pcap_file = None):
		self.container 	=	_container
		self.name 	= 	_container.name
		self.srv_type 	= 	type_of_server
		self.pcap	= 	pcap_file
		self.ip_addr 	= 	_container.get_ips()[0]
		self.state	=	_container.running
		self.host_port  =	src_port
		self.dest_port 	=	dst_port 
	
	#def network_stats(self):
		#subprocess. 
	


def add_iptable(INTF, SRC_PORT, DEST_IP, DEST_PORT) :
	ip_table_rule = "iptables -t nat -A PREROUTING -i " + INTF + " -p tcp --dport " + SRC_PORT + " -j DNAT --to " + DEST_IP + ":" + DEST_PORT
	print(ip_table_rule)
	subprocess.call(ip_table_rule.split(" "))



def del_iptable(INTF, SRC_PORT, DEST_IP, DEST_PORT) :
	ip_table_rule = "iptables -t nat -D PREROUTING -i " + INTF + " -p tcp --dport " + SRC_PORT + " -j DNAT --to " + DEST_IP + ":" + DEST_PORT
	print(ip_table_rule)
	subprocess.call(ip_table_rule.split(" "))



def server_main(CONTAINER_NAME, SERVER_TYPE, SRC_PORT, DST_PORT) :
	assert lxc.list_containers().count(BASE_CONTAINER)
	container = lxc_wrapper.lxc_main(CONTAINER_NAME, True)
	print("IP LEN" + str(len(container.get_ips())))
	time.sleep(5)
	ip_addr = container.get_ips()[0]
	
	if SERVER_TYPE == 'http' :
		lxc_wrapper.lxc_attach_process(container, "python3 -m http.server " + DST_PORT)
		add_iptable("eth0", SRC_PORT, ip_addr, DST_PORT)

	http_server = server_class(container, 'http', SRC_PORT, DST_PORT)
	




if __name__ == '__main__' :
	server_main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
