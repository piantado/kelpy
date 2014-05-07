# -*- coding: utf-8 -*-

from kelpy.Dragable import *
from kelpy.tobii.TobiiController import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Followable works with the Tobii Controller to update a sprite's position based on current eye gaze
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Followable(Dragable):

	def __init__(self, tobii_controller):
		Dragable.__init__(self)

		self.is_following = False
		self.tobii_controller = tobii_controller

	def set_follow(self, follow):
		if (follow):
			self.enable_follow()
		else:
			self.disable_follow()

	def enable_follow(self):
		self.is_following = True

	def disable_follow(self):
		self.is_following = False

	def process_follow(self, event):
	#currently does nothing with event for now, but could in the future
		if self.is_following is False :
			return False
		else:
			gaze_point = self.tobii_controller.get_center_gaze()
			oldxy = ( (self.x, self.y) )
			if not None in gaze_point:
				self.set_x(gaze_point[0])
				self.set_y(gaze_point[1])	

			## Band-aid to allow the followable to process drag zones properly... let's see if it works
				for z in self.drag_zones:
					wasinz = z.is_inside( oldxy )
					newpos = ( (self.x), (self.y) ) 
					nowinz = z.is_inside(newpos)
					if (not wasinz) and nowinz: # the first time you enter
						pygame.event.post(pygame.event.Event(ZONE_EVENT, motion="drag", direction="enter", obj=self, zone=z))
					if wasinz and (not nowinz): # first time you exit
						pygame.event.post(pygame.event.Event(ZONE_EVENT, motion="drag", direction="exit", obj=self, zone=z))
					
				return True
			else:
				return False
	




			




