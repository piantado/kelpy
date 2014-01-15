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
from kelpy.Dragable import *

IMAGE_SCALE = 0.25

MAX_DISPLAY_TIME = 5.0

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(800,600) )

OFF_LEFT = (-300, screen.get_height()/2)

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
	
	# Create a new Arrangeable
	arr = Dragable()
	arr.set_x(screen.get_width()/2)
	arr.set_y(screen.get_height()/2)
	arr.set_height(150)
	arr.set_width(200)
	arr.enable_dragging()
	
	print arr.position(), arr.get_bottom(), arr.get_right(), arr.get_left(), arr.get_top()
	
	# Draw a single animation in if you want!
	Q.append(obj=img, action='wait', duration=1.0)
	Q.append(obj=img, action='move', pos=(screen.get_width()/2, screen.get_height()/2), duration=0.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(img) # Draw and update in this order
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		## in this case we pull some trickery by calling the process_dragndrop function in a boolean statement.
		## while it also processes the dragging and dropping of the dragable object, it also returns true and false to start and end the drag and drog process.
		if arr.process_dragndrop(event):
			## if we're in a drag and drop sequence, we (in this case) set the images position to match the position of the dragable area (which we're moving).
			Q.append(obj=img, action='move', pos=(arr.get_x(), arr.get_y()), duration=0.0)
		
		## check out the position of the dragging by decommenting the following line:
		# print arr.position(), arr.get_bottom(), arr.get_right(), arr.get_left(), arr.get_top()
		
		

	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png") , kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png")]

# present a number of blocks
for i in range(1):
	
	targetidx = randint(0,len(target_images)-1)
	
	present_trial(target_images[targetidx])
	
	print i, targetidx, filename(target_images[targetidx])

