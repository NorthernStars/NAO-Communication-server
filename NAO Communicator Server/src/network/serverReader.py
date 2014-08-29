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
        self.run = True
        self.restarted = False
        self.server = None
    
    def exe(self): 
        # create & connect server      
        while self.run:        
            
            self.server = False
            self.server = NAOServer( self.host )
            
            if not self.server.isConnected():
                self.close()
            
            self.restarted = True
            
            # recieve data
            while self.server.active() and self.run:
                
                ret = self.server.read()
                if ret:
                    data, addr = ret
                    print "recieved data = " + str(data)
                    
                    if len( str(data) ) < 1:                        
                        self.server.close(True)
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
                                    self.server.close(True)                
                            
                                       
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
                    data = self.server.createDataResponsePackage(data, True)
                    self.server.send(data);
                    disconnect = True
                    
                elif data['command'] == dataCommands.SYS_GET_INFO:
                    data = self.server.createDataResponsePackage(data, True)
                    disconnect = not self.server.send(data)
                    
                # handle user
                else:
                    ret = NAOCommand.resolveCmd( data, addr )
                    data = self.server.createDataResponsePackage(data, ret)
                    disconnect = not self.server.send(data)
                    
            # handle protocol error
            else:
                data = self.server.createDataResponsePackage(data, False)
                disconnect = not self.server.send(data)    
            
            
            # check if command was successfully executed
            if disconnect:
                self.server.close(True)             
    
        
                        
    
    '''
    Closes server reader
    '''    
    def close(self):
        self.run = False
        self.server.close()
        print "closed server on", self.host