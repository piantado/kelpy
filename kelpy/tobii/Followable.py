# -*- coding: utf-8 -*-

from kelpy.Dragable import *
from kelpy.tobii.TobiiController import *
import math

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Followable works with the Tobii Controller to update a sprite's position based on current eye gaze
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Followable(Dragable):

	def __init__(self, tobii_controller):
		Dragable.__init__(self)

		self.is_following = False
		self.tobii_controller = tobii_controller
		self.jitter_threshold = 30 # threshold to keep sprite static when the eye gaze data is noisy

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
				#calculate difference in position between last eye gaze and this current eye gaze
				gazeDifference = math.sqrt((gaze_point[0] - self.x)**2 + (gaze_point[1] - self.y)**2)

				#only update the position when the difference between the current and previous eye gaze is greater than the jitter threshold
				if gazeDifference > self.jitter_threshold: 
					self.set_x(gaze_point[0])
					self.set_y(gaze_point[1])	

			## Band-aid to allow the followable to process drag zones properly.
			## NOTE: Processing following and drag n drop uses different loops, so if, for some reason, an object is both followable and drag-n-droppable,
			## it would require two different loops to process those interactions.
			## They would, as it is currently written, use the same list of drag and drop zones. 

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
	




			




