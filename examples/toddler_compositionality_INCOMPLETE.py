# -*- coding: utf-8 -*-
import os, sys
from random import randint, choice, sample, shuffle

from time import time

from kelpy.CommandableSprite import *
from kelpy.ImageClickResponse import *
from kelpy.DisplayQueue import *
from kelpy.AttentionGetter import *
from kelpy.OrderedUpdates import *

import kelpy # just for KELPY_VERSION
assert kelpy.KELPY_VERSION == 0.02 ## Just a version check

screen = initialize_kelpy(fullscreen=False) 

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
CENTER_STAGE  = ( WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

TRUCK_SCALE = 0.35
SCREEN_SCALE = 0.7

BLOCKER_X = WINDOW_WIDTH * 1. / 2.
BLOCKER_Y = WINDOW_HEIGHT * 2. / 3.
BLOCKER_POSITION = (BLOCKER_X, BLOCKER_Y)

RESPONSE1_X = WINDOW_WIDTH * 85./100.
RESPONSE1_Y = 300
RESPONSE1_POSITION = (RESPONSE1_X, RESPONSE1_Y)

RESPONSE2_X = WINDOW_WIDTH * 15./100.
RESPONSE2_Y = 300
RESPONSE2_POSITION = (RESPONSE2_X, RESPONSE2_Y)

OBJECT_START_POSITION = ( WINDOW_WIDTH + 400, BLOCKER_Y)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Some sound functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pygame.mixer

## Corr
#correct_sound_files = []
#correct_sounds = [
pygame.mixer.init()

correct_sounds = ["sounds/fanfare-1.wav"]
incorrect_sounds = ["sounds/wrong-sound-1.wav"]
#test_sounds = ["sounds/button-3.wav"]

#7,11,12
#reward_gifs = ["gifs/1.gif", "gifs/3.gif", "gifs/5.gif", "gifs/7.gif", "gifs/9.gif", "gifs/10.gif", "gifs/11.gif", "gifs/12.gif",   "gifs/16.gif", "gifs/18.gif", "gifs/20.gif", "gifs/22.gif", "gifs/27.gif", "gifs/31.gif", "gifs/32.gif", "gifs/34.gif", "gifs/37.gif", "gifs/38.gif", "gifs/39.gif"]
#reward_sounds = ["sounds/reward-2.wav","sounds/reward-3.wav","sounds/reward-4.wav" ]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# this sets up a trial and returns a set of objects, to be displayed etc. 
# this returns True if it was right on the first try
def present_trial(screen, object_type, object_color, object_pattern, functions, training=True, pre=""):
	
	
	Q = DisplayQueue();	

	in_object_path = kstimulus("feature_cars/"+object_type +"_"+ object_color +"_"+ object_pattern +".png")
	possible_answers = [kstimulus("feature_patches/blue_circles.png"), 
	                    kstimulus("feature_patches/blue_stars.png"),
	                    kstimulus("feature_patches/red_circles.png"), 
	                    kstimulus("feature_patches/red_stars.png")]
	
	out_object_color = object_color # These are altered below to create the new object
	out_object_pattern = object_pattern
	
	# now figure out what the right output should be!
	for f in functions:
		if f == "red": out_object_color = "red"
		elif f == "blue": out_object_color = "blue"
		elif f == "circles": out_object_pattern = "circles"
		elif f == "stars": out_object_pattern = "stars"
		else: print "*** Error bad object function"+functions+"\t"+f
	
	out_object_path = kstimulus("cars/"+object_type +"_"+ out_object_color +"_"+ out_object_pattern +".png")
	correct1_string = kstimulus("cars/"+object_color+"_"+object_pattern+".png") # the right answer
	correct2_string = kstimulus("cars/"+out_object_color+"_"+out_object_pattern+".png") # the right answer
	
	# now make a display screen for each function
	TIME_TO_GET_TO_RESPONSE1 = 1.5
	TIME_BETWEEN_SCREENS = 1.0 # this is how long it takes to move between screens (And to the first one after the first response)
	TIME_TO_APPLY_FUNCTION = 2.0 # each screen takes this long to apply its function
	REVEAL_TIME = 0.5
	
	displayscreens = [None]*len(functions)
	screen_active = [None]*len(functions)
	screen_inactive = [None]*len(functions)
	for fi in range(len(functions)):
		screen_inactive[fi] = kstimulus("feature_tvs/screen_inactive.png")# blink *off* when active. Bizarre, but this leaves it up
		screen_active[fi] = kstimulus("feature_tvs/screen_active_"+functions[fi]+".png") # store an array of images for when the screen activates
		displayscreens[fi] = CommandableImageSprite( screen, BLOCKER_POSITION, screen_inactive[fi], scale=SCREEN_SCALE)
	
	## arrange all the display screens horizontally
	displayscreens.reverse() # do this so that the order is correct -- left to right in function args is R-L on screen
	Arranger.ArrangeHorizontal(displayscreens, BLOCKER_X, BLOCKER_Y, pad=0)
	displayscreens.reverse()
	
	# Set up the sounds
	if training:
		correct_sound = random.choice(correct_sounds)
		incorrect_sound = random.choice(incorrect_sounds)
	else:
		correct_sound = random.choice(test_sounds)
		incorrect_sound = correct_sound
	
	
	# The image click responses
	if len(functions) == 1:
		pre = pre + functions[0] + "\tNA" + "\t" + q(in_object_path)
	else:
		pre = pre + functions[0] + "\t" + functions[1] + "\t" + q(in_object_path)
	
	response1 = ImageClickResponse( screen, RESPONSE1_POSITION, possible_answers, scale=0.50, correct=correct1_string, feedback=True, pre="R1\t"+pre, correct_sound=random.choice(correct_sounds), incorrect_sound=random.choice(incorrect_sounds)) ## Edited here to always play correct and incorrect regardless of training condition
	response1.start()
	response2 = ImageClickResponse( screen, RESPONSE2_POSITION, possible_answers, scale=0.50, correct=correct2_string, feedback=training, pre="R2\t"+pre, correct_sound=correct_sound, incorrect_sound=incorrect_sound)
	response2.start()
	
	# the object
	myobj = CommandableImageSprite(screen, OBJECT_START_POSITION, in_object_path, scale=TRUCK_SCALE)
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Now set up all the motions
	
	# move to the blocker's height, below RESPONSE1
	Q.append(obj=myobj, action='wagglemove', duration=TIME_TO_GET_TO_RESPONSE1, period=1., amount=1.25, pos=[RESPONSE1_X, BLOCKER_Y+48]) 
	Q.append(obj=response1, action='respond', duration=Infinity)  # duration=Infinity in order to keep this waiting as long as necessary
	
	#Q.append(obj=response1, action='hide') # After ms_nov7, we do NOT hide in order to make things better
	
	for fi in range(len(functions)):
		Q.append(obj=myobj, action='wagglemove', duration=TIME_BETWEEN_SCREENS, period=1., amount=0.25, pos=[displayscreens[fi].get_x()-20, displayscreens[fi].get_y()+38])
		Q.append(obj=myobj, action='waggle', duration=TIME_TO_APPLY_FUNCTION, period=0.5, amount=1.2)
		
		Q.append_simultaneous(obj=displayscreens[fi], action='swapblink', image=screen_active[fi], scale=SCREEN_SCALE, rotation=0, duration=TIME_TO_APPLY_FUNCTION, period=0.5)
		
		Q.append(obj=myobj, action='restore')
		
		# and leave the screen on
		Q.append(obj=displayscreens[fi], action='swap', image=screen_active[fi], rotation=0, scale=SCREEN_SCALE)
		
	
	Q.append(obj=response2, action='respond', duration=Infinity)  # duration=Infinity in order to keep this waiting as long as necessary
	
	# in training, reveal the object
	if training:
		Q.append(obj=myobj, action='swap', image=out_object_path, rotation=0, scale=TRUCK_SCALE)
		
		for fi in range(len(functions)):
			Q.append(obj=displayscreens[fi], action='move', pos=[displayscreens[fi].get_x(), -500], duration=1.0)
		
		Q.append(obj=myobj, action='wait', duration=2.0)
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	# NOTE: this controls the z-depth
	ou = OrderedUpdates(myobj, response1, response2, *displayscreens)

	for event in kelpy_standard_event_loop(screen, Q, ou, bottom_smile_updates): 
		if (  event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
				for x in dos: x.clickme(pygame.mouse.get_pos()) # everyone gets to process this:
		if event.type == QUIT: quit()
		if event.type == KEYDOWN and event.key == K_ESCAPE: quit()
			
				
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




def run():
	
	########
	# let's block mouse movement 
	#pygame.event.set_blocked(MOUSEMOTION)
	
	# okay we will pair each transformation up
	trucks = ["car1", "car2", "car3", "car4"]
		
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
	# The demo item 
	N = 1 # how many have we seen?
		
	demo_block_trials= [ # store the truck, color, texture, function
			[ trucks[0], "blue", "circles" , "red"], 
			[ trucks[0], "blue", "circles" , "stars"],
			[ trucks[0], "blue", "circles" , "circles"], 
			[ trucks[0], "red", "stars" , "blue"],
			[ trucks[0], "red", "stars" , "circles"],
			[ trucks[0], "red", "stars" , "stars"] 
			]
	for f in demo_block_trials:
		present_trial(screen, f[0], f[1], f[2], [f[3]], training=True, pre=str(N)+"\t") #f[3] is already a list for these
	
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
	# The training phase

	while True:
		
		same_color = choice(["red", "blue"])
		same_pattern = choice( ["circles", "stars"] )
		
		## NOTE: Keep these in here so that the choice is made for each block
		training_block_trials= [ # store the truck, color, texture, function
		
					[ choice(trucks), "blue", choice(["circles", "stars"])  , "red", True], 
					[ choice(trucks), "red", choice(["circles", "stars"])   , "blue", True], 
					[ choice(trucks), choice(["red", "blue"]), "stars", "circles", True], 
					[ choice(trucks), choice(["red", "blue"]), "circles"   , "stars", True],
					
					# and two with no changes
					[ choice(trucks), same_color, choice(["circles", "stars"]) , same_color, True],
					[ choice(trucks), choice(["red", "blue"]), same_pattern, same_pattern, True]
					]
		# randomize the order
		random.shuffle(training_block_trials)
	
		# present an entire training block
		correct_in_block = 0 # how many right in this training block?
		N_in_block = 0
		
		# pair each function wtih a random 
		for f in training_block_trials:
			
			was_correct = present_trial(screen, f[0], f[1], f[2], [f[3]], training=f[4], pre=str(N)+"\t") # we have to give the function as a list, even when there's just one
			
			N_in_block += 1
			if was_correct:
				correct_in_block += 1
			
			N += 1
			if (N % 2 == 0): gif_attention_getter(screen, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), reward_gifs, reward_sounds, duration=7.5)
			
		# done 8 overall and 3/4 in the last block
		if (correct_in_block >= 5):
			break
			
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
	## The testing phase
	for testing_block in range(20): # at most this many testing blocks
	
		# block of 8 random trials
		testing_block_trials= [ # store the truck, color, texture, function
		
					# 8 two-function tests
					[ choice(trucks), choice(["red", "blue"]), choice(["circles", "stars"]), sample(["red", "blue", "circles", "stars"], 2), False ], 
					[ choice(trucks), choice(["red", "blue"]), choice(["circles", "stars"]), sample(["red", "blue", "circles", "stars"], 2), False ], 
					[ choice(trucks), choice(["red", "blue"]), choice(["circles", "stars"]), sample(["red", "blue", "circles", "stars"], 2), False ], 
					[ choice(trucks), choice(["red", "blue"]), choice(["circles", "stars"]), sample(["red", "blue", "circles", "stars"], 2), False ], 
					
					# two single function tests with feedback
					[ choice(trucks), choice(["red", "blue"]), choice(["circles", "stars"]), sample(["red", "blue", "circles", "stars"], 1), True ], 
					[ choice(trucks), choice(["red", "blue"]), choice(["circles", "stars"]), sample(["red", "blue", "circles", "stars"], 1), True ], 
					
					]
		
		# randomize the order
		random.shuffle(testing_block_trials)
		
		# pair each function wtih a random 
		for f in testing_block_trials:
			
			was_correct = present_trial(screen, f[0], f[1], f[2], f[3], training=f[4], pre=str(N)+"\t") #f[3] is already a list for these
			
			N += 1
			if (N % 3 == 0): play_reward_image(screen)
	
	
run()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
