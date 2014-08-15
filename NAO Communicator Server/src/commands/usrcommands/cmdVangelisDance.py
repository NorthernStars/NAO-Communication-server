'''
Created on 16.07.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings
from thread import start_new_thread
from motVangelisDance import motVangelisDance
from time import sleep

class cmdVangelisDance(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "vangelisDance"
        
    def exe(self, args=None, addr=None):
        # create movement
        mot = motVangelisDance()
        start_new_thread( mot.exe, () )
        
        # play sound
        while not mot.ready:
            pass
        sleep(1)
        player = ALProxy('ALAudioPlayer', Settings.naoHostName, Settings.naoPort)
        player.post.playFileFromPosition("/home/nao/sounds/vangelis.mp3", 0, 1.0, 0.0)
        