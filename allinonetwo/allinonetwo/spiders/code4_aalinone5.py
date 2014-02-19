#!/usr/bin/env python 

import subprocess
import multiprocessing
import time
import code6_allinone4
import logging
import os
from threading import Thread
from Queue import Queue
import time


cd6m = code6_allinone4.main

num_fetch_threads = 15
enclosure_queue = Queue()
enpt = enclosure_queue.put




def main3(i, q):
    dne = q.task_done
    qget = q.get

    while True:
        filename, brandname, catname, l = qget()
        fn = open(filename, "a+")
        cd6m(fn, brandname, catname, l)
        fn.close()
        dne()


def main2(pthx):

    pth = pthx.split("/")

    dirfour = "dirfour_4men_"  +  pth[0][-8:]

    dirfour = dirfour + "/" +  "/".join(pth[1:-1])

    catname = pth[-2].split("-xx-")[-2]

    brandname = pth[-1][:-3]

    filename = dirfour + "/" + pth[-1]

    try:
        os.makedirs(dirfour)
    except:
        pass

    f = open(pthx)

    for l in f:
        enpt((filename, brandname, catname, l))

    f.close()



def main(pth_list):


    for i in xrange(num_fetch_threads):
        worker = Thread(target=main3, args=(i, enclosure_queue,))
        worker.setDaemon(True)
        worker.start()


    #map(main2, pth_list)
    for l in pth_list:
        main2(l)


    print '*** Main thread waiting ***'
    enclosure_queue.join()
    print '*** Done ***'


