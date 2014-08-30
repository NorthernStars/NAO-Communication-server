'''
Created on 06.01.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdSitDown(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.cmd = "SIT_DOWN"
    
    def exe(self, args=None, addr=None):
        
        # create proxy
        postureProxy = ALProxy("ALRobotPosture", Settings.naoHostName, Settings.naoPort)
        motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
        
        # sit down
        postureProxy.goToPosture("SitRelax", 0.8)
        
        # switch off motors
        motion.post.stiffnessInterpolation("Body", 0, 0.1)