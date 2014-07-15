'''
Created on 15.07.2014

@author: hannes
'''
from time import sleep
from networkService import NetworkService

if __name__ == '__main__':
    
    name = "naocom"
    regtype = "_naocom._tcp"
    
    ns = NetworkService();
    
    print "register service"
    ns.registerService(name, regtype, 1234)
    
    sleep(10.0)
    
    print "unregister service"
    ns.unregisterService(name, regtype)