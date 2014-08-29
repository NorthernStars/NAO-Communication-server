'''
Created on 29.08.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetSystemVolume(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "SET_SYSTEM_VOLUME"
        
    def exe(self, args=None, addr=None):
        
        # get proxies
        audio = ALProxy("ALAudioDevice", Settings.naoHostName, Settings.naoPort)
        
        # set system volume
        if len(args) > 0:
            audio.setOutputVolume( int(args[0]) )