'''
Created on 07.09.2012

@author: hannes
'''
import os, sys
from time import sleep
from network.serverManager import ServerManager
from commands.Command import NAOCommand


if __name__ == '__main__':
	
	# set current working padth
	path = os.path.dirname(sys.argv[0])
	if not path:
		path = str(os.getcwd())
		sys.argv[0] = path + "/" + str(sys.argv[0])
		
	print "set working path from " + str(os.getcwd()) + " to " + str(path) 
	os.chdir(path)
	
	# create commands list
	NAOCommand.addCmds()
	servermanager = ServerManager()
	
	# Endlosschleife	
	while(True):
		servermanager.manage()
		sleep(5)		
	
	print "ERROR: Program terminated"
	