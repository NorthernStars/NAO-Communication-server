'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy


class ledHappy(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_HAPPY"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.5
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x002e30, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x002022, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x20d700, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0xb59b04, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x3aff00, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x001a2a, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x00182e, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed7", 0x001232, rDuration );

            
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x007030, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x006622, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0xdb8f00, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x0aff04, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0xd3dd00, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x004c2a, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x00502e, rDuration*2 );
        self.ALLeds.fadeRGB( "FaceLed7", 0x004e32, rDuration*2 );        
        self.running = False