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
        self.cmd = "standUp"
    
    def exe(self, args=None, addr=None):
        
        # create proxy
        postureProxy = ALProxy("ALRobotPosture", Settings.naoHostName, 9559)
        
        # stand up
        postureProxy.goToPosture("Stand", 0.8)