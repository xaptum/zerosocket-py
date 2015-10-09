from zclient.zclient import ZClient
from zclient.zhttp import ZHttpServer
from zclient.zconfig import FileConfig
import time
import sys
import threading, select


sys.dont_write_bytecode = True

def fc():
    fc = FileConfig()
    fc.set('ZADR', 'broker.xaptum.com')
    fc.set('ZPRT', 3300)
    fc.set('ZDID', '4aa6c9e5-9b3e-11e4-ba11-42010af026b1')
    fc.set('ZUSR', 'waitbotmwc')
    fc.set('ZPAS', '5siKiyPyFcgpVvr/uEKqsQ==')
    fc.write()
        
def main():
    print "Starting Application\n"
    # Start zclient in its own thread

    try:
        i = 1;
        zclient = ZClient()
        zclient.start_daemon()

        while zclient.is_running():
            #time.sleep(0.20)
            time.sleep(1.0)
            s = "This is message: {0}".format(i)
            if i == 1:
                zclient.write( s )
            i += 1
            msg = zclient.read()
            if msg is not None:
                print "Got '%s'\n" % msg


    except KeyboardInterrupt:
        zclient.shutdown()

def http():
    server = ZHttpServer()
    server.start_server()
    
if __name__ == "__main__":
    print "poll in %d" % select.POLLIN
    print "poll pri %d" % select.POLLPRI
    print "poll out %d" % select.POLLOUT
    print "poll err %d" % select.POLLERR
    print "poll hup %d" % select.POLLHUP
    print "poll nval %d" % select.POLLNVAL

    main()
    #http()
    #fc()
