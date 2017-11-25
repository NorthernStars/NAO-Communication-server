'''
Created on 15.07.2014

@author: hannes
'''
from signal import SIGTERM
from os import killpg, setsid
from subprocess import Popen, PIPE


class NetworkService(object):
	'''
	Class to manage network services
	'''
	__registeredInfo = {}
	__timeout = 30.0

	def __init__(self, params=None):
		"""
		Constructor
		"""
		self.__registeredInfo = {}

	def __convertToListKey(self, key):
		return key.replace(".", "")

	def registerService(self, name, regtype, port):
		"""
		Registers new network service
		:param name:    Name of network service
		:param regtype: Type of network service
		:param port:    Port of network service
		:return:        None
		"""
		cmd = "avahi-publish-service " + str(name) + " " + str(regtype) + " " + str(port)
		p = Popen( cmd, stdout=PIPE, shell=True, preexec_fn=setsid )

		# add service to list
		regtype = self.__convertToListKey(regtype)
		self.__registeredInfo[name] = {}
		self.__registeredInfo[name][regtype] = p

	def unregisterService(self, name, regtype):
		"""
		Ungeristers network service
		:param name:    Name of network service
		:param regtype: Type of network service
		:return: True if successfuly unregistered, false otherweise
		"""
		regtype = self.__convertToListKey(regtype)
		service = self.getService(name, regtype)
		if service != None:

			killpg( service.pid, SIGTERM )
			self.__registeredInfo[name].pop(regtype)

			if len(self.__registeredInfo[name]) < 1:
				self.__registeredInfo.pop(name)

			return True

		return False

	def getService(self, name, regtype):
		"""
		Returns network service
		:param name: 	Name of network service
		:param regtype: Type of newtwork service
		:return: Network service or None if not found
		"""
		regtype = self.__convertToListKey(regtype)
		if name in self.__registeredInfo and regtype in self.__registeredInfo[name]:
			return self.__registeredInfo[name][regtype]

		return None

	def isServiceRegistered(self, name, regtype):
		"""
		Checks if network service is registered
		:param name: 	Network service name
		:param regtype: Network service type
		:return: True if service is registered, false otherwise
		"""
		regtype = self.__convertToListKey(regtype)
		if name in self.__registeredInfo and regtype in self.__registeredInfo[name]:
			return True

		return False