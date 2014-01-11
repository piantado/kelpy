import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *
from itertools import *
import csv


###################
## First we set up a bunch of constants.
##
WOFFSET = 200
HOFFSET = 100



###################################
## First we set up our screen.
screen = initialize_kelpy( dimensions=(800,600) )

#################
## and then set up some constants for our images, their scale and where they will be placed
##
IMAGE_SCALE = 0.75
OFF_SCREEN = (-300, -300)
ON_SCREEN = (screen.get_width()/2 , screen.get_height()/2)

##################
## Followed by some constants for our buttons, their placement on screen, their images, and their scale.
YES_BUTTON_SPOT = (200, 500)
NO_BUTTON_SPOT = (600, 500)
YES_BUTTON = kstimulus('yes_no_buttons/yes1.png')
NO_BUTTON = kstimulus('yes_no_buttons/no1.png')
BUTTON_SCALE = 0.3

MAX_DISPLAY_FOR_DEMO = 3.0


"""
	In this task we give our user a series of items and allow them to learn the correct one.
	The demonstration of correct can be multiple things, and depends on what the user loads into a csv file currently.
	This may change to something more intellegent soon.
"""	
incorrect_images = []
correct_images = []

def show_correct(input_image):
	"""
		This function demonstrates the 'correct' object. It displays it onto the screen for a short time.
	"""

	image = CommandableImageSprite( screen, OFF_SCREEN, input_image, scale=IMAGE_SCALE)
	
	Q = DisplayQueue()
	things = [image]
	Q.append(obj=image, action='move', pos= ON_SCREEN, duration=1.5)
	
	dos = OrderedUpdates(*things)
	
	play_sound( kstimulus('sounds/Tada.wav') )
	
	for event in kelpy_standard_event_loop(screen, Q, dos):
		if (time() - start_time) >= MAX_DISPLAY_FOR_DEMO:
			break
			
def present_trial(input_image):
	"""
		This is the main function we use to run the trial. It is run twice, once for the 'correct' option, once for the 'incorrect' option.
		It lacks the ability to get shuffled around, so while the many correct and incorrect options are shuffled, they only appear in the order of 'correct' then 'incorrect'.
		There are three sprites on screen, the image, the 'yes' button, and the 'no' button.
		
	"""
	start_time = time()

	Q = DisplayQueue()	
	image = CommandableImageSprite( screen, OFF_SCREEN, input_image, scale=IMAGE_SCALE)
	yes_button = CommandableImageSprite( screen, YES_BUTTON_SPOT, YES_BUTTON, scale=BUTTON_SCALE )
	no_button = CommandableImageSprite( screen, NO_BUTTON_SPOT, NO_BUTTON, scale=BUTTON_SCALE )
	
	things = (image, yes_button, no_button)
	dos = OrderedUpdates(*things)
	## The image is moved on screen...
	Q.append(obj=image, action='move', pos= ON_SCREEN, duration=1.5)
	
	for event in kelpy_standard_event_loop(screen, Q, dos):
		## If it is clicked, we determine whether it is a correct or incorrect image, and whether yes or no was clicked...
		if is_click(event):
			who = who_was_clicked(dos)
			trial_time = time() - start_time
			print trial_time, filename(input_image),
			if who is yes_button and input_image in correct_images:
				play_sound( kstimulus('sounds/Tada.wav'), wait=True)
				print True
				break
				
			elif who is no_button and not input_image in correct_images:
				play_sound( kstimulus('sounds/TadaWah2.wav'), wait=True)
				print True
				break
				
			elif who is no_button and input_image in correct_images:
				play_sound( kstimulus('sounds/Bad_Pick.wav'), wait=True)
				print False
				break
				
			elif who is yes_button and not input_image in correct_images:
				play_sound( kstimulus('sounds/Bad_Pick.wav'), wait=True)
				print False
				break
			## and we print the resuts using the code above.
				
def load_csv(filename, array_to_load):
	"""
	this function loads a csv file into an array.
	
	It accepts a filename (of the desired .csv file, to be placed in the same directory as the script.)
	as well as an array to load the stimuli into. The stimuli in this case are kept in the /kelpy/stimuli folder, so we use the kstimulus() function to load them.
	
	"""
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
				for i in row:
					array_to_load.append(kstimulus(i)) ## note the use of the kstimulus function.
					
					



load_csv('right-images.csv', correct_images)
load_csv('wrong-images.csv', incorrect_images)
	
for i in xrange(20):
	start_time = time()
	shuffle(correct_images)
	shuffle(incorrect_images)
	 
	## these currently run in a fixed order, which is quicker to figure out than the star or green part. 
	## That will have to be fixed soon.
	show_correct(correct_images[0])
	present_trial( incorrect_images[0] )
	present_trial( correct_images[1])