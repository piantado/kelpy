# -*- coding: utf-8 -*-
import os, sys
# sys.path.append('/home/piantado/Desktop/mit/Libraries/kelpy/') ## THIS SHOULD POINT TO KELPY
# sys.path.append('/home/piantado/Desktop/mit/Libraries/kelpy/kelpy') ## THIS SHOULD POINT TO KELPY
import pygame
from pygame.locals import *
from random import randint, choice, sample, shuffle
from time import time

from copy import copy

from kelpy.CommandableSprites import *
from kelpy.Miscellaneous import *

IMAGE_SCALE = 0.25
HOFFSET = 100
VOFFSET = 100

INCORRECT_SOUND = "sounds/button-1.wav"

##############################################
## Set up pygame

pygame.init()
#screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN)

screen = pygame.display.set_mode((800, 600))

WINDOW_WIDTH = screen.get_width() #1024
WINDOW_HEIGHT = screen.get_height() #768

background_color = (140, 140, 140) # 90 # 190

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run a single trial
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

# this sets up a trial and returns a set of objects, to be displayed etc. 
# this returns True if it was right on the first try
def present_trial(images, correct, sound):
	
	if len(images) != 4: print "*** ERROR! DID NOT SUPPLY 4 IMAGES: ", images
	
	img = [None] * 4
	
	## set the image locations
	img[0] = CommandableImageSprite( screen, (WINDOW_WIDTH/2-HOFFSET, WINDOW_HEIGHT/2-VOFFSET), images[0], scale=IMAGE_SCALE)
	img[1] = CommandableImageSprite( screen, (WINDOW_WIDTH/2-HOFFSET, WINDOW_HEIGHT/2+VOFFSET), images[1], scale=IMAGE_SCALE)
	img[2] = CommandableImageSprite( screen, (WINDOW_WIDTH/2+HOFFSET, WINDOW_HEIGHT/2-VOFFSET), images[2], scale=IMAGE_SCALE)
	img[3] = CommandableImageSprite( screen, (WINDOW_WIDTH/2+HOFFSET, WINDOW_HEIGHT/2+VOFFSET), images[3], scale=IMAGE_SCALE)
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Set up the updates, etc. 
	
	dos = pygame.sprite.OrderedUpdates() # like group, but draws in order of adding
	for i in img:
		dos.add(i)
	
	# Play the sound
	screen.fill(background_color)
	pygame.display.flip() # display most recently drawn stuff
	play_sound(sound, wait=True)
	
	# We should handle everything in here
	# and then return control to the main loop once we've completed
	start_time = time()
	while True:
		screen.fill(background_color)
		
		# Update and redraw all
		for c in dos:
			c.update() # maybe nothing happens?
			c.draw()
		
		pygame.display.flip()
		
		# process events in pygame
		for event in pygame.event.get():
			
			if (  event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
				
				# check if each of our images was clicked
				for x in range(len(img)):
					if img[x].click_inside(pygame.mouse.get_pos()):
						
						if images[x] == correct: 
							return (time()-start_time)
						else:
							play_sound(INCORRECT_SOUND, wait=False)
						
						
						
			if event.type == QUIT: quit()
			if event.type == KEYDOWN and event.key == K_ESCAPE: quit()
		
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
def run():
	
	"""
		Load the excel file etc. 
	"""
	
	target_images = ["images/car1_blue_stars.png","images/car1_red_circles.png","images/car1_red_stars.png","images/car2_blue_circles.png"]
	target_sounds = ["sounds/reward-2.wav", "sounds/reward-3.wav", "sounds/reward-4.wav", "sounds/fanfare-1.wav"]
	shuffle(target_images)
	
	for block in range(10):
		
		order = range(len(target_images))
		shuffle(order)
		
		for o in order:
			
			print present_trial(target_images, target_images[o], target_sounds[o])
	
	
	
run()

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
