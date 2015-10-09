'''
@copyright: Copyright (C) 2014-2014 Zero Socket
@license: http://www.gnu.org/licenses/gpl.html GPL version 2

Created on Jul 27, 2014
@author: pradeepbarthur
'''

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, popen
import cgi
from zexceptions import ZSException, ZSError
from zconfig import FileConfig
from zconfig import CONF_DIR
import sys, traceback

_PORT = 13300
_SERVER_ROOT = CONF_DIR

'''
Handle HTTP Requests
'''
class ZHttpHandler(BaseHTTPRequestHandler):
    def __request_param(self, map, key):
        try:
            value = map[key].value
        except:
            value = None

        return value
        
    def do_GET(self):
        if "/" == self.path:
            self.path = "/index.html"

        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True

            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
    
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
		
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(_SERVER_ROOT + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path == "/update":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                             'CONTENT_TYPE':self.headers['Content-Type'],
                    })

                host = "broker.xaptum.com" #self.__request_param(form, "xaptum-broker-host")
                port = "3300" #self.__request_param(form, "xaptum-broker-port")
                usr = self.__request_param(form, "xaptum-network-username")
                pwd = self.__request_param(form, "xaptum-network-password")
                guid = self.__request_param(form, "xaptum-connection-guid")
                ssid = self.__request_param(form, "wireless-ssid")
                wkey = self.__request_param(form, "wireless-key")

                # Update Xaptum File Config
                fc = FileConfig()
                fc.set('ZDID', guid)
                fc.set('ZUSR', usr)
                fc.set('ZPAS', pwd)
                fc.set('ZADR', host)
                fc.set('ZPRT', int(port))
                fc.write()
                fc.close()

                # Hack to update wireless config
                try:
                    s1 = "wpa-ssid"
                    s2 = "wpa-psk"
                    cmd_fmt = "sudo find /etc/network -type f -name interfaces -exec sed -i 's/%s.*/%s \"%s\"/g' {} +" 
                    cmd = cmd_fmt % (s1, s1, ssid)
                    popen( cmd )
                    cmd = cmd_fmt % (s2, s2, wkey)
                    popen( cmd )
                except:
                    pass

                # Update wireless config
                self.server.set_wireless_config( ssid, wkey )

                self.send_response(200)
                self.end_headers()
                self.wfile.write("Xaptum Configuration Has been updated! You may close this browser session!")
                self.server.stop_server()
                return
            
        except:
            self.send_error(500,'Unable to update Xaptum Configuration.')
            traceback.print_exc(file=sys.stdout)

'''
HTTP Server
'''
class ZHttpServer(HTTPServer):
    def __init__(self):
        self.__server = None
        self.__done = False
        self.__wireless_config = {}

        if issubclass(HTTPServer, object):
            self.__server = super(ZHttpServer, self).__init__(('', _PORT), ZHttpHandler)
        else:
            self.__server = HTTPServer.__init__(self, ('', _PORT), ZHttpHandler)
        
    def set_wireless_config(self, ssid, key):
        self.__wireless_config['SSID'] = ssid
        self.__wireless_config['KEY'] = key

    def get_wireless_config(self):
        return self.__wireless_config

    def serve_forever(self):
        raise ZSError("This method is not supported by ZHttpServer")

    def stop_server(self):
        self.__done = True
        self.socket.close()

    def start_server(self):
        while not self.__done:
            self.handle_request()
