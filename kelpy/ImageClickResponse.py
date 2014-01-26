# -*- coding: utf-8 -*-

from CommandableSprite import *
from CommandableImageSprite import *
from Arrangeable import *
from time import time
from random import randint, choice, sample, shuffle
import random
from math import *
from pygame.locals import *
from pygame.image import *
from DisplayQueue import *
from Miscellaneous import *
import sys

import pygame.mixer #for sound
"""
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# A bunch of images you can respond to
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
	# if correct is an index, then we keep clicking until correct
	# otherwise we just record one response
"""

class ImageClickResponse(CommandableSprite):
	"""
		
	"""
	
	def __init__(self, screen, init_position, imagepaths, randomize=True, feedback=True, correct=-1,  rotation=0, scale=1.0, pre="", correct_sound=None, incorrect_sound=None):
		
		"""
			This is a sprite with responses built in.
			screen: the screen to display the sprite onto.
			
		"""
		
		CommandableSprite.__init__(self, screen, init_position)
		
		self.pad = 5
		self.pre = pre
		self.correct_sound = correct_sound
		self.incorrect_sound = incorrect_sound
		
		# keep track of the total clicks
		self.click_count = 0
		self.responses = []  #we return a list of all responses
		
		x,y=init_position
		self.set_position(x,y)
		
		# Must make a copy or else all goes to hell with randomization
		self.imagepaths = copy(imagepaths)
		
		# assume we are given a string since that is easier to compare with shuffles
		if isinstance(correct, int):
			self.correct = self.imagepaths[i]
		else:
			self.correct = correct
		
		# randomize the order
		random.shuffle(self.imagepaths)
		
		self.correct_location = -1 # store what location  the correct answer is in
		for i in xrange(len(self.imagepaths)):
			if self.imagepaths[i] == correct: self.correct_location = i
		
		self.last_response = "NA"
		self.feedback = feedback
		self.children = map( lambda f : CommandableImageSprite(screen, OFFSCREEN, f, rotation, scale), self.imagepaths)
		
		self.visible = False
		for i in self.children: i.visible = False
		
		# set the positions of all my kids
		dim = Arranger.ArrangeVertical(self.children, x, y)
		self.set_dimensions(dim)
		
		# set up my own queue of events -- for processing things
		self.Q = DisplayQueue()
		self.waiting_for_response = False
		
		# this can be read after responding to see if we got it right on the first click
		self.was_correct = None
		
		self.enabled = True
		
	def start(self):
		CommandableSprite.start(self)
		for i in self.children: i.start()
		
	# how to update ourselves? Update our queue and children
	def update(self):
		# and a normal update
		CommandableSprite.update(self)
		
		# update my queue
		self.Q.update()
		
		# and my children
		for i in self.children: i.update()
		
	# update my kids
	def update_action(self, **c):
		
		ret = True
		
		if c['first']: # If this is the first function call
			self.start_x, self.start_y = self.position()
			self.start_time = time()
		
		action = c['action']
		
		# make setting visibiliy propogate down
		if action == 'show': 
			for i in self.children: i.visible = True
			self.visible=True
		elif action == 'hide':
			for i in self.children: i.visible = False
			self.visible=False
		elif action == 'reset': # call this to start a response all anew (for some reason)
			self.Q.purge()
			self.waiting_for_response = False
		elif action == 'respond':
			if not self.waiting_for_response:
				self.visible = True # show myself
				for i in self.children: i.visible = True # make visible
				self.finished_responding = False
				self.last_showtime = time()
				self.waiting_for_response = True # now we are waiting! 
				
		# and update my own queue -- maybe not needed here since we do this in update??
		qu = self.Q.update() # update my queue of events
		
		# return true if we are 
		return self.finished_responding and qu
		
	# display, 
	def draw(self):
		
		if self.visible:
			
			# the upper left and right positions
			r = self.get_pygame_Rect()
			
			# display a box
			pygame.draw.rect(self.screen, (250, 250, 250), r)
			pygame.draw.rect(self.screen, (0, 0, 0), r, 3)
			
			for i in self.children: i.draw()
	
		
	# returns the FIRST image you are inside of (e.g. no guarantees for overlap)
	def inside_image(self, point):
		x,y = point
		for ii in range(len(self.children)):
			#print "CLICK ", ii
			if self.children[ii].click_inside(point): return ii
				
		return -1			
	
	# only process click events by certain objects -- for instance, this guy!
	def clickme(self, point):
		#print point, self.get_right(), self.get_left(), self.get_top(), self.get_bottom()
		if self.visible and self.enabled:
			cl = self.inside_image(point) 
			if cl >= 0:
				self.click_count = self.click_count + 1
				t = time() - self.last_showtime
				# Print output and mirror to stderr
				print time(), self.pre, tab, self.feedback, tab, t, tab, (self.imagepaths[cl]==self.correct), tab, q(self.imagepaths[cl]), tab, q(self.correct), tab, self.correct_location, tab, cl, tab, self.click_count
				print >> sys.stderr, time(), self.pre, tab, self.feedback, tab, t, tab, (self.imagepaths[cl]==self.correct), tab, q(self.imagepaths[cl]), tab, q(self.correct), tab, self.correct_location, tab, cl, tab, self.click_count
				sys.stdout.flush()
				sys.stderr.flush()
				

				self.responses.append(cl)
				
				# Process correct/incorrect -- set self variable and play song
				if self.enabled:
					if self.imagepaths[cl] == self.correct:
						# did we get it right? (only on the first click)
						if self.was_correct == None: self.was_correct = True 
						if self.correct_sound != None:
							pygame.mixer.music.load(self.correct_sound)
							pygame.mixer.music.play()
					else:
						if self.was_correct == None: self.was_correct = False 
						# play the song
						if self.incorrect_sound != None:
							pygame.mixer.music.load(self.incorrect_sound)
							pygame.mixer.music.play()
					
					if self.feedback:
						
						#print "==>", cl, self.correct
						if self.imagepaths[cl] == self.correct:
							
							# first hide all wrong answers
							for ii in range(len(self.children)):
								if ii != cl: self.Q.append_simultaneous(obj=self.children[ii], action='hide')
							
							# then zoom the right answer
							for ii in range(len(self.children)):
								if ii == cl:
									#print "Queing circlezoom"
									# FOR EXP: self.Q.append(obj=self.children[ii], action='circlezoom', amount=0.05, period=0.5, duration=1.0)
									#FOR DEMO:
									self.Q.append(obj=self.children[ii], action='circlezoom', amount=0.01, period=0.5, duration=1.0)
									
									self.Q.append(obj=self.children[ii], action='restore')
									self.finished_responding = True # we are done responding, but there is still stuff on the queue
									self.enabled = False
						else:
							# FOR DEMO:
							self.Q.append(obj=self.children[cl], action='waggle', amount=1.0, period=0.25, duration=0.75)
		#					FOR EXP: self.Q.append(obj=self.children[cl], action='waggle', amount=5.0, period=0.25, duration=0.75)
							self.Q.append(obj=self.children[cl], action='restore') # restore rotation to 0
						
					else: # no feedback
						for ci in xrange(len(self.children)):
							if self.was_correct == None: # did we get it right? (only on the first click)
								self.was_correct = (self.imagepaths[cl] == self.correct)
							
							# zoom away on all non-selected ones
							if ci != cl:
								self.Q.append_simultaneous(obj=self.children[ci], action='zoom', amount=0.1, duration=1.0,)
							
							self.enabled = False
						
						
						self.finished_responding = True 
