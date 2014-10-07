'''
Created on 07.10.2014

@author: hannes
'''
from cmdPlayProgram import cmdPlayProgram

class cmdGetProgramStatus(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "PROGRAM_STATUS"
        
    def exe(self, args=None, addr=None):        
        # set stop flag
        print addr
        print "running? " + str(cmdPlayProgram.getStatus())