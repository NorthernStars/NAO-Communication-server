'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy


class ledMischievious(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_MISCHIEVIOUS"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.3
        
        self.ALLeds.post.fadeRGB( "FaceLed0", 0x060033, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0xf33300, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0xff3300, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x701a00, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0xff1a00, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x000000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed7", 0x000000, rDuration );

        self.ALLeds.post.fadeRGB( "FaceLed0", 0x140000, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0xff3300, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0xff0033, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0xf51a00, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0xff1a00, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0xff0033, rDuration*3 );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x7c0000, rDuration*3 );
        self.ALLeds.fadeRGB( "FaceLed7", 0x260000, rDuration*3 );
               
        self.running = False