'''
Created on 07.10.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

from time import sleep

from cmdSay import cmdSay

stopProgramFlag = False
programRunning = -1

class cmdPlayProgram(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "PLAY_PROGRAM"
        
    def exe(self, args=None, addr=None):
        
        global stopProgramFlag
        global programRunning
        
        stopProgramFlag = False
        
        for cmd in args:
            
            if stopProgramFlag:
                break;
            
            # increment command counter
            programRunning += 1
            
            # try to get cmd            
            cmd = eval( str(cmd) )
            if 'name' in cmd and 'data' in cmd:     
                           
                # select command
                if cmd['name'] == 'Say':
                    self.__say( cmd['data']['text'], addr )
                    
                elif cmd['name'] == 'Wait':
                    self.__wait( cmd['data']['time'] )
                    
                elif cmd['name'] == 'Stand up' or cmd['name'] == 'Sit down':
                    self.__posture( cmd['data']['posture'] )
        
        programRunning = -1
        
    def __posture(self, data):
        posture = ALProxy("ALRobotPosture", Settings.naoHostName, Settings.naoPort)
        posture.goToPosture( str(data), 0.8 )
        
    def __wait(self, data):
        i = float(data)/0.001
        
        while i > 0:
            sleep(0.001)
            i -= 1.0
        
    def __say(self, text, addr):
        cmdSay().exe([text.replace("\u0027", "'"), 100, 100], addr)
            
        
    @staticmethod
    def stopProgram():
        '''
        Static function to set stop flag
        '''
        stopProgramFlag = True
        
    @staticmethod
    def getStatus():
        '''
        Static function to get program status
        '''
        return programRunning