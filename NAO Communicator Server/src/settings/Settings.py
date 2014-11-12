'''
Created on 18.04.2013

@author: hannes
'''

class Settings(object):
    '''
    Settings class
    '''

    naoHostName = "127.0.0.1"
    naoPort = 9559
    serverDefaultIP = "127.0.0.1"
    serverDefaultPort = 5050
    serverServiceType = "_naocom._tcp"
    infoResendDelay = 1.0
    memoryCustomEventsFile = "almemory_custom.events"
    memoryCustomEvents = {}
    revision = 0
