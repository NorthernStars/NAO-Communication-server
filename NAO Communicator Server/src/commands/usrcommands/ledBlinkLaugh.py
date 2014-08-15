'''
Created on 08.08.2013

@author: hannes
'''
from settings.Settings import Settings
from naoqi import ALProxy
from ledBlink import ledBlink
from ledLaugh import ledLaugh


class ledBlinkLaugh(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ALLeds = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        self.cmd = "ledDisco"
        self.running = False
        self.ledBlink = ledBlink()
        self.ledLaugh = ledLaugh()
        
    def exe(self, args=None, addr=None):
        if not self.running:
            self.led()
        
    def led(self):
        self.running = True
        
        self.ledBlink.exe()
        self.ledLaugh.exe()
        
        self.running = False