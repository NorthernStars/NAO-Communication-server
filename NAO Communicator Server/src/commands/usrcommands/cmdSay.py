'''
Created on 08.09.2012

@author: hannes
'''
from naoqi import ALProxy
from settings.Settings import Settings

class cmdSay(object):
	'''
	classdocs
	'''
	
	def __init__(self):
		self.cmd = "SAY"
	
	def exe(self, args=None, addr=None):
		
		# check arguments
		if len(args) != 4:
			return False
		
		# create proxy
		tts = ALProxy('ALTextToSpeech', Settings.naoHostName, Settings.naoPort)
		
		# create sentence
		if len(args) > 2:	
			sentence = "\RSPD="+ str( args[1] ) + "\ "
			sentence += "\VCT="+ str( args[2] ) + "\ "
			sentence += str( args[0])
			sentence +=  "\RST\ "
			
			# say sentence
			tts.post.say( str(sentence) )