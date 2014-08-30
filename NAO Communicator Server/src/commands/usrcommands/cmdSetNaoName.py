'''
Created on 30.08.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetNaoName(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "SET_NAO_NAME"
        
    def exe(self, args=None, addr=None):
        
        # get proxy
        sys = ALProxy("ALSystem", Settings.naoHostName, Settings.naoPort)
        
        # set stiffness
        if len(args) > 0:
            sys.setRobotName( str(args[0]) )