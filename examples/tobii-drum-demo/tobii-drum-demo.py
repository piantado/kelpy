# -*- coding: utf-8 -*-

"""

	Eyetracker Demo 2
	This is a demo that makes use of the TobiiSprite's ability to use registered drag and drop zones. 
	It displays a drum and a stick. Look at the stick to pick it up, bang it against the drum to make it play! 

"""

import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *
from kelpy.Dragable import *
from kelpy.DragDrop import *
from kelpy.tobii.TobiiSimController import *
from kelpy.tobii.TobiiController import *
from kelpy.tobii.TobiiSprite import *

IMAGE_SCALE = 0.25
MAX_DISPLAY_TIME = 5.0

##############################################
## Set up pygame

screen, spot = initialize_kelpy( dimensions=(800,600) )


OFF_LEFT = (spot.west)

##############################################
## setup and activate tobii

# this creates a TobiiController that calls the actual Tobii SDK code
#tobii_controller = TobiiController(screen)
tobii_controller = TobiiSimController(screen)

# this searches for the tobii eyetracker that is connected.
# It times out based on the given amount of seconds (the default is 1,000 seconds) and exits this program
tobii_controller.wait_for_find_eyetracker(3)

#set the name of the data file that will output all of the Tobii data
tobii_controller.set_data_file('testdata.tsv')
#activate the first tobii eyetracker that was found
tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(imagepath):
	"""
	This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	## Images here are commandable sprites, so we can tell them what to do using Q below
	#tobii = TobiiSimController(screen)
	
	img = TobiiSprite( screen, spot.center, imagepath, tobii_controller, scale=IMAGE_SCALE)
	img.enable_follow()

	drum = DropSprite(screen, (609,407), kstimulus("common_objects/drum.png"), scale=IMAGE_SCALE)

	img.register_drag_zone(drum)

	images = [drum, img]

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(images) # Draw and update in this order
	
	start_time = time()
	#start tracking
	
	tobii_controller.start_tracking()	
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
	
	# This also turns it off when the sprite it not looked at any longer.
		img.process_follow(event)   ## simple, right?

		if was_dragged_into_zone(event):  ## This is a function located in the EventHandler that watches for drag zone events.
			print "Nice Drumming!"
			play_sound(kstimulus("sounds/Button-Reverb.wav"))

		if event.type == QUIT:
			tobii_controller.close_data_file()
			tobii_controller.destroy()
				
		
	tobii_controller.stop_tracking()
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	



# for this one we only present one block.

present_trial(kstimulus("common_objects/glitch_misc/beam.png"))
		

#make sure the TobiiController has closed the data file and removed itself
tobii_controller.close_data_file()
tobii_controller.destroy()

