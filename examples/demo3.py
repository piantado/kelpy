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
from kelpy.EventHandler import *

IMAGE_SCALE = 0.25


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
## These lines set up a spot to hide things. When we want to not diplay something, we will
## move it to these spots, off the screen.
OFF_LEFT = (-300, WINDOW_HEIGHT/2)
OFF_RIGHT = (1100, WINDOW_HEIGHT/2)

## Also when we want to display something on screen, they will be sent to these points.
ON_LEFT = (WINDOW_WIDTH/2-HOFFSET, WINDOW_HEIGHT/2)
ON_RIGHT = (WINDOW_WIDTH/2+HOFFSET, WINDOW_HEIGHT/2)

onscreen_positions = [ON_LEFT, ON_RIGHT]
offscreen_positions = [OFF_LEFT, OFF_RIGHT]

##############################################
## We create a string to hold the filepath to the sound that will play 
## when the 'correct' option is clicked.
## NOTE that when picking our stimuli we use the 'kstimulus' function from the Miscellaneous class.
##	this method is used to keep all paths relative, even if the kelpy script you write is placed somewhere else (outside of this examples folder).
sound_yup_path = kstimulus('sounds/Affirmative.wav')
sound_nope_path = kstimulus('sounds/Error3.wav')

##############################################
#This is the function we will eventually use to run the trial.
## It requires an array of image paths to be passed to it.

def present_trial(car_paths, animal_paths):
		
		## First we set up the elements of the trial.
		## The images we will be using are set up like so...
	
	## We pick two random images from the list.
	pick1 = randint(0, len(car_paths)-1)
	pick2 = randint(0, len(animal_paths)-1)
	
	## Create two CommandableImageSprite objects with those two images.
	## One is off to the left, one is off to the right.
	## We start by first making an empty array to hold the objects.
	
	img = [None] * 2
	
	## We shuffle out offscreen values and assign one of them to each image.
	## This will make them appear to come from random directions when they come on screen.
	shuffle(offscreen_positions)
	
	## We then create our kelpy CommandableImageSprite objects.
	## These are initialized by passing the object it's screen (to be diplayed on, the start position, the image path, and the scale of the object.
	img[0] = CommandableImageSprite( screen, offscreen_positions[0], car_paths[pick1], scale=IMAGE_SCALE)
	img[1] = CommandableImageSprite( screen, offscreen_positions[1], animal_paths[pick2], scale=IMAGE_SCALE)
	
	## We then designate which image is going to be the correct one.
	## To accomplish this we just store a reference to one of the objects in the variable 'correct'.
	## for this demo we are always going to pick the animal as the correct image.
	correct = img[1]
	
	## This is our instance variable to print whether the user picked the right object during the trial.
	pickedCorrectly = None
	
	## This line sets up the display queue, which is our list of things to happen.
	Q = DisplayQueue()
	
	## These next lines are a script of what is to happen in the experiment.
	## We move the two objects in from their start positions offscreen.
	## They are moved to a shuffled position from the onscreen_positions array.
	## We shuffle the array to randomize the positions.
	shuffle(onscreen_positions)
	Q.append(obj=img[0], action='move', pos= onscreen_positions[0], duration=1.5)
	Q.append(obj=img[1], action='move', pos= onscreen_positions[1], duration=1.5)
		
	# We store the order that we will draw and update things in this variable 'dos'
	dos = OrderedUpdates(*img) 
	
	## And we take a note of the time that the trial starts with this line.
	## Calling the time() method from the python time library.
	start_time = time()
	
	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos):
		
		# If the event is a click:
		if isClick(event):
			# check if each of our images was clicked.
			## We use the function wasClicked from the kelpy EventHandler library to return which item was clicked.
			who = wasClicked(dos)
			if who is correct:
	## if the image that was clicked is the 'correct' one, play a sound and print true. 
				play_sound(sound_yup_path, wait=True, volume=7.0)
				print True
			else:
			## otherwise print the fail sound and print false.
				play_sound(sound_nope_path, wait=True, volume=7.0)
				print False
			break

# Set up images:
car_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png"), kstimulus('feature_cars/car3_blue_circles.png'), kstimulus('feature_cars/car4_red_circles.png')]
animal_images = [kstimulus('animals/giraffe.png'), kstimulus('animals/zebra.png')]
# present a number of blocks
for block in range(10):

	
	# Randomize the order
	shuffle(car_images)
	shuffle(animal_images)
	
	
	print block, present_trial(car_images, animal_images)


##run()
	
	
		
		
		