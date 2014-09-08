'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy


class ledThinking(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_THINKING"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.5;
        
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x1111FF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x1111FF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x1111FF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x1111FF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x33CCFF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x33CCFF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x1111FF, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed7", 0x1111FF, rDuration );
            
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x33CCFF, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x33CCFF, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x33CCFF, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x33CCFF, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x1111FF, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x1111FF, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x33CCFF, rDuration*3 );
        self.ALLeds.fadeRGB( "FaceLed7", 0x33CCFF, rDuration*3 );
        self.running = False