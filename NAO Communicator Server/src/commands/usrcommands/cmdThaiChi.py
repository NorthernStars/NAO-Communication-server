'''
Created on 06.01.2013

@author: hannes
'''
from naoqi import ALProxy
from motThaiChi import motThaiChi
from thread import start_new_thread
from settings.Settings import Settings

class cmdThaiChi(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.cmd = "thaiChi"
    
    def exe(self, args=None, addr=None):        
        # create movement
        start_new_thread( motThaiChi().exe, () )
        
        # play sound
        player = ALProxy('ALAudioPlayer', Settings.naoHostName, Settings.naoPort)
        player.post.playFileFromPosition("/home/nao/sounds/thaichi.mp3", 0, 1.0, 0.0)