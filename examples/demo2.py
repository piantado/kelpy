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

IMAGE_SCALE = 0.25
HOFFSET = 100
VOFFSET = 100

##############################################
## Set up pygame

screen = initialize_kelpy( dimensions=(800,600) )
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

OFF_LEFT = (-300, WINDOW_HEIGHT/2)
background_color = (140, 140, 140) # 90 # 190

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial(images, correct):
	
	assert len(images) == 4, "*** ERROR! DID NOT SUPPLY 4 IMAGES: " + str(images)
	
	img = [None] * 4
	
	## set the image locations
	## Images here are commandable sprites, so we can tell them what to do using Q below
	img[0] = CommandableImageSprite( screen, OFF_LEFT, images[0], scale=IMAGE_SCALE)
	img[1] = CommandableImageSprite( screen, (WINDOW_WIDTH/2-HOFFSET, WINDOW_HEIGHT/2+VOFFSET), images[1], scale=IMAGE_SCALE)
	img[2] = CommandableImageSprite( screen, (WINDOW_WIDTH/2+HOFFSET, WINDOW_HEIGHT/2-VOFFSET), images[2], scale=IMAGE_SCALE)
	img[3] = CommandableImageSprite( screen, (WINDOW_WIDTH/2+HOFFSET, WINDOW_HEIGHT/2+VOFFSET), images[3], scale=IMAGE_SCALE)
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# A queue of animation operations
	Q = DisplayQueue()
	
	# Draw a single animation in if you want!
	Q.append(obj=img[0], action='move', pos=(WINDOW_WIDTH/2-HOFFSET, WINDOW_HEIGHT/2-VOFFSET), duration=3.0)
	
	# What order do we draw sprites and things in?
	dos = OrderedUpdates(*img) # Draw and update in this order
	
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kely_standard_event_loop(screen, Q, dos):
		
		# If the event is a click:
		if (  event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
			
			# check if each of our images was clicked
			for x in range(len(img)):
				if img[x].click_inside(pygame.mouse.get_pos()):
					
					# Make whoever is clicked move into the middle
					Q.append(obj=img[x], action='move', pos=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), duration=1.0)
					
					#if images[x] == correct: 
						#return (time()-start_time)
					
	
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
	
	print block, targetidx, target_images[targetidx], present_trial(target_images, target_images[targetidx])


run()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
