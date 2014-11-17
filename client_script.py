#!/usr/bin/python3

"""SPORA CLIENT

Usage:
  client_script.py (-h | --help)
  client_script.py --version
  client_script.py --url=<url> [--force_cmd | --force_browser] --session=<num> [--parallel] [--time=<ts>] [--workers=<th>]

Options:
  -h --help             Show this screen.
  --url=<url>  		URL to open. Can be ftp, http, https links. Multiple url separated by space 
  --session=<num>  	Number of sessions to start
  --parallel  		Start sessions in parallel
  --force_cmd  		Force to use urllib instead of webbrowser even if X Server is running
  --force_broswer       Force to use the browser
  --time=<ts>   	Time in seconds between every request. Ignored in case of parallel
  --workers=<th>        Number of tasks running in parallel. Default is 2
  --version             Show version.
"""


import os
import time
import webbrowser
from docopt import docopt
import urllib.request as url
from multiprocessing import Process, Queue, current_process


USE_URLLIB = False
TRY_PARALLEL = False
SLEEPY_TIME = 0
WORKER_COUNT = 2



def worker(work_queue, done_queue):
	for url_list in iter(work_queue.get, 'STOP'):
		try:
			status_code = client_main(url_list, 1)
			done_queue.put("%s - %s got %s." % (current_process().name, url, status_code))
		except Exception as e:
			done_queue.put("%s failed on %s with: %s" % (current_process().name, url, e.message))
	return True



def urllib_handler(URL, SESSIONS):
	for i in range(SESSIONS):
		time.sleep(SLEEPY_TIME)
		try:
			ufd = url.urlretrieve(URL)
		except ConnectionResetError:
			print("Connection Error")





def webbrowser_handler(URL, SESSIONS):
	for i in range(SESSIONS):
		time.sleep(SLEEPY_TIME)
		try:
			webbrowser.open_new_tab(URL)
		except ConnectionResetError:
			print('Connection Error')





def parallel_main(URL_LIST, SESSION):
	sites = [URL_LIST]*SESSION
	workers = WORKER_COUNT
	work_queue = Queue()
	done_queue = Queue()

	for url_list in sites:
		work_queue.put(url_list)
	
	for w in range(workers):
		p = Process(target=worker, args=(work_queue, done_queue))
		p.start()
		
	for i in range(len(sites)):
		done_queue.get()
	
	for w in range(workers):
                work_queue.put('STOP')


def client_main(URL_LIST, SESSIONS):
	for URL in URL_LIST.split():
		if USE_URLLIB:
			urllib_handler(URL, SESSIONS)
		else:
			webbrowser_handler(URL, SESSIONS)
	
	return 'OK'




if __name__ == '__main__' :
	args = docopt(__doc__, version='SPORA CLIENT 0.1')
	
	if args['--time']:
		SLEEPY_TIME = int(args['--time'])
	
	try:
		display = os.environ['DISPLAY']
		if display:
			USE_URLLIB = False
			SLEEPY_TIME = 2
	except KeyError:
		display = None
		USE_URLLIB = True
	
	if args['--force_cmd']:
		USE_URLLIB = True
	if args['--force_browser']:
		USE_URLLIB = False
		SLEEPY_TIME = 2
	
	if args['--parallel']:
		TRY_PARALLEL = True
	if args['--workers']:
		WORKER_COUNT = int(args['--workers'])	
	if not TRY_PARALLEL:
		client_main(args['--url'], int(args['--session']))
	else:
		parallel_main(args['--url'], int(args['--session']))
			
