'''
Created on 07.01.2013

@author: hannes
'''
from cmdSay import cmdSay
from naoqi import ALProxy
from settings.Settings import Settings

class cmdRedBallTracker(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.cmd = "trackBall"
        self.started = False
        self.trackerProxy = ALProxy("ALRedBallTracker", Settings.naoHostName, 9559)
        self.trackerProxy.setWholeBodyOn(True)
    
    def exe(self, args=None, addr=None):
        say = cmdSay()
        
        # check if to start or stop tracker
        if(not self.trackerProxy.isActive()):
            
            # init position
            postureProxy =  ALProxy("ALRobotPosture", Settings.naoHostName, 9559)
            postureProxy.goToPosture("StandInit", 0.8)            
            
            # say
            say.exe(["", "red ball tracker started", "100", "100"])
            
            # start tracker            
            self.trackerProxy.startTracker()
            self.started = True
        
        elif self.trackerProxy.isActive():
            
            # stop tracker
            self.trackerProxy.stopTracker()
            
            # say
            say.exe(["", "red ball tracker stopped", "100", "100"])