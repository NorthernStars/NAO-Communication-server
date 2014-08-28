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
                    try:
                        data = eval( data )
                    except:
                        data = None
                        ret = False                   
                    
                    # check for connect
                    if data:
                        if 'command' in data:
                            
                            # handle build in commands
                            if data['command'] == dataCommands.SYS_DISCONNECT:
                                data = self.server.createDataResponsePackage(data, True)
                                self.server.send(data);
                                ret = False
                                
                            elif data['command'] == dataCommands.SYS_GET_INFO:
                                data = self.server.createDataResponsePackage(data, True)
                                ret = self.server.send(data)
                                
                            # handle user
                            else:
                                ret = NAOCommand.resolveCmd( data, addr )
                                
                        # handle protocol error
                        else:
                            data = self.server.createDataResponsePackage(data, False)
                            ret = self.server.send(data)                  
                
                    # check if command was successfully executed
                    if not ret:
                        self.server.close(True)
                    
    '''
    Closes server reader
    '''    
    def close(self):
        self.run = False
        self.server.close()
        print "closed server on", self.host