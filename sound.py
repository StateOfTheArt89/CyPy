from pybass.pybass import *

def playSound(filename):
	Sound(filename).play()

class Sound(object):

	def __init__(self, filename, loop=False):
		self.handle = BASS_StreamCreateFile(False, filename, 0, 0, BASS_SAMPLE_LOOP if loop else 0 )
		if self.handle == 0:
			print "BASS_StreamCreateFile error", get_error_description(BASS_ErrorGetCode())
	
	def play(self):
		if not BASS_ChannelPlay(self.handle, False):
			print 'BASS_ChannelPlay error', get_error_description(BASS_ErrorGetCode())

	def pause(self):
		if self.handle == 0:
			return
		BASS_ChannelPause(self.handle)

	def stop(self):
		if self.handle == 0:
			return
		BASS_ChannelStop(self.handle)