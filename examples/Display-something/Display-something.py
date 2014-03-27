# -*- coding: utf-8 -*-

"""

	A simple example. One car drives in (irrelevant).
	The task ends when the user clicks the car.
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
	img = CommandableImageSprite( screen, OFF_LEFT, imagepath, scale=IMAGE_SCALE)
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# Draw a single animation in if you want!
	Q.append(obj=img, action='wait', duration=1.0)
	Q.append(obj=img, action='move', pos=spot.center, duration=0.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(img) # Draw and update in this order
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		if( time() - start_time > MAX_DISPLAY_TIME): 
			break
		
		# If the event is a click:
		if is_click(event):
			break
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),
kstimulus("feature_cars/car1_red_circles.png") , 
kstimulus("feature_cars/car1_red_stars.png"),
 kstimulus("feature_cars/car2_blue_circles.png"),
 kstimulus("glitch-npcs/regular/npc_salmon.png"),
 kstimulus("glitch-npcs/regular/npc_jabba.png"),
kstimulus("glitch-npcs/regular/npc_myopic_frog.png"),
kstimulus("glitch-npcs/regular/npc_piggy.png")]
# present a number of blocks

shuffle(target_images)
for i in range(10):
	targetidx = randint(0,len(target_images)-1)
		
	present_trial(target_images[targetidx])
	print i, targetidx, filename(target_images[targetidx])

