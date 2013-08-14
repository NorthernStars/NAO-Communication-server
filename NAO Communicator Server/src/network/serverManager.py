'''
Created on 13.08.2013

@author: hannes
'''
from fcntl import ioctl
from array import array
from struct import unpack, pack
from socket import socket, inet_ntoa, AF_INET, SOCK_DGRAM
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
    
    @staticmethod
    def localifs():
        """
        Used to get a list of the up interfaces and associated IP addresses
        on this machine (linux only).
    
        Returns:
            List of interface tuples.  Each tuple consists of
            (interface name, interface IP)
        """
        SIOCGIFCONF = 0x8912
        MAXBYTES = 8096
        
        var1 = 32
        var2 = 32
    
        sock = socket(AF_INET, SOCK_DGRAM)
        names = array('B', '\0' * MAXBYTES)
        outbytes = unpack('iL', ioctl(sock.fileno(), SIOCGIFCONF, pack('iL', MAXBYTES, names.buffer_info()[0]) ))[0]
    
        namestr = names.tostring()
        return [(namestr[i:i+var1].split('\0', 1)[0], inet_ntoa(namestr[i+20:i+24])) for i in xrange(0, outbytes, var2)]
        
    '''
    Gets alist of ip addresses
    '''
    @staticmethod
    def getIpAdresses(_except=[]):
        ips = []
        
        # extract ip
        for dev in ServerManager.localifs():
            if len(dev) > 1 and dev[1] not in _except:
                ips.append(dev[1])           
            
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
            