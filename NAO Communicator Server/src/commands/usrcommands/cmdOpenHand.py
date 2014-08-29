'''
Created on 29.08.2014

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdOpenHand(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "OPEN_HAND"
        
    def exe(self, args=None, addr=None):
        
        # get proxy
        motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
        
        # set stiffness
        if len(args) > 1:
            if 'True' in args[1]:
                motion.openHand( str(args[0]) )
            else:
                motion.closeHand( str(args[0]) )