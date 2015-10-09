#!/usr/bin/env python
#
# beaconbot.py
# 
# Kismet listener that stores client messages
# 
# Copyright (c) David C. Lambert, 2014
# All Right Reserved
#

import os
import sys
import thread
import signal
import sqlite3
import random
import traceback

from json import dumps
from flask import jsonify
from numpy import histogram
from time import sleep, time
from Queue import Queue, Full
from pprint import pprint
from threading import Thread
from datetime import datetime
from argparse import ArgumentParser
from collections import namedtuple
from requests import get, post, ConnectionError, Timeout, exceptions

from kismetclient import handlers
from kismetclient import Client as KismetClient

from zclient.zclient import ZClient

ClientRecord = namedtuple('ClientRecord', ['bot_mac', 'timestamp', 'mac', 'signal_dbm', 'bssid'])

# define Shutdown condition
Shutdown = False

# define ZClient

zclient = None

# define KismetListener Thread subclass
class KismetListener(Thread):
    @staticmethod
    def handle_client(listener, mac, bssid, signal_dbm):
        rec = ClientRecord(bot_mac = listener.bot_mac,
                                        timestamp = time(),
                                        mac = mac,
                                        signal_dbm = int(signal_dbm),
                                        bssid = bssid)
        json = dumps(rec)
        zclient.write( json )

    def __init__(self, addr='127.0.0.1', port=2501, bot_mac=""):
        Thread.__init__(self)

        self.daemon = True
        self._address = (addr, port)

        self.kclient_ = KismetClient(self._address)
        self.kclient_.bot_mac = bot_mac

        self.handle_client.fields = 'mac,bssid,signal_dbm'
        self.kclient_.register_handler('CLIENT', self.handle_client)

    def run(self):
        try:
            while (True):
                self.kclient_.listen()
        except:
            sys.stderr.write("Problem listening to Kismet: %s\n" % sys.exc_info()[0])
            traceback.print_exc(file=sys.stderr)
            if zclient is not None:
                zclient.shutdown()
            sys.exit(1)

# start zclient
def init_zclient():
    global zclient
    zclient = ZClient()
    zclient.start_daemon()

# fire up kismet listener
def init_kismet_listener(address, port, bot_mac):
    try:
        listener = KismetListener(address, port, bot_mac)
        listener.start()
    except:
        sys.stderr.write("Problem initializing KismetListener: %s\n" % sys.exc_info()[0])
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


# grep the first ethernet interface mac address for ID purposes
def get_mac(iface):
    import netifaces
    addresses = netifaces.ifaddresses(iface)
    return addresses[netifaces.AF_LINK][0]['addr']

def get_net_config(config):
    print "Got Config: %s" % config

# define SIGTERM handler
def handle_sigterm(signal, frame):
    global Shutdown
    global zclient
    sys.stderr.write("Got SIGTERM, shutting down...\n")
    Shutdown = True
    if zclient is not None:
        zclient.shutdown()
    sys.exit(1)


# parse cmd line args
def parse_args():
    desc = 'Beaconbot Kismet client'
    parser = ArgumentParser(description=desc)

    parser.add_argument('-P', dest='kismet_port', default='2501')
    parser.add_argument('-A', dest='kismet_address', default='127.0.0.1')
    parser.add_argument('-I', dest='bot_iface', default='eth0')
    parser.add_argument('-S', dest='sleep_time', type=float, default=30.0)
    parser.add_argument('-N', dest='batch_size', type=int, default=200)
    parser.add_argument('-D', dest='db_file', default="")
    parser.add_argument('-U', dest='dest_url', default="")
    parser.add_argument('-u', dest='config_url', default="")
    parser.add_argument('-s', dest='summary_dump', action="store_true")

    return parser.parse_args()

def main():
    use_DB = False
    use_net = False

    # add SIGTERM handler
    signal.signal(signal.SIGTERM, handle_sigterm)

    # grab args
    res = parse_args()
    sys.stderr.write("%s\n" % res)

    # get params from net config
    bot_mac = get_mac(res.bot_iface)
    #if (len(res.config_url)):
    #    url = "%s/?mac=%s" % (res.config_url, bot_mac)
    #    res = get_net_config(url, res)

    init_zclient()

    init_kismet_listener(res.kismet_address,
                         res.kismet_port,
                         bot_mac)

    try:
        while (not Shutdown):
#            sys.stderr.write("%s %d %d\n" % (str(datetime.now()), dumped_records, queue.qsize()))
            msg = zclient.read()
            if msg is not None:
                get_net_config(msg)

            sleep(res.sleep_time)

    except KeyboardInterrupt:
        sys.stderr.write("Shutting down\n")

    except:
        sys.stderr.write("Unexpected error: %s\n" % sys.exc_info()[0])
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    finally:
        if zclient is not None:
            zclient.shutdown()

    sys.exit(0)

# main
if (__name__ == '__main__'):
    main()
