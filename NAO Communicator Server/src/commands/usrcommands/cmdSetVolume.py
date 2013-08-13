'''
Created on 11.01.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdSetVolume(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "setVolume"
        
    def exe(self, args=None, addr=None):
        
        # get proxies
        audio = ALProxy("ALAudioDevice", Settings.naoHostName, 9559)
        
        # get volume
        volume = 100
        if( args != None ):
            volume = int( args[1] )
        
        # set volume
        if(volume < 0):
            volume = 0
        elif(volume > 100):
            volume = 100
            
        print "set volume to " + str(volume)            
        audio.setOutputVolume(volume)