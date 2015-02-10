from zclient import ZClient
import time
import sys
import threading

sys.dont_write_bytecode = True

        
def main():
    print "Starting Application\n"
    # Start zclient in its own thread

    try:
        i = 1;
        zclient = ZClient()
        zclient.start_daemon()

        while zclient.is_running():
            time.sleep(0.20)
            zclient.write( "This is message: {0}".format(i) )
            i += 1
            msg = zclient.read()
            if msg is not None:
                print "Got %s\n" % msg

    except KeyboardInterrupt:
        zclient.shutdown()
    
if __name__ == "__main__":
    main()
