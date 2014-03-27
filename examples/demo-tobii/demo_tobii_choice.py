# -*- coding: utf-8 -*-

"""

	This example builds off of demo3b which is a 2-AFC task. However, instead of clicking on the 'correct' image, the program recognizes a person's selection based on which image was looked at for longer during the trial.

	For the correct image, an 'affirmative' sound plays.
	For the other image, an 'error' sound plays.
	There is a set trial time; if an image is not looked at for longer than the set looking threshold and the looking proportions do not differ more than the set difference threshold, an error sound will also play.

	The trial number, images, and their respective looking proportions over the duration of the trial are printed to the console
		
	Like demo3b, this takes a csv file of image pairs instead of having the images hard coded into the program.
	
	Rather than CommandableImageSprites, TobiiSprites are created which also require a TobiiController.
	
	
"""

import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time
import csv

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *

from kelpy.tobii.TobiiController import *
from kelpy.tobii.TobiiSprite import *
from kelpy.tobii.TobiiWatcher import *


########################################
##The following are constants that are used to set up the size and arrangement of images later.
##
IMAGE_SCALE = 0.25
HOFFSET = 300
VOFFSET = 100

##############################################
## Set up pygame
## this is the initialization line, to set up a screen that we will diplay things on.
# the tobii eyetracker requires the screen to be fullsized for accurate gaze points
screen, spot = initialize_kelpy( dimensions = (1024, 768) )

##############################################
## This line fetches the size of the screen (the one we just created) and assigns 
## the values to some constants that we can refer to later.
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

## Those positions are then stored in arrays so they may be shuffled (randomized).
#check the spot values to figure out where they actually are...
onscreen_positions = [spot.b1, spot.b4]
offscreen_positions = [spot.west, spot.east]

##############################################
## We create a string to hold the filepath to the sound that will play when the 'correct' option is clicked.
sound_yup_path = kstimulus('sounds/Affirmative.wav')
sound_nope_path = kstimulus('sounds/Error3.wav')

###############################################
## Almost finished! We finally set up some arrays to hold the filepaths to the images we will be using.
## NOTE: In this version of the demo we intake a csv file that holds predetermined groupings of stimuli.
## These groups are presented randomly

car_images = []   ## we create some blank lists
animal_images = [] ## another blank list

## Check demo3b for more details on how this csv section works!
with open('stimuli_pairings.csv', 'rb') as f:
	
	reader =  csv.reader(f, delimiter=",")
	
	for row in reader:
		car_images.append(kstimulus(row[0]))
		animal_images.append(kstimulus(row[1]))

##############################################
## setup and activate tobii

# this creates a TobiiController that calls the actual Tobii SDK code
tobii_controller = TobiiController(screen)

# this searches for the tobii eyetracker that is connected.
# It times out based on the given amount of seconds (the default is 1,000 seconds) and exits this program
tobii_controller.wait_for_find_eyetracker(3)

#set the name of the data file that will output all of the Tobii data
tobii_controller.set_data_file('testdata.tsv')

#activate the first tobii eyetracker that was found
tobii_controller.activate(tobii_controller.eyetrackers.keys()[0])

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

	## We then create our TobiiSprite objects.
	## These are initialized the same way as CommandableImageSprites, but must also have the TobiiController as an argument and has an optional argument of "is_following" (defaults to False). In this example, since we don't want the images to move with eye gaze, we will leave is_following at its default value
	img[0] = TobiiSprite( screen, offscreen_positions[0], car_paths[pick1], tobii_controller, scale=IMAGE_SCALE)
	img[1] = TobiiSprite( screen, offscreen_positions[1], animal_paths[pick2], tobii_controller, scale=IMAGE_SCALE)

	## We then designate which image is going to be the correct one, and store a reference to that object.
	## in this case the image assigned to img[1] is always drawn from our pool of animal images.
	correct = img[1]

	## This line sets up the display queue (from the kelpy class DisplayQueue(). Think of this as our list of things to happen.
	Q = DisplayQueue()

	#### These next lines are a script of what is to happen in the experiment.

	## We move the two objects in from their start positions offscreen.
	## They are moved to a shuffled position from the onscreen_positions array.
	## Note that we first shuffle the array to randomize the positions.
	shuffle(onscreen_positions)

	Q.append(obj=img[0], action='move', pos= onscreen_positions[0], duration=0.5)
	Q.append(obj=img[1], action='move', pos= onscreen_positions[1], duration=0.5)
	
	# We store the order that we will draw and update things in this variable 'dos'
	dos = OrderedUpdates(*img) 

	## And we take a note of the time that the trial starts with this line.
	## Calling the time() method from the python time library.
	start_time = time()
		
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
	if  onscreen_positions[0] is spot.west:
		car_position = 'LEFT'
		animal_position = 'RIGHT'
	else:
		car_position = 'RIGHT'
		animal_position = 'LEFT'

	#start tracking
	tobii_controller.start_tracking()	
	

	## The standard event loop in kelpy -- this loops infinitely to process interactions
	## and throws events depending on what the user does
	trial_time = 5.0
	for event in kelpy_standard_event_loop(screen, Q, dos, throw_null_events=True):
		
		if (time() - start_time > trial_time): 
			print "trial end"
			break

		#this is set specifically for the tobii controller; otherwise the program hangs
		#since the text file is not closed
		if event.type == QUIT:
			tobii_controller.close_data_file()
			tobii_controller.destroy()
			
	
	tobii_controller.stop_tracking()
	
	chosen = None
	max_value = 0.0;
	proportions = looking_proportions(dos, trial_time) 
	print proportions
	
	for item, value in proportions.iteritems():
		if value > max_value:
			chosen = item
			max_value = value 

	if chosen is not None:
		print "chosen: ", filename(chosen.image_path), proportions[chosen]
	else:
		print "nothing chosen"
	
	if chosen is correct:
	## Print whether the correct item was clicked, which car was used, it's position, which animal was used and it's position, and how long the trial took in seconds.
		play_sound(sound_yup_path, wait=True, volume=5.0)
		return True, car_used, car_position, animal_used, animal_position, trial_time
	else:
	## otherwise print the fail sound and print false.
		play_sound(sound_nope_path, wait=True, volume=5.0)
		return False, car_used, car_position, animal_used, animal_position, trial_time

##################################
## (end of present trial function)
			
			
			
# Then finally we use a for loop and the present_trial function to present a number of blocks.
for block in range(10):
	
	## we print the block number along with the trial results.
	print block, present_trial(car_images, animal_images)

#make sure the TobiiController has closed the data file and removed itself
tobii_controller.close_data_file()
tobii_controller.destroy()

##run()
	
	
		
		
		
