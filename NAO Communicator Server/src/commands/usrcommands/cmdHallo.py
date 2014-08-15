'''
Created on 08.09.2012

@author: hannes
'''
import naoqi
from thread import start_new_thread
from time import sleep
from motHallo import motHallo
from settings.Settings import Settings

class cmdHallo(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.cmd = "hallo"
    
    def exe(self, args=None, addr=None):
        
        # create proxy
        tts = naoqi.ALProxy('ALTextToSpeech', Settings.naoHostName, Settings.naoPort)
        
        # create movement
        mot = motHallo()
        start_new_thread(mot.exe, ())
        
        # wait a second
        sleep(1.5)
        
        # say sentence
        tts.post.say( "Hallo" )