
"""
	
	For giving clicking scale responses
	
"""

import pygame
from kelpy.CommandableSprites import *

class SelectionSlider(CommandableSprite):
	
	def __init__(self, screen, init_position, width=600, height=75, color=(255,0,0)):
		CommandableSprite.__init__(self, screen, init_position)	
		self.__dict__.update(locals())
	
	def update(self):
		CommandableSprite.update(self)
		
		l = self.get_left()
		r = self.get_right()
		y = self.get_y()
		t = self.get_top()
		b = self.get_bottom()
		
		pygame.draw.aaline(self.screen, self.color, (l,y), (r,y))
		
		# and draw endlines
		pygame.draw.aaline(self.screen, self.color, (l,t), (l,b))		
		pygame.draw.aaline(self.screen, self.color, (r,t), (r,b))		
		
	def clickme(self, point):
		
		if self.click_inside(point):
			print point
	
	