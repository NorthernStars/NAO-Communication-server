'''
Created on 08.08.2013

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdEvolutionDance(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "evolutionOfDance"
        self.bFallManagerEnabled = True
        
    def exe(self, args=None, addr=None):
        # raise micro event
        mem = ALProxy("ALMemory", Settings.naoHostName, 9559)
        self.ready = True
        mem.raiseMicroEvent("NAOComEvolutionDance", True)
        