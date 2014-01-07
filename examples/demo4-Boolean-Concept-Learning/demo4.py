import os, sys
import pygame
from random import randint, choice, sample, shuffle
from time import time

from kelpy.CommandableImageSprite import *
from kelpy.Miscellaneous import *
from kelpy.DisplayQueue import *
from kelpy.OrderedUpdates import *
from kelpy.EventHandler import *

WOFFSET = 200
HOFFSET = 100
IMAGE_SCALE = 0.75

screen = initialize_kelpy( dimensions=(800,600) )

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

OFF_SCREEN = (-300, -300)
ON_SCREEN = (WINDOW_WIDTH/2 , WINDOW_HEIGHT/2)

YES_BUTTON_SPOT = (200, 500)
NO_BUTTON_SPOT = (600, 500)
YES_BUTTON = kstimulus('yes_no_buttons/yes1.png')
NO_BUTTON = kstimulus('yes_no_buttons/no1.png')
BUTTON_SCALE = 0.3


MAX_DISPLAY_FOR_DEMO = 5.0

## In this task we give our user a series of items and allow them to learn the correct one.
incorrect_images = [kstimulus('shapes/circle_green.png'), kstimulus('shapes/circle_purple.png'), kstimulus('shapes/star_purple.png')]
correct_image = kstimulus('shapes/star_green.png')

def show_correct(correct_image):
	
	images = [None] * 1
	
	images[0] = CommandableImageSprite( screen, OFF_SCREEN, correct_image, scale=IMAGE_SCALE)
	
	global start_time 
	start_time = time()
	
	Q = DisplayQueue()
	
	Q.append(obj=images[0], action='move', pos= ON_SCREEN, duration=1.5)
	
	dos = OrderedUpdates(*images)
	
	play_sound( kstimulus('sounds/Tada.wav'))
	
	for event in kelpy_standard_event_loop(screen, Q, dos):
		if (time() - start_time) >= MAX_DISPLAY_FOR_DEMO:
			break
			
def present_trial(incorrect_images, correct_image):
	this_trial = time()
	images = [None] * 6
	
	images[0] = CommandableImageSprite( screen, OFF_SCREEN, correct_image, scale=IMAGE_SCALE)
	images[1] = CommandableImageSprite( screen, OFF_SCREEN, incorrect_images[0], scale=IMAGE_SCALE)
	images[2] = CommandableImageSprite( screen, OFF_SCREEN, incorrect_images[1], scale=IMAGE_SCALE)
	images[3] = CommandableImageSprite( screen, OFF_SCREEN, incorrect_images[2], scale=IMAGE_SCALE)
	images[4] = CommandableImageSprite( screen, YES_BUTTON_SPOT, YES_BUTTON, scale=BUTTON_SCALE)
	images[5] = CommandableImageSprite( screen, NO_BUTTON_SPOT, NO_BUTTON, scale=BUTTON_SCALE)

	correct = images[0]
	
	Q = DisplayQueue()
	dos = OrderedUpdates(*images)
	
	pick = randint(0,3)
	
	
	Q.append(obj=images[pick], action='move', pos= ON_SCREEN, duration=1.5)

	for event in kelpy_standard_event_loop(screen, Q, dos):
		if is_click(event):
			who = who_was_clicked(dos)
			
			if who is images[4] and images[pick] is correct:
				trial_time = time() - start_time
				this_trial_time = time() - this_trial
				play_sound( kstimulus('sounds/Tada.wav'))
				print True, filename(correct_image) , trial_time, this_trial_time
				break
				
			elif who is images[5] and images[pick] is not correct:
				trial_time = time() - start_time
				this_trial_time = time() - this_trial
				play_sound( kstimulus('sounds/TadaWah2.wav'))
				print True, filename(incorrect_images[pick-1]),  trial_time, this_trial_time
				break
				
			elif who is images[5] and images[pick] is correct:
				play_sound( kstimulus('sounds/Bad_Pick.wav'))
				trial_time = time() - start_time
				this_trial_time = time() - this_trial
				print False , filename( correct_image) , trial_time, this_trial_time
				break
				
			elif who is images[4] and images[pick] is not correct:
				trial_time = time() - start_time
				this_trial_time = time() - this_trial
				play_sound( kstimulus('sounds/Bad_Pick.wav'))
				print False , filename( incorrect_images[pick-1]), trial_time, this_trial_time
				break

show_correct(correct_image)
for i in xrange(20):
	present_trial(incorrect_images, correct_image)
