# -*- coding: utf-8 -*-

"""

	A simple example. A car appears, and the user may drag it around the screen.
	
	******** DOES NOT WORK CORRECTLY YET ****************
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

IMAGE_SCALE = 0.15

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(800,600) )
spot = Spots(screen)

BLICKET_DETECTOR_POSITION = (screen.get_width()/2, (screen.get_height()/2 + 100)) 
blicketd_image_path = (kstimulus('feature_tvs/screen_inactive.png'))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(imagepath):
	"""
	This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	## Images here are commandable sprites, so we can tell them what to do using Q below
	
	thing = CommandableImageSprite( screen, spot.topq1, imagepath, scale=IMAGE_SCALE)
	
	blicketd = CommandableImageSprite( screen,  BLICKET_DETECTOR_POSITION, blicketd_image_path, scale = .5)
	
	things = [thing, blicketd]
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	# A queue of animation operations
	Q = DisplayQueue()
	
	
	bd = Arrangeable()
	
	bd.set_x = 400
	bd.set_y = 400
	bd.set_height(200)
	bd.set_width(300)
	
	
	# Create new Dragables
	
	
	drag = Dragable()
	drag.set_x(spot.topq1[0])
	drag.set_y(spot.topq1[1])
	drag.set_height(150)
	drag.set_width(200)
	drag.register_drop_zone(bd)
	drag.enable_dragging()
	
	blicket = drag
	
	#print drag.position(), drag.get_bottom(), drag.get_right(), drag.get_left(), drag.get_top()
	
	# Draw a single animation in if you want!
	#Q.append(obj=img, action='wait', duration=1.0)
	#Q.append(obj=img, action='move', pos=(screen.get_width()/4, screen.get_height()/4), duration=0.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(*things) # Draw and update in this order
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
				## if we're in a drag and drop sequence, we (in this case) set the images position to match the position of the dragable area (which we're moving).
		print event	
		
		
		if drag.process_dragndrop(event):
			Q.append(obj=thing, action='move', pos=(drag.get_x(), drag.get_y()), duration=0.0)
			
		if event.type == ZONE_EVENT and event.motion == 'drop' and event.direction == 'enter':
			#if who is blicket:
			play_sound( kstimulus('sounds/Bing.wav') )
			
			## check out the position of the dragging by decommenting the following line:
			# print drag.position(), drag.get_bottom(), drag.get_right(), drag.get_left(), drag.get_top()
			
		

	
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

