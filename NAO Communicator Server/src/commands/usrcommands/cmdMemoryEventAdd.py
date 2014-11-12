'''
Created on 12.11.2014

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdMemoryEventAdd(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cmd = "MEMORY_EVENT_ADD"
        
        # create list of memory events
        try:
            fi = open( Settings.memoryCustomEventsFile, 'r' )
            txt = ""
            for line in fi:
                txt += line.strip()
            fi.close()
            
            if txt.startswith("{") and txt.endswith("}"):
                Settings.memoryCustomEvents = eval(txt)
        except:
            pass
        
    def exe(self, args=None, server=None):        
        # get proxy
        mem = ALProxy("ALMemory", Settings.naoHostName, Settings.naoPort)
        
        # set stiffness
        if len(args) > 1:
            
            key = str(args[0])
            name = str(args[1])
            
            if key not in Settings.memoryCustomEvents:
            
                # declare event in ALMemory and to list
                
                mem.declareEvent( key )
            
                # add event to file list
                Settings.memoryCustomEvents[key] = name
                try:
                    fo = open( Settings.memoryCustomEventsFile, 'w' )
                    fo.write( str(Settings.memoryCustomEvents) )
                    fo.close()
                except:
                    pass
                