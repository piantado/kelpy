# -*- coding: utf-8 -*-

# TODO: This has not really been tested with non-circled. 

from kelpy.CommandableSprites import *
import pygame

from random import randint
from pygame.gfxdraw import aacircle 

# For outputting images
import Image
import ImageDraw
import numpy

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
			else:       A = 3.1415926535 * ((self.width-2.*pad)/2.)**2.0 ## TODO: Make this really the area of the ellipse
			
			self.radii = numpy.sqrt(A * sizes / 3.1415926535)
				
			circlearea = numpy.sum( self.radii**2.0 * 3.1415926535)
			print A, circlearea
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
	#def update(self):
	
		#CommandableSprite.update(self)
		
		#mx = self.get_x()
		#my = self.get_y()
		
		#l = self.get_left()
		#t = self.get_top()
		
		##pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
		#pygame.draw.rect(self.screen,self.bg_color,self.get_pygame_Rect())
		
		#if self.circled:
			#if self.circle_width == 0: # no border --- just draw the background
				#pygame.draw.circle(self.screen, self.circle_color, (mx, my), min(self.width/2,self.height/2) )
			#else: 
			
			
			##aacircle(self.screen, mx, my, min(self.width/2,self.height/2), self.circle_color)
		
		#for dx,dy in self.dot_positions:
			##print dx,dy
			#pygame.draw.circle(self.screen, self.dot_color, (dx+l, dy+t), self.radius, self.circle_width)
			##aacircle(self.screen, dx+l, dy+t, self.radius, self.dot_color)
		
		
		
		
		
		