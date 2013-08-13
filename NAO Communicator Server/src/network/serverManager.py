'''
Created on 13.08.2013

@author: hannes
'''
from os import popen
from thread import start_new_thread
from network.serverReader import ServerReader

class ServerManager(object):
    '''
    Manages several servers
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.serverReader = []
        self.exceptIps = ["127.0.0.1"]
    
    '''
    Gets alist of ip addresses form ifconfig command
    '''
    @staticmethod
    def getIpAdresses(_except=[]):
        ips = []
        stream = popen("ifconfig | grep \"inet addr:\"")
        
        # extract ip
        for line in stream:
            line = line.split()
            if len(line) > 1:
                line = line[1].split(":")
                if len(line) > 1 and line[1] not in _except:
                    ips.append(line[1]) 
            
        return ips
    
    '''
    Checks if a ip is inside server readers list
    '''
    def isIpInServerReadersList(self, ip=""):
        for reader in self.serverReader:
            if reader.host == ip:
                return True
        return False
    
    '''
    Closes all unsused server readers in list
    '''
    def closeUnsusedReaders(self, ips=[]):    
        for reader in self.serverReader:
            if reader.host not in ips:
                reader.close()
                self.serverReader.remove(reader)            

    '''
    Checks servers
    '''    
    def manage(self):        
        # get list of ips
        ips = self.getIpAdresses(self.exceptIps)
        
        # check if there's already a server for that ip
        for ip in ips:
            if not self.isIpInServerReadersList(ip):
                self.serverReader.append( ServerReader(ip) )
                start_new_thread( self.serverReader[len(self.serverReader)-1].exe, () )

        # check for unsused readers
        self.closeUnsusedReaders(ips)
            