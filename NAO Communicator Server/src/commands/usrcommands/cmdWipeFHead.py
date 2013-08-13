'''
Created on 06.01.2013

@author: hannes
'''
from motWipeFHead import motWipeFHead
from settings.Settings import Settings

class cmdWipeFHead(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.cmd = "wipeFHead"
    
    def exe(self, args=None, addr=None):
        
        # create movement
        motWipeFHead().exe()