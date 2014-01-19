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

display_spots = [spot.topq1, spot.topq2, spot.topq3, spot.topq4 ]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

## This demo uses two special classes that inherit from the CommandableImageSprite class and the Dragable class.
## They are the DragSprite and DropSprite classes, which are available from the line " from kelpy.DragDrop import * "
## These classes allow dragging and dropping. They will throw events when these actions happen, which are then picked up in the event loop.

def present_trial(image1, image2, image3, theblicket):
	"""
		This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	#####
	## First we create all of our objects, a bunch of DragSprites and a DropSprite.
	
	## one of our sprites has been designated as the Blicket, it will always be the last filepath passed into the function.
	## This should make it easier when I (or you) implement a csv reader to input the stimuli later.
	
	## The positions are randomized before the trial starts, so they are not always in the same place.
	## NOTE: Right now, this version does not have a demonstration of the blicket.
	thing1 = DragSprite( screen, display_spots[0], image1, scale=IMAGE_SCALE )
	thing2 = DragSprite( screen, display_spots[1], image2, scale=IMAGE_SCALE )
	thing3 = DragSprite( screen, display_spots[2], image3, scale=IMAGE_SCALE )
	blicket = DragSprite(screen, display_spots[3], theblicket, scale=IMAGE_SCALE ) 
	blicket_detector = DropSprite( screen,  BLICKET_DETECTOR_POSITION, blicketd_image_path, scale = .5)
	
	## then we stick those in a list so we can add them to the ordered update list and have them appear on the screen.
	things = [thing1, thing2, thing3, blicket, blicket_detector]
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	# A queue of animation operations
	Q = DisplayQueue()
	
	############################
	## Register the drop zone in each sprite's list of Drop Zones. 
	###	If the sprite is dropped onto this zone, it will send out a ZONE_EVENT into the event loop. We can then pick this event up using some handy functions in the EventHandler class.
	for i in xrange(4):
		things[i].register_drop_zone(blicket_detector)	
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(*things) # Draw and update in this order
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		#################################33
		##This next line is all you need to make your drag sprites dragable!
		## This version uses a loop to check over all the dragable items in the things list.
		for i in xrange(4):
			things[i].process_dragndrop(event)
		
		######
		## Then we use the next two functions to check if a Zone_Event signals that we have dropped onto a drop zone (so something would need to happen!)
		##
		if was_dropped_into_zone(event):
			#########
			## Check who was dropped, whether it was the thing we wanted (which it undoubtedly will be in this example...)
			if who_was_dropped(event) is blicket:
				## Then play a sound! Huzzah!
				play_sound( kstimulus('sounds/Bing.wav') )
			else:
				play_sound( kstimulus('sounds/Bad_Pick.wav') )
			
			## check out the position of the dragging by decommenting the following line:
			# print drag.position(), drag.get_bottom(), drag.get_right(), drag.get_left(), drag.get_top()

###################
###NOTE: Right now if multiple DragSprites are on top of each other, they all get clicked and dragged. This is not ideal, and a way to only click the one on top should be implemented.
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:


# present a number of blocks
for i in range(1):
	shuffle(display_spots)
	present_trial(kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png") , kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png"))
	## print some data at the end.
	print i, targetidx, filename(target_images[targetidx])

