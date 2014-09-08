'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy
from time import sleep


class ledBlink(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_BLINK"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.05;
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0xffffff, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0xffffff, rDuration );
        self.ALLeds.fadeRGB( "FaceLed7", 0x000000, rDuration );
        
        sleep(0.1)
        
        self.ALLeds.fadeRGB( "FaceLeds", 0xffffff, rDuration );
        
        self.running = False