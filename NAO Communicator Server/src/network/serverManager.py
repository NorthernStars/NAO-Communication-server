'''
Created on 13.08.2013

@author: hannes
'''
from fcntl import ioctl
from array import array
from struct import unpack, pack
from socket import socket, inet_ntoa, AF_INET, SOCK_DGRAM
from thread import start_new_thread
from subprocess import Popen, PIPE
from network.serverReader import ServerReader
from network.networkService import NetworkService
from settings.Settings import Settings
from naoqi import ALProxy

from time import sleep

class ServerManager(object):
    '''
    Manages several servers
    '''
    __networkService = None
    __serverReader = []
    __exceptIps = []
    __sysProxy = None

    def __init__(self, exceptIps=["127.0.0.1"]):
        '''
        Constructor
        '''
        self.__serverReader = []
        self.__exceptIps = exceptIps
        self.__networkService = NetworkService()
        self.__sysProxy = ALProxy("ALSystem", Settings.naoHostName, Settings.naoPort)
    
    @staticmethod
    def getLocalInterfaces():
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
        for dev in ServerManager.getLocalInterfaces():
            if len(dev) > 1 and dev[1] not in _except:
                
                # get ipv6 address
                ipv6 = ServerManager.getIpv6Adress(dev[0], _except)
                if ipv6:
                    ips.append(ipv6)
                
                ips.append(dev[1])           
           
        return ips
    
    @staticmethod
    def getIpv6Adress(interface, _except=[]):
        # get ipaddress
        cmd = ["ifconfig", str(interface)]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE)
        ret, err = p.communicate()
        
        if not err:
            ret = ret.split("\n")
            
            # search for ipv6 address
            for line in ret:
                if "inet6" in line:
                    data = line.split(": ")
                    if len(data) > 1:
                        data = data[1].split(" ")[0].split("/")
                        return  str(data[0]) + "%" + str(interface)
        
        return None
    
    '''
    Checks if a ip is inside server readers list
    '''
    def isIpInServerReadersList(self, ip=""):
        for reader in self.__serverReader:
            if reader.host == ip:
                return True
        return False
    
    '''
    Closes all unsused server readers in list
    '''
    def closeUnsusedReaders(self, ips=[]):    
        for reader in self.__serverReader:
            if reader.host not in ips:
                reader.close()
                self.__serverReader.remove(reader)            

    '''
    Checks servers
    '''    
    def manage(self):        
        # get list of ips
        ips = self.getIpAdresses(self.__exceptIps)
        
        # check if there's already a server for that ip
        new = False
        for ip in ips:
            if not self.isIpInServerReadersList(ip):
                self.__serverReader.append( ServerReader(ip) )
                start_new_thread( self.__serverReader[len(self.__serverReader)-1].exe, () )
                new = True
                sleep(0.1)
                
        # check if to restart service
        if new or len(ips) < 1:
            self.__networkService.unregisterService( str(self.__sysProxy.robotName()), Settings.serverServiceType ) 
        
        if new:            
            self.__networkService.registerService( str(self.__sysProxy.robotName()), Settings.serverServiceType, Settings.serverDefaultPort )

        # check for unsused readers
        self.closeUnsusedReaders(ips)
            