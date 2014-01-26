# -*- coding: utf-8 -*-

from kelpy.CommandableImageSprite import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This extends CommandableImageSprites so that they interact with the Tobii eyetracker
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
class TobiiSprite(CommandableImageSprite):
	def __init__(self, screen, init_position, imagepath, tobii_controller, **kwargs):
		""" 
		same args as CommandableImageSprite except for --

		tobii_controller: 
		a TobiiController object which is a wrapper for the Tobii SDK
		"""
		
		self.tobii_controller = tobii_controller
		self.last_look_timepoint = -1 #stores the latest timestamp that this sprite was looked at
		self.total_look_time = 0 #stores the cumulative looking time for this sprite
		
		# call parent init
		CommandableImageSprite.__init__(self, screen, init_position, imagepath, **kwargs)
		
		
	def is_looked_at(self):
		""" 
		Reports whether I'm currently being looked at
		
		"""
		#get gaze position and compare to object on screen
		
		gaze_point = self.tobii_controller.get_center_gaze()
		if not None in gaze_point:
			#see if gaze is inside image
			if self.is_inside(gaze_point):
				return True
				
		#otherwise not being looked at
		return False
		
	def get_look_time(self):
		""" 
		Reports current duration of looking time in milliseconds
		
		"""
		return self.total_look_time
	
	def update_action(self, **c):
		"""
		Actions specific to TobiiSprites -- nothing really so far except for 'follow' which
		is just a test action
		"""
		# try updating as a parent -- this defines self.start_x, self.start_y
		if CommandableSprite.update_action(self, **c): return True
		
		action = c['action']
		duration = c.get('duration', float('inf')) # get the duration else inf if none is specified
		
		if action == 'follow':
			#follows eye gaze indefinitely if duration is not set
			if c.get('finish',False) is True:
				duration = 0.0
			
			if (time() - c['start_time']) < duration:
				gaze_point = self.tobii_controller.get_center_gaze()
				if not None in gaze_point:
					self.set_x(gaze_point[0])
					self.set_y(gaze_point[1])				
		elif CommandableImageSprite.update_action(self, **c): return True
		else: return False
		
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
		

			
		
		
