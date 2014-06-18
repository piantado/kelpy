# -*- coding: utf-8 -*-

from kelpy.CommandableImageSprite import *
from kelpy.tobii.Followable import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This extends CommandableImageSprites so that they interact with the Tobii eyetracker
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
class TobiiSprite(CommandableImageSprite, Followable):
	def __init__(self, screen, init_position, imagepath, tobii_controller, **kwargs):
		""" 
		same args as CommandableImageSprite except for --

		tobii_controller: 
		a TobiiController object which is a wrapper for the Tobii SDK
		"""
		# call parent init
		Followable.__init__(self, tobii_controller)
		CommandableImageSprite.__init__(self, screen, init_position, imagepath, **kwargs)
		#the structure of this code is currently oddly set up; the position of the image is set in CommandableImageSprite, but then it's reset when Arrangeable.init is called within Followable (thus at 0,0). Then the position has to be reset. Really should only need to set the position once; too much overlapping inheritance...
		#self.set_position(init_position)
		#self.set_height(self.display_image.get_height())
		#self.set_width(self.display_image.get_width())
	
		self.tobii_controller = tobii_controller
		self.last_look_timepoint = -1 #stores the latest timestamp that this sprite was looked at
		self.total_look_time = 0 #stores the cumulative looking time for this sprite
	
	def is_looked_at(self):
		""" 
		Reports whether I'm currently being looked at
		
		"""
		#get gaze position and compare to object on screen
		
		gaze_point = self.tobii_controller.get_center_gaze()
		if not None in gaze_point:
			#see if gaze is inside image
			if self.is_inside(gaze_point):
				## print self.is_inside(gaze_point) #############
				return True
				
		#otherwise not being looked at
		return False
		
	def get_look_time(self):
		""" 
		Reports current duration of looking time in milliseconds
		
		"""
		return self.total_look_time
		
	def update(self):
		"""
		Updates looking state and cumulative looking time -- a pretty rough way to determine
		looking time currently
		"""
		#add additional time between now and last timepoint if I was being looked at
		if self.is_looked_at():
			current_timepoint = time()
			if self.last_look_timepoint is not -1:
				self.total_look_time = self.total_look_time + (current_timepoint - self.last_look_timepoint)
				
			#update previous timepoint to now	
			self.last_look_timepoint = current_timepoint
			
		else: #no longer being looked at, so set back to default
			self.last_look_timepoint = -1

		#update position if set to following eye gaze
		#Followable.update(self)
		

			
		
		
