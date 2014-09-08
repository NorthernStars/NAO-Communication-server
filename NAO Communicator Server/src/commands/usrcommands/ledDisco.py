'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy


class ledDisco(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_DISCO"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        rDuration = 0.5
        self.ALLeds.post.fadeRGB( "FaceLed0", 0xff0000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0x00ff00, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x0000ff, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0xff0000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0x00ff00, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x0000ff, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0xff0000, rDuration );
        self.ALLeds.post.fadeRGB( "FaceLed7", 0x00ff00, rDuration );

        self.ALLeds.post.fadeRGB( "FaceLed0", 0x00ff00, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed1", 0xff0000, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed2", 0x00ff00, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed3", 0x0000ff, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed4", 0xff0000, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed5", 0x00ff00, rDuration*2 );
        self.ALLeds.post.fadeRGB( "FaceLed6", 0x0000ff, rDuration*2 );
        self.ALLeds.fadeRGB( "FaceLed7", 0xff0000, rDuration*2 );
        
        self.running = False