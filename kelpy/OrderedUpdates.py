"""

	This is a friendlier version of pygame's OrderedUpdate

"""

import pygame
from kelpy.Dragable import *

class OrderedUpdates(pygame.sprite.OrderedUpdates):
	
	def __init__(self, *args):
		pygame.sprite.OrderedUpdates.__init__(self) # create myself
		
		for a in args:
			if isinstance(a, list): # allow us to pass lists as arguments (awesome)
				for ai in a: self.add(ai)
			else:
				self.add(a)
				
	def append(self, x):
		self.add(x)
	
	def update(self):
		# Like all kelpy, we will have an update function that does everything important
		for x in self:
			x.update()
			x.draw()
			
	def process_dragndrop(self, event):
		"""
			This deals with the ordered updates events. We process from top to botton, 
			but when we find one we drag (return True from o.maybedrag), then we return
			True. This stops us from processing drag events from things behind (that are, e.g. 
			occluded)
			
			TODO: drag_brings_to_top - if True, then when we touch something, it becomes the top layer
		"""
		
		for o in reversed(self.sprites()):
			if o.isdraggable and o.process_dragndrop(event):
				return True
		
		return False


	def process_follow(self, event):
		"""
			The first Followable sprite will update its position based on eye gaze.
			Only one sprite should be followable at a time I'm assuming; perhaps 
			integrate this feature with whether the sprite is currently visible or not.
		"""
		for o in reversed(self.sprites()):
			#check if the object has a "is_following" attribute; specific to Followable class
			if hasattr(o, 'is_following') and o.process_follow(event):
				return True
		
		return False

		
		
