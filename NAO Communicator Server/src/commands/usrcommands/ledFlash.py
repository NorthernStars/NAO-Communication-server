'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy


class ledFlash(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_FLASH"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.2
        self.ALLeds.post.fadeRGB( "FaceLeds", 0xffaa55, rDuration );
        self.ALLeds.fadeRGB( "FaceLeds", 0x111111, rDuration*2 );        
        self.running = False