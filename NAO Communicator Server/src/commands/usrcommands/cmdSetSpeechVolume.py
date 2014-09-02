'''
Created on 02.09.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetSpeechVolume(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "SET_SPEECH_VOLUME"
        
    def exe(self, args=None, addr=None):
        
        # get proxies
        tts = ALProxy("ALTextToSpeech", Settings.naoHostName, Settings.naoPort)
        
        # set system volume
        if len(args) > 0:
            tts.setVolume( float(args[0]) )