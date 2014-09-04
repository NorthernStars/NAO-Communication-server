'''
Created on 04.09.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetSpeechLanguage(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "SET_SPEECH_LANGUAGE"
        
    def exe(self, args=None, addr=None):
        
        # get proxies
        tts = ALProxy("ALTextToSpeech", Settings.naoHostName, Settings.naoPort)
        
        # set system volume
        if len(args) > 0:
            tts.setLanguage( str(args[0]) )