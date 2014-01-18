# -*- coding: utf-8 -*-
import pygame
from pygame import Rect

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# For arranging stuff on the screen
# This uses the width.height and pos (position)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Arrangeable():
	
	def __init__(self):
		self.x = 0
		self.y = 0
		self.height = -1
		self.width  = -1
		
	def set_x(self, v): self.x = v
	def set_y(self, v): self.y = v
	def set_width(self, v): self.width=v
	def set_height(self, v): self.height=v
	
	def get_x(self): return self.x
	def get_y(self): return self.y
	def position(self): return self.x,self.y
	def get_height(self): return self.height
	def get_width(self):  return self.width
	
	# give this locations for the top, bottom, left, and right of this thing
	def set_bottom(self, v): self.set_y(v + self.get_height()/2)
	def set_top(self, v):    self.set_y(v - self.get_height()/2)
	def set_right(self, v):  self.set_x(v + self.get_width()/2)
	def set_left(self, v):   self.set_x(v - self.get_width()/2)
	
	def get_bottom(self): return (self.get_y() + self.get_height()/2)
	def get_top(self):    return (self.get_y() - self.get_height()/2)
	def get_right(self):  return (self.get_x() + self.get_width()/2)
	def get_left(self):   return (self.get_x() - self.get_width()/2)
	
	def add_position(self, a, b):
		self.set_x(self.get_width()+a)
		self.set_y(self.get_height()+b)
	
	def set_position(self, a, b=None):
		if b is None:
			self.set_x(a[0])
			self.set_y(a[1])
		else:
			self.set_x(a)
			self.set_y(b)
			
	def set_dimensions(self, a, b=None):
		if b is None:
			self.set_width(a[0])
			self.set_height(a[1])
		else:
			self.set_width(a)
			self.set_height(b)	
		
	# check if a click is inside of you and on an image
	def clicked(self, event, button=1):
		#print event
		""" check if a pygame event clicks me (whether or not it is a click event"""
		return event.type == pygame.MOUSEBUTTONDOWN and event.button == button and self.click_inside( event.pos )
		
	def click_inside(self, point):
		return self.is_inside(point)
	def is_inside(self, point):
		x, y = point
		#print point, self.get_right(), self.get_left(), self.get_top(), self.get_bottom()
		return (x < self.get_right() and x > self.get_left() and y > self.get_top() and y < self.get_bottom())	
	
	
	# a bounding rectangle
	def get_pygame_Rect(self):
		return pygame.Rect(self.get_x() - self.get_width()/2, self.get_y() - self.get_height()/2, self.get_width(), self.get_height())

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# For arranging stuff on the screen
# This uses the width.height and pos (position)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Arranger():
	
	# arrange centered at x,y with pad all around
	@staticmethod 
	def ArrangeHorizontal(a, x, y, pad=10):
		
		total_length = pad
		for i in range(len(a)):
			total_length += a[i].get_width() + pad
			
		# now start at
		curx = x - total_length/2 - pad
		
		for i in range(len(a)):
			h = a[i].get_width()
			a[i].set_position(curx+h/2, y)
			curx = curx + h + pad	
		return [ total_length, pad + max( map( lambda i: i.get_height() + pad, a))]
		
	# arrange centered at x,y with pad all around
	# returns the total dimensions
	@staticmethod 
	def ArrangeVertical(a, x, y, pad=10):
		
		total_length = pad
		for i in range(len(a)):
			total_length += a[i].get_height() + pad
			
		cury = y - total_length/2 + pad
		
		for i in range(len(a)):
			h = a[i].get_height()
			a[i].set_position(x, cury + h/2)
			cury = cury + h + pad	
		
		return [ pad + max( map( lambda i: i.get_width() + pad, a)), total_length]