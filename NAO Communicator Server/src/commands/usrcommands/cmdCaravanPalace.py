'''
Created on 16.07.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings
from thread import start_new_thread
from motCaravanPalace import motCaravanPalace
from time import sleep

class cmdCaravanPalace(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "caravanPalace"
        
    def exe(self, args=None, addr=None):
        # create movement
        mot = motCaravanPalace()
        start_new_thread( mot.exe, () )
        start_new_thread( caravanPalaceLedAnimation().exe, () )
        
        # play sound
        while not mot.ready:
            pass
        sleep(1)
        player = ALProxy('ALAudioPlayer', Settings.naoHostName, 9559)
        player.post.playFileFromPosition("/home/nao/sounds/caravanPalace.wav", 0, 1.0, 0.0)
 
 
class caravanPalaceLedAnimation(object):
    
    def __init__(self):
        pass
    
    def exe(self):
        
        ALLeds = ALProxy("ALLeds", Settings.naoHostName, 9559)
        
        sleep(0.24)
        rDuration = 0.05;
        ALLeds.post.fadeRGB( "FaceLed0", 0x000000, rDuration );
        ALLeds.post.fadeRGB( "FaceLed1", 0x000000, rDuration );
        ALLeds.post.fadeRGB( "FaceLed2", 0xffffff, rDuration );
        ALLeds.post.fadeRGB( "FaceLed3", 0x000000, rDuration );
        ALLeds.post.fadeRGB( "FaceLed4", 0x000000, rDuration );
        ALLeds.post.fadeRGB( "FaceLed5", 0x000000, rDuration );
        ALLeds.post.fadeRGB( "FaceLed6", 0xffffff, rDuration );
        ALLeds.fadeRGB( "FaceLed7", 0x000000, rDuration );

        sleep( 0.1 );
        
        rDuration = 0.05;
        ALLeds.fadeRGB( "FaceLeds", 0xffffff, rDuration );   