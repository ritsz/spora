#!/usr/bin/python3

"""SPORA CLIENT

Usage:
  client_script.py (-h | --help)
  client_script.py --version
  client_script.py --url=<url> [--force_cmd | --force_browser] --session=<num> [--parallel] [--time=<ts>]

Options:
  -h --help             Show this screen.
  --url=<url>  		URL to open. Can be ftp, http, https links 
  --session=<num>  	Number of sessions to start
  --parallel  		Start sessions in parallel
  --force_cmd  		Force to use urllib instead of webbrowser even if X Server is running
  --force_broswer       Force to use the browser
  --time=<ts>   	Time in seconds between every request. Ignored in case of parallel
  --version             Show version.
"""


import os
import time
import webbrowser
from docopt import docopt
import urllib.request as url


USE_URLLIB = False
TRY_PARALLEL = False
SLEEPY_TIME = 0

def urllib_handler(URL, SESSIONS):
	for i in range(SESSIONS):
		time.sleep(SLEEPY_TIME)
		ufd = url.urlretrieve(URL)

def webbrowser_handler(URL, SESSIONS):
	for i in range(SESSIONS):
		time.sleep(SLEEPY_TIME)
		webbrowser.open_new_tab(url)

if __name__ == '__main__' :
	args = docopt(__doc__, version='SPORA CLIENT 0.1')
	print(args)

	if args['--time']:
		SLEEPY_TIME = int(args['--time'])
	
	try:
		display = os.environ['DISPLAY']
		if display:
			USE_URLLIB = True 
	except KeyError:
		display = None
		USE_URLLIB = True
	
	if args['--force_cmd']:
		USE_URLLIB = True
	if args['--force_browser']:
		USE_URLLIB = False
	
	if args['--parallel']:
		TRY_PARALLEL = True

	
	if USE_URLLIB:
		urllib_handler(args['--url'], int(args['--session']))
	else:	
		webbrowser_handler(args['--url'], int(args['--session']))
