'''
@copyright: Copyright (C) 2014-2014 Zero Socket
@license: http://www.gnu.org/licenses/gpl.html GPL version 2

Created on Jul 27, 2014
@author: pradeepbarthur
'''

from zexceptions import ZSException, ZSError
from zsocket import zsocket
from zconfig import FileConfig
from zhttp import ZHttpServer
from Queue import Queue, Empty
import threading, select

import sys, traceback
import time

_MAX_QUEUE_SIZE = 1000
_DELIM = b'.\r\n'

class ZClient(object):
    class zclient_thread(threading.Thread):
        def __init__(self, zclient):
            self.__zclient = zclient
            threading.Thread.__init__(self)

        def run(self):
            self.__zclient.start()

    def __init__(self):
        self.__read_queue = Queue(_MAX_QUEUE_SIZE)
        self.__write_queue = Queue(_MAX_QUEUE_SIZE)
        self.__wireless_config = None
        self.__zsock = None
        self.__done = False

    @classmethod
    def reset_config(cls):
        FileConfig.delete_config_file()

    def is_running(self):
        return not self.__done

    def get_wireless_config(self):
        return self.__wireless_config

    def write(self, item):
        msg = item + _DELIM
        self.__write_queue.put_nowait(msg)

    def read(self):
        try:
            return self.__read_queue.get_nowait()
        except Empty:
            return None

    def shutdown(self):
        self.__done = True
        self.__zsock.close()
        print "Shutting down zclient"

    def start(self):
        self.__loop()

    def start_daemon(self):
        th = ZClient.zclient_thread(self)
        th.start()

    def __msg(self):
        msg = None
        try:
            msg = self.__write_queue.get_nowait()
        except Empty:
            pass

        return msg

    def __loop(self):
        config_available = False

        try:
            fc = FileConfig()
            fc.read()
            config_available = True
    
        except:
            pass

        # Start Http Server to accept the config
        if not config_available:
            server = ZHttpServer()
            server.start_server()
            self.__wireless_config = server.get_wireless_config()

        # Create zero socket and connect
        self.__zsock = zsocket()
        self.__zsock.connect()

        # Cereate poll
        p = select.poll()
        p.register(self.__zsock.fileno())
        
        
        # Now config is available
        while not self.__done:
            # Poll For message from write queue
            msg = self.__msg()
            if msg is not None:
                self.__zsock.send(msg)

            # Poll for socket
            events = p.poll()
            for (fd,event) in events:
                if event & select.POLLIN == select.POLLIN:
                    msg = self.zsock.recv()
                    self.__read_queue.put_nowait(msg)
