#!/usr/bin/python3

import lxc
import sys
import platform


BASE_CONTAINER = 'LXC_REMOTE'
_DEBUG_ = False



def pr_debug(debug_log) :
	global _DEBUG_
	if _DEBUG_ == True :
		print(debug_log)



def ip_from_name(CONTAINER_NAME):
	assert lxc.list_containers().count(CONTAINER_NAME), "The container " + CONTAINER_NAME + " doesn't exist"
	container = lxc.Container(CONTAINER_NAME)
	if (container.running):
		return container.get_ips()[0]
	else:
		return None



def health_check_stopped(CONTAINER_NAME, container) :
	assert(container.config_file_name == "%s/%s/config" %(lxc.default_config_path, CONTAINER_NAME))
	assert container.init_pid == -1, "Container is already RUNNING"
	assert(container.name == CONTAINER_NAME)
	assert not container.running, "Container is already RUNNING"
	assert(container.state == "STOPPED")



def health_check_started(CONTAINER_NAME, container) :
	assert(container.config_file_name == "%s/%s/config" %(lxc.default_config_path, CONTAINER_NAME))
	assert(container.init_pid != -1)
	assert(container.name == CONTAINER_NAME)
	assert(container.running)
	assert(container.state == "RUNNING")



def __lxc_clone (container):
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



def lxc_create (container_name, template, new = False) :
	container = lxc.Container(container_name)
	if container.defined == True :
		pr_debug("<debug> Conatiner is already defined, return the object.");
	elif new == False:
		pr_debug("<debug> Cloning base container. Igonring the --template argumnets");
		container = __lxc_clone(container)
	else:
		#TODO : Create new container and return object
		pr_debug("<debug> Creating a new container")
		container.create(template)
		health_check_stopped(container.name, container)
	
	return container

def lxc_kill (container, level = 2) :
	if container.running :
		pr_debug("<debug> Stopping the container")
		container.stop()
		container.wait("STOPPED", 5)
		health_check_stopped(container.name, container)

	if level == 2 :
		pr_debug("<debug> Destroying the container and relinquishing resources")
		container.destroy()
		assert(not container.defined)


def lxc_start (container) :
	health_check_stopped(container.name, container);
	assert container.start(), "Container didn't start"
	container.wait("RUNNING", 5)
	pr_debug("<debug> Container has been started")
	health_check_started(container.name, container)
	return container



def lxc_attach_process (container, command_str, wait=False):
	assert container.running, "Container not running. Process not attached"
	try:
		if wait == False:
			pid = container.attach(lxc.attach_run_command, command_str.split(" "))
		else:
			pid = container.attach_wait(lxc.attach_run_command, command_str.split(" "))

		print(pid)
	except OSError:
		print("Not able to attach '", command_str, "' to the container", container.name)
	


def lxc_attach_process_name (CONTAINER_NAME, command_str, wait=False):
	container = lxc.Container(CONTAINER_NAME)
	lxc_attach_process(container, command_str, wait)



def lxc_attach_shell (container):
	assert container.running, "Container not running. Shell not available"
	container.attach_wait(lxc.attach_run_shell)


def lxc_main (CONTAINER_NAME, TEMPLATE, NEW, DEBUG) :	
	global _DEBUG_
	_DEBUG_ = DEBUG
	container = lxc_create(CONTAINER_NAME, TEMPLATE, NEW)
	if (not container.running):
		container = lxc_start(container)
	
	return container




if __name__ == '__main__' :
	if (sys.argv[2] == '1') :
		lxc_main(sys.argv[1], True)
	else :
		lxc_main(sys.argv[1], False)
