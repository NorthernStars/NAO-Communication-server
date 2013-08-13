'''
Created on 18.04.2013

@author: hannes
'''
from motShakeHand import motShakeHand
from motOpenCloseHands import motHands

'''
Class for open the hand for hand shaking
'''
class cmdShakeHands(object):
    '''
    classdocs
    '''

    handState = False;

    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "shakeHands1"
        self.handState = False  # true hand is initiated, otherwise false
        
    def exe(self, args=None, addr=None):
        if self.handState:
            motHands().closeHand("RHand")
            motShakeHand().shakeHand()
            motHands().openHand("RHand")
            self.handState = False
        else:
            motShakeHand().initHand()
            motHands().openHand("RHand")
            self.handState = True
        