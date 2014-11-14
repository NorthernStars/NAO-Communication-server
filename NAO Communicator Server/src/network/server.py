'''
Created on 07.09.2012

@author: hannes
'''
import socket
import dataCommands
import dataJoints
import sys
import traceback
from naoqi import ALProxy
from settings.Settings import Settings
from time import time
from threading import Lock
from time import sleep
from thread import start_new_thread

class NAOServer(object):
	'''
	classdocs
	'''

	__framesize=1024
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


	def __init__(self, host=Settings.serverDefaultIP, port=Settings.serverDefaultPort, framesize=1024):
		'''
		Constructor
		'''
		
		self.__type = socket.AF_INET
		if ":" in host:
			self.__type = socket.AF_INET6
		
		try:
			if self.__type == socket.AF_INET6:
				self.__addr = (str(host), port)
			else:
				self.__addr = (socket.gethostbyname(host), port)
		except:
			self.__addr = (Settings.serverDefaultIP, port)
			
		self.__sysProxy = ALProxy("ALSystem", Settings.naoHostName, Settings.naoPort)
		self.__batProxy = ALProxy("ALBattery", Settings.naoHostName, Settings.naoPort)
		self.__lifeProxy = ALProxy("ALAutonomousLife", Settings.naoHostName, Settings.naoPort)
		self.__motionProxy = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
		self.__audioProxy = ALProxy("ALAudioDevice", Settings.naoHostName, Settings.naoPort)
		self.__ttsProxy = ALProxy("ALTextToSpeech", Settings.naoHostName, Settings.naoPort)
		self.__playerProxy = ALProxy("ALAudioPlayer", Settings.naoHostName, Settings.naoPort)
		
		self.__robotName = self.__sysProxy.robotName()
		self.__speechLanguagesList = self.__ttsProxy.getAvailableLanguages()
		self.__speechVoicesList = self.__ttsProxy.getAvailableVoices()
				
		self.__stiffnessData = {}
		self.__audioData = {}
		
		self.__stiffnessDataLock = Lock()
		self.__audioDataLock = Lock()
		self.__requiredData = []
		
		self.__lastSend = 0.0
			
		self.__framesize = framesize
		self.__sock = socket.socket(self.__type, socket.SOCK_STREAM)
		self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__initServer()

		
	def __initServer(self, reconnect=False):
		'''
		Initiates the server
		'''	
		self.__connected = False	
		start_new_thread(self.__datapackageCreationTask, ())
		self.__sock.settimeout(None)
		self.__connected = self.__connect(reconnect)
		
	def __connect(self, reconnect=False):
		'''
		connects the socket to the specified adress
		'''
		if self.__sock:
			try:

				if not reconnect:
					# get socket address
					for family, _, _, _, sockaddr in socket.getaddrinfo( self.__addr[0], self.__addr[1], 0, 0, socket.SOL_TCP ):
						if family == self.__type:
							self.__addr = sockaddr
							break
		
					print "binding to " + str(self.__addr)					
					self.__sock.bind( self.__addr )
					self.__sock.listen(1)				
				
				print "waiting for connection"
				while not self.__conn:
					self.__conn, self.__remoteAddr = self.__sock.accept()
				
				print "connected to ", self.__remoteAddr
				if self.__connectionHandshake():
					return True
						
			except socket.error as msg:
				info = sys.exc_info()
				print "ERROR CONNECTING TO " + str(self.__addr) + ":" + str(msg)
				traceback.print_tb( info[2] )				
				
			return False
		
	
	def __connectionHandshake(self):
		while not self.__connected:
			ret = self.read()

			if ret and len(ret) > 1:
				try:
					data = eval(ret[0])
				except:
					data = {}
					
				if 'command' in data and dataCommands.SYS_CONNECT in data['command']:
					data = self.createDataResponsePackage(data, True)
					self.send(data)
					return True
		
		return False
	
	def createDataResponsePackage(self, request, success=True):
		'''
		Creates data response package
		'''
		
		self.__audioDataLock.acquire()
		self.__stiffnessDataLock.acquire()
		
		data = {
			'request': request,
			'requestSuccessfull': success,
			'revision': str(Settings.revision).replace("L", "").replace("l", ""),
			'naoName': self.__robotName,
			'batteryLevel': int( self.__batProxy.getBatteryCharge() ),
			'lifeState': self.__lifeProxy.getState() if "lifeState" in self.__requiredData else "disabled",
			'stiffnessData': self.__stiffnessData,
			'audioData': self.__audioData,
			'customMemoryEvents': Settings.memoryCustomEvents }
		
		self.__audioDataLock.release()
		self.__stiffnessDataLock.release()
				
		return data
	
	def createDataRequestPackage(self, command="", arguments=[]):
		'''
		Creates a request package
		'''
		return {"command": command, "commandArguments": arguments}
	
	def __createDataRequestPackage(self, aCommand, aArguments=[] ):
		'''
		Creates data request package
		'''
		return {'command': aCommand, 'commandArguments': aArguments}
	
	
	def __datapackageCreationTask(self):
		'''
		Background task to create stiffness and audio datapackage
		'''
		while not self.__conn:
			pass
		
		while self.__conn:
			self.__audioDataLock.acquire()
			self.__audioData = self.__createAudioDatapackage()
			self.__audioDataLock.release()
			
			self.__stiffnessDataLock.acquire()
			self.__stiffnessData = self.__createStiffnessDatapackage()
			self.__stiffnessDataLock.release()
			
			sleep(0.25)
			
			# check if to send info package
			if( time() - self.__lastSend > Settings.infoResendDelay ):
				request = self.__createDataRequestPackage( dataCommands.SYS_SEND_INFO, [] )
				data = self.createDataResponsePackage(request, False)
				self.send(data)
								
	
	def __createStiffnessDatapackage(self):
		'''
		Creates stiffness data package
		'''
		
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
		'''
		Creates audio data package
		'''
			
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
		'''
		Returns true if the socket is active
		'''
		if self.__sock and self.__conn:
			return True
		
		return False
	
	
	def read(self):
		'''
		Reads from socket and return tuple of data (data, adress)
		'''
		if self.__sock and self.__conn:
			try:		
						
				data = self.__conn.recv(self.__framesize)				
				return (data, self.__remoteAddr)
			
			except:
				pass
				
		return False
	
	
	def send(self, data):
		'''
		Sends data to socket
		'''
		if self.__sock and self.__conn:
			try:				
				self.__conn.send( str(data) + "\n" )
				self.__lastSend = time()
				return True
			except:
				pass
				
		return False
	
	
	'''
	Closes the server
	'''
	def close(self, restart=False):
		'''
		close socket connection
		'''
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
					print "restarting connection"
					self.__initServer(True)
				
				return True
			
			except:
				print "COULD NOT CLOSE SOCKET CONNECTION"
		
		return False
	
	def isConnected(self):
		return self.__connected
	
	def setRequiredData(self, data=[]):
		self.__requiredData = data
	
		