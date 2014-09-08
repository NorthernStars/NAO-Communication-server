'''
Created on 08.09.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdMemoryEventRaise(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "MEMORY_EVENT_RAISE"
        
    def exe(self, args=None, addr=None):
        
        # get proxy
        mem = ALProxy("ALMemory", Settings.naoHostName, Settings.naoPort)
        
        # set stiffness
        if len(args) > 0:
            mem.raiseEvent( str(args[0]), None )