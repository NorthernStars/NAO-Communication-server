import socket
import dataCommands
import dataJoints
import logging
from settings.Settings import Settings
from time import time
from threading import Lock
from time import sleep
from thread import start_new_thread


class NAOServer(object):
	"""
	Server to read data from remote control
	"""

	__framesize = 1024
	__sock = None
	__conn = None
	__addr = ("", None)
	__remoteAddr = None
	__type = socket.AF_INET
	__connected = False

	__sysProxy = None
	__batProxy = None
	__lifeProxy = None
	__motionProxy = None
	__audioProxy = None
	__ttsProxy = None
	__playerProxy = None

	__robotName = "Nao"
	__speechLanguagesList = []
	__speechVoicesList = []

	__stiffnessData = {}
	__audioData = {}

	__stiffnessDataLock = None
	__audioDataLock = None
	__requiredData = []

	__lastSend = 0.0
	__session = None

	def __init__(self, session, host=Settings.serverDefaultIP, port=Settings.serverDefaultPort, framesize=1024):
		"""
		Constructor
		:param host:		hostname or ip to bind to
		:param port: 		port to bind to
		:param framesize: 	size of data frames to receive
		"""

		self.__type = socket.AF_INET
		if ":" in host:
			self.__type = socket.AF_INET6

		try:
			if self.__type == socket.AF_INET6:
				self.__addr = (str(host), port)
			else:
				self.__addr = (socket.gethostbyname(host), port)
		except socket.gaierror:
			self.__addr = (Settings.serverDefaultIP, port)

		logging.error( str(self.__addr) )
		
		self.__session = session

		self.__sysProxy = self.__session.service("ALSystem")
		self.__batProxy = self.__session.service("ALBattery")
		self.__lifeProxy = self.__session.service("ALAutonomousLife")
		self.__motionProxy = self.__session.service("ALMotion")
		self.__audioProxy = self.__session.service("ALAudioDevice")
		self.__ttsProxy = self.__session.service("ALTextToSpeech")
		self.__playerProxy = self.__session.service("ALAudioPlayer")

		self.__robotName = self.__sysProxy.robotName()
		self.__speechLanguagesList = self.__ttsProxy.getAvailableLanguages()
		self.__speechVoicesList = self.__ttsProxy.getAvailableVoices()

		self.__stiffnessData = {}
		self.__audioData = {}
		self.__batLevel = 0
		self.__lifeState = None

		self.__stiffnessDataLock = Lock()
		self.__audioDataLock = Lock()
		self.__requiredData = []

		self.__lastSend = 0.0

		self.__framesize = framesize
		self.__sock = socket.socket(self.__type, socket.SOCK_STREAM)
		self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__initServer()

	def __initServer(self, reconnect=False):
		"""
		Initiates the server
		:param reconnect: Set true to reconnect
		:return: None
		"""
		self.__connected = False
		start_new_thread(self.__datapackageCreationTask, ())
		self.__sock.settimeout(None)
		self.__connected = self.__connect(reconnect)

	def __connect(self, reconnect=False):
		"""
		Binds the server
		:param reconnect: Set true to reconnect socket
		:return: True if binding was successful, false otherwise
		"""
		if self.__sock:
			try:

				if not reconnect:
					# get socket address
					for family, _, _, _, sockaddr in socket.getaddrinfo( self.__addr[0], self.__addr[1], 0, 0, socket.SOL_TCP ):
						if family == self.__type:
							self.__addr = sockaddr
							break

					# bind socket to ip and port
					logging.debug( "binding server to %s", str(self.__addr) )
					self.__sock.bind( self.__addr )
					self.__sock.listen(1)

				# waiting for connection
				logging.debug( "%s waiting for connection", self.__addr )
				while not self.__conn:
					self.__conn, self.__remoteAddr = self.__sock.accept()

				# waiting for connection handshake
				logging.debug( "connected %s to %s, waiting for handshake", self.__addr, self.__remoteAddr )
				if self.__connectionHandshake():
					logging.debug( "connection handshake with %s successful", self.__remoteAddr )
					return True
				logging.error( "handshake with %s failed", self.__remoteAddr )

			except socket.error as msg:
				logging.error( "error connecting to %s:%s ", str(self.__addr), str(msg) )

			return False

	def __connectionHandshake(self):
		"""
		Waits for connection handshake
		:return:	True if handshake was successful, false otherwise
		"""
		while not self.__connected:
			ret = self.read()

			if ret and len(ret) > 1:
				try:
					data = eval(ret[0])
				except (ValueError, SyntaxError):
					data = {}

				if 'command' in data and dataCommands.SYS_CONNECT in data['command']:
					data = self.createDataResponsePackage(data, True)
					self.send(data)
					return True

		return False

	def createDataResponsePackage(self, request, success=True):
		"""
		Creates data response package
		:param request:	Request package
		:param success:	Set true if request was successful
		:return:	JSON data for data response package
		"""

		self.__audioDataLock.acquire()
		self.__stiffnessDataLock.acquire()

		data = {
			'request': request,
			'requestSuccessfull': success,
			'revision': str(Settings.revision).replace("L", "").replace("l", ""),
			'naoName': self.__robotName,
			'batteryLevel': self.__batLevel,
			'lifeState': self.__lifeState,
			'stiffnessData': self.__stiffnessData,
			'audioData': self.__audioData,
			'customMemoryEvents': Settings.memoryCustomEvents }

		self.__audioDataLock.release()
		self.__stiffnessDataLock.release()

		return data

	@staticmethod
	def createDataRequestPackage(command="", arguments=[]):
		"""
		Creates a data request
		:param command:	Command
		:param arguments:	Arguments of command
		:return:			JSON data package for request package
		"""
		return {"command": command, "commandArguments": arguments}

	def __datapackageCreationTask(self):
		"""
		Background task to create status data packages
		:return: None
		"""
		while not self.__conn:
			pass

		while self.__conn:
			self.__audioDataLock.acquire()
			self.__audioData = self.__createAudioDatapackage()
			self.__audioDataLock.release()

			self.__stiffnessDataLock.acquire()
			self.__stiffnessData = self.__createStiffnessDatapackage()
			self.__stiffnessDataLock.release()

			self.__batLevel = self.__batProxy.getBatteryCharge()
			self.__lifeState = self.__lifeProxy.getState() if "lifeState" in self.__requiredData else "disabled"

			sleep(Settings.systemInfoRenewInterval)

	def __createStiffnessDatapackage(self):
		"""
		Creates stiffness data package
		:return:	JSON data for stiffness data package
		"""

		data = {'jointStiffness': {}}
		for joint in dataJoints.JOINTS:
			try:

				stiffnessList = []
				if "stiffnessData" in self.__requiredData:
					stiffnessList = self.__motionProxy.getStiffnesses( dataJoints.JOINTS[joint] )

				stiffness = 0.0
				for stiff in stiffnessList:
					if stiff > 0.0:
						stiffness += stiff

				if len(stiffnessList) > 0:
					stiffness = stiffness / len(stiffnessList)
				data['jointStiffness'][ dataJoints.JOINTS[joint] ] = stiffness

			except:
				print "ERROR: Unknown joint " + str(joint)
		data['leftHandOpen'] = self.__motionProxy.getAngles("LHand", True)[0] > 0.3
		data['rightHandOpen'] = self.__motionProxy.getAngles("RHand", True)[0] > 0.3
		return data

	def __createAudioDatapackage(self):
		"""
		Creates audio data package
		:return:	JSON data for audio data package
		"""

		data = {
			'masterVolume': self.__audioProxy.getOutputVolume() if "masterVolume" in self.__requiredData else 0,
			'playerVolume': self.__playerProxy.getMasterVolume() if "playerVolume" in self.__requiredData else 0.0,
			'speechVolume': self.__ttsProxy.getVolume() if "speechVolume" in self.__requiredData else 0.0,
			'speechVoice': self.__ttsProxy.getVoice() if "speechVoice" in self.__requiredData else "",
			'speechLanguage': self.__ttsProxy.getLanguage() if "speechLanguage" in self.__requiredData else "",
			'speechLanguagesList': self.__speechLanguagesList if "speechLanguagesList" in self.__requiredData else [],
			'speechVoicesList': self.__speechVoicesList if "speechVoicesList" in self.__requiredData else [],
			'speechPitchShift': self.__ttsProxy.getParameter("pitchShift") if "speechPitchShift" in self.__requiredData else 0.0,
			'speechDoubleVoice': self.__ttsProxy.getParameter("doubleVoice") if "speechDoubleVoice" in self.__requiredData else 0.0,
			'speechDoubleVoiceLevel': self.__ttsProxy.getParameter("doubleVoiceLevel") if "speechDoubleVoiceLevel" in self.__requiredData else 0.0,
			'speechDoubleVoiceTimeShift': self.__ttsProxy.getParameter("doubleVoiceTimeShift") if "speechDoubleVoiceTimeShift" in self.__requiredData else 0.0
			}
		return data


	def active(self):
		"""
		Checks if the socket is active and connected
		:return: True if socket is connected and active, false otherwise
		"""
		if self.__sock and self.__conn:
			return True

		return False


	def read(self):
		"""
		Reads data from socket
		:return: Tuple of (data, remote address)
		"""
		if self.__sock and self.__conn:
			try:

				data = self.__conn.recv(self.__framesize)
				return (data, self.__remoteAddr)

			except:
				pass

		return False


	def send(self, data):
		"""
		Sends data to connected client
		:param data: Data to send
		:return:	True if successful, false otherweise
		"""
		if self.__sock and self.__conn:
			try:
				self.__conn.send( str(data) + "\n" )
				self.__lastSend = time()
				return True
			except:
				pass

		return False


	def close(self, restart=False):
		"""
		Closes server connection
		:param restart: Set true to restart connection after closing
		:return:	True if successful, false otherwise
		"""
		if self.__sock:

			try:
				if self.__conn:
					self.__conn.close()
					self.__conn = None

				if not restart:
					self.__sock.close()
					self.__sock = None
					self.__remoteAddr = None
					self.__connected = False

				else:
					logging.debug( "restarting server %s", self.__addr )
					self.__initServer(True)

				return True

			except:
				logging.error( "could not close server %s", self.__addr )

		return False

	def isConnected(self):
		return self.__connected

	def setRequiredData(self, data=[]):
		self.__requiredData = data

