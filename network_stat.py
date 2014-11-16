#!/usr/bin/python3

import os
import re

INTF_FILE = '/proc/net/if_inet6'
STAT_FILE = '/proc/net/dev'

def human_readable(num):
	if num < 1024:
		return str(num)+'B'
	elif num < 1024*1024:
		return str(float(num)/1024)[:6] + "KB"
	elif num < 1024*1024*1024:
		return str(float(num)/(1024*1024))[:6] + "MB"
	else:
		return str(float(num)/(1024*1024*1024))[:6] + "GB"

def make_stat_dict(stat_list):
	
	# The RX stats for our veth interface will be TX inside the container, vice versa
	# Hence the change b/w tx and rx from proc file to dictionary
	stat_dict = dict()
	stat_dict['tx_bytes'] = human_readable(int(stat_list[1]))
	stat_dict['tx_pkts'] = stat_list[2]
	stat_dict['tx_err'] = stat_list[3]
	stat_dict['tx_drop'] = stat_list[4]
	stat_dict['rx_bytes'] = human_readable(int(stat_list[9]))
	stat_dict['rx_pkts'] = stat_list[10]
	stat_dict['rx_err'] = stat_list[11]
	stat_dict['rx_drop'] = stat_list[12]
	return stat_dict

#Match all veth interface by default.
def interface_stat(match_intf = 'veth\S+'):
	assert os.path.isfile(INTF_FILE), INTF_FILE+" not found"
	assert os.path.isfile(STAT_FILE), STAT_FILE+" not found"
	
	stats = dict()
	with open(STAT_FILE, 'r') as stat_file:
		if not stat_file:
			print('Couldn\'t open the procfs file')
		# LETS USE GENERATORS, SHALL WE
		for line in (x for x in stat_file if re.match(match_intf, x)): 
			lis = line.split()
			stats[lis[0]] = dict()
			stats[lis[0]] = make_stat_dict(lis)

	return stats


def display_stat(intf = None, FILE = None):
	head_str = "Interface\tRX-Pkt\tRX-Bytes\tRX-Err\tRX-Drop\tTX-Pkt\tTX-Bytes\tTX-Err\tTX-Drop"
	print(head_str)
	FILE.write(head_str+'\n')
	if intf is None:
		stats = interface_stat()
	else:
		stats = interface_stat(intf)
	for interface in stats.keys():
		stat_str = interface+"\t"+stats[interface]['rx_pkts']+"\t"+stats[interface]['rx_bytes']+"\t"+stats[interface]['rx_err']+"\t"+stats[interface]['rx_drop']+"\t"+stats[interface]['tx_pkts']+"\t"+stats[interface]['tx_bytes']+"\t"+stats[interface]['tx_err']+"\t"+stats[interface]['tx_drop']
		FILE.write(stat_str+'\n')
		print(stat_str)


# If no name provided, print all stats
def show_stat(NAME = None, FILE = 'lxc_stat.txt'):
	with open(FILE, 'a') as log_file:
		if NAME is None:
			display_stat(FILE = log_file)
		else:
			display_stat('veth'+NAME, log_file)

