'''
Created on 15.07.2013

@author: hannes
'''

from naoqi import ALProxy
from thread import start_new_thread
from time import sleep
from motGangnamStyle import motGangnamStyle, motGangnamStyleInit
from settings.Settings import Settings

class cmdGangnamStyle(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.cmd = "gangnamStyle"
    
    def exe(self, args=None, addr=None):
        # create movement
        motGangnamStyleInit().exe()
        mot = motGangnamStyle()
        start_new_thread( mot.exe, () )
        
        # play sound
        while not mot.ready:
            pass
        sleep(1)
        player = ALProxy('ALAudioPlayer', Settings.naoHostName, Settings.naoPort)
        player.post.playFileFromPosition("/home/nao/sounds/gangnam.wav", 0, 1.0, 0.0)