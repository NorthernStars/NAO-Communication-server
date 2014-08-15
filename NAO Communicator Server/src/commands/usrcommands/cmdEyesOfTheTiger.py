'''
Created on 11.08.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdEyesOfTheTiger(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "eyesOfTheTiger"
        self.bFallManagerEnabled = True
        
    def exe(self, args=None, addr=None):
        # raise micro event
        mem = ALProxy("ALMemory", Settings.naoHostName, Settings.naoPort)
        self.ready = True
        mem.raiseMicroEvent("NAOComEyesOfTheTiger", True)
        