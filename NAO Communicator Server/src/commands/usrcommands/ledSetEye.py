'''
Created on 08.09.2014

@author: hannes
'''

from settings.Settings import Settings
from naoqi import ALProxy


class ledSetEye(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "LED_SET_EYE"
        self.running = False
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led(args)
        
    def led(self, args):
        self.running = True
        rDuration = 0.05;
        
        if len(args) > 1:
            if "left" in str(args[0]):
                self.ALLeds.post.fadeRGB( "LeftFaceLeds", int(args[1]), rDuration );
            elif "right" in str(args[0]):
                self.ALLeds.post.fadeRGB( "RightFaceLeds", int(args[1]), rDuration );                    
        
        self.running = False