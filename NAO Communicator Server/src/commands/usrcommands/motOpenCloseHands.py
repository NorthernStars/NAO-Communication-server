'''
Created on 06.01.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class motHands(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def openHand(self, args=None):
        try:
            motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
            if args != None:
                motion.openHand(args)
            else:
                self.openHand("LHand")
        except BaseException, err:
            print err
    
    def closeHand(self, args=None):
        try:
            motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
            if args != None:
                motion.closeHand(args)
            else:
                self.closeHand(args)("LHand")
        except BaseException, err:
            print err

