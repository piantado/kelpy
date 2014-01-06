# -*- coding: utf-8 -*-

"""

	A simple example. One car drives in (irrelevant)
	Users must click until they get the "right" car. For simplicity, there is no cue to "right"
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

screen = initialize_kelpy( dimensions=(800,600) )
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

OFF_LEFT = (-300, WINDOW_HEIGHT/2)
background_color = (140, 140, 140) # 90 # 190

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(imagepath):
	
	## Images here are commandable sprites, so we can tell them what to do using Q below
	img = CommandableImageSprite( screen, OFF_LEFT, imagepath, scale=IMAGE_SCALE)
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# Draw a single animation in if you want!
	Q.append(obj=img, action='wait', duration=1.0)
	Q.append(obj=img, action='move', pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), duration=0.0)
	
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
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png") , kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png")]

# present a number of blocks
for i in range(10):
	
	targetidx = randint(0,len(target_images)-1)
	
	present_trial(target_images[targetidx])
	
	print i, targetidx, filename(target_images[targetidx])


run()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
