'''
Created on 07.09.2012

@author: hannes
'''
import socket
from settings.Settings import Settings
from commands.usrcommands.cmdSay import cmdSay
from commands.usrcommands.cmdChangeLang import cmdChangelang

class NAOServer(object):
	'''
	classdocs
	'''

	host = None
	port = None
	__framesize=1024
	__sock = None
	__init = False


	def __init__(self, restart=False, host=Settings.serverDefaultIP, port=Settings.serverDefaultPort, framesize=1024):
		'''
		Constructor
		'''
		
		try:
			self.host = socket.gethostbyname(host)
		except:
			self.host = Settings.serverDefaultIP
			
		self.port = port
		self.__framesize = framesize
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__sock.settimeout(2.0)
		ret = self.__connect()
		
		if ret:
			if not restart:	
				cmdChangelang().exe([None, "English"])		
				cmdSay().exe([None, "Control server started.", 100, 100])			
			
		
	def __connect(self):
		'''
		connects the socket to the specified adress
		'''
		if self.__sock:
			try:
				self.__sock.bind( (str(self.host), self.port ) )
				print "bind to " + str(self.host) + " on port " + str(self.port)
				return True
			except:
				print "ERROR CONNECTING TO " + str(self.host) + ":" + str(self.port)
			return False
		
		
	def active(self):
		'''
		Returns true if the socket is active
		'''
		if self.__sock:
			return True
		
		return False
	
	
	def read(self):
		'''
		Reads from socket and return tuple of data (data, adress)
		'''
		if self.__sock:
			try:
				
				(daten, addr) = self.__sock.recvfrom(self.__framesize)
				
				# if first connect, say something
				if not self.__init:
					cmdChangelang().exe([None, "English"])
					cmdSay().exe([None, "App connected", 100, 100])
					self.__init = True
				
				return (daten, addr)
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
				self.__sock.close()
				self.__sock = None
				if not restart:
					cmdChangelang().exe([None, "English"])
					cmdSay().exe([None, "Control server stopped.", 100, 100])
				return True
			except:
				print "COULD NOT CLOSE SOCKET CONNECTION"
		
		return False
		
	
		