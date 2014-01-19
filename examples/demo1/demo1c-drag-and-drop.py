# -*- coding: utf-8 -*-

"""

	A simple example. A car appears, and the user may drag it around the screen. If it is dragged onto the car detector, it makes a noise.
	
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

IMAGE_SCALE = 0.15

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(800,600) )
spot = Spots(screen)

BLICKET_DETECTOR_POSITION = (spot.middle[0], spot.middle[1] + 100) 
blicketd_image_path = (kstimulus('feature_tvs/screen_inactive.png'))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

## This demo uses two special classes that inherit from the CommandableImageSprite class and the Dragable class.
## They are the DragSprite and DropSprite classes, which are available from the line " from kelpy.DragDrop import * "
## These classes allow dragging and dropping. They will throw events when these actions happen, which are then picked up in the event loop.

def present_trial(imagepath):
	"""
		This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	
	## The two items in this demo are the Thing (our dragable DragSprite) and the blicket_detector, the drop-zone-able DropSprite.
	
	thing = DragSprite( screen, spot.topq1, imagepath, scale=IMAGE_SCALE)
	blicket_detector = DropSprite( screen,  BLICKET_DETECTOR_POSITION, blicketd_image_path, scale = .5)
	
	## then we stick those in a list so we can add them to the ordered update list and have them appear on the screen.
	things = [thing, blicket_detector]
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	# A queue of animation operations
	Q = DisplayQueue()
	
	############################
	## Register the drop zone in the DragSprite's list of Drop Zones. 
	###	If the sprite is dropped onto this zone, it will send out a ZONE_EVENT into the event loop. We can then pick this event up using some handy functions in the EventHandler class.
	thing.register_drop_zone(blicket_detector)	
	
	# Draw a single animation in if you want!
	#Q.append(obj=img, action='wait', duration=1.0)
	#Q.append(obj=img, action='move', pos=(screen.get_width()/4, screen.get_height()/4), duration=0.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(*things) # Draw and update in this order
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		#################################33
		##This next line is all you need to make your drag sprites dragable!
		##
		thing.process_dragndrop(event)
		
		######
		## Then we use the next two functions to check if a Zone_Event signals that we have dropped onto a drop zone (so something would need to happen!)
		##
		if was_dropped_into_zone(event):
			#########
			## Check who was dropped, whether it was the thing we wanted (which it undoubtedly will be in this example...)
			if who_was_dropped(event) is thing:
				## Then play a sound! Huzzah!
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
	
	## pick a random index...
	targetidx = randint(0,len(target_images)-1)
	
	## feed that imagepath to the main function, and run it!
	present_trial(target_images[targetidx])
	
	## print some data at the end.
	print i, targetidx, filename(target_images[targetidx])

