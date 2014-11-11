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
			
		elif len(args) > 0:
			# say sentence
			tts.post.say( str(args[0]).strip() )