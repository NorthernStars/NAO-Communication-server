'''
Created on 29.08.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetJointStiffness(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "SET_JOINT_STIFFNESS"
        
    def exe(self, args=None, addr=None):
        
        # get proxy
        motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
        
        # set stiffness
        if len(args) > 1:
            motion.setStiffnesses( str(args[0]), float(args[1]) )