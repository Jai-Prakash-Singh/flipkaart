#!/usr/bin/env python 

import subprocess
import multiprocessing
import time
import code6_allinone2
import logging
from Queue import Queue
from threading import Thread


mp_num_fetch_threads = 5
mp_enclosure_queue = multiprocessing.Queue()
#mp_enclosure_queue = Queue()



logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
		                        )

def main2(i, q):
    while True:
        pth = q.get()
	logging.debug(pth)
        code6_allinone2.main(pth)
        time.sleep(2)
        #q.task_done()
    
    

def main():
    #f = open("availdirthree")
    #dirthree = f.read().strip()
    #f.close()

    dirthree = "dirthree08022014"

    output = subprocess.check_output(["find", dirthree + "/women/",  "-name",  "*.csv"])
    pth_list = output.strip().split("\n")

    val = len(pth_list)/5
    val1 = val*4
    val2 = val*5
  
    pth_list = pth_list[val1:]

    for i in range(mp_num_fetch_threads):
        worker = multiprocessing.Process(target=main2, args=(i, mp_enclosure_queue,))
        #worker = Thread(target=main2,  args=(i, mp_enclosure_queue,))
    	#worker.setDaemon(True)
    	worker.start()

    for pth in pth_list:
         mp_enclosure_queue.put(pth)

    #for pth in pth_list:
    #    code6_allinone2.main(pth)    
         


    


if __name__=="__main__":
    main()




