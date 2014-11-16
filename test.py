from threading import Thread
import urllib.request as url
import re

def VideoHandler(id_list):
    for id in id_list:
        try:
            print(str(id), "RUN")
            data = url.urlretrieve("https://10.0.3.191")
        except:
            import traceback
            traceback.print_exc()

threads = []
nb_threads = 8
max_id = 10000
for i in range( nb_threads):
    id_range = range(i*max_id//nb_threads, (i+1)*max_id//nb_threads + 1)
    thread = Thread(target=VideoHandler, args=(id_range,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join() # wait for completion
