# -*- coding: utf-8 -*-

"""

	A simple example. A car appears, and the user may drag it around the screen.
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
IMAGE_SCALE = 0.25

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(800,600) )

spot = Spots(screen)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(imagepath):
	"""
	This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	## This image is a DragSprite, a dragable version of the CommandableImageSprite. It accept similar parameters.
	img = DragSprite( screen, spot.west, imagepath, scale=IMAGE_SCALE)
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
		
	# Draw a single animation in if you want!
	Q.append(obj=img, action='wait', duration=1.0)
	Q.append(obj=img, action='move', pos=(screen.get_width()/2, screen.get_height()/2), duration=0.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(img) # Draw and update in this order
	
	## Note the time...
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		## This is all you have to do to allow dragging!!
		
		img.process_dragndrop(event)
		
		## check out the position of the dragging by decommenting the following line:
		# print arr.position(), arr.get_bottom(), arr.get_right(), arr.get_left(), arr.get_top()
		
		

	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png"), kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png")]

targetidx = randint(0,len(target_images)-1)

present_trial(target_images[targetidx])

print i, targetidx, filename(target_images[targetidx])

