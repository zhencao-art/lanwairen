# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import threading

class RWLock:
    def __init__(self,name):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers   = 0
        self._name = name

    def read_lock(self):
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def read_unlock(self):
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def write_lock(self):
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def write_unlock(self):
        self._read_ready.release()
