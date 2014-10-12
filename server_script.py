#!/usr/bin/python3

import lxc
import subprocess
import lxc_wrapper

BASE_CONTAINER = 'LXC_REMOTE'


def add_iptable(INTF, SRC_PORT, DEST_IP, DEST_PORT) :
	ip_table_rule = "iptables -t nat -A PREROUTING -i " + INTF + " -p tcp --dport " + SRC_PORT + " -j DNAT --to " + DEST_IP + ":" + DEST_PORT
	print(ip_table_rule)
	subprocess.call(ip_table_rule.split(" "))

def del_iptable(INTF, SRC_PORT, DEST_IP, DEST_PORT) :
	ip_table_rule = "iptables -t nat -D PREROUTING -i " + INTF + " -p tcp --dport " + SRC_PORT + " -j DNAT --to " + DEST_IP + ":" + DES    T_PORT
	print(ip_table_rule)
	subprocess.call(ip_table_rule.split(" "))


def server_main(CONTAINER_NAME, SERVER_TYPE) :
	assert lxc.list_containers().count(BASE_CONTAINER)

if __name__ == '__main__' :
	add_iptable('eth0', '80', '10.0.3.214', '8080')
	assert lxc.list_containers().count(BASE_CONTAINER)
