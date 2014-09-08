'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy


class ledLaugh(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_LAUGH"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.5;
        
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x787e22, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x2ec122, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x1e9922, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed7", 0x000000, rDuration );
            
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x040022, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x14a122, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x000022, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x000000, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x00000e, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x56ff11, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x000022, rDuration*2 );
        self.ALLeds.fadeRGB( "FaceLed7", 0x000011, rDuration*2 );
        self.running = False