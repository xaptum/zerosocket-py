from zclient import ZClient
import time
import sys

sys.dont_write_bytecode = True

class App:
    def loop(self, zclient):
        print "App is looping\n"
        i = 1;
        while zclient.is_running():
            time.sleep(0.20)
            zclient.write( "This is message: {0}".format(i) )
            i += 1
            msg = zclient.read()
            if msg is not None:
                print "Got %s\n" % msg
                
    
def main():
    c = ZClient(App())
    c.loop()
    
if __name__ == "__main__":
    main()
