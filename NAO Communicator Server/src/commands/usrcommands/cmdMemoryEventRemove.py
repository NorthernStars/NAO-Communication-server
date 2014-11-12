'''
Created on 12.11.2014

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdMemoryEventRemove(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "MEMORY_EVENT_REMOVE"
        
    def exe(self, args=None, server=None):        
        # get proxy
        mem = ALProxy("ALMemory", Settings.naoHostName, Settings.naoPort)
        
        # set stiffness
        if len(args) > 0:
            
            key = str(args[0])
            
            if key in Settings.memoryCustomEvents:
            
                # declare event in ALMemory and to list
                
                mem.removeData( key )
            
                # add event to file list
                Settings.memoryCustomEvents.pop(key)
                try:
                    fo = open( Settings.memoryCustomEventsFile, 'w' )
                    fo.write( str(Settings.memoryCustomEvents) )
                    fo.close()
                except:
                    pass