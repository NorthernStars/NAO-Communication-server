'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy

from time import sleep

class ledCircleEyes(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_CIRCLE_EYES"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        
        nNbrSegment = 8;
        rTime= 0.7
        nNbrTurn = 1
        p = [0, 255, 255]   # r, g, b
        nColor = (p[0]<<16) + (p[1] << 8) + p[2]
        
        for i in range( nNbrSegment*nNbrTurn ):
            self.ALLeds.post.fadeRGB( "FaceLed%d" % (i%nNbrSegment) , nColor, rTime );
            self.ALLeds.post.fadeRGB( "FaceLed%d" % (i%nNbrSegment) , 0x000000, rTime*1.25 );
            sleep( rTime*0.25 );
        sleep( rTime*0.5 ); 
               
        self.running = False