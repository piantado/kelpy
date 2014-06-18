# -*- coding: utf-8 -*-

from kelpy.Arrangeable import *
from kelpy.tobii.TobiiController import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Followable works with the Tobii Controller to update a sprite's position based on current eye gaze
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Followable(Arrangeable):

	def __init__(self, tobii_controller):
		Arrangeable.__init__(self)

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
		if self.is_following is False:
			return False
		else:
			gaze_point = self.tobii_controller.get_center_gaze()
			if not None in gaze_point:
				self.set_x(gaze_point[0])
				self.set_y(gaze_point[1])	
				return True
			else:
				return False


			




