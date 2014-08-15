'''
Created on 11.08.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdVelocityWalk(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.cmd = "velocityWalk"
    
    '''
    Velocity walk arguments: [command, x, y, theta, frequency]
    '''
    def exe(self, args=None, addr=None):
        
        # check arguments
        if len(args) != 5:
            print "argument error", args
            return False
        
        # get data
        x = float(args[1])
        y = float(args[2])
        theta = float(args[3])
        frequency = float(args[4])
        
        # create proxy
        print "velocityWalk", x, y, theta, frequency
        motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
        motion.setWalkTargetVelocity(x, y, theta, frequency)
        
        