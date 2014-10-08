'''
Created on 07.10.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

from time import sleep
from os.path import expanduser

from cmdSay import cmdSay
from cmdMemoryEventRaise import cmdMemoryEventRaise

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
                    cmdSay().exe([cmd['data']['text'].replace("\u0027", "'"), 100, 100], addr)
                    
                elif cmd['name'] == 'Wait':
                    self.__wait( cmd['data']['time'] )
                    
                elif cmd['name'] == 'Stand up' or cmd['name'] == 'Sit down':
                    self.__posture( cmd['data']['posture'] )
                    
                elif cmd['name'] == 'Eye LEDs':
                    self.__eye_leds( cmd['data']['color'] )
                    
                elif cmd['name'] == 'Hello':
                    cmdMemoryEventRaise().exe(["animationHello"], addr)
                    
                elif cmd['name'] == 'Stiffness':
                    self.__stiffness( cmd['data'] )
                    
                elif cmd['name'] == 'Play':
                    self.__play( cmd['data']['file'] ) 
        
        programRunning = -1
        
    def __play(self, data):
        audio = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        data = expanduser("~") + "/" + data.replace("\u0027", "'")
        print "started playing", data
        aID = audio.post.playFile(data)
        
        # wait for sound to finish
        while not stopProgramFlag and audio.isRunning(aID):
            sleep(0.001)
            
        audio.stop(aID)
        print "stopped"
        
    def __stiffness(self, data):
        if "status" in data and "joint" in data:
            stiffness = 1.0 if data['status'] else 0.0
            motion =  ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
            motion.setStiffnesses( data["joint"], stiffness )
        
    def __eye_leds(self, data):
        b = (data & 255 )/ 255.0
        g = ((data >> 8) & 255) / 255.0
        r = ((data >> 16) & 255) / 255.0
        led = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        led.fadeRGB("FaceLeds", r, g, b, 1.0)
        
    def __posture(self, data):
        posture = ALProxy("ALRobotPosture", Settings.naoHostName, Settings.naoPort)
        posture.goToPosture( str(data), 0.8 )
        
    def __wait(self, data):
        i = float(data)/0.001
        
        while i > 0:
            sleep(0.001)
            i -= 1.0
        
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