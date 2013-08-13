'''
Created on 13.08.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings
import socket

class cmdInfo(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.cmd = "info"
    
    def exe(self, args=None, addr=None):
        
        if len(args) != 2 and addr != None:
            pass
        
        sentinel = ALProxy('ALSentinel', Settings.naoHostName, 9559)
        battery = sentinel.getBatteryLevel()
        robotName = socket.gethostname()
        remoteHost = addr[0]
        remotePort = args[1]
        
        msg = "[info," + str(robotName) + "," + str(battery) + "]"
        
        # create socket for connection to remote host
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, (remoteHost, int(remotePort)))
        sock.close