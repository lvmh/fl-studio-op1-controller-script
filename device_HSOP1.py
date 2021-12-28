# name=**HS OP-1 CONFIG**
# url=https://github.com/ryrun/FL-OP1-controller-script

import patterns
import channels
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import screen

import midi
import utils

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]
scrollvar = 0
class TGeneric():
	def __init__(self):
		return

	def set_scrollvar_to(self, int):
		global scrollvar    # Needed to modify global copy of globvar]
		scrollvar = int

	def OnInit(self):
		print('init ready')

	def OnDeInit(self):
		print('deinit ready')

	def OnMidiMsg(self, event):
		print ("ITS WORKINGGGG: {:X} {:X} {:2X} {}".format(event.status, event.data1, event.data2,  EventNameT[(event.status - 0x80) // 16] + ': '+  utils.GetNoteName(event.data1)))
		print (event.data1)
		print (event.data2)
		print (scrollvar)
		if event.data2 > 0 and event.data1 != 4:
			# 39 = play button
			if event.data1 == 39:
				print ("HELLO")
				transport.start()
				event.handled = True
			# 40 = stop button
			elif event.data1 == 40:
				transport.stop()
				event.handled = True
			# 38 = record button
			elif event.data1 == 38:
				transport.record()
				event.handled = True
			# 06 = metronome button
			elif event.data1 == 6:
				transport.globalTransport(midi.FPT_Metronome, 1, event.pmeFlags)
				event.handled = True
			# 0A = mixer button = show fl mixer
			elif event.data1 == 10:
				transport.globalTransport(midi.FPT_F9, 1, event.pmeFlags)
				event.handled = True
			# 9 = tape button = show fl playlist
			elif event.data1 == 9:
				transport.globalTransport(midi.FPT_F5, 1, event.pmeFlags)
				event.handled = True
			# 8 = drum button = show fl channel rack
			elif event.data1 == 8:
				transport.globalTransport(midi.FPT_F6, 1, event.pmeFlags)
				event.handled = True
			# 8 = synth button = show fl piano roll
			elif event.data1 == 7:
				transport.globalTransport(midi.FPT_F7, 1, event.pmeFlags)
				event.handled = True
			# 15 = up button = up arrow
			elif event.data1 == 15:
				if ui.getFocused(0) == 1:
					transport.globalTransport(midi.FPT_Left, 1, event.pmeFlags)
				else:
					transport.globalTransport(midi.FPT_Up, 1, event.pmeFlags)
				event.handled = True
			# 16 = down button = down arrow
			elif event.data1 == 16:
				if ui.getFocused(0) == 1:
					transport.globalTransport(midi.FPT_Right, 1, event.pmeFlags)
				else:
					transport.globalTransport(midi.FPT_Down, 1, event.pmeFlags)
				event.handled = True
			# 5 = help button = mute
			elif event.data1 == 5:
				# mixer
				if ui.getFocused(0) == 1:
					mixer.muteTrack(mixer.trackNumber())
				# channels
				elif ui.getFocused(1) == 1:
					channels.muteChannel(channels.channelNumber())
				event.handled = True
			# 67 = clicking red = solo track/channel
			elif event.data1 == 67:
				# mixer
				if ui.getFocused(0) == 1:
					mixer.soloTrack(mixer.trackNumber())
				# channels
				elif ui.getFocused(1) == 1:
					channels.soloChannel(channels.channelNumber())
				event.handled = True

			else:
				event.handled = False
		else:
			# 4 = turning ornage = adjust selected track/channel vol
			if event.data1 == 4:
				counter = 0
				if event.data2 == 127:
					counter = 0.01
				elif event.data2 == 0:
					counter = -0.01
				elif event.data2 > scrollvar:
					counter = 0.01
				else:
					counter = -0.01
				# mixer
				if ui.getFocused(0) == 1:
					mixer.setTrackVolume(mixer.trackNumber(), mixer.getTrackVolume(mixer.trackNumber()) + counter)
				# channels
				elif ui.getFocused(1) == 1:
					channels.setChannelVolume(channels.channelNumber(), channels.getChannelVolume(channels.channelNumber()) + counter)
				event.handled = True

				Generic.set_scrollvar_to(event.data2)

			else:
				event.handled = False

Generic = TGeneric()

def OnInit():
	Generic.OnInit()

def OnDeInit():
	Generic.OnDeInit()

def OnMidiMsg(event):
	Generic.OnMidiMsg(event)
