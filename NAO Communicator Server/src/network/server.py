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
			
		self.__framesize = framesize
		self.__sock = socket.socket(self.__type, socket.SOCK_STREAM)
		self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__initServer()

		
	def __initServer(self, reconnect=False):
		'''
		Initiates the server
		'''	
		self.__connected = False	
		#self.__sock.settimeout(2.0)
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
				data = eval(ret[0])	
				if 'command' in data and dataCommands.SYS_CONNECT in data['command']:
					data = self.createDataResponsePackage(data, True)
					self.send(data)
					return True
		
		return False
	
	def createDataResponsePackage(self, request, success=True):
		'''
		Creates data response package
		'''
		sysProxy = ALProxy("ALSystem", Settings.naoHostName, Settings.naoPort)
		batProxy = ALProxy("ALBattery", Settings.naoHostName, Settings.naoPort)
		
		data = {
			'request': request,
			'requestSuccessfull': success,
			'naoName': str( sysProxy.robotName() ),
			'batteryLevel': int( batProxy.getBatteryCharge() ),
			'stiffnessData': self.__createStiffnessDatapackage(),
			'audioData': self.__createAudioDatapackage() }			
			
		return data
	
	def __createDataRequestPackage(self, aCommand, aArguments=[] ):
		'''
		Creates data request package
		'''
		return {'command': aCommand, 'commandArguments': aArguments}
	
	def __createStiffnessDatapackage(self):
		'''
		Creates stiffness data package
		'''
		motionProxy = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
		data = {'jointStiffness': {}}
		for joint in dataJoints.JOINTS:
			try:
				stiffnessList = motionProxy.getStiffnesses( dataJoints.JOINTS[joint] )
				stiffness = 0.0
				for stiff in stiffnessList:
					if stiff > 0.0:
						stiffness += stiff
				
				stiffness = stiffness / len(stiffnessList)
				data['jointStiffness'][ dataJoints.JOINTS[joint] ] = stiffness
						
					
			except:
				print "ERROR: Unknown joint " + str(joint)
		return data
	
	def __createAudioDatapackage(self):
		'''
		Creates audio data package
		'''
		ttsProxy = ALProxy("ALTextToSpeech", Settings.naoHostName, Settings.naoPort)
		playerProxy = ALProxy("ALAudioPlayer", Settings.naoHostName, Settings.naoPort)
		
		data = {
			'masterVolume': playerProxy.getMasterVolume(),
			'speechVolume': ttsProxy.getVolume(),
			'speechVoice': ttsProxy.getVoice(),
			'speechLanguage': ttsProxy.getLanguage(),
			'speechLanguagesList': ttsProxy.getAvailableLanguages(),
			'speechVoicesList': ttsProxy.getAvailableVoices(),
			'speechPitchShift': ttsProxy.getParameter("pitchShift"),
			'speechDoubleVoice': ttsProxy.getParameter("doubleVoice"),
			'speechDoubleVoiceLevel': ttsProxy.getParameter("doubleVoiceLevel"),
			'speechDoubleVoiceTimeShift': ttsProxy.getParameter("doubleVoiceTimeShift")
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
	
		