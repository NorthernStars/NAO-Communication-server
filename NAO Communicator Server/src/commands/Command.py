from commands.usrcommands import * 			# @UnusedWildImport
from thread import start_new_thread
import logging
import os
import inspect
import commands.usrcommands

class NAOCommand(object):
	"""
	Main command class
	"""
	lst = []
	
	'''
	------------------------------------------------------
	INSERT NEW NAO COMMANDS HERE
	------------------------------------------------------
	'''
	@staticmethod
	def addCmds():
		"""
		Adds commands to a list (NAOCommand.lst) and returns that list
		"""
		
		# load modules dynamicaly
		dirs = ["commands/usrcommands"]				# list of dirs to search for modules
		for d in dirs:
			logging.info( "searching for modules in %s", d )
		
			# get files in dir
			for f in os.listdir(d):
				modulePath = d.replace("/", ".") + "."
				
				# import module
				if f.endswith(".py") and not f.startswith("__") and not f.startswith("_"):
					moduleName = modulePath + f.replace(".py", "")
					module = __import__( moduleName, globals(), locals(), ['object'], -1 )
				
					# get classes from module
					for name, cls in inspect.getmembers( module, inspect.isclass ):
						if modulePath in cls.__module__:
						
							try:
							
								# check if class is command class
								obj = cls()
								if getattr( obj, 'cmd', None ):
									NAOCommand.lst.append( obj )	# add to command list
									logging.debug( "imported %s", cls )
									
							except Exception, e:
								logging.error( "cannot import %s\n%s", cls, e )


	'''
	------------------------------------------------------
	'''
	
	@staticmethod
	def resolveCmd(data, server):
		"""
		Resolves command.
		Command name will be used to resolve from command class argument cmd.
		Optional arguments will be passed to command class execution.
		Command will be started as new thread.
		:param data:	List of command data: [ [command, [arg1, arg2] ]
		:param server:	NAOServer object that received the data. Can be used to send data back
		:return:		True if command was found and executed successful, false othwerwise
		"""
		'''
		Resolves recieved data in form of [ command, [argument1, argument2, ...] ]
		'''
		
		# go through commands list ans search for command
		for cmd in NAOCommand.lst:
			if str(cmd.cmd) == data['command']:
				start_new_thread( cmd.exe, (data['commandArguments'], server) )
				return True
		
		logging.warning( "could not find command %s", str(data) )
		return False

