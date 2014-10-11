#!/usr/bin/python3

import lxc
import sys

BASE_CONTAINER = 'LXC_REMOTE'

def pr_debug(debug_log) :
	if len(sys.argv) > 2 and sys.argv[2] == '1' :
		print(debug_log)


def __lxc_create (container):
	# Check if base container is installed
	assert lxc.list_containers().count(BASE_CONTAINER), "The container " + BASE_CONTAINER + " doesn't exist"
	# Check platform details
	# Clone base container with new name
	assert container.clone(BASE_CONTAINER), 'Cloning was unsuccessful'
	# Check config details and health
	# Return container object 
	return container

def lxc_create (container_name) :
	container = lxc.Container(container_name)
	if container.defined == True :
		pr_debug("<debug> Conatiner is already defined, return the object.");
		return container
	else :
		pr_debug("<debug> Creating container.");
		container = __lxc_create(container)			

if __name__ == '__main__' :
	try :
		lxc_create(sys.argv[1])
	except IndexError :
		print("Usage : ./lxc_wrapper.py <name of container>")
