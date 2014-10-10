'''
Created on 07.10.2014

@author: hannes
'''
from cmdPlayProgram import cmdPlayProgram

class cmdStopProgram(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "STOP_PROGRAM"
        
    def exe(self, args=None, socket=None):        
        # set stop flag
        cmdPlayProgram.stopProgram()