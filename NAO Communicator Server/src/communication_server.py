import os, sys, argparse
import logging
import signal
from time import sleep

from settings.Settings import Settings
from network.serverManager import ServerManager
from commands.Command import NAOCommand

globalStop = False

def signalHandler(signal, frame):
	global globalStop
	logging.error("Caught SIGINT singal, try to stop program")
	globalStop = True



def parseSettings():
	"""
	Function to parse settings from command line arguments
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument( "-rip", "--robotip", help="Robot ip (default: 127.0.0.1)", type=str, default="127.0.0.1" )
	parser.add_argument( "-rp", "--robotport", help="Robot port", type=int, default=9559 )
	parser.add_argument( "-rusr", "--robotuser", help="Robot login user (default: nao)", type=str, default="nao" )
	parser.add_argument( "-rpw", "--robotpassword", help="Robot login password (default: nao)", type=str, default="nao" )
	parser.add_argument( "-cmod", "--custommodules", help="Relative path to directory with custom modules to load (default ../custom)", type=str, default="../custom" )
	parser.add_argument("-gdir", "--globaldir",
						help="Absolute path to gloabl directory containing that may be loaded from command modules (default /home/nao)", type=str,
						default="/home/nao")
	parser.add_argument( "-sip", "--serverip", help="Server ip (default: 127.0.0.1)", type=str, default="127.0.0.1" )
	parser.add_argument( "-sp", "--serverport", help="Server port (default: 5050)", type=int, default=5050 )
	parser.add_argument( "-st", "--servicetype", help="Network service type (default _naocom._tcp)", type=str, default="_naocom._tcp" )
	parser.add_argument("-sysival", "--systeminforenewinterval", help="Interval to renew system information (default: 1.0)", type=float, default=1.0)
	parser.add_argument("-log", "--loglevel", help="Log level (default: INFO)", type=str, default="INFO")

	args = parser.parse_args()
	Settings.naoHostName = args.robotip
	Settings.naoPort = args.robotport
	Settings.naoPassword = args.robotpassword
	Settings.naoDefaultUser = args.robotuser
	Settings.serverDefaultIP = args.serverip
	Settings.serverDefaultPort = args.serverport
	Settings.serverServiceType = args.servicetype
	Settings.systemInfoRenewInterval = args.systeminforenewinterval
	Settings.customModulesPath = args.custommodules
	Settings.globalDirectory = args.globaldir

	numeric_level = getattr(logging, args.loglevel.upper(), None)
	if not isinstance(numeric_level, int):
			raise ValueError('Invalid log level: %s' % args.loglevel)
	else:
		logging.basicConfig(level=numeric_level)

	return True

if __name__ == '__main__':

	global globalStop

	# add signal handler
	signal.signal(signal.SIGINT, signalHandler)

	# parse settings
	parseSettings();
	logging.debug("Parsed command line options")

	# set current working path
	path = os.path.dirname(sys.argv[0])
	if not path:
		path = str(os.getcwd())
		sys.argv[0] = path + "/" + str(sys.argv[0])

		logging.debug("set working path from %s to %s", str(os.getcwd()), str(path))
		os.chdir(path)

	# create commands list
	NAOCommand.addCmds()
	servermanager = ServerManager()

	# Endlosschleife
	while not globalStop:
		if not servermanager.manage():
			break;
		sleep(2.0)

	# stop running command threads
	NAOCommand.stopThreads()

	logging.error( "Terminated" )

