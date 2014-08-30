'''
Created on 06.01.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdStandUp(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.cmd = "STAND_UP"
    
    def exe(self, args=None, addr=None):
        
        # create proxy
        postureProxy = ALProxy("ALRobotPosture", Settings.naoHostName, Settings.naoPort)
        
        # stand up
        postureProxy.goToPosture("Stand", 0.8)