'''
Created on 07.01.2013

@author: hannes
'''
from cmdSay import cmdSay
from naoqi import ALProxy
from settings.Settings import Settings

class cmdFaceTracker(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.cmd = "trackFace"
        self.started = False
        self.trackerProxy = ALProxy("ALFaceTracker", Settings.naoHostName, 9559)
        self.trackerProxy.setWholeBodyOn(True)
    
    def exe(self, args=None, addr=None):
        say = cmdSay()
        
        # check if to start or stop tracker
        if(not self.trackerProxy.isActive()):
            
            # init position
            postureProxy =  ALProxy("ALRobotPosture", Settings.naoHostName, 9559)
            postureProxy.goToPosture("StandInit", 0.8)            
            
            # say
            say.exe(["", "face tracker started", "100", "100"])
            
            # start tracker            
            self.trackerProxy.startTracker()
            self.started = True
        
        elif self.trackerProxy.isActive():
            
            # stop tracker
            self.trackerProxy.stopTracker()
            
            # say
            say.exe(["", "face tracker stopped", "100", "100"])