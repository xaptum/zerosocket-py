'''
@copyright: Copyright (C) 2014-2014 Zero Socket
@license: http://www.gnu.org/licenses/gpl.html GPL version 2

Created on Jul 27, 2014
@author: pradeepbarthur
'''

import socket
import ssl
import re
import json
from zexceptions import (ZSError, ZSException)
from zconfig import FileConfig
from zconfig import CONF_DIR


_CERT_FILE = CONF_DIR + '/.cacert.pem'
 
class zsocket(object):
    '''
    members:
        sock : socket
    '''


    def __init__(self, config = None, transport = 'SSL'):
        '''
        Constructor
        '''
        self.__sentHeader = False
        self.__starthdr_pat_ = re.compile('^\s*\{')
        self.__endhdr_pat_ = re.compile('^\s*\{.*\}\s*;')
        self.__endhdr_rep_ = re.compile('\}\s*;\s*$')
        if config is None:
            self.__conf = FileConfig()
            self.__conf.read()
        else:
            self.__conf = config

        # Create Socket. By default 'SSL'
        self.socket( transport )

    def __del__(self):
        '''
        Destructor
        '''
        self.__conf
    
    def socket(self, transport='SSL', family=socket.AF_INET, type_=socket.SOCK_STREAM , proto=0):
        '''
        @param family: socket family, defaults to AF_INET
        @param type_: socket type, defaults to SOCK_STREAM
        @param proto: protocol used, defaults to 0 , select by type_
        @param transport: transport to use, defaults to 'SSL' 
        @summary: transport determines the types of connections, SSL/TLS or regular socket (TCP)
        '''
        if transport is 'SSL':
            rawsock = socket.socket(family,type_,proto)
            self.__sock = ssl.wrap_socket(rawsock,ca_certs=_CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)
        else:
            self.__sock = socket.socket(family,type_,proto)
        return self
        
    def connect(self,address = None):
        '''
        @summary: connect behavior is determined by socket type (SSL/TLS or regular socket)
        @return: passes the return from connect bach to the caller
        '''
        if address is None:
            return self.__sock.connect(self.__conf.getaddress());
        else:
            return self.__sock.connect();
    
    ''' 
    # no supported in this release   
    def recvfrom(self, bufsize,flags = None):
        ' ' '
        @param bufsize: size to receive
        @param flags:  
        ' ' '
    '''

    def recv(self,bufsize,flags = 0):
        '''
        @summary: provides a recv interface for zerosocket
        '''
        return self.__recv_header(bufsize, flags)

        
    def recv_into(self, buff , nbytes = 4096, flags = 0):
        '''
        @return: buff: type buffer
        '''
        rbuff = self.__recv_header(nbytes, flags)
        buff[:] = rbuff
        return 
        
    def send(self, string , flags = 0):
        '''
        '''
        return self.__send_header(string,flags,None)
        
    def sendall(self, string, flags = 0):
        '''
        '''
        return self.__send_header(string,flags,0)
        
    def sendto(self, string, flags, address = None):
        '''
        @param string: 
        @param flags: 
        @param address: 
        @summary: if (address is None):
                    def sendto(self, string, address):
        '''
        return self.__send_header(string,flags,address)

    def shutdown(self,how):
        return self.__sock.shutdown(how)

    def fileno(self):
        return self.__sock.fileno()

    def close(self):
        self.__sock.close()

    def __recv_header(self,length,flags):
        '''
        @warning: this is a private method, do not call me from object
        @summary: there are no optional parameters, send me None if you intend so
        '''
        parts=[]
        #self.__checkClosed()
        if not self.__sock:
            raise ValueError("Read on closed or unwrapped Zero Socket.")
        try:
            while True:
                chunk = self.__sock.recv(length or 4096, flags)
                parts.append(chunk)
                fulldata = "".join(parts)
                if self.__starthdr_pat_.match(fulldata):
                    match = self.__endhdr_pat_.match(fulldata)
                    if match:
                        #print ('I found zero socket header')
                        #print ('header  :' + match.group(0))
                        #print ('payload :' + fulldata[match.end():] )
                        self.__parse_header(match.group(0))
                        return fulldata[match.end():]
                    else:
                        print ('zero socket header started, more data required to parse the whole header')
                        continue
                else:
                    print ('zero socket header not found')
                    return fulldata
        except Exception as zse: # as zse
            raise ZSException("in __recv_header ",zse)
    
    def __send_header(self,string,flags,address):
        '''
        @return: returns the remaining part, that is payload
        '''
        if self.__sentHeader is None or self.__sentHeader is False:
            zsstr = str(self.__conf) + ';' + string
            self.__sentHeader = True
        else:
            zsstr = string
        ''' Append zeroSocket header '''
        if address is None:
            return self.__sock.send(zsstr,flags)
        else:
            return self.__sock.send(zsstr,flags,address)

    def __parse_header(self,buf):
        jstr = self.__endhdr_rep_.sub('}',buf)
        #print "parsing : %s" % jstr
        jobj = json.loads(jstr)
        for key,value in jobj.iteritems():
            self.__conf.set(key, value)
