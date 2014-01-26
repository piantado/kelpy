# -*- coding: utf-8 -*-

"""

	A simple example. Two animals are displayed, one is the 'correct' one.
	If the correct one is clicked, one event happens (sound playing).
	If the other is clicked, an alternate sound is played.
	The trial number and result (picked correctly true or false) is printed to the console.
	
	The main method ( present_trial() )accepts two arrays of image paths and follows the format :
	present_trial(imagepath_array1, imagepath_array2)
	
	NOTE: It is recommended that you keep stimuli in the appropriate kelpy/stimuli folder.
	This way you can simply pass the filepath relative to that folder as a string to the kstimulus() function (illustrated below):
	sound_yup_path = kstimulus('sounds/Affirmative.wav')
	This allows your python scripts to live anywhere on your hard drive and still access the stimuli in the kelpy folder.
	
	
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



########################################
##The following are constants that are used to set up the size and arrangement of images later.
##
IMAGE_SCALE = 0.25
HOFFSET = 200
VOFFSET = 100

##############################################
## Set up pygame
## this is the initialization line, to set up a screen that we will diplay things on.
screen = initialize_kelpy( dimensions=(800,600) )

##############################################
## These lines set up a spot to hide things off screen. When we want to not diplay something, we will
## move it to these spots, off the screen.
OFF_LEFT = (-300, screen.get_height()/2)
OFF_RIGHT = (1100, screen.get_height()/2)

## Also when we want to display something on screen, they will be sent to these points.
ON_LEFT = (screen.get_width()/2-HOFFSET, screen.get_height()/2)
ON_RIGHT = (screen.get_width()/2+HOFFSET, screen.get_height()/2)

## Those positions are then stored in arrays so they may be shuffled (randomized).
onscreen_positions = [ON_LEFT, ON_RIGHT]
offscreen_positions = [OFF_LEFT, OFF_RIGHT]

##############################################
## We create a string to hold the filepath to the sound that will play when the 'correct' option is clicked.
sound_yup_path = kstimulus('sounds/Affirmative.wav')
sound_nope_path = kstimulus('sounds/Error3.wav')

###############################################
## Almost finished! We finally set up some arrays to hold the filepaths to the images we will be using.
## We use two different arrays so that one group of them can be designated the 'correct' group.
## In this case the animal group is later designated to be 'correct' within the function.
car_images = [kstimulus("feature_cars/car1_blue_stars.png"),kstimulus("feature_cars/car1_red_circles.png"), kstimulus('feature_cars/car3_blue_circles.png'), kstimulus('feature_cars/car4_red_circles.png')]
animal_images = [kstimulus('animals/giraffe.png'), kstimulus('animals/zebra.png')]


##############################################
#This is the function we will eventually use to run the trial.
## It requires two arrays of image filepaths be passed to it.

def present_trial(car_paths, animal_paths):
	"""
		This is our main method that we use to run this trial. It accepts two string arrays as it's parameters.
		car_paths 
		animal_paths 
		
		These arrays are shuffled and one image from each of them is randomly picked to be the stimuli for the trial.
		This function makes use of some kelpy classes to display the images and then handle user interaction.
		
	"""
	## First we set up the elements of the trial.
	## The images we will be using are set up like so...
	
	## We pick two random images from the list and assign them to the variables pick1 and pick2.

	pick1 = randint(0, len(car_paths)-1)
	pick2 = randint(0, len(animal_paths)-1)

	## Later this function will create two CommandableImageSprite objects with those two images.
	## We start by first making an empty array to hold the objects.
	img = [None] * 2

	## We shuffle out offscreen values and later assign one of them to each image.
	## This will make them appear to come from random directions when they come on screen.
	shuffle(offscreen_positions)

	## We then create our kelpy CommandableImageSprite objects.
	## These are initialized by passing the object it's screen (to be diplayed on), the start position, the image path, and the scale of the object.
	img[0] = CommandableImageSprite( screen, offscreen_positions[0], car_paths[pick1], scale=IMAGE_SCALE)
	img[1] = CommandableImageSprite( screen, offscreen_positions[1], animal_paths[pick2], scale=IMAGE_SCALE)

	## We then designate which image is going to be the correct one, and store a reference to that object.
	## in this case the image assigned to img[1] is always drawn from our pool of animal images.
	correct = img[1]

	## This line sets up the display queue (from the kelpy class DisplayQueue(). Think of this as our list of things to happen.
	Q = DisplayQueue()
	
	## And we take a note of the time that the trial starts with this line.
	## Calling the time() method from the python time library.
	start_time = time()
	
	#### These next lines are a script of what is to happen in the experiment.

	## We move the two objects in from their start positions offscreen.
	## They are moved to a shuffled position from the onscreen_positions array.
	## Note that we first shuffle the array to randomize the positions.
	shuffle(onscreen_positions)
	
	Q.append(obj=img[0], action='move', pos= onscreen_positions[0], duration=1.5)
	Q.append(obj=img[1], action='move', pos= onscreen_positions[1], duration=1.5)
	
	# We store the order that we will draw and update things in this variable 'dos'
	dos = OrderedUpdates(*img) 

	
		
	#####################################################
	##These next few lines are used to print all of our info in a nice and orderly fashion.
	##the python str method rsplit is used to seperate the filename from the rest of the filepath.
	## we simply match everything 1 backslash from the end, it returns both items in a list.
	## we want the last item, so we ask for item 1 from the list. It's repeated for the car and animal images.
	car_used = filename(car_images[pick1])
	animal_used = filename(animal_images[pick2])
	
	###############
	## Then we determine whether the onscreen position for the car was left or right. We deduce that the animal was the opposite.
	## These variables are used later to print the on screen position.
	if  onscreen_positions[0] is ON_LEFT:
		car_position = 'LEFT'
		animal_position = 'RIGHT'
	else:
		car_position = 'RIGHT'
		animal_position = 'LEFT'
	
	
	

	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	for event in kelpy_standard_event_loop(screen, Q, dos):
		
		# If the event is a click:
		if is_click(event):
			
			## check if each of our images was clicked.
			## (we use the function wasClicked from the kelpy EventHandler library to return which item was clicked.)
			who = who_was_clicked(dos)
			
			if who is correct:
			## Print whether the correct item was clicked, which car was used, it's position, which animal was used and it's position, and how long the trial took in seconds.
				trial_time = time() - start_time
				play_sound(sound_yup_path, wait=True, volume=7.0)
				return True, car_used, car_position, animal_used, animal_position, trial_time
			else:
			## otherwise print the fail sound and print false.
				trial_time = time() - start_time
				play_sound(sound_nope_path, wait=True, volume=7.0)
				return False, car_used, car_position, animal_used, animal_position, trial_time
			break
##################################
## (end of present trial function)
			
			

			
# Then finally we use a for loop and the present_trial function to present a number of blocks.
for block in range(10):
	
	## we print the block number along with the trial results.
	print block, present_trial(car_images, animal_images)


##run()
	
	
		
		
		
