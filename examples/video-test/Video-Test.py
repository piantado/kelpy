# -*- coding: utf-8 -*-

"""
	This is the video test demo from the kelpy library. We make use of an earlier demo to show how to use the video recording function in this library.
	The way the video recording works is a little complicated, but can be scripted to be run somewhat easily.

	Other than the video recording function, this demo is unchanged.
	Keep in mind this is the *exact same demo* as the normal 'blicket detector' except for one thing below.\/ \/ \/
	The thing is marked somewhat clearly
	
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
############################################################################
import kelpy.ScreenVideoRecorder  ###################THIS THING! <<<---------- <<<------------ 
###### To make the recording function work, you simply import the library . 
##### by importing the kelpy.ScreenVideoRecorder you tell that program to screen grab every frame.
#### This will make a folder full of bitmaps in the directory with your script.
### You then have to run the ScreenVideoRecorder.py on it's own in that folder's parent directory and point it to the folder with an argument
## filled with bitmaps. It will compile all the stuff into an avi.
#
##Or alternatively, you can run your experiment with the run-kelpy.py script
#### this will automatically pick out the latest folder and run the video compiler after the experiment has finished.
#####
######
#######
########
#########					only old stuff after this!
###########################################################################

IMAGE_SCALE = 0.15

screen, spots = initialize_kelpy( dimensions=(800,600) )

## The blicket detector will be positioned slightly below the center spot.
BLICKET_DETECTOR_POSITION = (spots.center[0], spots.center[1] + 100) 
## and we set the blicket_detector's image path
blicketd_image_path = (kstimulus('feature_tvs/screen_inactive.png'))

## this array holds all of our possible spots to place the possible blickets...
display_spots = [spots.a1, spots.a2, spots.a3, spots.a4 ]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	


def present_trial(image1, image2, image3, theblicket):
	
	thing1 = DragSprite( screen, display_spots[0], image1, scale=IMAGE_SCALE )
	thing2 = DragSprite( screen, display_spots[1], image2, scale=IMAGE_SCALE )
	thing3 = DragSprite( screen, display_spots[2], image3, scale=IMAGE_SCALE )
	blicket = DragSprite(screen, display_spots[3], theblicket, scale=IMAGE_SCALE ) 
	blicket_detector = DropSprite( screen,  BLICKET_DETECTOR_POSITION, blicketd_image_path, scale = .5)
	
	## then we stick those in a list so we can add them to the ordered update list and have them appear on the screen.
	things =  [thing1, thing2, thing3, blicket, blicket_detector]
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
	start_time = time()
	
	##These functions are used to blink the blicket detector on or off, two different versions depending on whether the subject gets the right object or not.
	
	def blink_detector_off():	
		Q.append(obj=blicket_detector, action='swap', image=kstimulus('feature_tvs/screen_inactive.png'), start_time=0, rotation=0, scale=.5, brightness=1.0)
	def blink_detector_right():
		Q.append(obj=blicket_detector, action='swap', image=kstimulus('feature_tvs/screen_active_star.png'), rotation=0, scale=.499999999, brightness=1.0)
		Q.append(obj=blicket_detector, action='wait', duration=1.0 )
		blink_detector_off()
	def blink_detector_wrong():
		Q.append(obj=blicket_detector, action='swap', image=kstimulus('feature_tvs/screen_active.png'), rotation=0, scale=.5, brightness=1.0)
		Q.append(obj=blicket_detector, action='wait', duration=.4 )
		blink_detector_off()
		
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		for thing in reversed(things):
			if thing.process_dragndrop(event):
				bring_clicked_to_top(thing, things, dos)
				break
		
		## To make the DragSprites dragable, we use a loop to check over all the dragable items in the things list.
		#for thing in reversed(things) :
			### all the is required to run the process_dragndrop function during each eventloop cycle.
			#if thing.process_dragndrop(event):
				#things[thing]
				#break
		
		######
		## Then we use the next two functions to check if a Zone_Event signals that we have dropped onto a drop zone (so something would need to happen!)
		##
		if was_dropped_into_zone(event):
			#########
			## Check who was dropped, whether it was the thing we wanted (which it undoubtedly will be in this example...)
			who = who_was_dropped(event)
			if who is blicket:
				## Then play a sound! Huzzah!
				play_sound( kstimulus('sounds/Bing.wav'), wait=False )
				blink_detector_right()
				print True, time() - start_time, filename(theblicket)
			else:
				## You have failed to detect the blicket, therefore you get a red blinky light and a buzzer noise.
				blink_detector_wrong()
				play_sound( kstimulus('sounds/Bad_Pick.wav'), wait=False)
				print False, time() - start_time, filename(who.image_path)
			
			## check out the position of the dragging by decommenting the following line:
			# print drag.position(), drag.get_bottom(), drag.get_right(), drag.get_left(), drag.get_top()

###################
###
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
## Present the trial (shuffle the display spots, also)
shuffle(display_spots)
present_trial(kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png") , kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png"))

	

