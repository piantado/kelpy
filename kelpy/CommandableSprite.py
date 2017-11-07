# -*- coding: utf-8 -*-

from pygame import Rect, Color
from pygame.sprite import Sprite
from Arrangeable import *
from Dragable import *
from time import time
from copy import copy
from math import *
from pygame.locals import *
import pygame


"""
	TODO: Break this up into separate classes
	      Change the naming of rotate etc. so that if duration is not specified, it happens immediately

"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This extends sprites by making them commandable, so that they will do things at certain times
# (in a sequence)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CommandableSprite(Sprite, Dragable):
	
	def __init__(self, screen, init_position, isdraggable=False,name=None):
		
		#Arrangeable.__init__(self)
		Sprite.__init__(self)
		
		Dragable.__init__(self)
		self.set_draggable(isdraggable)
		
		self.commands = []
		self.running = False	
		self.screen = screen
		self.set_position(init_position)
		self.update_callbacks = [] 
		self.isdraggable = isdraggable
		
	def add_update_callback(self, f):
		self.update_callbacks.append(f)
	
	def update(self):
		for x in self.update_callbacks:
			x(self)
			
	# this starts the timer for it to start processing actions
	def start(self):
		self.running = True
		self.start_x = self.get_x()
		self.start_y = self.get_y()
	
	def position(self):
		return [self.get_x(), self.get_y()]
	
	def stop(self):
		self.running = False
	
	# This pushes a list of commands onto myself
	def push_commands(self, **d):
		self.commands.append(d)

	# get rid of the current command
	def next_command(self): 
		if len(self.commands) > 0:
			del self.commands[0]
	
	
	# NOTE: We re-did this so that each commandable sprite just
	# processes single commands, and the queue is external
	# Update the current action
	def update_action(self, **c):

		if c['first']: # If this is the first function call
			self.start_x, self.start_y = self.position()
	
		action = c['action']
		duration = c.get('duration', 0.0) # get the duration else 0.0 if none is specified
		#print duration, duration==0.0
		t = 1.0 if duration == 0.0 else (time() - c['start_time']) / float(duration) # what percent of the way through are we?
		
		# update according to remaining time
		if action == 'move': # move
			
			x,y = c['pos']
			self.set_x( (x - self.start_x) * t + self.start_x)
			self.set_y( (y - self.start_y) * t + self.start_y)
			
			if c.get('finish',None) is True: self.set_position(c['pos']) # make sure you end up where you should
		elif action == 'wait': # wait in a location
			pass # do nothing
		elif action == 'hide': # hide, don't draw. These implicitly take duration as a "wait" afterwards, NOT as a hide or show for that long
			self.visible=False
		elif action == 'show':
			if self.visible == False: self.last_showtime = time() # store when we were last shown
			self.visible=True
		else:
			# no match
			return False
			
		return True # Matched something 
		
	## Overwrite this in inherited classes
	def draw(self):
		pass
	
	def clickme(self, *args):
		pass
	
	