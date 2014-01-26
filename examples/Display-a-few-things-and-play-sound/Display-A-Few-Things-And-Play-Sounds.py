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

IMAGE_SCALE = 0.20
HOFFSET = 100
VOFFSET = 100

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(800,600) )

############
## Generate a bunch of spots to place stuff on screen.
spot = Spots(screen)

## Set out offscreen spot...
OFF_LEFT = spot.west
background_color = (140, 140, 140) # 90 # 190

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(images, targetidx):
	
	
	assert len(images) == 4, "*** ERROR! DID NOT SUPPLY 4 IMAGES: " + str(images)
	
	img = [None] * 4
	
	## set the image locations
	## Images here are commandable sprites, so we can tell them what to do using Q below
	img[0] = CommandableImageSprite( screen, OFF_LEFT, images[0], scale=IMAGE_SCALE)
	img[1] = CommandableImageSprite( screen, spot.middleq2, images[1], scale=IMAGE_SCALE)
	img[2] = CommandableImageSprite( screen, spot.topq3, images[2], scale=IMAGE_SCALE)
	img[3] = CommandableImageSprite( screen, spot.middleq3, images[3], scale=IMAGE_SCALE)
	correct = img[targetidx]
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# Draw a single animation in if you want!
	Q.append(obj=img[0], action='move', pos=spot.topq2, duration=3.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(*img) # Draw and update in this order
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos):
		
		# If the event is a click:
		if is_click(event):
			
			# check if each of our images was clicked
			whom = who_was_clicked(dos)
					
			if whom is correct: 
				play_sound(kstimulus('sounds/Beep2.wav'))
				Q.append(obj=whom, action='move', pos=(screen.get_width()/2, screen.get_height()/2), duration=1.0)
				return (time()-start_time)
			if whom is not correct:
				play_sound(kstimulus('sounds/Error.wav'))
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:
target_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png") , kstimulus("feature_cars/car1_red_stars.png"), kstimulus("feature_cars/car2_blue_circles.png")]

# present a number of blocks
for block in range(10):

	
	# Randomize the order
	shuffle(target_images)
	targetidx = randint(0,3)
	
## finally run the thing, also print the block number, the targetidx, and the index of the correct image.
## the last item is the presen_trial function that actually runs the trial.
	print block, targetidx, filename(target_images[targetidx]), present_trial(target_images, targetidx)

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
