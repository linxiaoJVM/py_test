'''
Created on 2014-7-19

@author: lin
'''
import os
import threading
import multiprocessing

def worker(sign,lock):
    lock.acquire()
    print(sign,os.getpid())
    lock.release()

print ("main",os.getpid)

#Multi-thread
records = []
lock = threading.Lock()
for i in range(5):
    thread = threading.Thread(target=worker,args=('thread',lock))
    thread.start()
    records.append(thread)
    
for thread in records:
    thread.join()
    
#Multi-process
records = []
lock = multiprocessing.Lock()
for i in range(5):
    process = multiprocessing.Process(target=worker,args=('process',lock))
    process.start()
    records.append(process)

for process in records:
    process.join()

    