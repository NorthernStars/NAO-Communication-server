import logging
import dataCommands
from server import NAOServer
from settings.Settings import Settings
from commands.Command import NAOCommand

class ServerReader(object):
	"""
	Reads continuously data from NAOServer
	"""


	def __init__(self, host="localhost", session=None):
		"""
		Constructor
		:param host: Hostname or ip to connect to
		"""
		self.host = host
		self.__session = session
		self.__run = True
		self.__resetTimer = 0.0
		self.__restarted = False
		self.__server = None

	def exe(self):
		"""
		Creates and runs server
		:return: None
		"""

		# create & connect __server
		while self.__run:

			logging.info( "starting server reader %s on %s", self, self.host )
			self.__server = False
			self.__server = NAOServer( self.__session, self.host, Settings.serverDefaultPort )

			if not self.__server.isConnected():
				self.close()

			self.__restarted = True

			# recieve data
			while self.__server.active() and self.__run:

				ret = self.__server.read()
				if ret:
					data, addr = ret
					logging.debug( "recieved data = %s", str(data) )

					if len( str(data) ) < 1:
						self.__server.close(True)
					else:
						try:

							# try to interprete as one command
							data = eval( data )
							self.__handleData(data, addr)

						except:

							# more commands in one string > split data
							data = data.split("}{")

							# check for beginng and ending brackets
							for d in data:
								if not d.startswith("{"):
									d = "{" + d
								if not d.endswith("}"):
									d += "}"

								# handle command
								try:
									d = eval( str(d) )
									self.__handleData(d, addr)
								except:
									self.__server.close(True)
				else:
					logging.debug( "no data received" )

	def __sendSystemInfoData(self, data):
		"""
		Sends system information data to remote client
		:param data: Request data
		:return: True if successful, false othwerwise
		"""
		if self.__server:
			data = self.__server.createDataResponsePackage(data, True)
			return self.__server.send(data)
		logging.error( "no server set!" )
		return False


	def __handleData(self, data, addr):
		"""
		Handles received data
		:param data:	Received data string
		:param addr:	Remote address of received data
		:return: None
		"""

		# check for connect
		if data:
			if 'command' in data and 'commandArguments' in data:

				disconnect = False

				# handle build in commands
				if data['command'] == dataCommands.SYS_DISCONNECT:
					self.__sendSystemInfoData(data)
					disconnect = True

				elif data['command'] == dataCommands.SYS_GET_INFO:
					disconnect = not self.__server.send(data)

				elif data['command'] == dataCommands.SYS_SET_REQUIRED_DATA:
					self.__server.setRequiredData( data['commandArguments'] )
					disconnect = not self.__sendSystemInfoData(data)

				# handle user command
				else:
					ret = NAOCommand.resolveCmd( data, self.__server, self.__session )
					data = self.__server.createDataResponsePackage(data, ret)

					if self.__server.send(data):
						# also send system information
						disconnect = not self.__sendSystemInfoData(data)
					else:
						disconnect = True

			# handle protocol error
			else:
				logging.error( "Protocol error receiving %s", str(data) )
				disconnect = not self.__sendSystemInfoData(data)


			# check if command was executed succesfuly
			if disconnect:
				logging.warning( "restarting server due to communication errors." )
				self.__server.close(True)


	def close(self):
		"""
		Closes server reader
		:return: None
		"""
		self.__run = False
		if self.__server:
			self.__server.close()
		logging.info( "closed server reader on %s", self.host )
