#!/usr/bin/python3

import lxc
import platform
import sys

BASE_CONTAINER = 'LXC_REMOTE'

def pr_debug(debug_log) :
	if len(sys.argv) > 2 and sys.argv[2] == '1' :
		print(debug_log)

def health_check_stopped(CONTAINER_NAME, container) :
	assert(container.config_file_name == "%s/%s/config" %(lxc.default_config_path, CONTAINER_NAME))
	assert(container.init_pid == -1)
	assert(container.name == CONTAINER_NAME)
	assert(not container.running)
	assert(container.state == "STOPPED")

def health_check_started(CONTAINER_NAME, container) :
	assert(container.config_file_name == "%s/%s/config" %(lxc.default_config_path, CONTAINER_NAME))
	assert(container.init_pid != -1)
	assert(container.name == CONTAINER_NAME)
	assert(container.running)
	assert(container.state == "RUNNING")


def __lxc_create (container):
	# Check if base container is installed
	assert lxc.list_containers().count(BASE_CONTAINER), "The container " + BASE_CONTAINER + " doesn't exist"
	# Check platform details
	assert platform.architecture()[0] == '32bit', "Support for 64 bit not available yet"
	assert platform.processor() == "i686", "x86_64 processors not supported currently"
	# Clone base container with new name
	assert container.clone(BASE_CONTAINER), 'Cloning was unsuccessful'
	pr_debug("<debug> Container was successfully cloned from the base container.")
	# Check config details and health
	health_check_stopped(container.name, container)
	# Return container object 
	return container

def lxc_create (container_name) :
	container = lxc.Container(container_name)
	if container.defined == True :
		pr_debug("<debug> Conatiner is already defined, return the object.");
	else :
		pr_debug("<debug> Creating container.");
		container = __lxc_create(container)
	
	return container

def lxc_start (container) :
	health_check_stopped(container.name, container);
	assert container.start(), "Container didn't start"
	pr_debug("<debug> Container has been started")
	health_check_started(container.name, container)
	return container

if __name__ == '__main__' :
	try :
		container = lxc_create(sys.argv[1])
	except IndexError :
		print("Usage : ./lxc_wrapper.py <name of container>")
	
	container = lxc_start(container)
