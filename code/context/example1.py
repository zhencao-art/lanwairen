# !/usr/bin/python
import time
import threading

class Context:
    def __init__(self,callback):
        self.m_fn = callback

    def finished(self):
        self.m_fn()

thread_lock = threading.Lock()
thread_cond = threading.Condition(thread_lock)

work_queue = []
thread_stop = False

def thread_entry():
    print "thread_entry"
    thread_lock.acquire()
    print "child thread get"
    while not thread_stop: 
        print "Run One len = " + str(len(work_queue))
        for i in work_queue:
            i.finished()

        for i in range(0,len(work_queue)-1):
            work_queue.pop(i)

        thread_cond.wait()
        print "child get notify"
    thread_lock.release()


def callback_1():
    print "callback_1"

def callback_2():
    print "callback_2"

context1 = Context(callback_1)
context2 = Context(callback_1)
context3 = Context(callback_2)

finish_thread = threading.Thread(target = thread_entry)
finish_thread.start()


time.sleep(5)
thread_lock.acquire()
print "main thread get"
work_queue.append(context1)
thread_cond.notify()
print "main noftify"
thread_lock.release()
print "main thread put"

#time.sleep(1)
thread_lock.acquire()
print "main thread get"
work_queue.append(context2)
print "main noftify"
thread_cond.notify()
print "main thread put"
thread_lock.release()

#time.sleep(2)
thread_lock.acquire()
work_queue.append(context3)
thread_cond.notify()
thread_lock.release()
#
#time.sleep(2)
thread_lock.acquire()
thread_cond.notify()
thread_lock.release()

finish_thread.join()
