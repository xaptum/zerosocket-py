'''
@copyright: Copyright (C) 2014-2014 Zero Socket
@license: http://www.gnu.org/licenses/gpl.html GPL version 2

Created on Jul 27, 2014
@author: pradeepbarthur
'''
import FileConfig
import zerosocket


class zsocket(object):
    '''
    @version: 1.0
    @contact: pradeep@xaptum.com
    @summary: zsocket is a wrapper class for socket or ssl class object.
                implements an interface pattern inorder to detect and extract zero socket header
                
     
    private members:
    __sock : zerosocket
    __conf : [fileconfig] type config
    '''
    
    def recv(self,bufsize,flags = 0):
        '''
        @param bufsize: 
        @param flags:  
        '''
        return self.__zsock.recv(bufsize,flags)
        
    def recvfrom(self, bufsize,flags = 0):
        '''
        @param bufsize: 
        @param flags: 
        '''
        return self.__zsock.recvfrom(bufsize,flags)

    def recv_into(self, buff , nbytes = None, flags = 0):
        '''
        @param buff: type buffer
        '''
        return self.__zsock.recv_into(buff,nbytes,flags)
        
    def send(self, string , flags = 0):
        '''
        '''
        return self.__zsock.send(string,flags)
        
    def sendall(self, string, flags = 0):
        '''
        '''
        return self.__zsock.sendall(string,flags)
        
    def sendto(self, string, flags, address = 0):
        '''
        if (address is None):
            def sendto(self, string, address):
        '''
        return self.__zsock.sendto(string,flags,address)
    
    def shutdown(self,how):
        '''
        @param how: 
        '''
        return self.__zsock.shutdown(how)

    def close(self):
        self.__zsock.close()
