'''
Created on 07.09.2012

@author: hannes
'''
from commands.usrcommands import * 			# @UnusedWildImport
from thread import start_new_thread

class NAOCommand(object):
	'''
	Main command clas
	'''
	lst = []
	
	'''
	------------------------------------------------------
	INSERT NEW NAO COMMANDS HERE
	------------------------------------------------------
	'''
	@staticmethod
	def addCmds():
		'''
		adds commands to a lst and returns that lst
		'''		
		NAOCommand.lst.append( cmdSetSystemVolume.cmdSetSystemVolume() )
		NAOCommand.lst.append( cmdSetPlayerVolume.cmdSetPlayerVolume() )
		NAOCommand.lst.append( cmdSetJointStiffness.cmdSetJointStiffness() )
		
		NAOCommand.lst.append( cmdOpenHand.cmdOpenHand() )
		NAOCommand.lst.append( cmdSetLifeState.cmdSetLifeState() )
		NAOCommand.lst.append( cmdSetNaoName.cmdSetNaoName() )			
		
		NAOCommand.lst.append( cmdSay.cmdSay() )
		NAOCommand.lst.append( cmdStandUp.cmdStandUp() )
		NAOCommand.lst.append( cmdSitDown.cmdSitDown() )
		NAOCommand.lst.append( cmdVelocityWalk.cmdVelocityWalk() )
		NAOCommand.lst.append( cmdChangeLang.cmdChangelang() )
		NAOCommand.lst.append( cmdSetVolume.cmdSetVolume() )
		
		NAOCommand.lst.append( ledAngry.ledAngry() )
		NAOCommand.lst.append( ledBlink.ledBlink() )
		NAOCommand.lst.append( ledCautious.ledCautious() )
		NAOCommand.lst.append( ledCircleEyes.ledCircleEyes() )
		NAOCommand.lst.append( ledDisco.ledDisco() )
		NAOCommand.lst.append( ledFlash.ledFlash() )
		NAOCommand.lst.append( ledHappy.ledHappy() )
		NAOCommand.lst.append( ledLaugh.ledLaugh() )
		NAOCommand.lst.append( ledMischievious.ledMischievious() )
		NAOCommand.lst.append( ledThinking.ledThinking() )


	'''
	------------------------------------------------------
	'''
	
	@staticmethod
	def resolveCmd(data, addr):
		'''
		Resolves recieved data in form of [ command, [argument1, argument2, ...] ]
		'''
		
		# go through commands list ans search for command
		for cmd in NAOCommand.lst:
			if str(cmd.cmd) == data['command']:
				start_new_thread( cmd.exe, (data['commandArguments'], addr) )
				return True
		
		print "could not find command " + str(data)				
		return False

