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
		NAOCommand.lst.append( cmdInfo.cmdInfo() )
		NAOCommand.lst.append( cmdSay.cmdSay() )
		NAOCommand.lst.append( cmdHallo.cmdHallo() )
		NAOCommand.lst.append( cmdStandUp.cmdStandUp() )
		NAOCommand.lst.append( cmdSitDown.cmdSitDown() )
		NAOCommand.lst.append( cmdVelocityWalk.cmdVelocityWalk() )
		NAOCommand.lst.append( cmdWipeFHead.cmdWipeFHead() )
		NAOCommand.lst.append( cmdThaiChi.cmdThaiChi() )
		NAOCommand.lst.append( cmdRedBallTracker.cmdRedBallTracker() )
		NAOCommand.lst.append( cmdChangeLang.cmdChangelang() )
		NAOCommand.lst.append( cmdFaceTracker.cmdFaceTracker() )
		NAOCommand.lst.append( cmdShakeHands.cmdShakeHands() )
		NAOCommand.lst.append( cmdGangnamStyle.cmdGangnamStyle() )
		NAOCommand.lst.append( cmdCaravanPalace.cmdCaravanPalace() )
		NAOCommand.lst.append( cmdEvolutionDance.cmdEvolutionDance() )
		NAOCommand.lst.append( cmdEyesOfTheTiger.cmdEyesOfTheTiger() )
		NAOCommand.lst.append( cmdVangelisDance.cmdVangelisDance() )
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
		# create array from data
		data = str(data)
		data = data.replace('[', '')
		data = data.replace(']', '')
		data = data.replace('\'', '')		
		data = str(data).split(',')
		
		# remove whitespaces
		for i in range( len(data) ):
			data[i] = str(data[i]).strip()
			
		# check if command exsists
		if len(data) == 0:
			return False
		
		# check if to restart server connection
		if data[0] == "dummyStop":
			return "restart"
		
		# go through commands list ans search for command
		ret = False
		for cmd in NAOCommand.lst:
			if str(cmd.cmd) == str(data[0]):
				ret = True
				start_new_thread( cmd.exe, (data, addr) )
		
		if not ret:
			print "could find command", str(data[0])
				
		return True

