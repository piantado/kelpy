# -*- coding: utf-8 -*-

"""
A simple utility for picking out spots on a screen. Running this program will display a gridded, but otherwise blank canvas.
The will print the coordinates to the console when the user clicks anywhere on the canvas. Voila!

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

### If there have been no arguments passed to this program from the command line, start at 800,600
if len(sys.argv) == 1:
	screen, spot = initialize_kelpy( dimensions=(800,600) )
else: ## Else we are assuming this has been given two arguments, the length and height.
	## So we set up using those dimensions. They have to be cast to integers.
	## Just for fun, note the arguments list is length 3 at this point, 0 is the program name.

	## Set up using the dimensions from the arguments list.
	screen, spot = initialize_kelpy( dimensions=(int(sys.argv[1]),int(sys.argv[2])) )

OFF_LEFT = (spot.west)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

def present_trial():
	"""
	This is the main function used to run this demo. It is fed an imagepath and uses this to create a CommandableImageSprite offscreen. This Sprite is later moved onto the screen, where it hangs out until it is clicked.

	"""
	## Images here are commandable sprites, so we can tell them what to do using Q below
	## We don't actually need this sprite, but I've left it in just so the event loop has something to loop over.
		
	array_length = screen.get_width()/20
	lines_width = [None] * (array_length)
	
	


	start_time = time()
	line = pygame.draw.line(screen, (0,0,0), ( spot.center),(screen.get_height(), screen.get_width()), 5)
	

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	# A queue of animation operations
	Q = DisplayQueue()

	dos = OrderedUpdates() # Draw and update in this order

	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		index = 0
		#numlines= 0
		
		
		if event.type is pygame.MOUSEBUTTONUP:
			print event.pos

		
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main experiment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# Set up images:


# present a number of blocks
for i in range(1):
	present_trial()
	
