from thread import start_new_thread
from settings.Settings import Settings
import logging
import os
import sys
import inspect
import shutil

class NAOCommand(object):
	"""
	Main command class
	"""
	lst = []
	
	@staticmethod
	def __cleanTmp():
		if os.path.exists("tmp"):
			shutil.rmtree("tmp")
		os.mkdir("tmp")
		f = open("tmp/__init__.py", 'w')
		f.close()
	

	@staticmethod
	def __getUserModulesPaths():
		dirs = []
		for d in Settings.customModulesPath.split(","):
			# check if path endswith /
			if d.endswith("/"):
				d = "".join( d.rsplit("/", 1) )
				
			# check if path exists and is directory:
			if not os.path.exists(d) or not os.path.isdir(d):
				logging.warning( "%s is not a valid directory", d )
				continue
			
			# check if __init__.py is in path
			if not os.path.exists( d + "/__init__.py" ):
				logging.warning( "%s is missing __init__.py", d )
				continue
			
			# copy files to tmp
			packageName = d.rsplit("/")[-1]
			shutil.copytree( d, "tmp/" + packageName )
			
			# add new path to dirs list
			dirs.append( "tmp/" + packageName )
		
		return dirs
			
			
	@staticmethod
	def addCmds():
		"""
		Adds commands to a list (NAOCommand.lst) and returns that list
		"""		
		# clean tmp
		NAOCommand.__cleanTmp()
		
		# get dirs of modules
		dirs = ["commands/usrcommands"]				# list of dirs to search for modules
		dirs = dirs + NAOCommand.__getUserModulesPaths()
	
		# load modules dynamicaly
		for d in dirs:
			logging.info( "searching for modules in %s", d )			
			if not os.path.exists(d) or not os.path.isdir(d):
				logging.warning( "%s is not a valid directory", d )
			else:
			
				# create module path for import
				modulePath = d.replace("/", ".") + "."
			
				# get files in dir		
				for f in os.listdir(d):
				
					# import module
					if f.endswith(".py") and not f.startswith("__") and not f.startswith("_"):
						moduleName = modulePath + f.replace(".py", "")
						module = __import__( moduleName, globals(), locals(), ['object'], -1 )
				
						# get classes from module
						for name, cls in inspect.getmembers( module, inspect.isclass ):
							if modulePath in cls.__module__:
						
								try:
							
									# try to create object from class
									nClassArgs = len( inspect.getargspec( cls.__init__ )[0] )
									if nClassArgs == 2:
										obj = cls(Settings)
									elif nClassArgs == 3:
										obj = cls(Settings, None)
									else:
										obj = cls()
								
									# check if class is command class
									if getattr( obj, 'cmd', None ):
										NAOCommand.lst.append( obj )	# add to command list
										logging.debug( "imported %s", cls )
									
								except Exception, e:
									logging.error( "cannot import %s\n%s", cls, e )
									
	@staticmethod
	def startDefaultModules(session):
		"""
		Starts the modules marked as default
		"""
		logging.info( "loading default modules" )
		for cmd in NAOCommand.lst:
			if getattr( cmd, 'default', None ):
				NAOCommand.resolveCmd( { 'command': cmd.cmd, 'commandArguments': [] }, None, session )

	
	@staticmethod
	def resolveCmd(data, server, session):
		"""
		Resolves command.
		Command name will be used to resolve from command class argument cmd.
		Optional arguments will be passed to command class execution.
		Command will be started as new thread.
		:param data:	List of command data: { 'command': COMMAND, 'commandArguments': [arg1, arg2] ]
		:param server:	NAOServer object that received the data. Can be used to send data back
		:param session:	Session object for getting robot services
		:return:		True if command was found and executed successful, false othwerwise
		"""
		'''
		Resolves recieved data in form of [ command, [argument1, argument2, ...] ]
		'''
		
		# go through commands list ans search for command
		for cmd in NAOCommand.lst:
			if str(cmd.cmd) == data['command']:
				
				# check if session is needed
				nFuncArgs = len( inspect.getargspec( cmd.exe )[0] )
				args = ()
				if nFuncArgs == 5:
					args = (data['commandArguments'], server, session, Settings)
				elif nFuncArgs == 4:
					args = (data['commandArguments'], server, session)
				elif nFuncArgs == 3:
					args = (data['commandArguments'], server)
				elif nFuncArgs == 2:
					args = (data['commandArguments'])

				# check if module has function to set command reference
				func = getattr( cmd, "setResolveCommandFunction", None )
				print func
				if callable(func):
					try:
						cmd.setResolveCommandFunction( NAOCommand.resolveCmd )
					except:
						logging.warning( "Was not able to set resolve command function on module %s", cmd )

				return start_new_thread( cmd.exe, args )
		
		logging.warning( "could not find command %s", str(data) )
		return False

