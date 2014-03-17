# -*- coding: utf-8 -*-

"""

	A simple example for using tobii with kelpy
"""
import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.tobii.TobiiController import *
from kelpy.tobii.TobiiSprite import *
from kelpy.tobii.TobiiWatcher import *

from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *

IMAGE_SCALE = 0.25

MAX_DISPLAY_TIME = 5.0

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(1024,768) )

spot = Spots(screen)

#CENTER = (screen.get_width()/2, screen.get_height()/2)

tobii_controller = TobiiController(screen)
    
#find tobii
tobii_controller.wait_for_find_eyetracker(3)
tobii_controller.set_data_file('testdata.tsv')
tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])


    
##############################################
## We create a string to hold the filepath to the sound that will play when the 'correct' option is clicked.
sound_yup_path = kstimulus('sounds/Affirmative.wav')  

    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(imagepath):
	"""
	The sprite in this trial will move around the screen based on eye gaze.

	"""
	## This is a TobiiSprite which has activated its Followable state (is_following = True)
	img = TobiiSprite( screen, spot.center, imagepath, tobii_controller, scale=IMAGE_SCALE)
	img.enable_follow();
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# Draw a single animation in if you want!		
	# Q.append(obj=img, action='darken', amount=0.5, duration=4.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(img) # Draw and update in this order
	
	#start tracking
	tobii_controller.start_tracking()
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		#if (img.is_looked_at()):
		#		play_sound(sound_yup_path, wait=True, volume=7.0)
		#		break
		
		if( time() - start_time > MAX_DISPLAY_TIME): 
			break
		
		# If the event is a click:
		if is_click(event):
			break

		if event.type == QUIT:
			tobii_controller.close_data_file()
			tobii_controller.destroy()

		img.process_follow(event)
			
	tobii_controller.stop_tracking()	

	print img.get_look_time()
	duration = time() - start_time 
	print looking_proportions(dos, duration)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png") , kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png")]

# present a number of blocks
for i in range(5):
	
	targetidx = randint(0,len(target_images)-1)
	
	present_trial(target_images[targetidx])
	
	print i, targetidx, filename(target_images[targetidx])

tobii_controller.close_data_file()
tobii_controller.destroy()
