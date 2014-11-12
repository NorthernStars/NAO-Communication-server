'''
Created on 07.10.2014

@author: hannes
'''

from naoqi import ALProxy
from settings.Settings import Settings

from time import sleep
from os.path import expanduser
from math import radians
from thread import start_new_thread

from cmdSay import cmdSay
from cmdMemoryEventRaise import cmdMemoryEventRaise
from cmdSetSpeechLanguage import cmdSetSpeechLanguage

stopProgramFlag = False
programRunning = -1

class cmdPlayProgram(object):
    '''
    classdocs
    '''
    
    __motionActive = False


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "PLAY_PROGRAM"
        self.__motionActive = False
        
    def exe(self, args=None, server=None):
        
        global stopProgramFlag
        global programRunning
        
        stopProgramFlag = False
        programRunning = 0
        
        for cmd in args:
            
            # check if to stop
            if stopProgramFlag:
                break;
            
            # try to get cmd            
            cmd = eval( str(cmd) )
            if 'name' in cmd and 'data' in cmd: 
                
                # send current command index
                if server:
                    data = server.createDataRequestPackage("PROGRAM_STATUS", [str(programRunning)])
                    data = server.createDataResponsePackage(data)
                    server.send(data)  
                           
                # select command
                if cmd['name'] == 'Say':
                    cmdSay().exe([cmd['data']['text'].replace("\u0027", "'"), 100, 100], server)
                    
                elif cmd['name'] == 'Wait':
                    self.__wait( cmd['data']['time'] )
                    
                elif cmd['name'] == 'Stand up' or cmd['name'] == 'Sit down':
                    self.__posture( cmd['data']['posture'] )
                    
                elif cmd['name'] == 'Eye LEDs':
                    self.__eye_leds( cmd['data']['color'] )
                    
                elif cmd['name'] == 'Hello':
                    cmdMemoryEventRaise().exe(["animationHello"], server)
                    
                elif cmd['name'] == 'Stiffness':
                    self.__stiffness( cmd['data'] )
                    
                elif cmd['name'] == 'Play':
                    self.__play( cmd['data']['file'] ) 
                    
                elif cmd['name'] == 'Language':
                    cmdSetSpeechLanguage().exe( [cmd['data']['language']] , server)
                    
                elif cmd['name'] == 'Walk to':
                    self.__walk_to( cmd['data'] )
                
                elif cmd['name'] == 'Sensor':
                    self.__sensor( cmd['data'] )
                    
            
            # increment command counter
            programRunning += 1
        
        programRunning = -1
        # send current command index
        if server:
            data = server.createDataRequestPackage("PROGRAM_STATUS", [str(programRunning)])
            data = server.createDataResponsePackage(data, False)
            server.send(data)
        
    def __sensor(self, data):
        global stopProgramFlag
        
        if 'type' in data and 'value' in data:
            if data['type'] == 'Tactile' or data['type'] == 'Bumper':
                sensor = ALProxy("ALTouch", Settings.naoHostName, Settings.naoPort)
                value = str( data['value'] )
                value = value.replace("Left Hand", "LHand").replace("Right Hand", "RHand")
                value = value.replace("Left Bumper", "LFoot/Bumper/Left").replace("Right Bumper", "RFoot/Bumper/Right")
                value = value.replace(" Side", "")
                value = value.replace(" ", "/Touch/")
                ret = False
                print value
                print sensor.getStatus()
                while not ret and not stopProgramFlag:
                    for sens in sensor.getStatus():
                        if sens[0] == value:
                            ret = sens[1]                    
                    sleep(0.01)
             
#             elif data['type'] == 'Chest button':
#                 pass
            
            elif data['type'] == 'Sonar':
                mem = ALProxy("ALMemory", Settings.naoHostName, Settings.naoPort)
                sonar = ALProxy("ALSonar", Settings.naoHostName, Settings.naoPort)
                sonar.subscribe("NAOCOM")
                
                key = str( data['value'] )
                key = key.replace("detected", "Detected").replace("NOT", "Nothing").replace(" ", "")
                key = "Sonar" + key
                value = mem.getData(key)
                while value == mem.getData(key) and not stopProgramFlag:
                    sleep(0.01)
                    
                sonar.unsubscribe("NAOCOM")
                
        
    def __walk_to(self, data):
        #self.__posture("Stand")
        motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
        motion.setMoveArmsEnabled( data['arms'], data['arms'] )
        
        self.__motionActive = True
        start_new_thread( self.__motion_background_task, () )

        collisionDetectionEnabled = motion.getExternalCollisionProtectionEnabled("Move")
        motion.setExternalCollisionProtectionEnabled("Move", False)
        motion.moveTo( data['x'], data['y'], radians(data['theta']) )
        motion.setExternalCollisionProtectionEnabled("Move", collisionDetectionEnabled) 
        
        self.__motionActive = False
        
    def __motion_background_task(self):
        global stopProgramFlag
        motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
        while self.__motionActive:
            if stopProgramFlag:
                motion.stopMove()
                
        
    def __play(self, data):
        audio = ALProxy("ALLeds", Settings.naoHostName, Settings.naoPort)
        data = expanduser("~") + "/" + data.replace("\u0027", "'")
        print "started playing", data
        aID = audio.post.playFile(data)
        
        # wait for sound to finish
        global stopProgramFlag
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
        global stopProgramFlag
        i = float(data)/0.001
        
        while i > 0 and not stopProgramFlag:
            sleep(0.001)
            i -= 1.0
        
    @staticmethod
    def stopProgram():
        '''
        Static function to set stop flag
        '''
        global stopProgramFlag
        stopProgramFlag = True
        
    @staticmethod
    def getStatus():
        '''
        Static function to get program status
        '''
        global programRunning
        return programRunning