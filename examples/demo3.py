# -*- coding: utf-8 -*-

"""

	A simple example. Two animals are displayed, one is the 'correct' one.
	If the correct one is clicked, one event happens (sound playing).
	If the other is clicked, an alternate sound is played.
	The trial number and result (picked correctly true or false) is printed to the console.
	
	
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

MAX_DISPLAY_TIME = 5.0

IMAGE_SCALE = 0.25
HOFFSET = 200
VOFFSET = 100

##############################################
## Set up pygame
## this is the initialization line, to set up a screen that we will diplay things on.
screen = initialize_kelpy( dimensions=(800,600) )

##############################################
## This line fetches the size of the screen (the one we just created) and assigns 
## the values to some constants that we can refer to later.
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

##############################################
## This line sets up a spot to hide things. When we want to not diplay something, we will
## move it to this spot, off the screen.
OFF_LEFT = (-300, WINDOW_HEIGHT/2)
OFF_RIGHT = (1100, WINDOW_HEIGHT/2)

##############################################
## We create a string to hold the filepath to the sound that will play 
## when the 'correct' option is clicked.
sound_yup_path = '../kelpy/stimuli/sounds/Affirmative.wav'
sound_nope_path = '../kelpy/stimuli/sounds/Error3.wav'

##############################################
## and then this line sets the background color.
#background_color = (140, 140, 140) # 90 # 190

#This is the function we will eventually use to run the trial.
## It requires an array of image paths to be passed to it.

def present_trial(imagepaths):
		
		## First we set up the elements of the trial.
		## The images we will be using are set up like so...
	
	## We pick two random images from the list.
	pick1 = randint(0, len(imagepaths)-1)
	pick2 = randint(0, len(imagepaths)-1)
	
	## Create two CommandableImageSprite objects with those two images.
	## One is off to the left, one is off to the right.
	## We start by first making an empty array to hold the objects.
	
	img = [None] * 2
	img[0] = CommandableImageSprite( screen, OFF_LEFT, imagepaths[pick1], scale=IMAGE_SCALE)
	img[1] = CommandableImageSprite( screen, OFF_RIGHT, imagepaths[pick2], scale=IMAGE_SCALE)
	
	## We then set one to randomly be the 'correct' one. 
	## To accomplish this we just store a reference to one of the objects in the variable 'correct'.
	correct = img[randint(0,1)]
	
	## This is our instance variable to print whether the user picked the right object during the trial.
	pickedCorrectly = None
	
	## This line sets up the display queue, which is our list of things to happen.
	Q = DisplayQueue()
	
	## These next lines are a script of what is to happen in the experiment.
	## We move the two objects in from their start positions offscreen.
	Q.append(obj=img[0], action='move', pos=(WINDOW_WIDTH/2-HOFFSET, WINDOW_HEIGHT/2), duration=1.5)
	Q.append(obj=img[1], action='move', pos=(WINDOW_WIDTH/2+HOFFSET, WINDOW_HEIGHT/2), duration=1.5)
		
	# We store the order that we will draw and update things in this variable 'dos'
	dos = OrderedUpdates(*img) 
	
	## And we take a note of the time that the trial starts with this line.
	## Calling the time() method from the python time library.
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos):
		
		# If the event is a click:
		if (  event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
			
			# check if each of our images was clicked
			for x in range(len(img)):
				if img[x].click_inside(pygame.mouse.get_pos()):
					
					## Waggle the one that was clicked. TODO get this to work! Doesn't right now.
					Q.append(obj=img[x], action='waggle', amount=360, period=1, finish=True)
				
				## if the image that was clicked is the 'correct' one, play a sound and print true.
					if img[x] is correct: 
							play_sound(sound_yup_path, wait=True, volume=7.0)
							print True
					else:
						## otherwise print the fail sound and print false.
							play_sound(sound_nope_path, wait=True, volume=7.0)
							print False
			break

# Set up images:
target_images = [kstimulus("animals/giraffe.png"),kstimulus("animals/zebra.png"), kstimulus('people/girl1.png')]

# present a number of blocks
for block in range(10):

	
	# Randomize the order
	shuffle(target_images)
	
	print block, present_trial(target_images)


##run()
	
	
		
		
		