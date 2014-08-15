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

	__framesize=1024
	__sock = None
	__init = False
	__conn = None
	__addr = ("", None)
	__remoteAddr = None
	__type = socket.AF_INET
	__connected = False


	def __init__(self, restart=False, host=Settings.serverDefaultIP, port=Settings.serverDefaultPort, framesize=1024):
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
		self.__connected = False	
		self.__sock = socket.socket(self.__type, socket.SOCK_STREAM)
		#self.__sock.settimeout(2.0)
		self.__connected = self.__connect()
		
		if self.__connected:
			if not restart:	
				cmdChangelang().exe([None, "English"])		
				cmdSay().exe([None, "Control server started.", 100, 100])	
		
	def __connect(self):
		'''
		connects the socket to the specified adress
		'''
		if self.__sock:
			try:

				# get socket address
				for family, _, _, _, sockaddr in socket.getaddrinfo( self.__addr[0], self.__addr[1], 0, 0, socket.SOL_TCP ):
					if family == self.__type:
						self.__addr = sockaddr
						break
	
				print "binding to " + str(self.__addr)
				self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				self.__sock.bind( self.__addr )
				self.__sock.listen(1)				
				
				print "waiting for connection"
				while not self.__conn:
					self.__conn, self.__remoteAddr = self.__sock.accept()
				
				print "connected to ", self.__remoteAddr
				self.__connectionHandshake()
				
				return True
			
			except:
				print "ERROR CONNECTING TO " + str(self.__addr)
				
			return False
		
	
	def __connectionHandshake(self):
		while not self.__connected:
			ret = self.read()
			if ret:
				ret = eval(ret)		
		
		
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
				
				# if first connect, say something
				if not self.__init:
					cmdChangelang().exe([None, "English"])
					cmdSay().exe([None, "App connected", 100, 100])
					self.__init = True
				
				return (data, self.__remoteAddr)
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
				self.__conn = None
				self.__remoteAddr = None
				self.__addr = ("", None)
				if not restart and self.__connected:
					cmdChangelang().exe([None, "English"])
					cmdSay().exe([None, "Control server stopped.", 100, 100])
				return True
			except:
				print "COULD NOT CLOSE SOCKET CONNECTION"
		
		return False
	
	def isConnected(self):
		return self.__connected
	
		