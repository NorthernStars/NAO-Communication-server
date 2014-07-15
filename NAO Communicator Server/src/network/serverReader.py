'''
Created on 13.08.2013

@author: hannes
'''
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
        
        while self.run:
        
            # create & connect server
            self.server = NAOServer(self.restarted, self.host)
            self.restarted = True
            
            # recieve data
            while self.server.active() and self.run:
                
                data = ()
                addr = ""
                
                ret = self.server.read()
                if ret:
                    data, addr = ret
                    print "recieved data = " + str(data)
                
                    # resolve command
                    ret = NAOCommand.resolveCmd( eval(data), addr)
                
                    # check if command was successfully executed
                    if not ret:
                        print "RESTART CONNECTION"
                        self.server.close(True)
                    
    '''
    Closes server reader
    '''    
    def close(self):
        self.run = False
        self.server.close()
        print "closed server on", self.host