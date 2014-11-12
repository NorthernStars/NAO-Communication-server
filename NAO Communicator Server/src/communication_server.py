'''
Created on 07.09.2012

@author: hannes
'''
import os, sys
from time import sleep

from settings.Settings import Settings
from network.serverManager import ServerManager
from commands.Command import NAOCommand



def parseSettings(args=[]):
	'''
	Function to parse settings from command line arguments
	'''
	i = 0
	while i < len(args):
		
		if '?' in args[i]:
			
			# print help text
			print "NAO Communication server syntax:"
			print str(sys.argv[0]).split('/')[-1] + " [options]"
			print "Options:"
			print "-naohost <value>\tNAO host name or ip."
			print "-naoport <value>\tNAO NAOqi port."
			print "-serverip <value>\tCommunication server ip."
			print "-serverport <value>\tCommuncation server port."
			print "-servicetype <value>\tCommunication server network service type to publish."
			print "-resenddelay <value>\tFloat value in sec. for delay between resending info data."
			
			return False
			
		elif args[i].startswith('-') and i < len(args)-1:
			if "naohost" in args[i]:
				Settings.naoHostName = args[i+1]
			elif "naoport" in args[i]:
				Settings.naoPort = args[i+1]
			elif "serverip" in args[i]:
				Settings.serverDefaultIP = args[i+1]
			elif "serverport" in args[i]:
				Settings.serverDefaultPort = args[i+1]
			elif "servicetype" in args[i]:
				Settings.serverServiceType = args[i+1]
			elif "resenddelay" in args[i]:
				Settings.infoResendDelay = float(args[i+1])
		
		i += 2
		
	return True

if __name__ == '__main__':
	
	# set current working padth	
	path = os.path.dirname(sys.argv[0])
	if not path:
		path = str(os.getcwd())
		sys.argv[0] = path + "/" + str(sys.argv[0])
		
	os.chdir(path)
	print "set working path from " + str(os.getcwd()) + " to " + str(path)
	
	# parse settings 
	parseSettings( sys.argv[1:] );
	
	# create commands list
	NAOCommand.addCmds()
	servermanager = ServerManager()
		
	# Endlosschleife	
	while(True):
		servermanager.manage()
		sleep(2)		
	
	print "ERROR: Program terminated"
	