# -*- coding: utf-8 -*-

# TODO: This has not really been tested with non-circled. 

from kelpy.CommandableImageSprite import *
import pygame

from random import randint
from pygame.gfxdraw import aacircle, filled_circle

# For outputting images
import Image
import ImageDraw
import numpy

PI = 3.1415926535

class DotStimulus(CommandableSprite):
	"""
		A bunch of random dots in a circle
	"""
	
	def __init__(self, screen, init_position, N=10, area=None, minarea=0.001, radius=10, pad=10, height=2000, width=2000, border_width=0, border_color=(0,0,0), bg_color=(90,90,90), dot_color=(0,0,255), circled=True, circle_color=(255,255,255)):
		"""
			N = number of dots
			radius = radius of dots
			pad = pad between dots
			circle_width -- if 0, we fill; else we draw an outline
			If circled, we require that all the dots are within min(height/2,width/2) of the center
			
			If area is a float, we cover that percentage of the circular radius area. Minarea is the minimum amount
			that a single dot is allowed
		"""
		CommandableSprite.__init__(self, screen, init_position)
		
		self.__dict__.update(locals())
		
		if area is not None:
			assert( area > minarea*N ) # we must have enough available area!
			
			# let's sample uniformly, but only on the leftover area after giving everyone minarea
			r = numpy.array([ random.random() for r in xrange(N) ])
			r = r / sum(r)
			sizes = r*(area - minarea*N) + minarea
			assert( (sum(sizes) - area) < 1e-3)
			
			# pi R^2 = A
			if circled: A = self.width * self.height
			else:       A = PI * ((self.width-2.*pad)/2.)**2.0 
			
			self.radii = numpy.sqrt(A * sizes / PI)
				
			circlearea = numpy.sum( self.radii**2.0 * PI)
			#print A, circlearea
			assert( abs( area*A/circlearea - 1) < 0.01)
			
			#assert(
		else:
			self.radii = numpy.array( [ self.radius ] *  N )
		
		self.dot_positions = []
		i = 0 # which are we on?
		while i < N:
			
			r = self.radii[i]
			
			posx = randint(int(r+pad), int(width-r-pad))
			posy = randint(int(r+pad), int(height-r-pad))
			
			if circled and ((posx-self.width/2)**2 + (posy-self.height/2)**2)**0.5 > min(self.width/2,self.height/2)-pad - self.radii[i] - 2*self.border_width: 
				continue
			
			keep = True
			for j in xrange(len(self.dot_positions)):
				x,y = self.dot_positions[j]
				if ((posx - x)**2 + (posy-y)**2)**0.5 < self.radii[i]+self.radii[j] + pad:
					keep = False
					break
			
			if keep:
				self.dot_positions.append( (posx,posy) )
				i += 1
		
	def to_image(self, f, width=350, height=350):
		# This will draw these dots as an image. We use a different library here for outputting an image
		
		# set up the image
		im = Image.new('RGB', (self.width, self.height))
		
		draw = ImageDraw.Draw(im)
		
		draw.rectangle( (0,0,self.width,self.height), fill=self.bg_color)
		
		if self.border_width > 0:
			draw.ellipse((0,0,self.width,self.height), fill=self.border_color)
			
		draw.ellipse((self.border_width,self.border_width,self.width-self.border_width,self.height-self.border_width), fill=self.circle_color)
		
		for i in xrange(len(self.dot_positions)):
			x,y = self.dot_positions[i]
			r = self.radii[i]
			draw.ellipse( (x-r, y-r, x+r, y+r), fill=self.dot_color)
		
		im = im.resize((width,height), Image.ANTIALIAS) # downsize to antialias
		
		im.save(f)
	
	"""
	
			TODO: THIS IS OUTDATED -- DO NOT USE 
	"""
	def update(self):
	
		CommandableSprite.update(self)
		
		mx = int(self.get_x())
		my = int(self.get_y())
		
		l = int(self.get_left())
		t = int(self.get_top())
		
		if self.circled:
			if self.border_width == 0: # no border --- just draw the background
				pygame.draw.circle(self.screen, self.circle_color, (mx, my), min(self.width/2,self.height/2) )
			else: 
				filled_circle(self.screen, mx, my, min(self.width/2,self.height/2), (0,0,0) ) # draw a black outer rim
				aacircle(self.screen, mx, my, min(self.width/2,self.height/2), (0,0,0) ) # draw a black outer rim
				
				filled_circle(self.screen, mx, my, min(self.width/2-self.border_width,self.height/2-self.border_width), self.circle_color) 
				aacircle(self.screen, mx, my, min(self.width/2-self.border_width,self.height/2-self.border_width), self.circle_color) # and the inside the color we want
				
		# And draw each dot position
		for i in xrange(self.N):
			dx,dy = self.dot_positions[i]
			r = self.radii[i]
			
			# here we draw twice to antialias the edges
			filled_circle(self.screen, int(dx+l), int(dy+t), int(r), self.dot_color)
			aacircle(self.screen, int(dx+l), int(dy+t), int(r), self.dot_color)
		
		
		
		
		
		