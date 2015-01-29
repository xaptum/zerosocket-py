import Config
import FileConfig
import zsocket
import time

def createFileConfig():
# No path then creates a file sock.conf. If path is given tries to read from the file
    conf = FileConfig.FileConfig()
    conf.set('ZUSR', 'xxx')
    conf.set('ZPAS', 'CirzntUlsrJh3aLnOWzPKA==')
    conf.set('ZDID', '46d86470-3202-11e4-92b6-42010af0f312')
    conf.set('ZADR', 'broker.xaptum.com')
    conf.set('ZPRT', 3301)
    conf.write()
    conf.close()

def createConfig():
# No path then creates a file sock.conf. If path is given tries to read from the file
    conf = Config.Config()
    conf.set('ZUSR', 'waitbot')
    conf.set('ZPAS', 'T/K9VBAvxKjvoL01CWHx8Q==')
    conf.set('ZDID', '4aa6c9e5-9b3e-11e4-ba11-42010af026b1')
    conf.set('ZADR', 'broker.xaptum.com')
    conf.set('ZPRT', 3301)
    return conf

def send():
#    conf = FileConfig.FileConfig('sock.conf')
    conf = createConfig()
    sock = zsocket.zsocket(conf)
    sock.connect()

    for i in range(0,4):
#        time.sleep(0.20)
        sock.send("hello world")
    
#    buf = sock.recv(4096)
    sock.close()
#    print("received : %s", buf)

def main():
#    createConfig()
    send()

if __name__ == "__main__":
    main()
