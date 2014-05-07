# -*- coding: utf-8 -*-

"""

	Eyetracker Demo 2
	This is a demo that makes use of registered look zones to make some events happen.
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
from kelpy.tobii.TobiiSprite import *

IMAGE_SCALE = 0.25
MAX_DISPLAY_TIME = 5.0

##############################################
## Set up pygame

screen, spot = initialize_kelpy( dimensions=(800,600) )


OFF_LEFT = (spot.west)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(imagepath):
	"""
	This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	## Images here are commandable sprites, so we can tell them what to do using Q below
	tobii_sim = TobiiSimController(screen)
	img = TobiiSprite( screen, spot.center, imagepath, tobii_sim, scale=IMAGE_SCALE)
	
	drum = DropSprite(screen, (609,407), kstimulus("common_objects/drum.png"), scale=IMAGE_SCALE)

	img.register_drag_zone(drum)

	images = [img, drum]

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# Draw a single animation in if you want!
	Q.append(obj=img, action='wait', duration=1.0)
	Q.append(obj=img, action='move', pos=spot.center, duration=0.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(images) # Draw and update in this order
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		img.is_following =  img.is_looked_at()
		img.process_follow(event)

		if was_dropped_into_zone(event):
			print "Working somewhat!"
			play_sound(kstimulus("sounds/Button-Reverb.wav"))

		if( time() - start_time > MAX_DISPLAY_TIME): 
			pass
		
		# If the event is a click:
		if is_click(event):
			pass
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	



# present a number of blocks



present_trial(kstimulus("common_objects/glitch_misc/beam.png"))
		
