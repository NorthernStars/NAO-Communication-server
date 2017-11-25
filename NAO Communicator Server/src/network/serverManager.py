from thread import start_new_thread
from subprocess import Popen, PIPE
from serverReader import ServerReader
from networkService import NetworkService
from settings.Settings import Settings
from naoqi import ALProxy
from subprocess import check_output
import logging

from time import sleep

class ServerManager(object):
	"""
	Manages several servers
	"""
	__networkService = None
	__serverReader = []
	__exceptIps = []
	__sysProxy = None

	def __init__(self, exceptIps=["127.0.0.1", "0.0.0.0"]):
		"""
		Constructor
		"""
		self.__serverReader = []
		self.__exceptIps = exceptIps
		self.__networkService = NetworkService()
		self.__sysProxy = ALProxy("ALSystem", Settings.naoHostName, Settings.naoPort)

	@staticmethod
	def getLocalInterfaces():
		"""
		Used to get a list of the up interfaces and associated IP addresses
		on this machine (linux only).

		Returns:
			List of interface tuples.  Each tuple consists of
			(interface name, interface IPv4, interface IPv6)
		"""
		localifaces = []

		retstr = check_output(["ifconfig"])
		retstr = retstr.split('\n\n')

		# check interfaces
		for ifacestr in retstr:

			# get iface name
			ifname = ifacestr.split('Link encap', 1)[0].strip()
			if len(ifname) > 0:

				# get device information
				ifacestr = ifacestr.split('\n')
				ipv4 = None
				ipv6 = None
				for entry in ifacestr:

					# check for ip addresses
					if 'inet6' in entry:
						ipv6 = entry.strip().split(':', 1)[1].strip().split(' ')[0].strip().split('/')[0]
						ipv6 += "%"+ifname
					elif 'inet' in entry:
						ipv4 = entry.strip().split(':', 1)[1].strip().split(' ')[0].strip()

				if ipv4 != None or ipv6 != None:
					localifaces.append( (ifname, ipv4, ipv6) )

		return localifaces


	def getIpAdresses(self, _except=[]):
		"""
		Gets a list of ip addresses
		:param _except: Ip adresses to ignore
		:return: Array of ip adresses
		"""
		ips = []

		# extract ip
		for dev in self.getLocalInterfaces():
			if len(dev) > 2 and dev[1] not in _except and dev[2] not in _except:
				if dev[1] != None:
					ips.append(dev[1])
				if dev[2] != None:
					ips.append(dev[2])

		return ips


	def isIpInServerReadersList(self, ip=""):
		"""
		Checks if a ip is inside server readers list
		:param ip: Ip to check
		:return: True if ip is in readers list, false otherwise
		"""
		for reader in self.__serverReader:
			if reader.host == ip:
				return True
		return False

	def closeUnsusedReaders(self, ips=[]):
		"""
		Closes all unused server readers in list
		:param ips: Ips to ignore
		:return: None
		"""
		for reader in self.__serverReader:
			if reader.host not in ips:
				logging.debug( "Closing reader %s", str(reader.host) )
				reader.close()
				self.__serverReader.remove(reader)

	def manage(self):
		"""
		Manages several servers on different ips
		:return: True if closed carefuly, false otherwise
		"""

		# get list of ips
		ips = self.getIpAdresses(self.__exceptIps)
		if len(ips) == 0:
				logging.error( "No valid network interfaces found!" )
				return False
		else:
			logging.debug( "Managing servers on ips: %s", str(ips) )

		# check if there's already a server for that ip
		new = False
		for ip in ips:
			if not self.isIpInServerReadersList(ip):
				self.__serverReader.append( ServerReader(ip) )
				start_new_thread( self.__serverReader[len(self.__serverReader)-1].exe, () )
				new = True

		# check if to restart network service
		if new or len(ips) < 1:
			self.__networkService.unregisterService( str(self.__sysProxy.robotName()), Settings.serverServiceType )

		if new:
			logging.debug( "Registering network service" )
			self.__networkService.registerService( str(self.__sysProxy.robotName()), Settings.serverServiceType, Settings.serverDefaultPort )

		# check for unsused readers
		self.closeUnsusedReaders(ips)

		return True
