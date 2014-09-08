'''
Created on 29.08.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetLifeState(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "SET_LIFE_STATE"
        
    def exe(self, args=None, addr=None):
        
        # get proxies
        life = ALProxy("ALAutonomousLife", Settings.naoHostName, Settings.naoPort)
        
        # set life state
        if len(args) > 0:
            try:
                if str(args[0]) not in life.getState():
                    life.setState( str(args[0]) )
            except:
                print "can not set life state " + str(args[0]) + ". Set disabled instead."
                life.setState( 'disabled')
        