'''
Created on 13.08.2013

@author: hannes
'''
import dataCommands
from network.server import NAOServer
from commands.Command import NAOCommand

class ServerReader(object):
    '''
    continously reads socket data
    '''


    def __init__(self, host="localhost"):
        '''
        Constructor
        '''
        self.host = host
        self.__run = True
        self.__resetTimer = 0.0
        self.__restarted = False
        self.__server = None
    
    def exe(self): 
        # create & connect __server      
        while self.__run:        
            
            self.__server = False
            self.__server = NAOServer( self.host )
            
            if not self.__server.isConnected():
                self.close()
            
            self.__restarted = True
            
            # recieve data
            while self.__server.active() and self.__run:
                
                ret = self.__server.read()
                if ret:
                    data, addr = ret
                    print "recieved data = " + str(data)
                    
                    if len( str(data) ) < 1:                        
                        self.__server.close(True)
                    else:                    
                        try:
                                
                            # try to interprete as one command
                            data = eval( data )
                            self.__handleData(data, addr)
                            
                        except:
                             
                            # more commands in one string > split data
                            data = data.split("}{")
                             
                            # check for beginng and ending brackets
                            for d in data:
                                if not d.startswith("{"):
                                    d = "{" + d
                                if not d.endswith("}"):
                                    d += "}"
                                     
                                # handle command
                                try:
                                    d = eval( str(d) )
                                    self.__handleData(d, addr)
                                except:
                                    self.__server.close(True)  
                else:
                    print "no data"              
                            
                                       
    def __handleData(self, data, addr):
        '''
        Handles recieved data                
        '''
        # check for connect
        if data:
            if 'command' in data and 'commandArguments' in data:
                
                disconnect = False
                
                # handle build in commands
                if data['command'] == dataCommands.SYS_DISCONNECT:
                    data = self.__server.createDataResponsePackage(data, True)
                    self.__server.send(data);
                    disconnect = True
                    
                elif data['command'] == dataCommands.SYS_GET_INFO:
                    data = self.__server.createDataResponsePackage(data, True)
                    disconnect = not self.__server.send(data)
                    
                elif data['command'] == dataCommands.SYS_SET_REQUIRED_DATA:
                    self.__server.setRequiredData( data['commandArguments'] )
                    data = self.__server.createDataResponsePackage(data, True)
                    disconnect = not self.__server.send(data)
                    
                # handle user
                else:
                    ret = NAOCommand.resolveCmd( data, self.__server )                  
                    data = self.__server.createDataResponsePackage(data, ret)
                    disconnect = not self.__server.send(data)
                    
            # handle protocol error
            else:
                data = self.__server.createDataResponsePackage(data, False)
                disconnect = not self.__server.send(data)    
            
            
            # check if command was successfully executed
            if disconnect:
                self.__server.close(True)        
    
    
    '''
    Closes __server reader
    '''    
    def close(self):
        self.__run = False
        self.__server.close()
        print "closed __server on", self.host