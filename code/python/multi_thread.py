#!/usr/bin/python

import threading
import Queue
import time

class Builder:
    def run(self, idx, wq, wq_lock):
        print "running " + str(idx)
        while True:
            time.sleep(1)
            wq_lock.acquire()
            if not wq.empty():
                work = wq.get()
                wq_lock.release()
                print "process " + work + " on " + str(idx)
            else:
                wq_lock.release()

    def start(self):
        work_queue = Queue.Queue(10)
        lock = threading.Lock()
        threads = []
        for i in range(0, 4):
            thread = threading.Thread(target = self.run, args = (i, work_queue, lock,))
            threads.append(thread)

        for i in threads:
            print "start"
            i.start()

        lock.acquire()
        work_queue.put("1")
        work_queue.put("2")
        work_queue.put("3")
        work_queue.put("3")
        lock.release()

        for i in threads:
            i.join()

builder = Builder()

builder.start()
